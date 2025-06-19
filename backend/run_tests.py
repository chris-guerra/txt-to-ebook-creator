#!/usr/bin/env python3
"""
Comprehensive test runner for the Markdown to EPUB Creator backend.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print('='*60)
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("✅ SUCCESS")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print(f"Error code: {e.returncode}")
        if e.stdout:
            print("Output:")
            print(e.stdout)
        if e.stderr:
            print("Error:")
            print(e.stderr)
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("Checking dependencies...")
    
    required_packages = [
        'pytest',
        'fastapi',
        'uvicorn',
        'ebooklib',
        'markdown',
        'PIL',
        'magic'
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
    
    print("✅ All dependencies are installed")
    return True

def run_unit_tests():
    """Run unit tests."""
    return run_command(
        [sys.executable, '-m', 'pytest', 'tests/test_helpers.py', '-v'],
        "Unit Tests (Helper Functions)"
    )

def run_api_tests():
    """Run API tests."""
    return run_command(
        [sys.executable, '-m', 'pytest', 'tests/test_api.py', '-v'],
        "API Tests (Endpoints)"
    )

def run_integration_tests():
    """Run integration tests."""
    return run_command(
        [sys.executable, '-m', 'pytest', 'test_api.py', '-v'],
        "Integration Tests (Complete Workflow)"
    )

def run_all_tests():
    """Run all tests with coverage."""
    return run_command(
        [sys.executable, '-m', 'pytest', 'tests/', 'test_api.py', '-v', '--tb=short'],
        "All Tests"
    )

def run_linting():
    """Run code linting."""
    try:
        import flake8
        return run_command(
            [sys.executable, '-m', 'flake8', 'app/', 'tests/'],
            "Code Linting"
        )
    except ImportError:
        print("⚠️  flake8 not installed, skipping linting")
        return True

def cleanup_test_files():
    """Clean up any test files that might have been created."""
    test_files = [
        'test_book.md',
        'test_output.epub',
        'uploads/',
        'covers/'
    ]
    
    print("\nCleaning up test files...")
    for file_path in test_files:
        path = Path(file_path)
        if path.exists():
            if path.is_file():
                path.unlink()
                print(f"Removed file: {file_path}")
            elif path.is_dir():
                import shutil
                shutil.rmtree(path)
                print(f"Removed directory: {file_path}")

def main():
    """Main test runner."""
    print("🧪 Markdown to EPUB Creator - Test Suite")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Run tests
    results = []
    
    # Unit tests
    results.append(("Unit Tests", run_unit_tests()))
    
    # API tests
    results.append(("API Tests", run_api_tests()))
    
    # Integration tests
    results.append(("Integration Tests", run_integration_tests()))
    
    # Linting
    results.append(("Linting", run_linting()))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        cleanup_test_files()
        sys.exit(0)
    else:
        print("💥 Some tests failed!")
        cleanup_test_files()
        sys.exit(1)

if __name__ == "__main__":
    main() 