import pytest
import tempfile
import os
from pathlib import Path
from fastapi.testclient import TestClient
from PIL import Image
import io
import json

from app.main import app

client = TestClient(app)

class TestAPI:
    """Test cases for API endpoints."""
    
    def test_health_check(self):
        """Test health check endpoints."""
        # Test root endpoint
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        
        # Test health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_api_docs(self):
        """Test API documentation endpoints."""
        # Test OpenAPI docs
        response = client.get("/docs")
        assert response.status_code == 200
        
        # Test ReDoc
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def create_test_markdown_file(self):
        """Create a test markdown file."""
        content = """# My Test Book

## Chapter 1: Introduction
### Section 1.1: Getting Started
This is the first chapter of our test book. It contains an introduction to the topic.

### Section 1.2: Basic Concepts
Here we discuss the basic concepts that will be covered throughout the book.

## Chapter 2: Advanced Topics
### Section 2.1: Deep Dive
This chapter goes deeper into the subject matter.

### Section 2.2: Examples
Here are some practical examples to illustrate the concepts.

## Chapter 3: Conclusion
### Section 3.1: Summary
A summary of what we've learned.

### Section 3.2: Next Steps
Suggestions for further reading and exploration.
"""
        return content.encode('utf-8')
    
    def create_test_image(self, width=800, height=1200):
        """Create a test image."""
        img = Image.new('RGB', (width, height), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        return img_bytes.getvalue()
    
    def test_upload_markdown_file(self):
        """Test uploading a markdown file."""
        content = self.create_test_markdown_file()
        
        files = {
            'file': ('test_book.md', content, 'text/markdown')
        }
        
        response = client.post("/api/v1/conversion/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert "file_info" in data
        assert "file_id" in data["file_info"]
        assert "file_path" in data["file_info"]
        assert "file_size" in data["file_info"]
        
        return data["file_info"]["file_id"]
    
    def test_upload_txt_file(self):
        """Test uploading a text file."""
        content = b"This is a test text file.\n\nIt has multiple lines."
        
        files = {
            'file': ('test_book.txt', content, 'text/plain')
        }
        
        response = client.post("/api/v1/conversion/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert "file_info" in data
        assert "file_id" in data["file_info"]
        
        return data["file_info"]["file_id"]
    
    def test_upload_with_cover_image(self):
        """Test uploading a file with cover image."""
        content = self.create_test_markdown_file()
        image_content = self.create_test_image()
        
        files = {
            'file': ('test_book.md', content, 'text/markdown'),
            'cover_image': ('cover.jpg', image_content, 'image/jpeg')
        }
        
        response = client.post("/api/v1/conversion/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert "file_info" in data
        assert "cover_info" in data
        assert data["cover_info"] is not None
        
        return data["file_info"]["file_id"]
    
    def test_upload_invalid_file_type(self):
        """Test uploading an invalid file type."""
        content = b"%PDF-1.4\nThis is a PDF file"
        
        files = {
            'file': ('test.pdf', content, 'application/pdf')
        }
        
        response = client.post("/api/v1/conversion/upload", files=files)
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "Invalid file type" in data["error"]
    
    def test_upload_no_file(self):
        """Test uploading without a file."""
        response = client.post("/api/v1/conversion/upload")
        
        assert response.status_code == 422  # FastAPI returns 422 for missing required fields
        data = response.json()
        assert "detail" in data
    
    def test_upload_invalid_cover_image(self):
        """Test uploading with invalid cover image."""
        content = self.create_test_markdown_file()
        # Create an invalid image (too small)
        image_content = self.create_test_image(200, 300)
        
        files = {
            'file': ('test_book.md', content, 'text/markdown'),
            'cover_image': ('cover.jpg', image_content, 'image/jpeg')
        }
        
        response = client.post("/api/v1/conversion/upload", files=files)
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "too small" in data["error"]
    
    def test_convert_to_epub(self):
        """Test converting a file to EPUB."""
        # First upload a file
        file_id = self.test_upload_markdown_file()
        
        # Prepare metadata
        metadata = {
            "title": "My Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "language": "English",
            "description": "A test book for API validation",
            "keywords": ["test", "markdown", "epub"],
            "content_type": "prose"
        }
        
        data = {
            'file_id': file_id,
            'metadata_json': json.dumps(metadata),
            'content_type': 'prose'
        }
        
        response = client.post("/api/v1/conversion/convert", data=data)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "download_url" in data
        
        return data["download_url"]
    
    def test_convert_poetry(self):
        """Test converting poetry content."""
        # First upload a file
        file_id = self.test_upload_markdown_file()
        
        # Prepare metadata for poetry
        metadata = {
            "title": "My Poetry Book",
            "author": "Test Poet",
            "language": "English",
            "content_type": "poetry"
        }
        
        data = {
            'file_id': file_id,
            'metadata_json': json.dumps(metadata),
            'content_type': 'poetry'
        }
        
        response = client.post("/api/v1/conversion/convert", data=data)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "download_url" in data
    
    def test_convert_invalid_file_id(self):
        """Test converting with invalid file ID."""
        metadata = {
            "title": "My Test Book",
            "author": "Test Author"
        }
        
        data = {
            'file_id': 'invalid-file-id',
            'metadata_json': json.dumps(metadata),
            'content_type': 'prose'
        }
        
        response = client.post("/api/v1/conversion/convert", data=data)
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
    
    def test_convert_invalid_metadata(self):
        """Test converting with invalid metadata."""
        # First upload a file
        file_id = self.test_upload_markdown_file()
        
        # Invalid metadata (missing required fields)
        metadata = {
            "title": "",  # Empty title
            "author": "Test Author"
        }
        
        data = {
            'file_id': file_id,
            'metadata_json': json.dumps(metadata),
            'content_type': 'prose'
        }
        
        response = client.post("/api/v1/conversion/convert", data=data)
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
    
    def test_download_epub(self):
        """Test downloading an EPUB file."""
        # First convert a file
        download_url = self.test_convert_to_epub()
        
        # Download the file
        response = client.get(download_url)
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/epub+zip"
        assert len(response.content) > 0
    
    def test_download_invalid_file_id(self):
        """Test downloading with invalid file ID."""
        response = client.get("/api/v1/conversion/download/invalid-file-id")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
    
    def test_status_check(self):
        """Test status checking endpoint."""
        # First upload a file
        file_id = self.test_upload_markdown_file()
        
        # Check status
        response = client.get(f"/api/v1/conversion/status/{file_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "file_id" in data
    
    def test_status_check_invalid_file_id(self):
        """Test status check with invalid file ID."""
        response = client.get("/api/v1/conversion/status/invalid-file-id")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
    
    def test_delete_files(self):
        """Test deleting files."""
        # First upload a file
        file_id = self.test_upload_markdown_file()
        
        # Delete the files
        response = client.delete(f"/api/v1/conversion/files/{file_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
    
    def test_delete_invalid_file_id(self):
        """Test deleting with invalid file ID."""
        response = client.delete("/api/v1/conversion/files/invalid-file-id")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
    
    def test_complete_workflow(self):
        """Test the complete workflow from upload to download."""
        # 1. Upload file with cover image
        file_id = self.test_upload_with_cover_image()
        
        # 2. Convert to EPUB
        download_url = self.test_convert_to_epub()
        
        # 3. Download EPUB
        response = client.get(download_url)
        assert response.status_code == 200
        
        # 4. Clean up
        response = client.delete(f"/api/v1/conversion/files/{file_id}")
        assert response.status_code == 200 