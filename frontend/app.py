import streamlit as st
import os
from pathlib import Path
import magic
from typing import Optional, Tuple
import re

# Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = {
    'text/markdown': '.md',
    'text/plain': '.txt'
}

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
                st.success(f"File uploaded: {uploaded_file.name}")
                
                # Preview section with syntax highlighting
                st.header("Content Preview")
                content = uploaded_file.getvalue().decode()
                
                # Add syntax highlighting for markdown
                if uploaded_file.name.endswith('.md'):
                    st.markdown("""
                    <style>
                    .markdown-preview {
                        background-color: #f8f9fa;
                        padding: 1rem;
                        border-radius: 5px;
                        border: 1px solid #e9ecef;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="markdown-preview">', unsafe_allow_html=True)
                    st.markdown(content)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.text_area("Content", content, height=400)
            else:
                st.error(error_message)

        st.header("Cover Image")
        cover_image = st.file_uploader(
            "Upload cover image",
            type=['jpg', 'jpeg', 'png'],
            help="Recommended size: 1600x2400 pixels"
        )
        if cover_image:
            st.image(cover_image, caption="Cover Preview")
        
        st.write("")
        st.write("")
        # Convert button in right column
        convert_btn = st.button("Convert to EPUB", use_container_width=True)

if __name__ == "__main__":
    main()
