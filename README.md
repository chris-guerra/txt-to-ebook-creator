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

### Current Focus / Enfoque Actual

**Phase 3: API Endpoints and Integration** - The backend structure is complete, now we need to create the API endpoints and connect everything:

1. **API Endpoints (Priority 1):**
   - Create file upload endpoint
   - Create conversion endpoint
   - Create status checking endpoint
   - Create download endpoint
   - Add proper request/response handling

2. **Frontend Integration (Priority 2):**
   - Update frontend to call backend API
   - Replace simulation with real conversion
   - Implement actual file upload to backend
   - Add error handling for API calls
   - Test end-to-end functionality

3. **Advanced Features (Priority 3):**
   - Add EPUB validation
   - Implement file optimization
   - Add conversion options (format, quality)
   - Add batch processing capabilities

### Backend Implementation Details / Detalles de Implementación del Backend

✅ **COMPLETED** - The FastAPI backend structure is fully implemented:

#### Backend Architecture / Arquitectura del Backend
```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models/
│   │   └── book.py          # Pydantic data models
│   ├── converters/
│   │   └── markdown_to_epub.py  # Conversion logic
│   └── utils/
│       └── helpers.py       # Utility functions
```

#### Implemented Features / Características Implementadas
- ✅ FastAPI application with CORS configuration
- ✅ Pydantic models for data validation
- ✅ File upload and validation utilities
- ✅ Image processing and validation
- ✅ Markdown to EPUB conversion logic
- ✅ Error handling and health checks
- ✅ File management and cleanup

#### Technical Components / Componentes Técnicos
- ✅ **FastAPI**: Modern, fast web framework
- ✅ **Pydantic**: Data validation and serialization
- ✅ **ebooklib**: EPUB file generation
- ✅ **python-magic**: File type detection
- ✅ **Pillow**: Image processing
- ✅ **markdown**: Markdown to HTML conversion

### Recommended Next Steps / Próximos Pasos Recomendados

1. **Create API Endpoints:**
   ```bash
   cd backend
   # Create routers for different endpoints
   # Implement file upload API
   # Implement conversion API
   ```

2. **Then Frontend Integration:**
   - Update frontend to call backend API
   - Replace simulation with real conversion
   - Test complete workflow

3. **Finally Testing:**
   - End-to-end testing
   - Error handling validation
   - Performance optimization

Would you like to proceed with creating the API endpoints?

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
