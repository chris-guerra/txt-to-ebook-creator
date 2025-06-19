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
- Preview of uploaded file name
- Required field (marked with *)
- Syntax highlighting for Markdown files
- Error handling for invalid files
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
- Upload button with preview
- Size and format requirements displayed
- Image preview after upload
- Validation for image dimensions
- Optional field
- Located in right column

### Content Preview
- Syntax highlighted preview
- Scrollable preview area
- Real-time updates
- Clear section separation
- Shows after file upload
- Different display for .md and .txt files
- Located in right column

### Action Buttons
- Convert to EPUB button
- Clear visual hierarchy
- Disabled states for unavailable actions
- Located in right column below cover image

### Status and Feedback
- Progress bar for conversion
- Status messages
- Error notifications
- Success confirmations
- Required field indicators (*)
- File validation feedback

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
   - Preview updates in real-time
   - Required field indicators
   - File validation feedback

4. Accessibility
   - High contrast text
   - Clear button labels
   - Keyboard navigation support
   - Required field indicators

5. Responsive Design
   - Adapts to different screen sizes
   - Collapsible sections for mobile
   - Scrollable preview area
   - Maintains two-column layout on desktop

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
   - ✅ Create preview component with syntax highlighting
   - ✅ Add file size validation
   - ✅ Add file type validation
   - ✅ Implement error handling for invalid files
   - ✅ Add syntax highlighting for Markdown files

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
   - ✅ Add basic preview
   - ✅ Add image validation
   - ✅ Add image size validation
   - ✅ Add image format validation
   - ✅ Add dimension validation
   - ✅ Add aspect ratio checking
   - ✅ Display detailed image information
   - ✅ Provide recommendations for optimal dimensions

5. Conversion and Download
   - ⏳ Implement conversion process
   - ⏳ Add progress indicators
   - ⏳ Create download functionality
   - ⏳ Add error handling
   - ⏳ Implement success notifications

### Current Focus / Enfoque Actual

The next immediate steps should be:

1. Implement Conversion Process:
   - Connect to backend API
   - Add progress indicators
   - Handle conversion errors
   - Implement download functionality

2. Backend Development:
   - Set up FastAPI application
   - Implement Markdown to EPUB conversion
   - Create API endpoints
   - Handle file processing

### System Dependencies / Dependencias del Sistema

The application requires some system-level dependencies:

1. libmagic (for file type detection)
   - On macOS: `brew install libmagic`
   - Required for proper file type validation
   - Used by python-magic package
   - Ensures accurate MIME type detection

### Validation Rules / Reglas de Validación

The application implements the following validation rules:

1. **Title Validation:**
   - Required field
   - Minimum 2 characters
   - Maximum 200 characters
   - Cannot be empty or whitespace only

2. **Author Validation:**
   - Required field
   - Minimum 2 characters
   - Maximum 100 characters
   - Cannot be empty or whitespace only

3. **ISBN Validation:**
   - Optional field
   - Must be 10 or 13 digits
   - Supports ISBN-10 with 'X' as last character
   - Removes hyphens and spaces automatically

4. **Description Validation:**
   - Optional field
   - Maximum 1000 characters
   - Allows empty values

5. **Cover Image Validation:**
   - Optional field
   - Maximum file size: 5MB
   - Supported formats: JPEG, PNG
   - Minimum dimensions: 800x1200 pixels
   - Maximum dimensions: 3000x4000 pixels
   - Recommended dimensions: 1600x2400 pixels
   - Aspect ratio warning for non-2:3 ratios
   - Detailed image information display

Would you like to proceed with either of these areas?

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
