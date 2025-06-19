import streamlit as st
import os
from pathlib import Path
import magic
from typing import Optional, Tuple
import re
from PIL import Image
import io
import time
import base64

# Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = {
    'text/markdown': '.md',
    'text/plain': '.txt'
}

# Image validation constants
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_FORMATS = ['JPEG', 'PNG']
MIN_IMAGE_DIMENSIONS = (800, 1200)  # Minimum width, height
RECOMMENDED_IMAGE_DIMENSIONS = (1600, 2400)  # Recommended width, height
MAX_IMAGE_DIMENSIONS = (3000, 4000)  # Maximum width, height

# Page configuration
st.set_page_config(
    page_title="Markdown to EPUB Creator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .upload-section {
        border: 2px dashed #ccc;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
    }
    .required-field::after {
        content: " *";
        color: red;
    }
    .error-message {
        color: #ff4b4b;
        font-size: 0.8em;
        margin-top: 0.2em;
    }
    .success-message {
        color: #00acb5;
        font-size: 0.8em;
        margin-top: 0.2em;
    }
    .warning-message {
        color: #ffa500;
        font-size: 0.8em;
        margin-top: 0.2em;
    }
    .file-info {
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 5px;
        border: 1px solid #e9ecef;
        margin-top: 0.5rem;
    }
    .conversion-status {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #4caf50;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def validate_file(file) -> Tuple[bool, Optional[str]]:
    """Validate uploaded file for size and type."""
    if file is None:
        return False, "No file uploaded"
    
    # Check file size
    file_size = file.getbuffer().nbytes
    if file_size > MAX_FILE_SIZE:
        return False, f"File size exceeds {MAX_FILE_SIZE/1024/1024}MB limit"
    
    # Check file type
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file.getvalue())
    
    if file_type not in ALLOWED_MIME_TYPES:
        return False, f"Invalid file type. Allowed types: {', '.join(ALLOWED_MIME_TYPES.values())}"
    
    return True, None

def validate_cover_image(image_file) -> Tuple[bool, Optional[str], Optional[dict]]:
    """Validate cover image for size, format, and dimensions."""
    if image_file is None:
        return True, None, None  # Image is optional
    
    # Check file size
    file_size = image_file.getbuffer().nbytes
    if file_size > MAX_IMAGE_SIZE:
        return False, f"Image size exceeds {MAX_IMAGE_SIZE/1024/1024}MB limit", None
    
    try:
        # Open image to check format and dimensions
        image = Image.open(image_file)
        
        # Check format
        if image.format not in ALLOWED_IMAGE_FORMATS:
            return False, f"Invalid image format. Allowed formats: {', '.join(ALLOWED_IMAGE_FORMATS)}", None
        
        # Get dimensions
        width, height = image.size
        
        # Check minimum dimensions
        if width < MIN_IMAGE_DIMENSIONS[0] or height < MIN_IMAGE_DIMENSIONS[1]:
            return False, f"Image too small. Minimum dimensions: {MIN_IMAGE_DIMENSIONS[0]}x{MIN_IMAGE_DIMENSIONS[1]} pixels", None
        
        # Check maximum dimensions
        if width > MAX_IMAGE_DIMENSIONS[0] or height > MAX_IMAGE_DIMENSIONS[1]:
            return False, f"Image too large. Maximum dimensions: {MAX_IMAGE_DIMENSIONS[0]}x{MAX_IMAGE_DIMENSIONS[1]} pixels", None
        
        # Check aspect ratio (should be roughly 2:3 for book covers)
        aspect_ratio = width / height
        ideal_ratio = 2/3  # 0.667
        ratio_tolerance = 0.2
        
        if abs(aspect_ratio - ideal_ratio) > ratio_tolerance:
            st.warning(f"⚠️ Image aspect ratio ({aspect_ratio:.2f}) differs from ideal book cover ratio (0.67). Recommended: 2:3 ratio.")
        
        image_info = {
            'format': image.format,
            'width': width,
            'height': height,
            'size_mb': file_size / (1024 * 1024),
            'aspect_ratio': aspect_ratio
        }
        
        return True, None, image_info
        
    except Exception as e:
        return False, f"Error processing image: {str(e)}", None

