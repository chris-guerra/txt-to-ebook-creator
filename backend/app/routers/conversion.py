from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from typing import Optional
import json
import os
from pathlib import Path

from ..models.book import BookMetadata, ConversionRequest, ConversionResponse, ConversionStatus
from ..converters.markdown_to_epub import MarkdownToEPUBConverter
from ..utils.helpers import (
    validate_uploaded_file, 
    validate_cover_image, 
    save_uploaded_file, 
    save_cover_image,
    generate_file_id,
    cleanup_file
)

router = APIRouter()

# In-memory storage for conversion status (in production, use Redis or database)
conversion_status = {}

@router.post("/upload", response_model=dict)
async def upload_file(
    file: UploadFile = File(...),
    cover_image: Optional[UploadFile] = File(None)
):
    """
    Upload Markdown/TXT file and optional cover image.
    
    Returns:
        dict: File information and validation status
    """
    # Validate uploaded file
    is_valid, error_message = validate_uploaded_file(file)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Validate cover image if provided
    cover_image_info = None
    if cover_image:
        is_valid, error_message, image_info = validate_cover_image(cover_image)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)
        cover_image_info = image_info
    
    # Generate unique file ID
    file_id = generate_file_id()
    
    # Save uploaded file
    file_path = save_uploaded_file(file, file_id)
    
    # Save cover image if provided
    cover_path = None
    if cover_image:
        cover_path = save_cover_image(cover_image, file_id)
    
    # Store file information
    file_info = {
        "file_id": file_id,
        "filename": file.filename,
        "file_size": file.size,
        "file_path": file_path,
        "cover_path": cover_path,
        "cover_info": cover_image_info
    }
    
    return {
        "success": True,
        "message": "File uploaded successfully",
        "file_info": file_info
    }

@router.post("/convert", response_model=ConversionResponse)
async def convert_to_epub(
    background_tasks: BackgroundTasks,
    file_id: str = Form(...),
    metadata_json: str = Form(...),
    content_type: str = Form(default="prose")
):
    """
    Convert uploaded file to EPUB format.
    
    Args:
        file_id: Unique identifier for the uploaded file
        metadata_json: JSON string containing book metadata
        content_type: Type of content (prose/poetry)
    
    Returns:
        ConversionResponse: Conversion status and file information
    """
    try:
        # Parse metadata
        metadata_dict = json.loads(metadata_json)
        metadata = BookMetadata(**metadata_dict)
        
        # Get file paths (in production, retrieve from database)
        file_path = f"uploads/{file_id}.md"  # Simplified for demo
        cover_path = f"uploads/covers/{file_id}_cover.jpg" if os.path.exists(f"uploads/covers/{file_id}_cover.jpg") else None
        
        # Validate file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Uploaded file not found")
        
        # Initialize converter
        converter = MarkdownToEPUBConverter()
        
        # Convert to EPUB
        epub_path = converter.convert(
            markdown_file_path=file_path,
            metadata=metadata,
            cover_image_path=cover_path
        )
        
        # Generate download URL
        download_url = f"/api/v1/conversion/download/{file_id}"
        
        # Store conversion status
        conversion_status[file_id] = {
            "status": "completed",
            "progress": 100,
            "message": "Conversion completed successfully",
            "epub_path": epub_path,
            "download_url": download_url
        }
        
        # Schedule cleanup of temporary files
        background_tasks.add_task(cleanup_file, file_path)
        if cover_path and os.path.exists(cover_path):
            background_tasks.add_task(cleanup_file, cover_path)
        
        return ConversionResponse(
            success=True,
            message="Conversion completed successfully",
            file_id=file_id,
            download_url=download_url
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid metadata JSON format")
    except Exception as e:
        # Update status to failed
        conversion_status[file_id] = {
            "status": "failed",
            "progress": 0,
            "message": f"Conversion failed: {str(e)}",
            "error": str(e)
        }
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

@router.get("/status/{file_id}", response_model=ConversionStatus)
async def get_conversion_status(file_id: str):
    """
    Get conversion status for a file.
    
    Args:
        file_id: Unique identifier for the file
    
    Returns:
        ConversionStatus: Current conversion status
    """
    if file_id not in conversion_status:
        raise HTTPException(status_code=404, detail="File not found")
    
    status = conversion_status[file_id]
    return ConversionStatus(
        status=status["status"],
        progress=status.get("progress", 0),
        message=status["message"],
        file_id=file_id
    )

@router.get("/download/{file_id}")
async def download_epub(file_id: str):
    """
    Download converted EPUB file.
    
    Args:
        file_id: Unique identifier for the file
    
    Returns:
        FileResponse: EPUB file for download
    """
    if file_id not in conversion_status:
        raise HTTPException(status_code=404, detail="File not found")
    
    status = conversion_status[file_id]
    if status["status"] != "completed":
        raise HTTPException(status_code=400, detail="Conversion not completed")
    
    epub_path = status.get("epub_path")
    if not epub_path or not os.path.exists(epub_path):
        raise HTTPException(status_code=404, detail="EPUB file not found")
    
    # Get filename from path
    filename = os.path.basename(epub_path)
    
    return FileResponse(
        path=epub_path,
        filename=filename,
        media_type="application/epub+zip"
    )

@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """
    Delete uploaded file and any associated converted files.
    
    Args:
        file_id: Unique identifier for the file
    
    Returns:
        dict: Deletion status
    """
    try:
        # Clean up files
        file_path = f"uploads/{file_id}.md"
        cover_path = f"uploads/covers/{file_id}_cover.jpg"
        epub_path = conversion_status.get(file_id, {}).get("epub_path")
        
        # Delete files
        cleanup_file(file_path)
        cleanup_file(cover_path)
        if epub_path:
            cleanup_file(epub_path)
        
        # Remove from status
        if file_id in conversion_status:
            del conversion_status[file_id]
        
        return {
            "success": True,
            "message": "Files deleted successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting files: {str(e)}") 