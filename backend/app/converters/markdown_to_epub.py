import os
import uuid
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import HTTPException
from ebooklib import epub
import markdown
from ..models.book import BookMetadata, ContentType
from ..utils.helpers import generate_file_id

class MarkdownToEPUBConverter:
    """Convert Markdown files to EPUB format."""
    
    def __init__(self):
        self.output_dir = "outputs"
        Path(self.output_dir).mkdir(exist_ok=True)
    
    def convert(
        self, 
        markdown_file_path: str, 
        metadata: BookMetadata, 
        cover_image_path: Optional[str] = None,
        output_filename: Optional[str] = None
    ) -> str:
        """
        Convert Markdown file to EPUB.
        
        Args:
            markdown_file_path: Path to the Markdown file
            metadata: Book metadata
            cover_image_path: Optional path to cover image
            output_filename: Optional output filename
            
        Returns:
            Path to the generated EPUB file
        """
        try:
            # Read markdown content
            with open(markdown_file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # Convert markdown to HTML
            html_content = self._markdown_to_html(markdown_content)
            
            # Create EPUB book
            book = self._create_epub_book(metadata, html_content, cover_image_path)
            
            # Generate output filename
            if not output_filename:
                safe_title = "".join(c for c in metadata.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                output_filename = f"{safe_title}.epub"
            
            output_path = Path(self.output_dir) / output_filename
            
            # Write EPUB file
            epub.write_epub(str(output_path), book)
            
            return str(output_path)
            
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error converting to EPUB: {str(e)}"
            )
    
    def _markdown_to_html(self, markdown_content: str) -> str:
        """Convert Markdown content to HTML."""
        # Configure markdown extensions for better conversion
        extensions = [
            'markdown.extensions.toc',
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.nl2br'
        ]
        
        md = markdown.Markdown(extensions=extensions)
        html = md.convert(markdown_content)
        
        # Add basic CSS styling
        css = """
        <style>
        body { font-family: serif; line-height: 1.6; margin: 2em; }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; }
        h2 { color: #34495e; border-bottom: 1px solid #bdc3c7; }
        h3 { color: #7f8c8d; }
        code { background-color: #f8f9fa; padding: 0.2em 0.4em; border-radius: 3px; }
        pre { background-color: #f8f9fa; padding: 1em; border-radius: 5px; overflow-x: auto; }
        blockquote { border-left: 4px solid #3498db; margin: 0; padding-left: 1em; }
        </style>
        """
        
        return f"{css}\n{html}"
    
    def _create_epub_book(
        self, 
        metadata: BookMetadata, 
        html_content: str, 
        cover_image_path: Optional[str] = None
    ) -> epub.EpubBook:
        """Create EPUB book with metadata and content."""
        # Create EPUB book
        book = epub.EpubBook()
        
        # Set metadata
        book.set_identifier(f"urn:uuid:{generate_file_id()}")
        book.set_title(metadata.title)
        book.set_language(metadata.language.lower())
        book.add_author(metadata.author)
        
        if metadata.publisher:
            book.add_metadata('DC', 'publisher', metadata.publisher)
        
        if metadata.publication_date:
            book.add_metadata('DC', 'date', metadata.publication_date.isoformat())
        
        if metadata.isbn:
            book.add_metadata('DC', 'identifier', metadata.isbn, {'scheme': 'ISBN'})
        
        if metadata.description:
            book.add_metadata('DC', 'description', metadata.description)
        
        if metadata.keywords:
            book.add_metadata('DC', 'subject', ', '.join(metadata.keywords))
        
        # Add cover image if provided
        if cover_image_path and os.path.exists(cover_image_path):
            try:
                with open(cover_image_path, 'rb') as cover_file:
                    book.set_cover("cover.jpg", cover_file.read())
            except Exception as e:
                print(f"Warning: Could not add cover image: {e}")
        
        # Create chapter
        chapter = epub.EpubHtml(
            title=metadata.title,
            file_name='chapter.xhtml',
            content=html_content
        )
        book.add_item(chapter)
        
        # Create table of contents
        book.toc = [epub.Link('chapter.xhtml', metadata.title, 'chapter')]
        
        # Add default NCX and Nav files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        
        # Define spine
        book.spine = ['nav', chapter]
        
        return book
    
    def cleanup_files(self, file_paths: list) -> bool:
        """Clean up temporary files."""
        success = True
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                success = False
        return success 