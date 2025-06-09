import streamlit as st
import os
from pathlib import Path
import magic
from typing import Optional, Tuple

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
        with st.form("metadata_form"):
            title = st.text_input("Title *", help="Required field")
            author = st.text_input("Author *", help="Required field")
            publisher = st.text_input("Publisher")
            pub_date = st.date_input("Publication Date")
            isbn = st.text_input("ISBN")
            language = st.selectbox(
                "Language",
                ["English", "Spanish", "French", "German", "Italian"]
            )
            description = st.text_area("Description")
            keywords = st.text_input("Keywords (comma-separated)")
            # The submit button will be placed in the right column
            st.form_submit_button("(Hidden)", disabled=True)

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
