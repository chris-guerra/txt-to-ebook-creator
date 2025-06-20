import os
import uuid
import magic
from pathlib import Path
from typing import Tuple, Optional, List, Dict, Any
from fastapi import UploadFile, HTTPException
from PIL import Image
import io
import re

# Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_COVER_SIZE = 2 * 1024 * 1024  # 2MB for Kindle compatibility
ALLOWED_MIME_TYPES = {
    'text/markdown': '.md',
    'text/plain': '.txt'
}
ALLOWED_IMAGE_FORMATS = ['JPEG', 'PNG']
MIN_IMAGE_DIMENSIONS = (400, 600)  # Reduced minimum dimensions
MAX_IMAGE_DIMENSIONS = (3000, 4000)
KINDLE_COVER_DIMENSIONS = (1600, 2400)  # Recommended Kindle cover size

def generate_file_id() -> str:
    """Generate a unique file ID."""
    return str(uuid.uuid4())

def validate_uploaded_file(file: UploadFile) -> Tuple[bool, Optional[str]]:
    """Validate uploaded file for size and type."""
    if not file:
        return False, "No file uploaded"
    
    # Check file size
    try:
        # Get file size by reading the entire file into memory
        content = file.file.read()
        file_size = len(content)
        file.file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            return False, f"File size exceeds {MAX_FILE_SIZE/1024/1024}MB limit"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"
    
    # Check file type
    try:
        # Read first 1KB for MIME detection
        content = file.file.read(1024)
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
        # Read the entire image content to get size
        content = image_file.file.read()
        file_size = len(content)
        image_file.file.seek(0)  # Reset to beginning
        
        if file_size > MAX_IMAGE_SIZE:
            return False, f"Image size exceeds {MAX_IMAGE_SIZE/1024/1024}MB limit", None
    except Exception as e:
        return False, f"Error reading image file: {str(e)}", None
    
    try:
        # Read image content again for processing
        content = image_file.file.read()
        image_file.file.seek(0)  # Reset to beginning
        
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

def process_cover_image_for_kindle(image_path: str, output_path: Optional[str] = None) -> str:
    """
    Process cover image to ensure Kindle compatibility.
    
    Args:
        image_path: Path to the original cover image
        output_path: Optional output path, if None will overwrite original
        
    Returns:
        Path to the processed image
    """
    try:
        # Open image
        with Image.open(image_path) as img:
            # Convert to RGB (Kindle requirement)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to recommended Kindle dimensions if too large
            if img.size[0] > KINDLE_COVER_DIMENSIONS[0] or img.size[1] > KINDLE_COVER_DIMENSIONS[1]:
                img.thumbnail(KINDLE_COVER_DIMENSIONS, Image.Resampling.LANCZOS)
            
            # Ensure minimum dimensions
            if img.size[0] < MIN_IMAGE_DIMENSIONS[0] or img.size[1] < MIN_IMAGE_DIMENSIONS[1]:
                # Resize to minimum while maintaining aspect ratio
                ratio = max(MIN_IMAGE_DIMENSIONS[0] / img.size[0], MIN_IMAGE_DIMENSIONS[1] / img.size[1])
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Save with optimized settings for Kindle
            output_path = output_path or image_path
            img.save(output_path, 'JPEG', quality=85, optimize=True)
            
            # Check file size
            file_size = os.path.getsize(output_path)
            if file_size > MAX_COVER_SIZE:
                # If still too large, reduce quality further
                img.save(output_path, 'JPEG', quality=70, optimize=True)
            
            return output_path
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing cover image: {str(e)}")

def create_safe_filename(title: str, extension: str = ".epub") -> str:
    """
    Create a safe filename for Kindle compatibility while preserving accented characters.
    
    Args:
        title: Book title
        extension: File extension
        
    Returns:
        Safe filename
    """
    # Remove or replace problematic characters for filesystems, but preserve accented characters
    # This preserves Spanish characters like á, é, í, ó, ú, ñ, ü, ¿, ¡
    safe_title = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', title)
    
    # Remove multiple consecutive underscores
    safe_title = re.sub(r'_+', '_', safe_title)
    
    # Remove leading/trailing underscores
    safe_title = safe_title.strip('_')
    
    # Limit length
    if len(safe_title) > 50:
        safe_title = safe_title[:50]
    
    return f"{safe_title}{extension}"

