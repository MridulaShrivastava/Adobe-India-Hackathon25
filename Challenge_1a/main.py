#!/usr/bin/env python3
"""
Persona-Driven Document Intelligence System
Analyzes multiple PDFs and extracts relevant sections based on user persona and job.
"""

import os
import json
import sys
import argparse
from pathlib import Path
from document_intelligence import DocumentIntelligenceSystem

def main():
    """Main function for persona-driven document analysis."""
    parser = argparse.ArgumentParser(description='Persona-Driven Document Intelligence')
    parser.add_argument('--persona', default='researcher', 
                       help='User persona (researcher, student, analyst, manager)')
    parser.add_argument('--job', default='literature review',
                       help='Job to be done (literature review, exam prep, trend analysis, etc.)')
    parser.add_argument('--input-dir', default='/app/input',
                       help='Input directory containing PDF files')
    parser.add_argument('--output-dir', default='/app/output',
                       help='Output directory for results')
    
    args = parser.parse_args()
    
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize document intelligence system
    system = DocumentIntelligenceSystem()
    
    # Check for PDF files
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in /app/input directory")
        print("Please place PDF files in the input directory and try again.")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    print(f"Persona: {args.persona}")
    print(f"Job: {args.job}")
    print("-" * 50)
    
    try:
        # Analyze documents
        result = system.analyze_documents(str(input_dir), args.persona, args.job)
        
        # Save result to JSON
        timestamp = result["metadata"]["timestamp"].replace(":", "-").replace(".", "-")
        output_file = output_dir / f"analysis_{args.persona}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\nAnalysis completed!")
        print(f"Processing time: {result['metadata']['processing_time_seconds']} seconds")
        print(f"Sections analyzed: {result['metadata']['total_sections_analyzed']}")
        print(f"Top sections selected: {result['metadata']['top_sections_selected']}")
        print(f"Results saved to: {output_file.name}")
        
        # Print top 3 sections for quick review
        if result["sections"]:
            print("\nTop 3 most relevant sections:")
            for i, section in enumerate(result["sections"][:3], 1):
                print(f"{i}. {section['section_title']} (Score: {section['relevance_score']})")
                print(f"   Document: {section['doc_name']}, Page: {section['page']}")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())