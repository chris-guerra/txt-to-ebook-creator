from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import date
from enum import Enum
import uuid

class ContentType(str, Enum):
    """Content type enumeration."""
    PROSE = "prose"
    POETRY = "poetry"

class BookMetadata(BaseModel):
    """Book metadata model with Kindle compatibility."""
    title: str = Field(..., min_length=2, max_length=200, description="Book title")
    author: str = Field(..., min_length=2, max_length=100, description="Book author")
    publisher: Optional[str] = Field(None, max_length=100, description="Publisher name")
    publication_date: Optional[date] = Field(None, description="Publication date in YYYY-MM-DD format")
    isbn: Optional[str] = Field(None, description="ISBN number (optional, UUID will be generated if not provided)")
    language: str = Field(default="es", description="Book language in ISO 639-1 format (e.g., 'es', 'en')")
    description: Optional[str] = Field(None, max_length=1000, description="Book description")
    keywords: Optional[List[str]] = Field(None, description="Keywords for the book")
    content_type: ContentType = Field(default=ContentType.PROSE, description="Content type")

    @validator('isbn')
    def validate_isbn(cls, v):
        """Validate ISBN format."""
        if v is None:
            return v
        
        # Remove hyphens and spaces
        isbn_clean = ''.join(filter(str.isalnum, v))
        
        # Check length (ISBN-10 or ISBN-13)
        if len(isbn_clean) not in [10, 13]:
            raise ValueError("ISBN must be 10 or 13 digits")
        
        # Check if all characters are digits (except last character for ISBN-10)
        if not isbn_clean[:-1].isdigit():
            raise ValueError("ISBN must contain only digits (except last character for ISBN-10)")
        
        # For ISBN-10, last character can be 'X'
        if len(isbn_clean) == 10 and not (isbn_clean[-1].isdigit() or isbn_clean[-1].upper() == 'X'):
            raise ValueError("ISBN-10 last character must be a digit or 'X'")
        
        return v

    @validator('language')
    def validate_language(cls, v):
        """Validate language code format."""
        if not v or len(v) != 2:
            raise ValueError("Language must be a 2-character ISO 639-1 code (e.g., 'es', 'en')")
        return v.lower()

    def get_identifier(self) -> str:
        """Get identifier for EPUB (ISBN if provided, otherwise UUID)."""
        if self.isbn:
            return self.isbn
        return str(uuid.uuid4())

class ConversionRequest(BaseModel):
    """Conversion request model."""
    metadata: BookMetadata
    content_type: ContentType = Field(default=ContentType.PROSE, description="Content type")

class ConversionResponse(BaseModel):
    """Conversion response model."""
    success: bool
    message: str
    file_id: Optional[str] = None
    download_url: Optional[str] = None
    error: Optional[str] = None
    kindle_compatible: Optional[bool] = None
    validation_issues: Optional[List[str]] = None
    epub_info: Optional[Dict[str, Any]] = None

class FileInfo(BaseModel):
    """File information model."""
    filename: str
    file_size: int
    file_type: str
    content_length: Optional[int] = None

class ConversionStatus(BaseModel):
    """Conversion status model."""
    status: str  # "pending", "processing", "completed", "failed"
    progress: int = Field(0, ge=0, le=100)
    message: str
    file_id: Optional[str] = None
    kindle_compatible: Optional[bool] = None
    validation_issues: Optional[List[str]] = None
    epub_info: Optional[Dict[str, Any]] = None 