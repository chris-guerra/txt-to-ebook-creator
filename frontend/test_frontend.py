#!/usr/bin/env python3
"""
Simple test script for the Streamlit frontend.
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def check_dependencies():
    """Check if frontend dependencies are installed."""
    print("Checking frontend dependencies...")
    
    required_packages = [
        'streamlit',
        'requests',
        'pillow',
        'python-magic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All frontend dependencies are installed")
    return True

def test_app_import():
    """Test that the app can be imported without errors."""
    print("Testing app import...")
    
    try:
        # Change to frontend directory
        frontend_dir = Path(__file__).parent
        sys.path.insert(0, str(frontend_dir))
        
        import app
        print("✅ App imported successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def test_backend_connection():
    """Test connection to backend API."""
    print("Testing backend connection...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and accessible")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Is it running on http://localhost:8000?")
        return False
    except Exception as e:
        print(f"❌ Backend connection test failed: {e}")
        return False

def test_file_validation():
    """Test file validation functions."""
    print("Testing file validation...")
    
    try:
        from app import validate_file, validate_cover_image
        
        # Test file validation
        from unittest.mock import Mock
        mock_file = Mock()
        mock_file.getbuffer.return_value.nbytes = 1024
        mock_file.getvalue.return_value = b"# Test Markdown\n\nThis is a test."
        
        is_valid, error = validate_file(mock_file)
        if is_valid:
            print("✅ File validation working")
        else:
            print(f"❌ File validation failed: {error}")
            return False
        
        # Test image validation (no image)
        is_valid, error, info = validate_cover_image(None)
        if is_valid:
            print("✅ Image validation working")
        else:
            print(f"❌ Image validation failed: {error}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        return False

def main():
    """Run frontend tests."""
    print("🧪 Frontend Test Suite")
    print("=" * 30)
    
    results = []
    
    # Check dependencies
    results.append(("Dependencies", check_dependencies()))
    
    # Test app import
    results.append(("App Import", test_app_import()))
    
    # Test file validation
    results.append(("File Validation", test_file_validation()))
    
    # Test backend connection (optional)
    backend_test = test_backend_connection()
    results.append(("Backend Connection", backend_test))
    
    # Summary
    print(f"\n{'='*40}")
    print("FRONTEND TEST SUMMARY")
    print('='*40)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All frontend tests passed!")
        print("\nTo start the frontend:")
        print("cd frontend && python run.py")
        sys.exit(0)
    else:
        print("💥 Some frontend tests failed!")
        if not backend_test:
            print("\nNote: Backend connection failed. Make sure to start the backend first:")
            print("cd backend && python run.py")
        sys.exit(1)

if __name__ == "__main__":
    main() 