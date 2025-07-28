"""
Document Intelligence System
Main orchestrator for persona-driven document analysis.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from pdf_processor import PDFProcessor
from persona_analyzer import PersonaAnalyzer

class DocumentIntelligenceSystem:
    """Main system for persona-driven document intelligence."""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.persona_analyzer = PersonaAnalyzer()
    
    def analyze_documents(self, input_dir: str, persona: str, job: str) -> Dict[str, Any]:
        """
        Analyze multiple PDFs based on persona and job requirements.
        
        Args:
            input_dir: Directory containing PDF files
            persona: User persona (researcher, student, analyst, etc.)
            job: Job to be done (literature review, exam prep, etc.)
            
        Returns:
            Complete analysis results
        """
        start_time = time.time()
        
        # Get all PDF files
        pdf_files = list(Path(input_dir).glob("*.pdf"))
        
        if not pdf_files:
            return self._create_empty_result(persona, job, "No PDF files found")
        
        # Extract sections from all documents
        all_sections = []
        processed_docs = []
        
        for pdf_file in pdf_files:
            try:
                print(f"Processing: {pdf_file.name}")
                
                # Extract outline from PDF
                outline_result = self.pdf_processor.extract_outline(str(pdf_file))
                
                # Convert outline to sections with full text
                sections = self._extract_sections_with_text(pdf_file, outline_result)
                
                # Add document name to each section
                for section in sections:
                    section["doc_name"] = pdf_file.stem
                
                all_sections.extend(sections)
                processed_docs.append({
                    "name": pdf_file.stem,
                    "title": outline_result.get("title", "Untitled"),
                    "sections_count": len(sections)
                })
                
            except Exception as e:
                print(f"Error processing {pdf_file.name}: {str(e)}")
                continue
        
        if not all_sections:
            return self._create_empty_result(persona, job, "No sections extracted from documents")
        
        # Analyze relevance based on persona and job
        print(f"Analyzing {len(all_sections)} sections for persona '{persona}' and job '{job}'")
        ranked_sections = self.persona_analyzer.analyze_relevance(all_sections, persona, job)
        
        # Extract top subsections with refined text
        subsections = self.persona_analyzer.extract_subsections(ranked_sections, top_n=15)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Create final result
        result = {
            "metadata": {
                "documents": processed_docs,
                "persona": persona,
                "job": job,
                "timestamp": datetime.now().isoformat(),
                "processing_time_seconds": round(processing_time, 2),
                "total_sections_analyzed": len(all_sections),
                "top_sections_selected": len(ranked_sections[:10])
            },
            "sections": [
                {
                    "doc_name": section["doc_name"],
                    "page": section["page"],
                    "section_title": section.get("title", "Untitled"),
                    "importance_rank": section["importance_rank"],
                    "relevance_score": round(section["relevance_score"], 2),
                    "persona_match": section.get("persona_match", ""),
                    "job_match": section.get("job_match", "")
                }
                for section in ranked_sections[:10]  # Top 10 sections
            ],
            "subsections": subsections[:8]  # Top 8 subsections with refined text
        }
        
        return result
    
    def _extract_sections_with_text(self, pdf_file: Path, outline_result: Dict) -> List[Dict]:
        """Extract sections with their full text content."""
        sections = []
        
        # Process each heading from the outline
        for heading in outline_result.get("outline", []):
            # Extract text content for this section
            section_text = self._extract_section_text(pdf_file, heading)
            
            sections.append({
                "title": heading["text"],
                "level": heading["level"],
                "page": heading["page"],
                "text": section_text
            })
        
        return sections
    
    def _extract_section_text(self, pdf_file: Path, heading: Dict) -> str:
        """Extract text content for a specific section."""
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(str(pdf_file))
            page_num = heading["page"] - 1  # Convert to 0-based index
            
            if page_num >= len(doc):
                doc.close()
                return ""
            
            # Extract text from the page
            page = doc[page_num]
            text = page.get_text()
            
            # Clean and limit text
            text = self._clean_extracted_text(text)
            
            doc.close()
            return text
            
        except Exception as e:
            print(f"Error extracting text for section '{heading['text']}': {str(e)}")
            return ""
    
    def _clean_extracted_text(self, text: str) -> str:
        """Clean extracted text from PDF."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        import re
        text = re.sub(r'\s+', ' ', text)
        
        # Limit length to avoid memory issues
        if len(text) > 2000:
            text = text[:2000] + "..."
        
        return text.strip()
    
    def _create_empty_result(self, persona: str, job: str, reason: str) -> Dict[str, Any]:
        """Create empty result structure."""
        return {
            "metadata": {
                "documents": [],
                "persona": persona,
                "job": job,
                "timestamp": datetime.now().isoformat(),
                "processing_time_seconds": 0.0,
                "total_sections_analyzed": 0,
                "top_sections_selected": 0,
                "error": reason
            },
            "sections": [],
            "subsections": []
        }