def validate_title(title: str) -> Tuple[bool, Optional[str]]:
    """Validate book title."""
    if not title or not title.strip():
        return False, "Title is required"
    if len(title.strip()) < 2:
        return False, "Title must be at least 2 characters long"
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters"
    return True, None

def validate_author(author: str) -> Tuple[bool, Optional[str]]:
    """Validate author name."""
    if not author or not author.strip():
        return False, "Author is required"
    if len(author.strip()) < 2:
        return False, "Author name must be at least 2 characters long"
    if len(author.strip()) > 100:
        return False, "Author name must be less than 100 characters"
    return True, None

def validate_isbn(isbn: str) -> Tuple[bool, Optional[str]]:
    """Validate ISBN format."""
    if not isbn:
        return True, None  # ISBN is optional
    
    # Remove hyphens and spaces
    isbn_clean = re.sub(r'[-\s]', '', isbn)
    
    # Check length (ISBN-10 or ISBN-13)
    if len(isbn_clean) not in [10, 13]:
        return False, "ISBN must be 10 or 13 digits"
    
    # Check if all characters are digits (except last character for ISBN-10)
    if not isbn_clean[:-1].isdigit():
        return False, "ISBN must contain only digits (except last character for ISBN-10)"
    
    # For ISBN-10, last character can be 'X'
    if len(isbn_clean) == 10 and not (isbn_clean[-1].isdigit() or isbn_clean[-1].upper() == 'X'):
        return False, "ISBN-10 last character must be a digit or 'X'"
    
    return True, None

def validate_description(description: str) -> Tuple[bool, Optional[str]]:
    """Validate description."""
    if not description:
        return True, None  # Description is optional
    
    if len(description.strip()) > 1000:
        return False, "Description must be less than 1000 characters"
    
    return True, None

