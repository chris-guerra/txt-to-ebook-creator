#!/usr/bin/env python3
"""
Simple test script for the Markdown to EPUB Creator API.
"""

import requests
import json
import time
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoints."""
    print("Testing health check endpoints...")
    
    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")
    
    # Test health endpoint
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health endpoint: {response.status_code} - {response.json()}")
    
    return response.status_code == 200

def test_api_docs():
    """Test API documentation endpoints."""
    print("\nTesting API documentation...")
    
    # Test OpenAPI docs
    response = requests.get(f"{BASE_URL}/docs")
    print(f"OpenAPI docs: {response.status_code}")
    
    # Test ReDoc
    response = requests.get(f"{BASE_URL}/redoc")
    print(f"ReDoc: {response.status_code}")
    
    return True

def create_test_markdown():
    """Create a test Markdown file with chapters."""
    test_content = """# My Test Book

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
    
    test_file = Path("test_book.md")
    test_file.write_text(test_content, encoding='utf-8')
    return test_file

def test_file_upload():
    """Test file upload endpoint."""
    print("\nTesting file upload...")
    
    # Create test file
    test_file = create_test_markdown()
    
    # Upload file
    with open(test_file, 'rb') as f:
        files = {'file': ('test_book.md', f, 'text/markdown')}
        response = requests.post(f"{BASE_URL}/api/v1/conversion/upload", files=files)
    
    print(f"Upload response: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"File ID: {result['file_info']['file_id']}")
        return result['file_info']['file_id']
    else:
        print(f"Upload failed: {response.text}")
        return None

def test_conversion(file_id):
    """Test conversion endpoint."""
    print(f"\nTesting conversion for file ID: {file_id}")
    
    # Prepare metadata
    metadata = {
        "title": "My Test Book",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "language": "en",
        "description": "A test book for API validation",
        "keywords": ["test", "markdown", "epub"],
        "content_type": "prose"
    }
    
    # Convert to EPUB
    data = {
        'file_id': file_id,
        'metadata_json': json.dumps(metadata),
        'content_type': 'prose'
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/conversion/convert", data=data)
    print(f"Conversion response: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Conversion successful: {result['message']}")
        return result.get('download_url')
    else:
        print(f"Conversion failed: {response.text}")
        return None

def test_download(download_url):
    """Test download endpoint."""
    print(f"\nTesting download: {download_url}")
    
    response = requests.get(f"{BASE_URL}{download_url}")
    print(f"Download response: {response.status_code}")
    
    if response.status_code == 200:
        # Save the file
        output_file = Path("test_output.epub")
        output_file.write_bytes(response.content)
        print(f"EPUB file saved as: {output_file}")
        return True
    else:
        print(f"Download failed: {response.text}")
        return False

def cleanup_test_files():
    """Clean up test files."""
    print("\nCleaning up test files...")
    
    files_to_remove = [
        "test_book.md",
        "test_output.epub"
    ]
    
    for file_path in files_to_remove:
        if Path(file_path).exists():
            Path(file_path).unlink()
            print(f"Removed: {file_path}")

def main():
    """Run all tests."""
    print("Starting API tests...")
    
    try:
        # Test health check
        if not test_health_check():
            print("Health check failed. Is the server running?")
            return
        
        # Test API docs
        test_api_docs()
        
        # Test file upload
        file_id = test_file_upload()
        if not file_id:
            print("File upload failed. Stopping tests.")
            return
        
        # Test conversion
        download_url = test_conversion(file_id)
        if not download_url:
            print("Conversion failed. Stopping tests.")
            return
        
        # Test download
        if test_download(download_url):
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Download test failed.")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
    finally:
        cleanup_test_files()

if __name__ == "__main__":
    main() 