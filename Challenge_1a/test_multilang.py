#!/usr/bin/env python3
"""
Test script to verify multilingual support and processing functionality.
"""

try:
    import os
    import json
    from pathlib import Path
    from pdf_processor import PDFProcessor
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure Python environment is properly configured.")
    exit(1)

def test_multilang_patterns():
    """Test multilingual pattern recognition."""
    processor = PDFProcessor()
    
    # Test cases for different languages
    test_cases = [
        # English
        {"text": "Chapter 1: Introduction", "expected": True, "lang": "English"},
        {"text": "1.1 Overview", "expected": True, "lang": "English"},
        {"text": "Section 2.3 Analysis", "expected": True, "lang": "English"},
        
        # Spanish
        {"text": "Capítulo 1: Introducción", "expected": True, "lang": "Spanish"},
        {"text": "1.1 Resumen", "expected": True, "lang": "Spanish"},
        {"text": "Sección 2.3 Análisis", "expected": True, "lang": "Spanish"},
        
        # French
        {"text": "Chapitre 1: Introduction", "expected": True, "lang": "French"},
        {"text": "1.1 Résumé", "expected": True, "lang": "French"},
        {"text": "Section 2.3 Analyse", "expected": True, "lang": "French"},
        
        # German
        {"text": "Kapitel 1: Einführung", "expected": True, "lang": "German"},
        {"text": "1.1 Zusammenfassung", "expected": True, "lang": "German"},
        {"text": "Abschnitt 2.3 Analyse", "expected": True, "lang": "German"},
    ]
    
    print("Testing multilingual pattern recognition:")
    print("-" * 50)
    
    for case in test_cases:
        result = processor.text_analyzer.looks_like_heading(case["text"])
        status = "✓" if result == case["expected"] else "✗"
        print(f"{status} {case['lang']}: '{case['text']}' -> {result}")
    
    print("\nTesting title detection:")
    print("-" * 30)
    
    title_cases = [
        "Understanding Artificial Intelligence Systems",
        "Comprensión de los Sistemas de IA",
        "Comprendre les Systèmes d'IA",
        "KI-Systeme verstehen"
    ]
    
    for title in title_cases:
        result = processor.text_analyzer.looks_like_title(title)
        status = "✓" if result else "✗"
        print(f"{status} '{title}' -> {result}")

def verify_directories():
    """Verify input/output directories exist and are accessible."""
    input_dir = Path("input")
    output_dir = Path("output")
    
    print("\nDirectory verification:")
    print("-" * 25)
    
    # Check if directories exist
    print(f"Input directory exists: {input_dir.exists()}")
    print(f"Output directory exists: {output_dir.exists()}")
    
    # Check if directories are writable
    try:
        test_file = output_dir / "test.txt"
        test_file.write_text("test")
        test_file.unlink()
        print("Output directory is writable: ✓")
    except Exception as e:
        print(f"Output directory write test failed: ✗ ({e})")
    
    # List any existing PDF files
    pdf_files = list(input_dir.glob("*.pdf")) if input_dir.exists() else []
    print(f"PDF files in input: {len(pdf_files)}")
    for pdf in pdf_files:
        print(f"  - {pdf.name}")

if __name__ == "__main__":
    print("PDF Document Outline Extractor - Test Suite")
    print("=" * 50)
    
    test_multilang_patterns()
    verify_directories()
    
    print("\n" + "=" * 50)
    print("Test completed. Ready for PDF processing!")