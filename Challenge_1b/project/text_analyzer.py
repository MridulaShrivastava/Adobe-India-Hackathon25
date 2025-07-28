"""
Text Analysis Module
Provides text analysis utilities for content classification.
"""

import re
from typing import List, Set

class TextAnalyzer:
    """Text analysis utilities."""
    
    def __init__(self):
        # Common title patterns (multilingual)
        self.title_patterns = [
            # English
            r'\b(introduction|overview|summary|conclusion|abstract|preface)\b',
            r'\b(chapter|section|part)\s+\d+',
            r'\b(user\s+guide|manual|handbook|tutorial)\b',
            
            # Spanish
            r'\b(introducción|resumen|conclusión|capítulo|sección)\b',
            
            # French
            r'\b(introduction|résumé|conclusion|chapitre|section)\b',
            
            # German
            r'\b(einführung|zusammenfassung|fazit|kapitel|abschnitt)\b',
            
            # Common academic/technical terms
            r'\b(analysis|research|study|report|documentation)\b',
        ]
        
        # Patterns that suggest NOT a title
        self.non_title_patterns = [
            r'^\d+\.\d+',  # Version numbers
            r'^page\s+\d+',  # Page numbers
            r'^figure\s+\d+',  # Figure captions
            r'^table\s+\d+',  # Table captions
            r'^\w+@\w+\.',  # Email addresses
            r'^https?://',  # URLs
        ]
        
        # Heading indicators (multilingual)
        self.heading_indicators = [
            # Numbered sections
            r'^\d+\.?\s+',
            r'^\d+\.\d+\.?\s+',
            r'^\d+\.\d+\.\d+\.?\s+',
            
            # Roman numerals
            r'^[IVX]+\.?\s+',
            
            # Letters
            r'^[A-Z]\.?\s+',
            
            # Common heading words
            r'^(chapter|section|part|appendix)\s+',
            r'^(capítulo|sección|parte|apéndice)\s+',  # Spanish
            r'^(chapitre|section|partie|annexe)\s+',   # French
            r'^(kapitel|abschnitt|teil|anhang)\s+',    # German
        ]
    
    def looks_like_title(self, text: str) -> bool:
        """Check if text looks like a document title."""
        text_lower = text.lower()
        
        # Check for non-title patterns
        for pattern in self.non_title_patterns:
            if re.search(pattern, text_lower):
                return False
        
        # Check for title patterns
        for pattern in self.title_patterns:
            if re.search(pattern, text_lower):
                return True
        
        # Additional heuristics
        # Titles often have title case
        if self._is_title_case(text):
            return True
        
        # Not too many special characters
        special_chars = len(re.findall(r'[^\w\s]', text))
        if special_chars / len(text) > 0.3:
            return False
        
        return True
    
    def looks_like_heading(self, text: str) -> bool:
        """Check if text looks like a heading."""
        text_lower = text.lower()
        
        # Check for heading indicators
        for pattern in self.heading_indicators:
            if re.search(pattern, text_lower):
                return True
        
        # Check if it's in title case
        if self._is_title_case(text):
            return True
        
        # Check if it's all caps (but not too long)
        if text.isupper() and len(text) <= 50:
            return True
        
        return False
    
    def get_heading_level_from_text(self, text: str) -> int:
        """Determine heading level from text content."""
        # Check for numbered sections
        if re.match(r'^\d+\.\d+\.\d+', text):
            return 3
        elif re.match(r'^\d+\.\d+', text):
            return 2
        elif re.match(r'^\d+\.', text):
            return 1
        
        # Check for common heading words
        text_lower = text.lower()
        if any(word in text_lower for word in ['chapter', 'capítulo', 'chapitre', 'kapitel']):
            return 1
        elif any(word in text_lower for word in ['section', 'sección', 'section', 'abschnitt']):
            return 2
        
        return 2  # Default to H2
    
    def _is_title_case(self, text: str) -> bool:
        """Check if text is in title case."""
        words = text.split()
        if len(words) < 2:
            return False
        
        # Check if most words start with capital letter
        capitalized = sum(1 for word in words if word and word[0].isupper())
        return capitalized / len(words) >= 0.7
    
    def clean_heading_text(self, text: str) -> str:
        """Clean heading text by removing numbering and extra whitespace."""
        # Remove common numbering patterns
        text = re.sub(r'^\d+\.?\s*', '', text)
        text = re.sub(r'^\d+\.\d+\.?\s*', '', text)
        text = re.sub(r'^\d+\.\d+\.\d+\.?\s*', '', text)
        text = re.sub(r'^[IVX]+\.?\s*', '', text)
        text = re.sub(r'^[A-Z]\.?\s*', '', text)
        
        return text.strip()