def validate_epub_for_kindle(epub_path: str) -> Tuple[bool, List[str]]:
    """
    Validate EPUB file for Kindle compatibility.
    
    Args:
        epub_path: Path to the EPUB file
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    try:
        # Check file exists
        if not os.path.exists(epub_path):
            return False, ["EPUB file does not exist"]
        
        # Check file size
        file_size = os.path.getsize(epub_path)
        if file_size > 50 * 1024 * 1024:  # 50MB limit
            issues.append(f"EPUB file too large: {file_size / (1024*1024):.1f}MB (max 50MB)")
        
        # Check filename
        filename = os.path.basename(epub_path)
        if re.search(r'[^a-zA-Z0-9_\-\.]', filename):
            issues.append("Filename contains special characters")
        
        # Basic EPUB structure check
        try:
            import zipfile
            with zipfile.ZipFile(epub_path, 'r') as epub_zip:
                file_list = epub_zip.namelist()
                
                # Check for required files
                required_files = ['META-INF/container.xml']
                for required_file in required_files:
                    if required_file not in file_list:
                        issues.append(f"Missing required file: {required_file}")
                
                # Check for content.opf (accept root, OEBPS/, or EPUB/ locations)
                opf_files = ['content.opf', 'OEBPS/content.opf', 'EPUB/content.opf']
                found_opf = any(opf in file_list for opf in opf_files)
                if not found_opf:
                    issues.append("Missing required file: content.opf (should be at root, OEBPS/, or EPUB/)")
                    # Add debug info about what files are actually present
                    opf_like_files = [f for f in file_list if 'opf' in f.lower()]
                    if opf_like_files:
                        issues.append(f"Found OPF-like files: {', '.join(opf_like_files)}")
                    else:
                        issues.append(f"No OPF files found. Available files: {', '.join(file_list[:10])}{'...' if len(file_list) > 10 else ''}")
                
                # Check for cover image
                has_cover = any('cover' in name.lower() for name in file_list)
                if not has_cover:
                    issues.append("No cover image found (recommended for Kindle)")
                
                # Check for large files
                for file_info in epub_zip.filelist:
                    if file_info.file_size > 5 * 1024 * 1024:  # 5MB per file
                        issues.append(f"Large file in EPUB: {file_info.filename} ({file_info.file_size / (1024*1024):.1f}MB)")
                
                # Additional EPUB structure checks
                if 'META-INF/container.xml' in file_list:
                    # Check if container.xml references the correct OPF file
                    try:
                        container_content = epub_zip.read('META-INF/container.xml').decode('utf-8')
                        if 'content.opf' not in container_content:
                            issues.append("container.xml may not reference content.opf correctly")
                    except:
                        issues.append("Could not read container.xml content")
        
        except zipfile.BadZipFile:
            issues.append("Invalid EPUB file (not a valid ZIP archive)")
        
        return len(issues) == 0, issues
        
    except Exception as e:
        return False, [f"Error validating EPUB: {str(e)}"]

def get_epub_info(epub_path: str) -> Dict[str, Any]:
    """
    Get detailed information about an EPUB file.
    
    Args:
        epub_path: Path to the EPUB file
        
    Returns:
        Dictionary with EPUB information
    """
    info = {
        'file_size_mb': 0,
        'filename': '',
        'has_cover': False,
        'chapter_count': 0,
        'total_files': 0,
        'validation_issues': [],
        'kindle_compatible': False,
        'epub_structure': {
            'has_container_xml': False,
            'has_content_opf': False,
            'opf_location': None,
            'has_ncx': False,
            'has_nav': False
        }
    }
    
    try:
        if os.path.exists(epub_path):
            info['file_size_mb'] = os.path.getsize(epub_path) / (1024 * 1024)
            info['filename'] = os.path.basename(epub_path)
            
            # Check EPUB structure
            import zipfile
            with zipfile.ZipFile(epub_path, 'r') as epub_zip:
                file_list = epub_zip.namelist()
                info['total_files'] = len(epub_zip.filelist)
                
                # Check EPUB structure components
                info['epub_structure']['has_container_xml'] = 'META-INF/container.xml' in file_list
                
                # Check for content.opf in different locations
                if 'OEBPS/content.opf' in file_list:
                    info['epub_structure']['has_content_opf'] = True
                    info['epub_structure']['opf_location'] = 'OEBPS/'
                elif 'content.opf' in file_list:
                    info['epub_structure']['has_content_opf'] = True
                    info['epub_structure']['opf_location'] = 'root'
                
                # Check for navigation files
                info['epub_structure']['has_ncx'] = any('toc.ncx' in f.lower() for f in file_list)
                info['epub_structure']['has_nav'] = any('nav.xhtml' in f.lower() for f in file_list)
                
                # Count chapters
                chapter_files = [f for f in file_list if 'chapter' in f.lower() and f.endswith('.xhtml')]
                info['chapter_count'] = len(chapter_files)
                
                # Check for cover
                cover_files = [f for f in file_list if 'cover' in f.lower()]
                info['has_cover'] = len(cover_files) > 0
            
            # Validate for Kindle
            is_valid, issues = validate_epub_for_kindle(epub_path)
            info['validation_issues'] = issues
            info['kindle_compatible'] = is_valid
        
    except Exception as e:
        info['validation_issues'] = [f"Error analyzing EPUB: {str(e)}"]
        info['kindle_compatible'] = False
    
    return info 