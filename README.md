# Markdown to EPUB Creator / Creador de Markdown a EPUB

A web application that converts Markdown/TXT files to EPUB format using FastAPI and Streamlit.

Una aplicación web que convierte archivos Markdown/TXT a formato EPUB utilizando FastAPI y Streamlit.

## Project Structure / Estructura del Proyecto

```
txt-to-ebook-creator/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── converters/          # Conversion logic
│   │   │   ├── __init__.py
│   │   │   └── markdown_to_epub.py
│   │   ├── models/             # Data models
│   │   │   ├── __init__.py
│   │   │   └── book.py
│   │   └── utils/              # Utility functions
│   │       ├── __init__.py
│   │       └── helpers.py
│   ├── tests/                  # Backend tests
│   │   └── __init__.py
│   └── requirements.txt        # Backend dependencies
├── frontend/
│   ├── app.py                 # Streamlit application
│   ├── pages/                 # Streamlit pages
│   │   └── __init__.py
│   ├── components/            # Reusable Streamlit components
│   │   └── __init__.py
│   └── requirements.txt       # Frontend dependencies
├── .gitignore
├── README.md
└── docker-compose.yml        # Docker configuration
```

## Features / Características

- Upload Markdown/TXT files
- Preview content before conversion
- Convert to EPUB format
- Download generated EPUB files
- Support for basic Markdown formatting
- Metadata handling (title, author, etc.)

## Content Structure / Estructura del Contenido

The application supports two types of content:
- Poetry / Poesía
- Prose / Prosa

### Markdown Formatting / Formato Markdown

The application uses the following heading hierarchy for book structure:
- `# Title` - Book Title / Título del Libro
- `## Chapter` - Chapter Title / Título del Capítulo
- `### Section` - Section Title / Título de Sección

Example / Ejemplo:
```markdown
# My Book Title
## Chapter 1
### Section 1.1
Content here...

## Chapter 2
### Section 2.1
More content...
```

## Book Metadata / Metadatos del Libro

The application allows you to add the following metadata to your ebook:
- Title / Título
- Author / Autor
- Publisher / Editor
- Publication Date / Fecha de Publicación
- ISBN
- Language / Idioma
- Description / Descripción
- Keywords / Palabras Clave
- Cover Image / Imagen de Portada
  - Supports common image formats (JPG, PNG)
  - Recommended size: 1600x2400 pixels
  - Minimum size: 800x1200 pixels

## UX Design / Diseño de UX

### Main Page Layout
- Title at the top: "Markdown to EPUB Creator"
- Sidebar for navigation and settings
- Two-column layout (equal width):
  - Left column: Book metadata form
  - Right column: File upload, cover image, and convert button

### Content Type Selection
- Radio buttons for Poetry/Prose selection
- Clear visual distinction between options
- Brief description of each type

### File Upload Section
- Drag and drop or click to upload interface
- Support for .md and .txt files
- Clear file size limits (10MB max)
- Success/error messages for upload status
- File size information display
- Required field (marked with *)
- Located in right column

### Metadata Form
- Clean, organized form layout
- Required fields clearly marked with *:
  - Title
  - Author
- Optional fields:
  - Publisher
  - Publication Date
  - ISBN
  - Language
  - Description
  - Keywords
- Input validation
- Multi-line text area for description
- Tag input for keywords
- Date picker for publication date
- Language dropdown
- Located in left column

### Cover Image Upload
- Upload button with validation
- Size and format requirements displayed
- Success/error messages for upload status
- File information display (format, dimensions, size)
- Validation for image dimensions
- Optional field
- Located in right column

### Action Buttons
- Convert to EPUB button
- Clear visual hierarchy
- Disabled states for unavailable actions
- Located in right column below cover image
- Smart warning system (only shows errors when user attempts conversion)

### Status and Feedback
- Progress bar for conversion
- Status messages
- Error notifications
- Success confirmations
- Required field indicators (*)
- File validation feedback
- Simple upload confirmation messages
- Contextual error messages (only when needed)

### UX Considerations
1. Progressive Disclosure
   - Show metadata form after file upload
   - Enable convert button only when all required fields are filled
   - Show download button only after successful conversion
   - Clear indication of required fields

2. Visual Hierarchy
   - Clear section headings
   - Consistent spacing
   - Visual separation between sections
   - Equal-width two-column layout
   - Left for information, right for actions

3. Feedback
   - Loading indicators
   - Success/error messages
   - Simple upload confirmations
   - Required field indicators
   - File validation feedback
   - Contextual warnings (only when user attempts action)

4. Accessibility
   - High contrast text
   - Clear button labels
   - Keyboard navigation support
   - Required field indicators

5. Responsive Design
   - Adapts to different screen sizes
   - Collapsible sections for mobile
   - Maintains two-column layout on desktop

## Frontend Implementation Status / Estado de Implementación del Frontend

✅ **COMPLETED** - The Streamlit frontend is fully implemented with all planned features:

