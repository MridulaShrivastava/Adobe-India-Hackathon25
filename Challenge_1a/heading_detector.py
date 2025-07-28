from typing import Dict, Any
from text_analyzer import TextAnalyzer

class HeadingDetector:
    def __init__(self):
        self.text_analyzer = TextAnalyzer()

    def analyze_block(self, block: Dict, font_analysis: Dict) -> Dict[str, Any]:
        text = block["text"]
        heading_score = self._calculate_heading_score(block, font_analysis)
        is_heading = heading_score >= 2.8

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
        score = 0.0
        text = block["text"]
        text_len = len(text)
        size_ratio = block["size"] / font_analysis["body_size"]
        flags = block["flags"]

        # Size scoring
        if size_ratio >= 1.8:
            score += 2.5
        elif size_ratio >= 1.4:
            score += 1.8
        elif size_ratio >= 1.1:
            score += 1.0

        # Styling: bold, italic
        if flags & 2**4:  # bold
            score += 1.0
        if flags & 2**6:  # italic
            score += 0.3

        # Looks like heading
        if self.text_analyzer.looks_like_heading(text):
            score += 1.0

        # All caps, short
        if text.isupper() and text_len <= 50:
            score += 1.0

        # Penalize long paragraphs
        if text_len > 200:
            score -= 1.5

        return max(0.0, score)

    def _determine_heading_level(self, block: Dict, font_analysis: Dict) -> int:
        text = block["text"]
        size_ratio = block["size"] / font_analysis["body_size"]
        content_hint = self.text_analyzer.get_heading_level_from_text(text)

        # Estimate level based on size ranking
        if size_ratio >= 1.8:
            size_level = 1
        elif size_ratio >= 1.4:
            size_level = 2
        elif size_ratio >= 1.1:
            size_level = 3
        else:
            size_level = 4

        # Final decision: minimum of content and size hints
        level = min(content_hint, size_level)
        return max(1, min(level, 3))
