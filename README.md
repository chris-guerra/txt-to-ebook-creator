# Markdown to EPUB Creator / Creador de EPUB desde Markdown

> **Project Context for AI Assistants**: This is a full-stack web application that converts Markdown files to EPUB format with full Kindle compatibility. It uses FastAPI (Python) for the backend API and Streamlit for the frontend interface. The project focuses on preserving Spanish accented characters, implementing Kindle metadata requirements, and providing comprehensive EPUB validation.

## 📋 Table of Contents / Índice
- [Project Overview](#project-overview)
- [Architecture & Technology Stack](#architecture--technology-stack)
- [Key Features](#key-features)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Development & Testing](#development--testing)
- [Kindle Compatibility](#kindle-compatibility)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Project Overview

A comprehensive tool for converting Markdown files to EPUB format with **full Kindle compatibility**. Features a FastAPI backend for robust file processing and a Streamlit frontend for an intuitive user experience.

**Primary Goals:**
- Convert Markdown/TXT files to Kindle-compatible EPUB format
- Preserve Spanish accented characters (á, é, í, ó, ú, ñ, ü)
- Implement all required Kindle metadata
- Provide comprehensive validation and error handling
- Support both prose and poetry content types

## 🏗️ Architecture & Technology Stack

### Backend (FastAPI)
- **Framework**: FastAPI with Uvicorn ASGI server
- **Core Libraries**: EbookLib, Markdown, Pillow (PIL), Python-magic
- **File Processing**: Upload validation, EPUB generation, cover image processing
- **API**: RESTful endpoints for file upload, conversion, and download

### Frontend (Streamlit)
- **Framework**: Streamlit for rapid web app development
- **Features**: File upload, metadata forms, real-time validation, download links
- **UI**: Responsive design with drag-and-drop functionality

### Project Structure
```
txt-to-ebook-creator/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── models/              # Pydantic data models
│   │   ├── routers/             # API route handlers
│   │   ├── converters/          # Markdown to EPUB conversion logic
│   │   └── utils/               # Helper functions and validation
│   ├── tests/                   # Comprehensive test suite
│   ├── requirements.txt         # Python dependencies
│   └── run_tests.py            # Test runner script
├── frontend/
│   ├── app.py                   # Streamlit application
│   └── requirements.txt         # Frontend dependencies
└── README.md                    # This file
```

## 🌟 Key Features

### ✅ **Kindle Compatibility**
- **Full Kindle Metadata Support**: Title, author, identifier, language, TOC, spine
- **EPUB 2.0 Format**: Optimized for Kindle compatibility
- **Cover Image Processing**: Automatic RGB conversion and size optimization
- **Safe Filenames**: Preserves accented characters while ensuring compatibility
- **Navigation Structure**: Proper NCX and NAV files for navigation
- **Validation**: Comprehensive EPUB structure validation

### 📚 **Content Processing**
- **Markdown Support**: Full Markdown syntax with extensions
- **Chapter Detection**: Automatic chapter and section parsing
- **Content Types**: Support for prose and poetry formats
- **Accented Characters**: Full support for Spanish and other languages
- **HTML Sanitization**: Clean, Kindle-compatible HTML output

### 🎨 **User Interface**
- **File Upload**: Drag-and-drop or file browser
- **Metadata Form**: Complete book information input with validation
- **Cover Image**: Optional cover image upload and processing
- **Real-time Preview**: Live conversion status and progress
- **Download**: Direct EPUB file download
- **Validation Feedback**: Detailed EPUB structure information

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd txt-to-ebook-creator
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd ../frontend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Start the Application

#### Start Backend Server
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Start Frontend Application
```bash
cd frontend
source venv/bin/activate
streamlit run app.py
```

#### Access Points
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 Usage Guide

### 1. Upload Your Markdown File
- Drag and drop your `.md` or `.txt` file
- Or use the file browser to select your file
- **Supported formats**: Markdown (.md), Text (.txt)
- **Maximum size**: 10MB

### 2. Add Book Metadata

#### Required Fields
- **Title** - Required for Kindle UI (2-200 characters)
- **Author** - Required for Kindle UI (2-100 characters)
- **Language** - Required, uses ISO 639-1 codes (e.g., "es", "en")

#### Optional Fields
- **Publisher** - Publisher name
- **Publication Date** - ISO format (YYYY-MM-DD)
- **ISBN** - Optional, UUID will be generated automatically if not provided
- **Description** - Book description (max 1000 characters)
- **Keywords** - Comma-separated keywords

### 3. Upload Cover Image (Optional)
- **Supported formats**: JPEG, PNG
- **Maximum size**: 5MB
- **Minimum dimensions**: 400x600 pixels
- **Recommended dimensions**: 1600x2400 pixels
- **Automatic processing**: RGB conversion and size optimization for Kindle

### 4. Convert and Download
- Click "Convert to EPUB" to start the conversion
- Monitor the conversion progress and validation results
- Download your EPUB file when ready

## 🔧 API Documentation

### Core Endpoints

#### File Upload
```http
POST /api/v1/conversion/upload
Content-Type: multipart/form-data

Parameters:
- file: Markdown/TXT file (required)
- cover_image: JPEG/PNG image (optional)
```

#### Conversion
```http
POST /api/v1/conversion/convert
Content-Type: application/x-www-form-urlencoded

Parameters:
- file_id: Uploaded file ID (required)
- metadata_json: JSON string with book metadata (required)
- content_type: "prose" or "poetry" (required)
```

#### Download
```http
GET /api/v1/conversion/download/{file_id}
```

#### Status Check
```http
GET /api/v1/conversion/status/{file_id}
```

#### File Management
```http
DELETE /api/v1/conversion/files/{file_id}
```

### Response Format
```json
{
  "success": true,
  "message": "Conversion completed successfully",
  "download_url": "/api/v1/conversion/download/{file_id}",
  "kindle_compatible": true,
  "validation_issues": [],
  "epub_info": {
    "file_size_mb": 1.2,
    "filename": "book.epub",
    "has_cover": true,
    "chapter_count": 5,
    "total_files": 12,
    "kindle_compatible": true,
    "epub_structure": {
      "has_container_xml": true,
      "has_content_opf": true,
      "opf_location": "EPUB/",
      "has_ncx": true,
      "has_nav": true
    }
  }
}
```

## 🧪 Development & Testing

### Running Tests
```bash
cd backend
python run_tests.py
```

### Individual Test Categories
```bash
# Unit tests (helper functions)
python -m pytest tests/test_helpers.py -v

# API tests (endpoints)
python -m pytest tests/test_api.py -v

# Kindle compatibility tests
python -m pytest tests/test_kindle_compatibility.py -v

# Integration tests (complete workflow)
python test_api.py
```

### Test Coverage
- **Unit Tests**: File validation, image processing, EPUB structure analysis
- **API Tests**: All endpoints with various scenarios
- **Integration Tests**: Complete conversion workflow
- **Kindle Tests**: Metadata validation, EPUB structure, compatibility checks

## 📊 Kindle Compatibility

### Metadata Requirements
The application implements all required Kindle metadata:

#### Required Metadata
- **Title**: Required for Kindle UI display
- **Author**: Required for Kindle UI and library organization
- **Identifier**: Automatically generated (ISBN if provided, otherwise UUID)
- **Language**: Uses ISO 639-1 codes (e.g., "es", "en")
- **TOC/Navigation**: Proper NCX and NAV files for navigation
- **Spine**: Correct reading order with navigation first

#### EPUB Structure Validation
- **Container.xml**: Required EPUB container file
- **Content.opf**: Accepts multiple locations (root, OEBPS/, EPUB/)
- **Navigation Files**: NCX and NAV for proper TOC
- **File Structure**: Validates complete EPUB structure
- **Size Limits**: Ensures Kindle-compatible file sizes

### Content Processing
- **HTML Sanitization**: Clean, Kindle-compatible HTML
- **Accented Characters**: Preserves Spanish characters (á, é, í, ó, ú, ñ, ü)
- **Safe Filenames**: Maintains compatibility while preserving characters
- **Cover Processing**: Automatic RGB conversion and size optimization

### Validation and Quality Assurance
- **EPUB Structure**: Comprehensive structure validation
- **Metadata Verification**: Ensures all required fields are present
- **File Integrity**: Validates ZIP structure and file relationships
- **Kindle Compatibility**: Specific checks for Kindle requirements

## 🔍 Troubleshooting

### Common Issues

#### File Upload Issues
- **File too large**: Maximum file size is 10MB
- **Invalid format**: Only .md and .txt files are supported
- **Encoding issues**: Ensure files are UTF-8 encoded

#### Conversion Issues
- **Missing metadata**: Ensure title, author, and language are provided
- **Invalid language code**: Use ISO 639-1 codes (e.g., "es", "en")
- **Cover image problems**: Use JPEG or PNG format, under 5MB

#### Kindle Compatibility Issues
- **EPUB validation warnings**: Check the detailed structure information
- **Cover not displaying**: Ensure cover image is properly formatted
- **Navigation problems**: Verify TOC structure in your markdown

### Validation Messages

#### ✅ Success Messages
- "EPUB structure is valid"
- "All required files present"
- "Kindle compatible"

#### ⚠️ Warning Messages
- "No cover image found (recommended for Kindle)"
- "Filename contains special characters"
- "Large file size detected"

#### ❌ Error Messages
- "Missing required file: content.opf"
- "Invalid EPUB structure"
- "Metadata validation failed"

## 📝 File Format Requirements

### Markdown Structure
```markdown
# Book Title

## Chapter 1
Content of chapter 1...

### Section 1.1
Subsection content...

## Chapter 2
Content of chapter 2...
```

### Supported Markdown Features
- **Headers**: # ## ### #### ##### ######
- **Emphasis**: *italic*, **bold**, ***bold italic***
- **Lists**: Ordered and unordered lists
- **Links**: [text](url)
- **Images**: ![alt](image_url)
- **Code**: `inline code` and code blocks
- **Blockquotes**: > quoted text
- **Tables**: Markdown table syntax

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch from `development`
3. Make your changes
4. Add tests for new functionality
5. Run the test suite: `python run_tests.py`
6. Submit a pull request to `development`

### Code Standards
- Follow PEP 8 for Python code
- Add comprehensive tests for new features
- Update documentation for API changes
- Ensure Kindle compatibility is maintained

### Testing Requirements
- All new features must have corresponding tests
- Maintain >90% test coverage
- Run full test suite before submitting PR
- Ensure all tests pass in CI/CD pipeline

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: This application is specifically designed for Kindle compatibility and includes comprehensive validation to ensure your EPUB files work perfectly with Amazon's Kindle devices and services.

**Nota**: Esta aplicación está específicamente diseñada para compatibilidad con Kindle e incluye validación integral para asegurar que tus archivos EPUB funcionen perfectamente con los dispositivos y servicios Kindle de Amazon.