### Completed Features / Características Completadas
- ✅ Complete user interface with two-column layout
- ✅ File upload with validation (Markdown/TXT, 10MB limit)
- ✅ Metadata form with comprehensive validation
- ✅ Cover image upload with dimension and format validation
- ✅ Conversion process with progress tracking
- ✅ Download functionality with automatic file naming
- ✅ Smart error handling and user feedback
- ✅ Session state management
- ✅ Responsive design and accessibility features

### Technical Implementation / Implementación Técnica
- ✅ Streamlit application with custom CSS styling
- ✅ File validation using python-magic
- ✅ Image processing with Pillow
- ✅ Form validation with real-time feedback
- ✅ Progress simulation with step-by-step updates
- ✅ Base64 download link generation
- ✅ Session state for form and conversion tracking

## Next Steps / Próximos Pasos

Implementation progress and next steps:

1. ✅ Basic Layout and Navigation
   - ✅ Set up main page structure
   - ✅ Implement sidebar navigation
   - ✅ Create basic styling
   - ✅ Implement two-column layout
   - ✅ Add required field indicators
   - ✅ Reorganize layout for better UX
   - ✅ Equal-width column distribution

2. ✅ File Upload and Preview
   - ✅ Implement file upload functionality
   - ✅ Add basic file validation
   - ✅ Add file size validation
   - ✅ Add file type validation
   - ✅ Implement error handling for invalid files
   - ✅ Simplified upload feedback (no previews)

3. ✅ Metadata Form
   - ✅ Create form layout
   - ✅ Add required field indicators
   - ✅ Implement input validation
   - ✅ Add real-time feedback
   - ✅ Add field-specific validation rules
   - ✅ Implement form state management
   - ✅ Add validation for:
     - Title (required, 2-200 characters)
     - Author (required, 2-100 characters)
     - ISBN (optional, 10 or 13 digits)
     - Description (optional, max 1000 characters)

4. ✅ Cover Image Upload
   - ✅ Implement image upload
   - ✅ Add image validation
   - ✅ Add image size validation
   - ✅ Add image format validation
   - ✅ Add dimension validation
   - ✅ Add aspect ratio checking
   - ✅ Display file information
   - ✅ Simplified upload feedback (no previews)

5. ✅ Conversion and Download
   - ✅ Implement conversion process (simulated)
   - ✅ Add progress indicators
   - ✅ Create download functionality
   - ✅ Add error handling
   - ✅ Implement success notifications
   - ✅ Add conversion status tracking
   - ✅ Implement file download links
   - ✅ Smart warning system (contextual error messages)

6. ✅ Backend Setup
   - ✅ Set up FastAPI application structure
   - ✅ Create data models with Pydantic
   - ✅ Implement utility functions
   - ✅ Create Markdown to EPUB converter
   - ✅ Add file validation and handling
   - ✅ Configure CORS for frontend integration
   - ✅ Add error handling and health checks

7. ✅ API Endpoints
   - ✅ Create file upload endpoint
   - ✅ Create conversion endpoint
   - ✅ Create status checking endpoint
   - ✅ Create download endpoint
   - ✅ Add proper request/response handling
   - ✅ Implement chapter structure parsing
   - ✅ Add background task processing

### Current Focus / Enfoque Actual

**Phase 4: Frontend Integration** - The backend API is complete, now we need to connect the frontend:

1. **Frontend Integration (Priority 1):**
   - Update frontend to call backend API
   - Replace simulation with real conversion
   - Implement actual file upload to backend
   - Add error handling for API calls
   - Test end-to-end functionality

2. **Testing and Optimization (Priority 2):**
   - End-to-end testing
   - Error handling validation
   - Performance optimization
   - File cleanup verification

3. **Advanced Features (Priority 3):**
   - Add EPUB validation
   - Implement file optimization
   - Add conversion options (format, quality)
   - Add batch processing capabilities

### Backend Implementation Details / Detalles de Implementación del Backend

✅ **COMPLETED** - The FastAPI backend is fully implemented with complete API:

#### Backend Architecture / Arquitectura del Backend
```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models/
│   │   └── book.py          # Pydantic data models
│   ├── converters/
│   │   └── markdown_to_epub.py  # Conversion logic with chapter parsing
│   ├── routers/
│   │   └── conversion.py    # API endpoints
│   └── utils/
│       └── helpers.py       # Utility functions
```

#### API Endpoints / Endpoints de la API

**Base URL**: `http://localhost:8000`

##### Health Check
- `GET /` - Root health check
- `GET /health` - Service health status

##### File Upload
- `POST /api/v1/conversion/upload`
  - **Purpose**: Upload Markdown/TXT file and optional cover image
  - **Parameters**:
    - `file` (required): Markdown or TXT file
    - `cover_image` (optional): Cover image (JPG/PNG)
  - **Response**: File information and validation status
  - **Example**:
    ```bash
    curl -X POST "http://localhost:8000/api/v1/conversion/upload" \
         -F "file=@book.md" \
         -F "cover_image=@cover.jpg"
    ```

