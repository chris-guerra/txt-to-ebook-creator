import os
import uuid
import re
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from fastapi import HTTPException
from ebooklib import epub
import markdown
from bs4 import BeautifulSoup
from ..models.book import BookMetadata, ContentType
from ..utils.helpers import generate_file_id, process_cover_image_for_kindle, create_safe_filename

class MarkdownToEPUBConverter:
    """Convert Markdown files to EPUB format with Kindle compatibility."""
    
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
        Convert Markdown file to EPUB with Kindle compatibility.
        
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
            
            # Process cover image for Kindle compatibility
            processed_cover_path = None
            if cover_image_path and os.path.exists(cover_image_path):
                processed_cover_path = process_cover_image_for_kindle(cover_image_path)
            
            # Create EPUB book
            book = self._create_epub_book(metadata, chapters, processed_cover_path)
            
            # Generate safe output filename
            if not output_filename:
                output_filename = create_safe_filename(metadata.title)
            
            output_path = Path(self.output_dir) / output_filename
            
            # Write EPUB file
            epub.write_epub(str(output_path), book)
            
            # Debug: Check what files were actually created
            print(f"DEBUG: EPUB created at {output_path}")
            try:
                import zipfile
                with zipfile.ZipFile(str(output_path), 'r') as epub_zip:
                    print(f"DEBUG: Files in EPUB: {epub_zip.namelist()}")
            except Exception as e:
                print(f"DEBUG: Could not inspect EPUB contents: {e}")
            
            # Clean up processed cover image
            if processed_cover_path and processed_cover_path != cover_image_path:
                try:
                    os.remove(processed_cover_path)
                except:
                    pass
            
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
        """Convert Markdown content to Kindle-compatible HTML."""
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
        
        # Sanitize HTML for Kindle compatibility
        html = self._sanitize_html_for_kindle(html)
        
        # Add Kindle-compatible CSS styling
        css = """
        <style>
        body { 
            font-family: "Times New Roman", serif; 
            line-height: 1.6; 
            margin: 1em; 
            text-align: justify;
            font-size: 1em;
        }
        h1 { 
            color: #000000; 
            border-bottom: 1px solid #000000; 
            font-size: 1.5em;
            margin-top: 1em;
            margin-bottom: 0.5em;
        }
        h2 { 
            color: #000000; 
            border-bottom: 1px solid #666666; 
            font-size: 1.3em;
            margin-top: 1em;
            margin-bottom: 0.5em;
        }
        h3 { 
            color: #333333; 
            font-size: 1.1em;
            margin-top: 1em;
            margin-bottom: 0.5em;
        }
        p {
            margin: 0.5em 0;
            text-indent: 1.5em;
        }
        code { 
            background-color: #f0f0f0; 
            padding: 0.1em 0.3em; 
            border-radius: 2px;
            font-family: monospace;
            font-size: 0.9em;
        }
        pre { 
            background-color: #f0f0f0; 
            padding: 0.5em; 
            border-radius: 3px; 
            overflow-x: auto;
            font-family: monospace;
            font-size: 0.9em;
            margin: 0.5em 0;
        }
        blockquote { 
            border-left: 3px solid #666666; 
            margin: 0.5em 0; 
            padding-left: 1em;
            font-style: italic;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 0.5em 0;
        }
        th, td {
            border: 1px solid #666666;
            padding: 0.3em;
            text-align: left;
        }
        th {
            background-color: #f0f0f0;
            font-weight: bold;
        }
        </style>
        """
        
        return f"{css}\n{html}"
    
    def _sanitize_html_for_kindle(self, html: str) -> str:
        """Sanitize HTML for Kindle compatibility while preserving accented characters."""
        try:
            # Parse HTML
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove problematic elements
            for element in soup.find_all(['script', 'style', 'iframe', 'object', 'embed']):
                element.decompose()
            
            # Ensure all tags are properly closed
            for tag in soup.find_all():
                if not tag.name in ['br', 'hr', 'img', 'input', 'meta', 'link']:
                    if not tag.contents and not tag.string:
                        tag.string = ""
            
            # Convert to string and clean up
            clean_html = str(soup)
            
            # Remove only truly problematic characters (control characters, not accented letters)
            # This preserves Spanish characters like á, é, í, ó, ú, ñ, ü, ¿, ¡
            clean_html = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', clean_html)
            
            # Ensure proper XHTML structure
            clean_html = re.sub(r'<([^>]+)>', lambda m: self._ensure_proper_tag(m.group(1)), clean_html)
            
            return clean_html
            
        except Exception as e:
            # If BeautifulSoup fails, do basic cleaning
            print(f"Warning: HTML sanitization failed, using basic cleaning: {e}")
            return self._basic_html_cleaning(html)
    
    def _ensure_proper_tag(self, tag_content: str) -> str:
        """Ensure proper XHTML tag formatting."""
        # Handle self-closing tags
        self_closing_tags = ['br', 'hr', 'img', 'input', 'meta', 'link']
        tag_name = tag_content.split()[0].lower()
        
        if tag_name in self_closing_tags and not tag_content.endswith('/'):
            return f"<{tag_content} />"
        
        return f"<{tag_content}>"
    
    def _basic_html_cleaning(self, html: str) -> str:
        """Basic HTML cleaning for Kindle compatibility while preserving accented characters."""
        # Remove script tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        
        # Remove style tags (we'll add our own)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        
        # Remove only control characters, NOT accented characters
        html = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', html)
        
        # Ensure proper line breaks
        html = html.replace('\n', ' ')
        html = re.sub(r'\s+', ' ', html)
        
        return html
    
    def _create_epub_book(
        self, 
        metadata: BookMetadata, 
        chapters: List[Tuple[str, str]], 
        cover_image_path: Optional[str] = None
    ) -> epub.EpubBook:
        """Create EPUB book with metadata and chapters."""
        # Create EPUB book
        book = epub.EpubBook()
        
        # Set required Kindle metadata
        book.set_identifier(f"urn:uuid:{metadata.get_identifier()}")
        book.set_title(metadata.title)
        book.set_language(metadata.language)  # Already in ISO format
        book.add_author(metadata.author)
        
        # Set optional metadata
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
                    cover_data = cover_file.read()
                    # Check file size for Kindle compatibility
                    if len(cover_data) <= 2 * 1024 * 1024:  # 2MB limit
                        book.set_cover("cover.jpg", cover_data)
                    else:
                        print(f"Warning: Cover image too large ({len(cover_data)} bytes), skipping")
            except Exception as e:
                print(f"Warning: Could not add cover image: {e}")
        
        # Create chapters
        epub_chapters = []
        toc_items = []
        
        for i, (chapter_title, chapter_content) in enumerate(chapters):
            # Create safe filename for Kindle
            safe_title = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', chapter_title)
            safe_title = re.sub(r'_+', '_', safe_title).strip('_')
            if len(safe_title) > 30:
                safe_title = safe_title[:30]
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
        
        # Set table of contents (required for Kindle)
        book.toc = toc_items
        
        # Add required navigation files for Kindle
        book.add_item(epub.EpubNcx())  # NCX navigation (EPUB 2.0)
        book.add_item(epub.EpubNav())  # NAV navigation (EPUB 3.0)
        
        # Define spine with proper reading order (required for Kindle)
        # Start with navigation, then all chapters
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