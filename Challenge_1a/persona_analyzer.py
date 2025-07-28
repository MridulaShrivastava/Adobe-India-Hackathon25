"""
Persona-Driven Document Analysis Module
Analyzes document sections based on user persona and job-to-be-done.
"""

import re
from typing import List, Dict, Any, Tuple
from collections import defaultdict

class PersonaAnalyzer:
    """Analyzes document relevance based on persona and job context."""
    
    def __init__(self):
        # Define persona-specific keywords and patterns
        self.persona_keywords = {
            "researcher": {
                "high": ["methodology", "methods", "approach", "experiment", "study", "analysis", 
                        "results", "findings", "conclusion", "discussion", "literature", "review",
                        "dataset", "benchmark", "evaluation", "performance", "comparison"],
                "medium": ["introduction", "background", "related work", "future work", "limitations",
                          "abstract", "summary", "overview"],
                "low": ["acknowledgments", "references", "appendix", "biography"]
            },
            "student": {
                "high": ["definition", "concept", "principle", "theory", "example", "formula",
                        "equation", "key", "important", "fundamental", "basic", "overview",
                        "introduction", "summary", "conclusion"],
                "medium": ["application", "practice", "exercise", "problem", "solution",
                          "case study", "illustration"],
                "low": ["advanced", "complex", "detailed", "technical", "specialized"]
            },
            "analyst": {
                "high": ["revenue", "profit", "growth", "market", "trend", "analysis", "data",
                        "statistics", "performance", "metrics", "kpi", "roi", "strategy",
                        "competitive", "financial", "economic", "business"],
                "medium": ["overview", "summary", "background", "context", "industry",
                          "sector", "comparison"],
                "low": ["technical", "implementation", "detailed", "appendix"]
            },
            "manager": {
                "high": ["strategy", "planning", "decision", "management", "leadership",
                        "team", "project", "goal", "objective", "outcome", "result",
                        "performance", "efficiency", "productivity"],
                "medium": ["process", "workflow", "implementation", "execution",
                          "coordination", "communication"],
                "low": ["technical", "detailed", "specification", "code"]
            }
        }
        
        # Job-specific keywords
        self.job_keywords = {
            "literature review": {
                "high": ["literature", "review", "survey", "related work", "previous",
                        "existing", "comparison", "analysis", "methodology", "approach"],
                "medium": ["introduction", "background", "conclusion", "summary"],
                "low": ["implementation", "technical", "detailed"]
            },
            "trend analysis": {
                "high": ["trend", "pattern", "growth", "change", "evolution", "development",
                        "analysis", "data", "statistics", "comparison", "temporal"],
                "medium": ["overview", "summary", "context", "background"],
                "low": ["technical", "implementation", "detailed"]
            },
            "exam prep": {
                "high": ["key", "important", "fundamental", "concept", "definition",
                        "principle", "formula", "equation", "example", "summary"],
                "medium": ["overview", "introduction", "conclusion", "review"],
                "low": ["advanced", "detailed", "complex", "specialized"]
            },
            "competitive analysis": {
                "high": ["competitive", "competitor", "comparison", "market", "analysis",
                        "strategy", "advantage", "position", "performance"],
                "medium": ["overview", "industry", "sector", "context"],
                "low": ["technical", "implementation", "detailed"]
            },
            "research methodology": {
                "high": ["methodology", "method", "approach", "technique", "procedure",
                        "experiment", "study", "analysis", "evaluation"],
                "medium": ["background", "related work", "literature"],
                "low": ["results", "conclusion", "discussion"]
            }
        }
        
        # Multilingual keyword mappings
        self.multilingual_keywords = {
            "spanish": {
                "methodology": ["metodología", "método", "enfoque"],
                "results": ["resultados", "hallazgos"],
                "analysis": ["análisis", "estudio"],
                "conclusion": ["conclusión", "resumen"],
                "introduction": ["introducción", "presentación"]
            },
            "french": {
                "methodology": ["méthodologie", "méthode", "approche"],
                "results": ["résultats", "conclusions"],
                "analysis": ["analyse", "étude"],
                "conclusion": ["conclusion", "résumé"],
                "introduction": ["introduction", "présentation"]
            },
            "german": {
                "methodology": ["methodologie", "methode", "ansatz"],
                "results": ["ergebnisse", "resultate"],
                "analysis": ["analyse", "studie"],
                "conclusion": ["fazit", "zusammenfassung"],
                "introduction": ["einführung", "einleitung"]
            }
        }
    
    def analyze_relevance(self, sections: List[Dict], persona: str, job: str) -> List[Dict]:
        """
        Analyze section relevance based on persona and job.
        
        Args:
            sections: List of extracted sections from documents
            persona: User persona (researcher, student, analyst, etc.)
            job: Job to be done (literature review, exam prep, etc.)
            
        Returns:
            List of sections with relevance scores and rankings
        """
        scored_sections = []
        
        for section in sections:
            score = self._calculate_relevance_score(section, persona.lower(), job.lower())
            
            scored_sections.append({
                **section,
                "relevance_score": score,
                "persona_match": self._get_persona_match_reason(section, persona.lower()),
                "job_match": self._get_job_match_reason(section, job.lower())
            })
        
        # Sort by relevance score (descending)
        scored_sections.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Add importance rank
        for i, section in enumerate(scored_sections):
            section["importance_rank"] = i + 1
        
        return scored_sections
    
    def _calculate_relevance_score(self, section: Dict, persona: str, job: str) -> float:
        """Calculate relevance score for a section."""
        text = section.get("text", "").lower()
        title = section.get("title", "").lower()
        combined_text = f"{title} {text}"
        
        score = 0.0
        
        # Persona-based scoring
        persona_score = self._score_by_keywords(combined_text, persona, self.persona_keywords)
        score += persona_score * 0.6  # 60% weight for persona
        
        # Job-based scoring
        job_score = self._score_by_keywords(combined_text, job, self.job_keywords)
        score += job_score * 0.4  # 40% weight for job
        
        # Multilingual support
        multilingual_bonus = self._calculate_multilingual_score(combined_text, persona, job)
        score += multilingual_bonus * 0.1
        
        # Section type bonus
        section_bonus = self._calculate_section_type_bonus(section, persona, job)
        score += section_bonus
        
        return min(score, 10.0)  # Cap at 10.0
    
    def _score_by_keywords(self, text: str, category: str, keyword_dict: Dict) -> float:
        """Score text based on keyword categories."""
        if category not in keyword_dict:
            return 0.0
        
        keywords = keyword_dict[category]
        score = 0.0
        
        # High importance keywords
        for keyword in keywords.get("high", []):
            if keyword in text:
                score += 3.0
        
        # Medium importance keywords
        for keyword in keywords.get("medium", []):
            if keyword in text:
                score += 2.0
        
        # Low importance keywords (negative for some personas)
        for keyword in keywords.get("low", []):
            if keyword in text:
                score -= 0.5
        
        return max(score, 0.0)
    
    def _calculate_multilingual_score(self, text: str, persona: str, job: str) -> float:
        """Calculate bonus score for multilingual keyword matches."""
        score = 0.0
        
        for lang, translations in self.multilingual_keywords.items():
            for english_term, foreign_terms in translations.items():
                for foreign_term in foreign_terms:
                    if foreign_term in text:
                        # Check if this term is relevant to persona/job
                        if self._is_term_relevant(english_term, persona, job):
                            score += 1.0
        
        return score
    
    def _is_term_relevant(self, term: str, persona: str, job: str) -> bool:
        """Check if a term is relevant to the given persona and job."""
        persona_keywords = self.persona_keywords.get(persona, {})
        job_keywords = self.job_keywords.get(job, {})
        
        all_relevant = []
        for category in ["high", "medium"]:
            all_relevant.extend(persona_keywords.get(category, []))
            all_relevant.extend(job_keywords.get(category, []))
        
        return term in all_relevant
    
    def _calculate_section_type_bonus(self, section: Dict, persona: str, job: str) -> float:
        """Calculate bonus based on section type and level."""
        bonus = 0.0
        level = section.get("level", "")
        
        # Higher level headings get slight bonus for structure
        if level == "H1":
            bonus += 0.5
        elif level == "H2":
            bonus += 0.3
        elif level == "H3":
            bonus += 0.1
        
        # Page position bonus (earlier pages often more important)
        page = section.get("page", 1)
        if page <= 3:
            bonus += 0.5
        elif page <= 10:
            bonus += 0.2
        
        return bonus
    
    def _get_persona_match_reason(self, section: Dict, persona: str) -> str:
        """Get explanation for why section matches persona."""
        text = f"{section.get('title', '')} {section.get('text', '')}".lower()
        
        if persona not in self.persona_keywords:
            return "Generic match"
        
        keywords = self.persona_keywords[persona]
        matches = []
        
        for keyword in keywords.get("high", []):
            if keyword in text:
                matches.append(keyword)
        
        if matches:
            return f"High relevance: {', '.join(matches[:3])}"
        
        for keyword in keywords.get("medium", []):
            if keyword in text:
                matches.append(keyword)
        
        if matches:
            return f"Medium relevance: {', '.join(matches[:3])}"
        
        return "Low relevance match"
    
    def _get_job_match_reason(self, section: Dict, job: str) -> str:
        """Get explanation for why section matches job."""
        text = f"{section.get('title', '')} {section.get('text', '')}".lower()
        
        if job not in self.job_keywords:
            return "Generic job match"
        
        keywords = self.job_keywords[job]
        matches = []
        
        for keyword in keywords.get("high", []):
            if keyword in text:
                matches.append(keyword)
        
        if matches:
            return f"Job-relevant: {', '.join(matches[:3])}"
        
        return "General job relevance"
    
    def extract_subsections(self, sections: List[Dict], top_n: int = 10) -> List[Dict]:
        """
        Extract and refine text from top-ranked sections.
        
        Args:
            sections: Ranked sections
            top_n: Number of top sections to process
            
        Returns:
            List of refined subsections
        """
        subsections = []
        
        for section in sections[:top_n]:
            # Extract meaningful text chunks
            text = section.get("text", "")
            refined_text = self._refine_text(text)
            
            if refined_text and len(refined_text) > 50:  # Minimum meaningful length
                subsections.append({
                    "doc_name": section.get("doc_name", "Unknown"),
                    "page": section.get("page", 1),
                    "section_title": section.get("title", "Untitled"),
                    "refined_text": refined_text,
                    "relevance_score": section.get("relevance_score", 0.0),
                    "importance_rank": section.get("importance_rank", 0)
                })
        
        return subsections
    
    def _refine_text(self, text: str) -> str:
        """Refine and clean extracted text."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers/footers patterns
        text = re.sub(r'\b(page|página|page)\s+\d+\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b\d+\s+(of|de|sur|von)\s+\d+\b', '', text, flags=re.IGNORECASE)
        
        # Clean up common PDF artifacts
        text = re.sub(r'[^\w\s\.,;:!?()-]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Ensure reasonable length
        if len(text) > 1000:
            # Take first 1000 characters and try to end at sentence boundary
            truncated = text[:1000]
            last_period = truncated.rfind('.')
            if last_period > 500:  # If we have a reasonable sentence ending
                text = truncated[:last_period + 1]
            else:
                text = truncated + "..."
        
        return text.strip()