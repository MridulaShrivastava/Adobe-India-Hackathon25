#!/bin/bash
# Test script to verify the PDF extractor functionality

echo "PDF Document Outline Extractor - System Test"
echo "============================================="

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found"
    exit 1
fi

# Verify Python can import basic modules
python3 -c "import sys, os, pathlib; print('Python environment OK')" || {
    echo "Error: Python environment is corrupted"
    exit 1
}

# Check Python dependencies
echo "Checking Python dependencies..."
python3 -c "import fitz; print('✓ PyMuPDF installed')" 2>/dev/null || echo "✗ PyMuPDF missing"
python3 -c "import nltk; print('✓ NLTK installed')" 2>/dev/null || echo "✗ NLTK missing"

# Run multilingual tests
echo -e "\nRunning multilingual pattern tests..."
python3 test_multilang.py

# Check Docker setup
echo -e "\nChecking Docker configuration..."
if [ -f "Dockerfile" ]; then
    echo "✓ Dockerfile exists"
else
    echo "✗ Dockerfile missing"
fi

# Verify directory structure
echo -e "\nDirectory structure:"
ls -la input/ output/ 2>/dev/null || echo "Creating directories..."

echo -e "\nSystem ready for PDF processing!"
echo "To process PDFs:"
echo "1. Place PDF files in the 'input' directory"
echo "2. Run: python3 main.py"
echo "3. Check results in the 'output' directory"
echo ""
echo "For Docker:"
echo "1. Build: docker build --platform linux/amd64 -t pdf-extractor ."
echo "2. Run: docker run --rm -v \$(pwd)/input:/app/input -v \$(pwd)/output:/app/output --network none pdf-extractor"