def simulate_conversion_process():
    """Simulate the conversion process with progress updates."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "Validating input files...",
        "Processing metadata...",
        "Converting Markdown to HTML...",
        "Generating EPUB structure...",
        "Adding cover image...",
        "Finalizing EPUB file...",
        "Conversion complete!"
    ]
    
    for i, step in enumerate(steps):
        status_text.text(step)
        progress = (i + 1) / len(steps)
        progress_bar.progress(progress)
        time.sleep(0.5)  # Simulate processing time
    
    progress_bar.empty()
    status_text.empty()
    
    return True

def create_download_link(data, filename, text):
    """Create a download link for the generated file."""
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/epub+zip;base64,{b64}" download="{filename}">{text}</a>'
    return href

def main():
    # Title
    st.title("📚 Markdown to EPUB Creator")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        content_type = st.radio(
            "Content Type",
            ["Prose", "Poetry"],
            help="Select the type of content you're converting"
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        Convert your Markdown or TXT files to EPUB format.
        - Use # for book title
        - Use ## for chapters
        - Use ### for displayed titles
        """)

    # Main layout: two columns (left and right)
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.header("Book Metadata")
        
        # Initialize session state for form validation
        if 'form_submitted' not in st.session_state:
            st.session_state.form_submitted = False
        
        with st.form("metadata_form"):
            title = st.text_input("Title *", help="Required field (2-200 characters)")
            author = st.text_input("Author *", help="Required field (2-100 characters)")
            publisher = st.text_input("Publisher", help="Optional field")
            pub_date = st.date_input("Publication Date")
            isbn = st.text_input("ISBN", help="Optional: 10 or 13 digits")
            language = st.selectbox(
                "Language",
                ["English", "Spanish", "French", "German", "Italian"]
            )
            description = st.text_area("Description", help="Optional field (max 1000 characters)")
            keywords = st.text_input("Keywords (comma-separated)", help="Optional field")
            
            # Form submission
            submitted = st.form_submit_button("Validate Form")
            
            if submitted:
                st.session_state.form_submitted = True
                
                # Validate all fields
                title_valid, title_error = validate_title(title)
                author_valid, author_error = validate_author(author)
                isbn_valid, isbn_error = validate_isbn(isbn)
                desc_valid, desc_error = validate_description(description)
                
                # Display validation results
                if not title_valid:
                    st.error(f"Title: {title_error}")
                if not author_valid:
                    st.error(f"Author: {author_error}")
                if not isbn_valid:
                    st.error(f"ISBN: {isbn_error}")
                if not desc_valid:
                    st.error(f"Description: {desc_error}")
                
                # Check if all required fields are valid
                if title_valid and author_valid:
                    st.success("✅ All required fields are valid!")
                    if isbn_valid and desc_valid:
                        st.success("✅ All optional fields are valid!")
                else:
                    st.warning("⚠️ Please fix the errors above before proceeding.")

    with right_col:
        st.header("Upload Your File")
        uploaded_file = st.file_uploader(
            "Choose a Markdown or TXT file *",
            type=['md', 'txt'],
            help="Upload your markdown or text file (Required, max 10MB)"
        )
        
        if uploaded_file:
            # Validate file
            is_valid, error_message = validate_file(uploaded_file)
            
            if is_valid:
                st.success(f"✅ File uploaded successfully: {uploaded_file.name}")
                file_size = uploaded_file.getbuffer().nbytes / (1024 * 1024)
                st.info(f"📄 File size: {file_size:.2f} MB")
            else:
                st.error(f"❌ {error_message}")

        st.header("Cover Image")
        cover_image = st.file_uploader(
            "Upload cover image",
            type=['jpg', 'jpeg', 'png'],
            help=f"Optional: JPG/PNG, max {MAX_IMAGE_SIZE/1024/1024}MB, min {MIN_IMAGE_DIMENSIONS[0]}x{MIN_IMAGE_DIMENSIONS[1]}px"
        )
        
        if cover_image:
            # Validate cover image
            is_valid, error_message, image_info = validate_cover_image(cover_image)
            
            if is_valid:
                st.success(f"✅ Cover image uploaded successfully: {cover_image.name}")
                if image_info:
                    st.info(f"📷 {image_info['format']} - {image_info['width']}x{image_info['height']}px - {image_info['size_mb']:.2f}MB")
            else:
                st.error(f"❌ {error_message}")
        
        st.write("")
        st.write("")
        
        # Conversion section
        st.header("Convert to EPUB")
        
        # Check if all required fields are ready
        file_ready = uploaded_file is not None and validate_file(uploaded_file)[0]
        metadata_ready = st.session_state.get('form_submitted', False)
        
        # Initialize session state for conversion attempts
        if 'conversion_attempted' not in st.session_state:
            st.session_state.conversion_attempted = False
        
        if file_ready and metadata_ready:
            convert_btn = st.button("🚀 Start Conversion", use_container_width=True)
            
            if convert_btn:
                # Start conversion process
                st.markdown('<div class="conversion-status">', unsafe_allow_html=True)
                st.success("🔄 Starting conversion process...")
                
                # Simulate conversion process
                if simulate_conversion_process():
                    st.success("✅ Conversion completed successfully!")
                    
                    # Create a sample EPUB file (in real implementation, this would be the actual converted file)
                    sample_epub_content = b"Sample EPUB content"  # This would be the actual EPUB file
                    filename = f"{title.replace(' ', '_') if title else 'book'}.epub"
                    
                    # Create download link
                    download_link = create_download_link(sample_epub_content, filename, "📥 Download EPUB")
                    st.markdown(download_link, unsafe_allow_html=True)
                    
                    st.info(f"📚 Your EPUB file '{filename}' is ready for download!")
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Show warnings only when user tries to convert without meeting requirements
            if st.button("🚀 Start Conversion", use_container_width=True, disabled=True):
                st.session_state.conversion_attempted = True
            
            # Show warnings only after conversion attempt
            if st.session_state.conversion_attempted:
                if not file_ready:
                    st.error("❌ Please upload a valid file first.")
                if not metadata_ready:
                    st.error("❌ Please validate your metadata form first.")

if __name__ == "__main__":
    main()
