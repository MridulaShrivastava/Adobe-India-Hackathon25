"""
Heading Detection Module
Advanced heading detection using multiple heuristics.
"""

from typing import Dict, Any
from text_analyzer import TextAnalyzer

class HeadingDetector:
    """Advanced heading detection using multiple heuristics."""
    
    def __init__(self):
        self.text_analyzer = TextAnalyzer()
    
    def analyze_block(self, block: Dict, font_analysis: Dict) -> Dict[str, Any]:
        """
        Analyze a text block to determine if it's a heading and its level.
        
        Args:
            block: Text block with formatting information
            font_analysis: Document-wide font analysis results
            
        Returns:
            Dictionary with heading analysis results
        """
        text = block["text"]
        
        # Calculate heading probability
        heading_score = self._calculate_heading_score(block, font_analysis)
        
        # Determine if it's a heading
        is_heading = heading_score >= 3.0
        
        if is_heading:
            level = self._determine_heading_level(block, font_analysis)
            return {
                "is_heading": True,
                "level": f"H{level}",
                "confidence": min(heading_score / 5.0, 1.0),
                "text_cleaned": self.text_analyzer.clean_heading_text(text)
            }
        
        return {
            "is_heading": False,
            "level": None,
            "confidence": 0.0,
            "text_cleaned": text
        }
    
    def _calculate_heading_score(self, block: Dict, font_analysis: Dict) -> float:
        """Calculate the likelihood of a block being a heading."""
        score = 0.0
        text = block["text"]
        
        # Font size factor
        body_size = font_analysis["body_size"]
        size_ratio = block["size"] / body_size
        
        if size_ratio >= 1.5:
            score += 3.0
        elif size_ratio >= 1.2:
            score += 2.0
        elif size_ratio >= 1.1:
            score += 1.0
        
        # Font style factors
        flags = block["flags"]
        if flags & 2**4:  # Bold
            score += 2.0
        if flags & 2**6:  # Italic (sometimes used for headings)
            score += 0.5
        
        # Text content analysis
        if self.text_analyzer.looks_like_heading(text):
            score += 2.0
        
        # Length factors
        text_length = len(text)
        if 5 <= text_length <= 100:
            score += 1.0
        elif text_length > 200:
            score -= 2.0  # Very long text unlikely to be heading
        
        # Position factors (headings often start lines)
        bbox = block["bbox"]
        left_margin = bbox[0]
        if left_margin < 100:  # Close to left margin
            score += 0.5
        
        # All caps (but not too long)
        if text.isupper() and text_length <= 50:
            score += 1.5
        
        # Sentence-like structure (periods, commas) - less likely to be heading
        if '.' in text and not text.endswith('.'):
            score -= 1.0
        if text.count(',') > 2:
            score -= 1.0
        
        return max(0.0, score)
    
    def _determine_heading_level(self, block: Dict, font_analysis: Dict) -> int:
        """Determine the heading level (1-3) based on various factors."""
        text = block["text"]
        
        # Check text content for level indicators
        content_level = self.text_analyzer.get_heading_level_from_text(text)
        
        # Font size-based level
        body_size = font_analysis["body_size"]
        size_ratio = block["size"] / body_size
        
        if size_ratio >= 2.0:
            size_level = 1
        elif size_ratio >= 1.5:
            size_level = 2
        else:
            size_level = 3
        
        # Font style influence
        flags = block["flags"]
        style_adjustment = 0
        
        if flags & 2**4:  # Bold
            style_adjustment -= 1  # Bold suggests higher level (lower number)
        
        # Combine factors
        final_level = min(content_level, size_level) + style_adjustment
        
        # Ensure level is within valid range
        return max(1, min(3, final_level))