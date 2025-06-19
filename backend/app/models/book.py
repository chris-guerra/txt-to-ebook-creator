from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date
from enum import Enum

class ContentType(str, Enum):
    """Content type enumeration."""
    PROSE = "prose"
    POETRY = "poetry"

class BookMetadata(BaseModel):
    """Book metadata model."""
    title: str = Field(..., min_length=2, max_length=200, description="Book title")
    author: str = Field(..., min_length=2, max_length=100, description="Book author")
    publisher: Optional[str] = Field(None, max_length=100, description="Publisher name")
    publication_date: Optional[date] = Field(None, description="Publication date")
    isbn: Optional[str] = Field(None, description="ISBN number")
    language: str = Field(default="English", description="Book language")
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