#!/usr/bin/env python3
"""
Quick test to verify OPF validation fix.
"""

import os
import tempfile
import zipfile
from app.utils.helpers import get_epub_info

def create_test_epub_with_epub_opf():
    """Create a test EPUB with OPF in EPUB/ directory."""
    with tempfile.NamedTemporaryFile(suffix='.epub', delete=False) as tmp_file:
        with zipfile.ZipFile(tmp_file.name, 'w') as epub_zip:
            # Add container.xml
            epub_zip.writestr('META-INF/container.xml', 
                '<?xml version="1.0"?><container><rootfiles><rootfile full-path="EPUB/content.opf"/></rootfiles></container>')
            
            # Add content.opf in EPUB/ directory
            epub_zip.writestr('EPUB/content.opf', 
                '<?xml version="1.0"?><package><metadata><title>Test</title></metadata><spine></spine></package>')
            
            # Add a sample chapter
            epub_zip.writestr('EPUB/chapter1.xhtml', '<html><body><h1>Test Chapter</h1></body></html>')
        
        return tmp_file.name

def test_opf_validation():
    """Test OPF validation with EPUB/content.opf."""
    print("Testing OPF validation fix...")
    
    # Create test EPUB
    epub_path = create_test_epub_with_epub_opf()
    
    try:
        # Get EPUB info
        info = get_epub_info(epub_path)
        
        # Check results
        print(f"EPUB Structure: {info['epub_structure']}")
        print(f"Has content.opf: {info['epub_structure']['has_content_opf']}")
        print(f"OPF Location: {info['epub_structure']['opf_location']}")
        print(f"Kindle Compatible: {info['kindle_compatible']}")
        print(f"Validation Issues: {info['validation_issues']}")
        
        # Verify the fix works
        assert info['epub_structure']['has_content_opf'] == True, "OPF not detected"
        assert info['epub_structure']['opf_location'] == 'EPUB/', "Wrong OPF location"
        # Don't assert Kindle compatibility since our test EPUB is minimal
        print("✅ OPF validation fix works correctly!")
        
    finally:
        # Cleanup
        os.unlink(epub_path)

if __name__ == "__main__":
    test_opf_validation() 