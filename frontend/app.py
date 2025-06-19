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
import requests
import json
from datetime import date

# API Configuration
API_BASE_URL = "http://localhost:8000"

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

def upload_file_to_api(file, cover_image=None):
    """Upload file to backend API."""
    try:
        files = {'file': (file.name, file.getvalue(), 'text/markdown')}
        
        if cover_image:
            files['cover_image'] = (cover_image.name, cover_image.getvalue(), 'image/jpeg')
        
        response = requests.post(f"{API_BASE_URL}/api/v1/conversion/upload", files=files)
        
        if response.status_code == 200:
            return True, response.json(), None
        else:
            return False, None, f"Upload failed: {response.text}"
            
    except requests.exceptions.ConnectionError:
        return False, None, "Could not connect to backend server. Make sure it's running on http://localhost:8000"
    except Exception as e:
        return False, None, f"Upload error: {str(e)}"

def convert_file_to_epub(file_id, metadata, content_type="prose"):
    """Convert file to EPUB using backend API."""
    try:
        # Prepare metadata for API
        metadata_dict = {
            "title": metadata["title"],
            "author": metadata["author"],
            "publisher": metadata.get("publisher"),
            "publication_date": metadata.get("publication_date"),
            "isbn": metadata.get("isbn"),
            "language": metadata.get("language", "English"),
            "description": metadata.get("description"),
            "keywords": metadata.get("keywords", []),
            "content_type": content_type.lower()
        }
        
        # Remove None values
        metadata_dict = {k: v for k, v in metadata_dict.items() if v is not None}
        
        data = {
            'file_id': file_id,
            'metadata_json': json.dumps(metadata_dict),
            'content_type': content_type.lower()
        }
        
        response = requests.post(f"{API_BASE_URL}/api/v1/conversion/convert", data=data)
        
        if response.status_code == 200:
            return True, response.json(), None
        else:
            return False, None, f"Conversion failed: {response.text}"
            
    except requests.exceptions.ConnectionError:
        return False, None, "Could not connect to backend server. Make sure it's running on http://localhost:8000"
    except Exception as e:
        return False, None, f"Conversion error: {str(e)}"

def download_epub_file(download_url):
    """Download EPUB file from backend API."""
    try:
        response = requests.get(f"{API_BASE_URL}{download_url}")
        
        if response.status_code == 200:
            return True, response.content, None
        else:
            return False, None, f"Download failed: {response.text}"
            
    except requests.exceptions.ConnectionError:
        return False, None, "Could not connect to backend server. Make sure it's running on http://localhost:8000"
    except Exception as e:
        return False, None, f"Download error: {str(e)}"

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
        
        # Backend status check
        st.markdown("---")
        st.markdown("### Backend Status")
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                st.success("✅ Backend Connected")
            else:
                st.error("❌ Backend Error")
        except:
            st.error("❌ Backend Offline")
            st.info("Start the backend with: `cd backend && python run.py`")

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
            keywords_input = st.text_input("Keywords (comma-separated)", help="Optional field")
            
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
                
                # Step 1: Upload file to backend
                with st.spinner("Uploading file to backend..."):
                    success, result, error = upload_file_to_api(uploaded_file, cover_image)
                    
                    if not success:
                        st.error(f"❌ {error}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        return
                    
                    file_id = result['file_info']['file_id']
                    st.success("✅ File uploaded to backend successfully!")
                
                # Step 2: Convert to EPUB
                with st.spinner("Converting to EPUB..."):
                    # Prepare metadata
                    keywords = [k.strip() for k in keywords_input.split(',')] if keywords_input else []
                    
                    metadata = {
                        "title": title,
                        "author": author,
                        "publisher": publisher if publisher else None,
                        "publication_date": pub_date.isoformat() if pub_date else None,
                        "isbn": isbn if isbn else None,
                        "language": language,
                        "description": description if description else None,
                        "keywords": keywords
                    }
                    
                    success, result, error = convert_file_to_epub(file_id, metadata, content_type)
                    
                    if not success:
                        st.error(f"❌ {error}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        return
                    
                    download_url = result.get('download_url')
                    st.success("✅ Conversion completed successfully!")
                
                # Step 3: Download EPUB file
                with st.spinner("Preparing download..."):
                    success, epub_data, error = download_epub_file(download_url)
                    
                    if not success:
                        st.error(f"❌ {error}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        return
                    
                    # Create download link
                    filename = f"{title.replace(' ', '_') if title else 'book'}.epub"
                    download_link = create_download_link(epub_data, filename, "📥 Download EPUB")
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