##### Conversion
- `POST /api/v1/conversion/convert`
  - **Purpose**: Convert uploaded file to EPUB format
  - **Parameters**:
    - `file_id` (required): Unique identifier from upload
    - `metadata_json` (required): JSON string with book metadata
    - `content_type` (optional): "prose" or "poetry" (default: "prose")
  - **Response**: Conversion status and download URL
  - **Example**:
    ```bash
    curl -X POST "http://localhost:8000/api/v1/conversion/convert" \
         -F "file_id=123e4567-e89b-12d3-a456-426614174000" \
         -F "metadata_json={\"title\":\"My Book\",\"author\":\"John Doe\"}" \
         -F "content_type=prose"
    ```

##### Status Check
- `GET /api/v1/conversion/status/{file_id}`
  - **Purpose**: Check conversion status
  - **Parameters**: `file_id` in URL path
  - **Response**: Current conversion status and progress
  - **Example**:
    ```bash
    curl "http://localhost:8000/api/v1/conversion/status/123e4567-e89b-12d3-a456-426614174000"
    ```

##### Download
- `GET /api/v1/conversion/download/{file_id}`
  - **Purpose**: Download converted EPUB file
  - **Parameters**: `file_id` in URL path
  - **Response**: EPUB file for download
  - **Example**:
    ```bash
    curl -O "http://localhost:8000/api/v1/conversion/download/123e4567-e89b-12d3-a456-426614174000"
    ```

##### File Management
- `DELETE /api/v1/conversion/files/{file_id}`
  - **Purpose**: Delete uploaded and converted files
  - **Parameters**: `file_id` in URL path
  - **Response**: Deletion status
  - **Example**:
    ```bash
    curl -X DELETE "http://localhost:8000/api/v1/conversion/files/123e4567-e89b-12d3-a456-426614174000"
    ```

#### Chapter Structure Handling / Manejo de Estructura de Capítulos

✅ **IMPLEMENTED** - The conversion system now properly handles the Markdown chapter structure:

**How it works**:
1. **Parsing**: The system parses Markdown content looking for `## Chapter` headings
2. **Chapter Creation**: Each `## Chapter` becomes a separate EPUB chapter
3. **Content Organization**: Content between chapters is properly organized
4. **Table of Contents**: Automatic TOC generation with chapter titles
5. **Fallback**: If no chapters found, entire content becomes one chapter

**Example Markdown Structure**:
```markdown
# My Book Title
## Chapter 1
### Section 1.1
Content here...

## Chapter 2
### Section 2.1
More content...
```

**Result**: Creates EPUB with separate chapters for "Chapter 1" and "Chapter 2", each with their own content and proper navigation.

#### Implemented Features / Características Implementadas
- ✅ FastAPI application with CORS configuration
- ✅ Pydantic models for data validation
- ✅ File upload and validation utilities
- ✅ Image processing and validation
- ✅ Markdown to EPUB conversion with chapter parsing
- ✅ Error handling and health checks
- ✅ File management and cleanup
- ✅ Background task processing
- ✅ Complete API with all endpoints
- ✅ Chapter structure parsing and EPUB generation

#### Technical Components / Componentes Técnicos
- ✅ **FastAPI**: Modern, fast web framework with automatic API documentation
- ✅ **Pydantic**: Data validation and serialization
- ✅ **ebooklib**: EPUB file generation and manipulation
- ✅ **python-magic**: Reliable file type detection
- ✅ **Pillow**: Image processing and validation
- ✅ **markdown**: Markdown to HTML conversion with extensions
- ✅ **Regex**: Chapter structure parsing
- ✅ **Background Tasks**: Asynchronous file processing

### Recommended Next Steps / Próximos Pasos Recomendados

1. **Update Frontend Integration:**
   ```bash
   cd frontend
   # Update app.py to call backend API
   # Replace simulation with real API calls
   # Test complete workflow
   ```

2. **Then Testing:**
   - End-to-end testing with real files
   - Error handling validation
   - Performance testing
   - File cleanup verification

3. **Finally Deployment:**
   - Docker containerization
   - Production deployment
   - Monitoring and logging

Would you like to proceed with updating the frontend to integrate with the backend API?

## Setup / Configuración

### Prerequisites / Prerrequisitos

- Python 3.8+
- pip
- Docker (optional)

### Installation / Instalación

1. Clone the repository:
```bash
git clone https://github.com/yourusername/txt-to-ebook-creator.git
cd txt-to-ebook-creator
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd ../frontend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Application / Ejecutar la Aplicación

1. Start the backend:
```bash
cd backend
uvicorn app.main:app --reload
```

2. Start the frontend:
```bash
cd frontend
streamlit run app.py
```

## Development / Desarrollo

### Backend Development

The backend is built with FastAPI and handles:
- File upload and processing
- Markdown to EPUB conversion
- API endpoints for the frontend
- Metadata processing and validation
- Cover image processing and optimization

### Frontend Development

The frontend is built with Streamlit and provides:
- User interface for file upload
- Content preview with syntax highlighting
- Conversion controls
- Download functionality
- Metadata form with validation
- Cover image upload and preview
- Content type selection (Poetry/Prose)

## Contributing / Contribuir

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License / Licencia

This project is licensed under the MIT License - see the LICENSE file for details.

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
