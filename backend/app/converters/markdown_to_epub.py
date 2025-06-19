import os
import uuid
import re
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
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
            
            # Parse markdown into chapters
            chapters = self._parse_markdown_chapters(markdown_content)
            
            # Create EPUB book
            book = self._create_epub_book(metadata, chapters, cover_image_path)
            
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
    
    def _parse_markdown_chapters(self, markdown_content: str) -> List[Tuple[str, str]]:
        """
        Parse Markdown content into chapters based on ## headings.
        
        Args:
            markdown_content: Raw markdown content
            
        Returns:
            List of (chapter_title, chapter_content) tuples
        """
        # Split content by ## headings (chapters)
        chapter_pattern = r'^##\s+(.+)$'
        chapter_matches = list(re.finditer(chapter_pattern, markdown_content, re.MULTILINE))
        
        chapters = []
        
        if not chapter_matches:
            # No chapters found, treat entire content as one chapter
            html_content = self._markdown_to_html(markdown_content)
            chapters.append(("Content", html_content))
        else:
            # Process each chapter
            for i, match in enumerate(chapter_matches):
                chapter_title = match.group(1).strip()
                
                # Get chapter content
                start_pos = match.end()
                if i + 1 < len(chapter_matches):
                    end_pos = chapter_matches[i + 1].start()
                else:
                    end_pos = len(markdown_content)
                
                chapter_content = markdown_content[start_pos:end_pos].strip()
                
                # Convert chapter content to HTML
                html_content = self._markdown_to_html(chapter_content)
                chapters.append((chapter_title, html_content))
        
        return chapters
    
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
        chapters: List[Tuple[str, str]], 
        cover_image_path: Optional[str] = None
    ) -> epub.EpubBook:
        """Create EPUB book with metadata and chapters."""
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
        
        # Create chapters
        epub_chapters = []
        toc_items = []
        
        for i, (chapter_title, chapter_content) in enumerate(chapters):
            # Create safe filename
            safe_title = "".join(c for c in chapter_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_').lower()
            filename = f"chapter_{i+1}_{safe_title}.xhtml"
            
            # Create EPUB chapter
            chapter = epub.EpubHtml(
                title=chapter_title,
                file_name=filename,
                content=chapter_content
            )
            book.add_item(chapter)
            epub_chapters.append(chapter)
            
            # Add to table of contents
            toc_items.append(epub.Link(filename, chapter_title, f"chapter_{i+1}"))
        
        # Set table of contents
        book.toc = toc_items
        
        # Add default NCX and Nav files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        
        # Define spine (navigation + all chapters)
        book.spine = ['nav'] + epub_chapters
        
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