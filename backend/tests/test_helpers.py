import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from PIL import Image
import io

from app.utils.helpers import (
    generate_file_id,
    validate_uploaded_file,
    validate_cover_image,
    save_uploaded_file,
    save_cover_image,
    cleanup_file
)

class TestHelpers:
    """Test cases for helper functions."""
    
    def test_generate_file_id(self):
        """Test file ID generation."""
        file_id1 = generate_file_id()
        file_id2 = generate_file_id()
        
        assert isinstance(file_id1, str)
        assert len(file_id1) > 0
        assert file_id1 != file_id2  # Should be unique
    
    def test_validate_uploaded_file_valid_markdown(self):
        """Test validation of valid markdown file."""
        # Create a mock UploadFile
        mock_file = Mock()
        mock_file.filename = "test.md"
        mock_file.file = io.BytesIO(b"# Test Markdown\n\nThis is a test.")
        
        is_valid, error = validate_uploaded_file(mock_file)
        
        assert is_valid
        assert error is None
    
    def test_validate_uploaded_file_valid_txt(self):
        """Test validation of valid text file."""
        # Create a mock UploadFile
        mock_file = Mock()
        mock_file.filename = "test.txt"
        mock_file.file = io.BytesIO(b"This is a test text file.")
        
        is_valid, error = validate_uploaded_file(mock_file)
        
        assert is_valid
        assert error is None
    
    def test_validate_uploaded_file_no_file(self):
        """Test validation with no file."""
        is_valid, error = validate_uploaded_file(None)
        
        assert not is_valid
        assert "No file uploaded" in error
    
    def test_validate_uploaded_file_too_large(self):
        """Test validation of file that's too large."""
        # Create a large mock file
        large_content = b"x" * (11 * 1024 * 1024)  # 11MB
        mock_file = Mock()
        mock_file.filename = "large.md"
        mock_file.file = io.BytesIO(large_content)
        
        is_valid, error = validate_uploaded_file(mock_file)
        
        assert not is_valid
        assert "exceeds" in error
    
    def test_validate_uploaded_file_invalid_type(self):
        """Test validation of invalid file type."""
        # Create a mock file with invalid content
        mock_file = Mock()
        mock_file.filename = "test.pdf"
        mock_file.file = io.BytesIO(b"%PDF-1.4\nThis is a PDF file")
        
        is_valid, error = validate_uploaded_file(mock_file)
        
        assert not is_valid
        assert "Invalid file type" in error
    
    def test_validate_cover_image_no_image(self):
        """Test validation with no cover image."""
        is_valid, error, info = validate_cover_image(None)
        
        assert is_valid
        assert error is None
        assert info is None
    
    def test_validate_cover_image_valid_jpeg(self):
        """Test validation of valid JPEG image."""
        # Create a test JPEG image
        img = Image.new('RGB', (800, 1200), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        mock_image = Mock()
        mock_image.filename = "cover.jpg"
        mock_image.file = img_bytes
        
        is_valid, error, info = validate_cover_image(mock_image)
        
        assert is_valid
        assert error is None
        assert info is not None
        assert info['format'] == 'JPEG'
        assert info['width'] == 800
        assert info['height'] == 1200
    
    def test_validate_cover_image_too_small(self):
        """Test validation of image that's too small."""
        # Create a small test image
        img = Image.new('RGB', (200, 300), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        mock_image = Mock()
        mock_image.filename = "small.jpg"
        mock_image.file = img_bytes
        
        is_valid, error, info = validate_cover_image(mock_image)
        
        assert not is_valid
        assert "too small" in error
    
    def test_validate_cover_image_too_large(self):
        """Test validation of image that's too large."""
        # Create a large test image
        img = Image.new('RGB', (4000, 6000), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        mock_image = Mock()
        mock_image.filename = "large.jpg"
        mock_image.file = img_bytes
        
        is_valid, error, info = validate_cover_image(mock_image)
        
        assert not is_valid
        assert "too large" in error
    
    def test_validate_cover_image_invalid_format(self):
        """Test validation of image with invalid format."""
        # Create a test image in unsupported format
        img = Image.new('RGB', (800, 1200), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='BMP')  # BMP is not supported
        img_bytes.seek(0)
        
        mock_image = Mock()
        mock_image.filename = "test.bmp"
        mock_image.file = img_bytes
        
        is_valid, error, info = validate_cover_image(mock_image)
        
        assert not is_valid
        assert "Invalid image format" in error
    
    def test_save_uploaded_file(self):
        """Test saving uploaded file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a mock file
            content = b"# Test Markdown\n\nThis is a test."
            mock_file = Mock()
            mock_file.filename = "test.md"
            mock_file.file = io.BytesIO(content)
            
            file_id = "test-123"
            file_path = save_uploaded_file(mock_file, file_id, temp_dir)
            
            # Check if file was saved
            assert os.path.exists(file_path)
            assert Path(file_path).read_bytes() == content
    
    def test_save_cover_image(self):
        """Test saving cover image."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test image
            img = Image.new('RGB', (800, 1200), color='red')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            
            mock_image = Mock()
            mock_image.filename = "cover.jpg"
            mock_image.file = img_bytes
            
            file_id = "test-123"
            file_path = save_cover_image(mock_image, file_id, temp_dir)
            
            # Check if file was saved
            assert os.path.exists(file_path)
    
    def test_cleanup_file(self):
        """Test file cleanup."""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
        
        # File should exist
        assert os.path.exists(temp_path)
        
        # Clean up file
        result = cleanup_file(temp_path)
        
        assert result
        assert not os.path.exists(temp_path)
    
    def test_cleanup_nonexistent_file(self):
        """Test cleanup of non-existent file."""
        result = cleanup_file("/nonexistent/file.txt")
        
        assert not result 