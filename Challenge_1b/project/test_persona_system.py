#!/usr/bin/env python3
"""
Test script for persona-driven document intelligence system.
"""

import json
import tempfile
from pathlib import Path
from document_intelligence import DocumentIntelligenceSystem

def test_persona_analysis():
    """Test persona-based analysis functionality."""
    print("Testing Persona-Driven Document Intelligence")
    print("=" * 50)
    
    # Initialize system
    system = DocumentIntelligenceSystem()
    
    # Test different persona/job combinations
    test_cases = [
        ("researcher", "literature review"),
        ("student", "exam prep"),
        ("analyst", "trend analysis"),
        ("manager", "competitive analysis")
    ]
    
    print("Testing persona/job combinations:")
    print("-" * 35)
    
    for persona, job in test_cases:
        print(f"✓ {persona.capitalize()} + {job.title()}")
        
        # Test keyword matching
        analyzer = system.persona_analyzer
        
        # Create mock section
        mock_section = {
            "title": "Methodology and Results Analysis",
            "text": "This section presents our research methodology and experimental results. We conducted a comprehensive analysis of the dataset using machine learning techniques.",
            "level": "H2",
            "page": 3,
            "doc_name": "test_paper"
        }
        
        # Analyze relevance
        scored_sections = analyzer.analyze_relevance([mock_section], persona, job)
        
        if scored_sections:
            score = scored_sections[0]["relevance_score"]
            print(f"  Relevance score: {score:.2f}")
        else:
            print("  No relevance score calculated")
    
    print("\nTesting multilingual support:")
    print("-" * 30)
    
    # Test multilingual keywords
    multilingual_sections = [
        {
            "title": "Metodología de Investigación",
            "text": "Esta sección presenta nuestra metodología de investigación y análisis de resultados.",
            "level": "H2", "page": 1, "doc_name": "spanish_paper"
        },
        {
            "title": "Méthodologie de Recherche", 
            "text": "Cette section présente notre méthodologie de recherche et analyse des résultats.",
            "level": "H2", "page": 1, "doc_name": "french_paper"
        },
        {
            "title": "Forschungsmethodologie",
            "text": "Dieser Abschnitt präsentiert unsere Forschungsmethodologie und Ergebnisanalyse.",
            "level": "H2", "page": 1, "doc_name": "german_paper"
        }
    ]
    
    for section in multilingual_sections:
        scored = analyzer.analyze_relevance([section], "researcher", "literature review")
        if scored:
            score = scored[0]["relevance_score"]
            lang = section["doc_name"].split("_")[0].title()
            print(f"✓ {lang}: {score:.2f}")
    
    print("\nSystem ready for document processing!")

def create_sample_output():
    """Create a sample output file for demonstration."""
    sample_result = {
        "metadata": {
            "documents": [
                {"name": "sample_paper", "title": "AI Research Methods", "sections_count": 12}
            ],
            "persona": "researcher",
            "job": "literature review", 
            "timestamp": "2024-01-15T10:30:00.000000",
            "processing_time_seconds": 2.5,
            "total_sections_analyzed": 12,
            "top_sections_selected": 8
        },
        "sections": [
            {
                "doc_name": "sample_paper",
                "page": 2,
                "section_title": "Related Work and Literature Review",
                "importance_rank": 1,
                "relevance_score": 9.2,
                "persona_match": "High relevance: literature, review, analysis",
                "job_match": "Job-relevant: literature, review, comparison"
            },
            {
                "doc_name": "sample_paper", 
                "page": 4,
                "section_title": "Methodology",
                "importance_rank": 2,
                "relevance_score": 8.7,
                "persona_match": "High relevance: methodology, approach",
                "job_match": "Job-relevant: methodology, analysis"
            }
        ],
        "subsections": [
            {
                "doc_name": "sample_paper",
                "page": 2,
                "section_title": "Related Work and Literature Review",
                "refined_text": "Previous research in this domain has focused on various machine learning approaches. Smith et al. (2023) proposed a novel neural network architecture that achieved state-of-the-art results on benchmark datasets. However, their approach has limitations in handling multilingual content...",
                "relevance_score": 9.2,
                "importance_rank": 1
            }
        ]
    }
    
    # Save sample output
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    sample_file = output_dir / "sample_analysis_researcher_2024-01-15.json"
    with open(sample_file, 'w', encoding='utf-8') as f:
        json.dump(sample_result, f, indent=2, ensure_ascii=False)
    
    print(f"\nSample output created: {sample_file}")
    print("This demonstrates the expected output format.")

if __name__ == "__main__":
    test_persona_analysis()
    create_sample_output()