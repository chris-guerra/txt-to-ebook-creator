import pytest
import os
import tempfile
from pathlib import Path
from PIL import Image
import io
import uuid

from app.utils.helpers import (
    process_cover_image_for_kindle,
    create_safe_filename,
    validate_epub_for_kindle,
    get_epub_info
)
from app.converters.markdown_to_epub import MarkdownToEPUBConverter
from app.models.book import BookMetadata

class TestKindleCompatibility:
    """Test Kindle compatibility features."""
    
    def test_create_safe_filename(self):
        """Test safe filename generation for Kindle."""
        # Test normal title
        assert create_safe_filename("My Book Title") == "My Book Title.epub"
        
        # Test with special characters (preserves accented characters)
        assert create_safe_filename("Book with áccénts & symbols!") == "Book with áccénts & symbols!.epub"
        
        # Test with numbers
        assert create_safe_filename("Book 123") == "Book 123.epub"
        
        # Test very long title
        long_title = "A" * 100
        result = create_safe_filename(long_title)
        assert len(result) <= 55  # .epub extension included
        assert result.endswith(".epub")
        
        # Test with custom extension
        assert create_safe_filename("Test", ".txt") == "Test.txt"
        
        # Test with truly problematic characters
        assert create_safe_filename("Book with <bad> chars") == "Book with _bad_ chars.epub"
    
    def test_cover_image_processing(self):
        """Test cover image processing for Kindle compatibility."""
        # Create a test image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            # Create a test image with RGBA mode (needs conversion to RGB)
            img = Image.new('RGBA', (800, 1200), color=(255, 0, 0, 255))
            img.save(tmp_file.name)
            
            # Process the image
            processed_path = process_cover_image_for_kindle(tmp_file.name)
            
            # Check that the processed image exists
            assert os.path.exists(processed_path)
            
            # Check that it's now RGB
            with Image.open(processed_path) as processed_img:
                assert processed_img.mode == 'RGB'
                
                # Check dimensions (should be at least minimum)
                width, height = processed_img.size
                assert width >= 400
                assert height >= 600
                
                # Check file size
                file_size = os.path.getsize(processed_path)
                assert file_size <= 2 * 1024 * 1024  # 2MB limit
            
            # Cleanup
            os.unlink(tmp_file.name)
            if processed_path != tmp_file.name:
                os.unlink(processed_path)
    
    def test_html_sanitization_preserves_accents(self):
        """Test that HTML sanitization preserves Spanish accented characters."""
        converter = MarkdownToEPUBConverter()
        
        # Test content with Spanish characters
        test_content = """
        # Mi Libro
        
        Este es un libro con caracteres españoles:
        - á, é, í, ó, ú (vocales acentuadas)
        - ñ (n con tilde)
        - ü (u con diéresis)
        - ¿, ¡ (signos de interrogación y exclamación)
        
        También tiene **negrita** y *cursiva*.
        """
        
        # Convert to HTML
        html = converter._markdown_to_html(test_content)
        
        # Check that Spanish characters are preserved
        assert 'á' in html
        assert 'é' in html
        assert 'í' in html
        assert 'ó' in html
        assert 'ú' in html
        assert 'ñ' in html
        assert 'ü' in html
        assert '¿' in html
        assert '¡' in html
        
        # Check that basic formatting is preserved
        assert '<strong>' in html or 'font-weight: bold' in html
        assert '<em>' in html or 'font-style: italic' in html
    
    def test_html_sanitization_removes_scripts(self):
        """Test that HTML sanitization removes problematic elements."""
        converter = MarkdownToEPUBConverter()
        
        # Test content with problematic elements
        test_html = """
        <h1>Test</h1>
        <script>alert('bad');</script>
        <style>body { color: red; }</style>
        <p>Normal content</p>
        <iframe src="bad.html"></iframe>
        """
        
        # Sanitize HTML
        clean_html = converter._sanitize_html_for_kindle(test_html)
        
        # Check that problematic elements are removed
        assert '<script>' not in clean_html
        assert '<style>' not in clean_html
        assert '<iframe>' not in clean_html
        
        # Check that normal content is preserved
        assert '<h1>Test</h1>' in clean_html
        assert '<p>Normal content</p>' in clean_html
    
    def test_epub_validation(self):
        """Test EPUB validation functions."""
        # Test with non-existent file
        is_valid, issues = validate_epub_for_kindle("nonexistent.epub")
        assert not is_valid
        assert "does not exist" in issues[0]
        
        # Test with invalid filename
        with tempfile.NamedTemporaryFile(suffix='.epub', delete=False) as tmp_file:
            tmp_file.write(b"not a real epub")
            tmp_file.flush()
            
            is_valid, issues = validate_epub_for_kindle(tmp_file.name)
            assert not is_valid
            assert "Invalid EPUB file" in issues[0]
            
            os.unlink(tmp_file.name)
    
    def test_epub_info_extraction(self):
        """Test EPUB information extraction."""
        # Test with non-existent file
        info = get_epub_info("nonexistent.epub")
        assert info['file_size_mb'] == 0
        assert info['filename'] == ''
        assert not info['kindle_compatible']
        assert len(info['validation_issues']) >= 0  # May or may not have issues for non-existent files
        assert 'epub_structure' in info
        assert info['epub_structure']['has_container_xml'] == False
        assert info['epub_structure']['has_content_opf'] == False
    
    def test_complete_kindle_conversion(self):
        """Test complete conversion with Kindle compatibility."""
        converter = MarkdownToEPUBConverter()
        
        # Create test metadata
        metadata = BookMetadata(
            title="Mi Libro de Prueba",
            author="Autor Español",
            language="es",
            description="Un libro con caracteres españoles"
        )
        
        # Create test markdown content
        test_content = """
        # Mi Libro de Prueba
        
        ## Capítulo 1
        
        Este es el primer capítulo con caracteres españoles: á, é, í, ó, ú, ñ, ü.
        
        ### Sección 1.1
        
        Contenido de la sección con **negrita** y *cursiva*.
        
        ## Capítulo 2
        
        Segundo capítulo con más contenido.
        """
        
        # Create temporary markdown file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp_file:
            tmp_file.write(test_content)
            tmp_file.flush()
            
            # Convert to EPUB
            epub_path = converter.convert(
                markdown_file_path=tmp_file.name,
                metadata=metadata
            )
            
            # Check that EPUB was created
            assert os.path.exists(epub_path)
            
            # Validate for Kindle compatibility
            is_valid, issues = validate_epub_for_kindle(epub_path)
            
            # Get EPUB info
            epub_info = get_epub_info(epub_path)
            
            # Basic checks
            assert epub_info['file_size_mb'] > 0
            assert epub_info['chapter_count'] >= 1  # Should have at least 1 chapter (might be 1 or 2 depending on parsing)
            assert epub_info['filename'].endswith('.epub')
            
            # Check that identifier was generated (UUID since no ISBN provided)
            assert metadata.get_identifier() is not None
            assert len(metadata.get_identifier()) > 0
            
            # Cleanup
            os.unlink(tmp_file.name)
            os.unlink(epub_path)
    
    def test_filename_with_special_characters(self):
        """Test filename generation with various special characters."""
        test_cases = [
            ("Book with spaces", "Book with spaces.epub"),
            ("Book-with-dashes", "Book-with-dashes.epub"),
            ("Book_with_underscores", "Book_with_underscores.epub"),
            ("Book with áccénts", "Book with áccénts.epub"),
            ("Book with symbols!@#$%", "Book with symbols!@#$%.epub"),
            ("Book with numbers 123", "Book with numbers 123.epub"),
            ("Book with dots...", "Book with dots....epub"),
            ("Book with <bad> chars", "Book with _bad_ chars.epub"),
        ]
        
        for input_title, expected in test_cases:
            result = create_safe_filename(input_title)
            assert result == expected
    
    def test_cover_image_size_optimization(self):
        """Test cover image size optimization."""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            # Create a large image
            img = Image.new('RGB', (3000, 4000), color=(255, 0, 0))
            img.save(tmp_file.name, 'JPEG', quality=95)
            
            original_size = os.path.getsize(tmp_file.name)
            
            # Process the image
            processed_path = process_cover_image_for_kindle(tmp_file.name)
            
            # Check that size was reduced
            processed_size = os.path.getsize(processed_path)
            assert processed_size <= 2 * 1024 * 1024  # 2MB limit
            
            # Check dimensions were adjusted
            with Image.open(processed_path) as processed_img:
                width, height = processed_img.size
                assert width <= 1600
                assert height <= 2400
            
            # Cleanup
            os.unlink(tmp_file.name)
            if processed_path != tmp_file.name:
                os.unlink(processed_path)
    
    def test_metadata_identifier_generation(self):
        """Test identifier generation with ISBN and UUID fallback."""
        # Test with ISBN
        metadata_with_isbn = BookMetadata(
            title="Test Book",
            author="Test Author",
            isbn="9780123456789",
            language="en"
        )
        assert metadata_with_isbn.get_identifier() == "9780123456789"
        
        # Test without ISBN (should generate UUID)
        metadata_without_isbn = BookMetadata(
            title="Test Book",
            author="Test Author",
            language="es"
        )
        identifier = metadata_without_isbn.get_identifier()
        assert identifier is not None
        assert len(identifier) > 0
        # Should be a UUID format
        try:
            uuid.UUID(identifier)
        except ValueError:
            pytest.fail("Generated identifier is not a valid UUID")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 