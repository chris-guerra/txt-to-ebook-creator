# Markdown to EPUB Creator / Creador de EPUB desde Markdown

A comprehensive tool for converting Markdown files to EPUB format with **full Kindle compatibility**. Features a FastAPI backend for robust file processing and a Streamlit frontend for an intuitive user experience.

Una herramienta completa para convertir archivos Markdown a formato EPUB con **compatibilidad completa con Kindle**. Incluye un backend FastAPI para procesamiento robusto de archivos y un frontend Streamlit para una experiencia de usuario intuitiva.

## 🌟 Key Features / Características Principales

### ✅ **Kindle Compatibility / Compatibilidad con Kindle**
- **Full Kindle Metadata Support**: All required Kindle metadata fields
- **EPUB 2.0 Format**: Optimized for Kindle compatibility
- **Cover Image Processing**: Automatic RGB conversion and size optimization
- **Safe Filenames**: Preserves accented characters while ensuring compatibility
- **Navigation Structure**: Proper TOC and spine configuration
- **Validation**: Comprehensive EPUB structure validation

### 📚 **Content Processing / Procesamiento de Contenido**
- **Markdown Support**: Full Markdown syntax with extensions
- **Chapter Detection**: Automatic chapter and section parsing
- **Content Types**: Support for prose and poetry formats
- **Accented Characters**: Full support for Spanish and other languages
- **HTML Sanitization**: Clean, Kindle-compatible HTML output

### 🎨 **User Interface / Interfaz de Usuario**
- **File Upload**: Drag-and-drop or file browser
- **Metadata Form**: Complete book information input
- **Cover Image**: Optional cover image upload and processing
- **Real-time Preview**: Live conversion status and progress
- **Download**: Direct EPUB file download
- **Validation Feedback**: Detailed EPUB structure information

## 📋 Requirements / Requisitos

### Backend Requirements
- Python 3.8+
- FastAPI
- Uvicorn
- EbookLib
- Markdown
- Pillow (PIL)
- Python-magic

### Frontend Requirements
- Python 3.8+
- Streamlit
- Requests

## 🚀 Installation / Instalación

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

## 🏃‍♂️ Running the Application / Ejecutar la Aplicación

### 1. Start the Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start the Frontend
```bash
cd frontend
source venv/bin/activate
streamlit run app.py
```

### 3. Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 Usage / Uso

### 1. Upload Your Markdown File
- Drag and drop your `.md` or `.txt` file
- Or use the file browser to select your file
- Supported formats: Markdown (.md), Text (.txt)

### 2. Add Book Metadata
Fill in the required and optional book information:

#### Required Fields / Campos Requeridos
- **Title / Título** - Required for Kindle UI
- **Author / Autor** - Required for Kindle UI  
- **Language / Idioma** - Required, uses ISO 639-1 codes (e.g., "es", "en")

#### Optional Fields / Campos Opcionales
- **Publisher / Editor**
- **Publication Date / Fecha de Publicación** - ISO format (YYYY-MM-DD)
- **ISBN** - Optional, UUID will be generated automatically if not provided
- **Description / Descripción**
- **Keywords / Palabras Clave**

### 3. Upload Cover Image (Optional)
- Supported formats: JPEG, PNG
- Automatic processing for Kindle compatibility
- Size optimization and RGB conversion

### 4. Convert and Download
- Click "Convert to EPUB" to start the conversion
- Monitor the conversion progress
- Download your EPUB file when ready

## 🔧 API Endpoints / Endpoints de la API

### File Upload / Subida de Archivos
- `POST /api/v1/conversion/upload` - Upload markdown file

### Conversion / Conversión
- `POST /api/v1/conversion/convert` - Convert to EPUB
- `GET /api/v1/conversion/status/{file_id}` - Check conversion status

### Download / Descarga
- `GET /api/v1/conversion/download/{file_id}` - Download EPUB file

### File Management / Gestión de Archivos
- `DELETE /api/v1/conversion/files/{file_id}` - Delete uploaded files

## 🧪 Testing / Pruebas

### Run All Tests
```bash
cd backend
python run_tests.py
```

### Individual Test Categories
```bash
# Unit tests
python -m pytest tests/test_helpers.py -v

# API tests
python -m pytest tests/test_api.py -v

# Kindle compatibility tests
python -m pytest tests/test_kindle_compatibility.py -v

# Integration tests
python test_api.py
```

## 📊 Kindle Compatibility Features / Características de Compatibilidad con Kindle

### Metadata Requirements / Requisitos de Metadatos
The application ensures full Kindle compatibility by implementing all required metadata:

#### Required Metadata / Metadatos Requeridos
- **Title**: Required for Kindle UI display
- **Author**: Required for Kindle UI and library organization  
- **Identifier**: Automatically generated (ISBN if provided, otherwise UUID)
- **Language**: Uses ISO 639-1 codes (e.g., "es", "en")
- **TOC/Navigation**: Proper NCX and NAV files for navigation
- **Spine**: Correct reading order with navigation first

#### EPUB Structure Validation / Validación de Estructura EPUB
- **Container.xml**: Required EPUB container file
- **Content.opf**: Accepts multiple locations (root, OEBPS/, EPUB/)
- **Navigation Files**: NCX and NAV for proper TOC
- **File Structure**: Validates complete EPUB structure
- **Size Limits**: Ensures Kindle-compatible file sizes

### Content Processing / Procesamiento de Contenido
- **HTML Sanitization**: Clean, Kindle-compatible HTML
- **Accented Characters**: Preserves Spanish characters (á, é, í, ó, ú, ñ, ü)
- **Safe Filenames**: Maintains compatibility while preserving characters
- **Cover Processing**: Automatic RGB conversion and size optimization

### Validation and Quality Assurance / Validación y Control de Calidad
- **EPUB Structure**: Comprehensive structure validation
- **Metadata Verification**: Ensures all required fields are present
- **File Integrity**: Validates ZIP structure and file relationships
- **Kindle Compatibility**: Specific checks for Kindle requirements

## 🔍 Troubleshooting / Solución de Problemas

### Common Issues / Problemas Comunes

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

### Validation Messages / Mensajes de Validación

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

## 📝 File Format Requirements / Requisitos de Formato de Archivo

### Markdown Structure / Estructura de Markdown
```markdown
# Book Title

## Chapter 1
Content of chapter 1...

### Section 1.1
Subsection content...

## Chapter 2
Content of chapter 2...
```

### Supported Markdown Features / Características de Markdown Soportadas
- **Headers**: # ## ### #### ##### ######
- **Emphasis**: *italic*, **bold**, ***bold italic***
- **Lists**: Ordered and unordered lists
- **Links**: [text](url)
- **Images**: ![alt](image_url)
- **Code**: `inline code` and code blocks
- **Blockquotes**: > quoted text
- **Tables**: Markdown table syntax

## 🤝 Contributing / Contribuir

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License / Licencia

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments / Agradecimientos

- **EbookLib**: For EPUB generation capabilities
- **FastAPI**: For the robust backend framework
- **Streamlit**: For the intuitive frontend interface
- **Markdown**: For content processing
- **Pillow**: For image processing capabilities

---

**Note**: This application is specifically designed for Kindle compatibility and includes comprehensive validation to ensure your EPUB files work perfectly with Amazon's Kindle devices and services.

**Nota**: Esta aplicación está específicamente diseñada para compatibilidad con Kindle e incluye validación integral para asegurar que tus archivos EPUB funcionen perfectamente con los dispositivos y servicios Kindle de Amazon.
