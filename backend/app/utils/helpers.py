import os
import uuid
import magic
from pathlib import Path
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException
from PIL import Image
import io

# Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_MIME_TYPES = {
    'text/markdown': '.md',
    'text/plain': '.txt'
}
ALLOWED_IMAGE_FORMATS = ['JPEG', 'PNG']
MIN_IMAGE_DIMENSIONS = (800, 1200)
MAX_IMAGE_DIMENSIONS = (3000, 4000)

def generate_file_id() -> str:
    """Generate a unique file ID."""
    return str(uuid.uuid4())

def validate_uploaded_file(file: UploadFile) -> Tuple[bool, Optional[str]]:
    """Validate uploaded file for size and type."""
    if not file:
        return False, "No file uploaded"
    
    # Check file size
    try:
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            return False, f"File size exceeds {MAX_FILE_SIZE/1024/1024}MB limit"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"
    
    # Check file type
    try:
        content = file.file.read(1024)  # Read first 1KB for MIME detection
        file.file.seek(0)  # Reset to beginning
        
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(content)
        
        if file_type not in ALLOWED_MIME_TYPES:
            return False, f"Invalid file type. Allowed types: {', '.join(ALLOWED_MIME_TYPES.values())}"
        
        return True, None
    except Exception as e:
        return False, f"Error detecting file type: {str(e)}"

def validate_cover_image(image_file: UploadFile) -> Tuple[bool, Optional[str], Optional[dict]]:
    """Validate cover image for size, format, and dimensions."""
    if not image_file:
        return True, None, None  # Image is optional
    
    # Check file size
    try:
        image_file.seek(0, 2)
        file_size = image_file.tell()
        image_file.seek(0)
        
        if file_size > MAX_IMAGE_SIZE:
            return False, f"Image size exceeds {MAX_IMAGE_SIZE/1024/1024}MB limit", None
    except Exception as e:
        return False, f"Error reading image file: {str(e)}", None
    
    try:
        # Read image content
        content = image_file.file.read()
        image_file.file.seek(0)
        
        # Open image to check format and dimensions
        image = Image.open(io.BytesIO(content))
        
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
        
        image_info = {
            'format': image.format,
            'width': width,
            'height': height,
            'size_mb': file_size / (1024 * 1024),
            'aspect_ratio': width / height
        }
        
        return True, None, image_info
        
    except Exception as e:
        return False, f"Error processing image: {str(e)}", None

def save_uploaded_file(file: UploadFile, file_id: str, upload_dir: str = "uploads") -> str:
    """Save uploaded file and return the file path."""
    # Create upload directory if it doesn't exist
    upload_path = Path(upload_dir)
    upload_path.mkdir(exist_ok=True)
    
    # Generate file path
    file_extension = Path(file.filename).suffix if file.filename else '.txt'
    file_path = upload_path / f"{file_id}{file_extension}"
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
        return str(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

def save_cover_image(image_file: UploadFile, file_id: str, upload_dir: str = "uploads/covers") -> str:
    """Save cover image and return the file path."""
    # Create upload directory if it doesn't exist
    upload_path = Path(upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)
    
    # Generate file path
    file_extension = Path(image_file.filename).suffix if image_file.filename else '.jpg'
    file_path = upload_path / f"{file_id}_cover{file_extension}"
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            content = image_file.file.read()
            buffer.write(content)
        return str(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving cover image: {str(e)}")

def cleanup_file(file_path: str) -> bool:
    """Delete a file from the filesystem."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False 