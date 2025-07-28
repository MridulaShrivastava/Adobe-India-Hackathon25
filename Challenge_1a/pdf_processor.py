"""
PDF Processing Module
Handles PDF parsing and outline extraction with multiple heuristics.
"""

import fitz  # PyMuPDF
import re
from typing import List, Dict, Any, Tuple
from text_analyzer import TextAnalyzer
from heading_detector import HeadingDetector

class PDFProcessor:
    """Main PDF processing class."""
    
    def __init__(self):
        self.text_analyzer = TextAnalyzer()
        self.heading_detector = HeadingDetector()
    
    def extract_outline(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract title and outline from PDF document.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with title and outline information
        """
        doc = fitz.open(pdf_path)
        
        try:
            # Extract text blocks with formatting information
            text_blocks = self._extract_text_blocks(doc)
            
            # Detect title and headings
            title = self._detect_title(text_blocks)
            headings = self._detect_headings(text_blocks)
            
            return {
                "title": title,
                "outline": headings
            }
            
        finally:
            doc.close()
    
    def _extract_text_blocks(self, doc: fitz.Document) -> List[Dict]:
        """Extract text blocks with formatting information from all pages."""
        text_blocks = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")
            
            for block in blocks.get("blocks", []):
                if "lines" not in block:
                    continue
                    
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["text"].strip():
                            text_blocks.append({
                                "text": span["text"].strip(),
                                "page": page_num + 1,
                                "font": span["font"],
                                "size": span["size"],
                                "flags": span["flags"],
                                "bbox": span["bbox"],
                                "block_bbox": block["bbox"]
                            })
        
        return text_blocks
    
    def _detect_title(self, text_blocks: List[Dict]) -> str:
        """Detect document title from text blocks."""
        if not text_blocks:
            return "Untitled Document"
        
        # Look for title in first few blocks
        candidates = []
        
        for i, block in enumerate(text_blocks[:20]):  # Check first 20 blocks
            text = block["text"]
            
            # Skip if too short or too long
            if len(text) < 3 or len(text) > 100:
                continue
            
            # Calculate title score based on multiple factors
            score = self._calculate_title_score(block, i, text_blocks)
            candidates.append((text, score))
        
        if candidates:
            # Return highest scoring candidate
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0]
        
        return "Untitled Document"
    
    def _calculate_title_score(self, block: Dict, position: int, all_blocks: List[Dict]) -> float:
        """Calculate likelihood score for a text block being the title."""
        score = 0.0
        text = block["text"]
        
        # Position factor (earlier = better, but not first line)
        if position == 0:
            score += 3
        elif position < 5:
            score += 5
        elif position < 10:
            score += 2
        
        # Font size factor
        avg_size = sum(b["size"] for b in all_blocks[:50]) / min(50, len(all_blocks))
        if block["size"] > avg_size * 1.2:
            score += 4
        
        # Font style factor (bold = better)
        if block["flags"] & 2**4:  # Bold flag
            score += 3
        
        # Length factor (not too short, not too long)
        if 10 <= len(text) <= 80:
            score += 2
        elif len(text) < 10:
            score -= 2
        
        # Content patterns
        if self.text_analyzer.looks_like_title(text):
            score += 3
        
        return score
    
    def _detect_headings(self, text_blocks: List[Dict]) -> List[Dict]:
        """Detect headings and their levels from text blocks."""
        headings = []
        
        # Analyze font characteristics
        font_analysis = self._analyze_fonts(text_blocks)
        
        for block in text_blocks:
            heading_info = self.heading_detector.analyze_block(block, font_analysis)
            
            if heading_info["is_heading"]:
                headings.append({
                    "level": heading_info["level"],
                    "text": block["text"],
                    "page": block["page"]
                })
        
        # Post-process to ensure logical heading hierarchy
        return self._refine_heading_levels(headings)
    
    def _analyze_fonts(self, text_blocks: List[Dict]) -> Dict:
        """Analyze font characteristics across the document."""
        sizes = [block["size"] for block in text_blocks]
        fonts = [block["font"] for block in text_blocks]
        
        # Calculate statistics
        size_stats = {
            "avg": sum(sizes) / len(sizes) if sizes else 12,
            "max": max(sizes) if sizes else 12,
            "min": min(sizes) if sizes else 12
        }
        
        # Find common font sizes and their frequencies
        size_freq = {}
        for size in sizes:
            size_freq[size] = size_freq.get(size, 0) + 1
        
        # Sort by frequency to find body text size
        common_sizes = sorted(size_freq.items(), key=lambda x: x[1], reverse=True)
        body_size = common_sizes[0][0] if common_sizes else 12
        
        return {
            "size_stats": size_stats,
            "body_size": body_size,
            "size_frequencies": size_freq,
            "font_list": list(set(fonts))
        }
    
    def _refine_heading_levels(self, headings: List[Dict]) -> List[Dict]:
        """Refine heading levels to ensure logical hierarchy."""
        if not headings:
            return headings
        
        # Sort by page and original position
        headings.sort(key=lambda x: x["page"])
        
        # Adjust levels to ensure proper hierarchy
        for i in range(1, len(headings)):
            current_level = int(headings[i]["level"][1])  # Extract number from "H1", "H2", etc.
            prev_level = int(headings[i-1]["level"][1])
            
            # Don't allow jumps of more than 1 level
            if current_level > prev_level + 1:
                headings[i]["level"] = f"H{prev_level + 1}"
        
        return headings