#!/usr/bin/env python3
"""
Streamlit frontend runner for Markdown to EPUB Creator.
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application."""
    # Change to the frontend directory
    frontend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(frontend_dir)
    
    # Run Streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.address", "localhost"
    ])

if __name__ == "__main__":
    main() 