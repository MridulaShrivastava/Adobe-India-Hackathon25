# Persona-Driven Document Intelligence System

A sophisticated document intelligence system that analyzes multiple PDFs and extracts the most relevant sections based on user persona and job requirements. Built on the Round 1A PDF extractor with advanced relevance scoring and multilingual support.

## Features

- **Persona-Driven Analysis**: Tailored extraction for researchers, students, analysts, and managers
- **Job-Specific Intelligence**: Optimized for literature reviews, exam prep, trend analysis, and more
- **Multi-Document Processing**: Analyzes 3-10 PDFs simultaneously with relevance ranking
- **Advanced Scoring Algorithm**: Combines persona keywords, job patterns, and structural factors
- **Multilingual Support**: English, Spanish, French, and German document analysis
- **Fast Processing**: Completes analysis of 3-5 PDFs in under 60 seconds
- **Docker-Ready**: Runs in isolated container environment
- **Modular Architecture**: Extends Round 1A with clean separation of concerns

## Usage Examples

### JSON Configuration Mode (Recommended)
Place persona configuration JSON files in the input directory along with PDF files:

```bash
# The system will automatically detect and process JSON configurations
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  persona-doc-intelligence
```

**Example JSON Configuration:**
```json
{
  "challenge_info": {
    "challenge_id": "round_1b_003",
    "description": "Creating manageable forms"
  },
  "documents": [
    {"filename": "Learn Acrobat - Create and Convert_1.pdf", "title": "Learn Acrobat - Create and Convert_1"},
    {"filename": "Learn Acrobat - Fill and Sign.pdf", "title": "Learn Acrobat - Fill and Sign"}
  ],
  "persona": {
    "role": "HR professional"
  },
  "job_to_be_done": {
    "task": "Create and manage fillable forms for onboarding and compliance."
  }
}
```

### Basic Usage
```bash
# Default: researcher doing literature review
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  persona-doc-intelligence
```

### Custom Persona and Job
```bash
# Student preparing for exams
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  persona-doc-intelligence \
  python main.py --persona student --job "exam prep"

# Analyst doing competitive analysis
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  persona-doc-intelligence \
  python main.py --persona analyst --job "competitive analysis"
```

## Supported Personas

- **researcher**: Methodology, results, datasets, benchmarks
- **student**: Definitions, concepts, examples, fundamentals
- **analyst**: Revenue, trends, performance, business metrics
- **manager**: Strategy, planning, decision-making, leadership

## Supported Jobs

- **literature review**: Related work, methodologies, comparisons
- **exam prep**: Key concepts, definitions, summaries
- **trend analysis**: Patterns, growth data, temporal analysis
- **competitive analysis**: Market positioning, strategic comparisons
- **research methodology**: Methods, approaches, techniques

## Technical Architecture

```
├── main.py                    # Entry point with CLI interface
├── document_intelligence.py   # Main orchestration system
├── persona_analyzer.py        # Persona-driven relevance analysis
├── pdf_processor.py          # PDF parsing (from Round 1A)
├── text_analyzer.py          # Text analysis utilities
├── heading_detector.py       # Heading detection logic
├── approach_explanation.md   # Technical approach documentation
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
└── README.md               # This file
```

### Docker Build and Run

```bash
# Build the container
docker build --platform linux/amd64 -t persona-doc-intelligence .

# Run with default settings (researcher + literature review)
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  persona-doc-intelligence
```

### Input/Output

- **Input**: Place 3-10 PDF files in the `input` directory
- **Output**: Single JSON file with analysis results in the `output` directory

### JSON Configuration Input

- **Persona JSON**: Configuration files specifying persona, job, and target documents
- **PDF Files**: Referenced documents must exist in the input directory
- **Multiple Configs**: System can process multiple persona configurations in one run

### Output Format

```json
{
  "metadata": {
    "documents": [{"name": "paper1", "title": "AI Research", "sections_count": 15}],
    "persona": "researcher",
    "job": "literature review",
    "timestamp": "2024-01-15T10:30:00",
    "processing_time_seconds": 45.2,
    "total_sections_analyzed": 87,
    "top_sections_selected": 10
  },
  "sections": [
    {
      "doc_name": "paper1",
      "page": 3,
      "section_title": "Methodology",
      "importance_rank": 1,
      "relevance_score": 8.5,
      "persona_match": "High relevance: methodology, approach, analysis",
      "job_match": "Job-relevant: literature, review, comparison"
    }
  ],
  "subsections": [
    {
      "doc_name": "paper1",
      "page": 3,
      "section_title": "Methodology",
      "refined_text": "Our approach combines multiple machine learning techniques...",
      "relevance_score": 8.5,
      "importance_rank": 1
    }
  ]
}
```

## Performance Specifications

- **Processing Speed**: ≤60 seconds for 3-5 PDFs
- **Memory Usage**: Optimized for container environments
- **Model Size**: <1GB (rule-based approach, no ML models)
- **Platform**: AMD64 CPU compatible, no GPU required
- **Scalability**: Handles 3-10 PDFs per analysis run

## Dependencies

- **PyMuPDF**: Efficient PDF parsing and text extraction  
- **Python 3.11**: Modern Python runtime

## Advanced Features

### Relevance Scoring Algorithm
- **Persona Keywords** (60% weight): Domain-specific vocabulary matching
- **Job Patterns** (40% weight): Task-oriented content identification  
- **Multilingual Bonus** (10% weight): Foreign language term recognition
- **Structural Factors**: Section hierarchy and page positioning

### Intelligent Text Processing
- **Content Refinement**: Removes PDF artifacts and formatting noise
- **Length Optimization**: Balances completeness with processing speed
- **Sentence Boundary Detection**: Ensures clean text truncation
- **Multilingual Cleaning**: Handles special characters across languages

## Testing Recommendations

Test with diverse scenarios:
- **Academic Papers**: Research methodologies, literature reviews
- **Business Reports**: Financial analysis, market research
- **Technical Manuals**: Implementation guides, specifications
- **Educational Materials**: Textbooks, study guides
- **Multilingual Documents**: Spanish, French, German content

## Example Use Cases

### Researcher + Literature Review
Extracts methodology sections, related work comparisons, and experimental results from academic papers.

### Student + Exam Prep  
Identifies key definitions, fundamental concepts, and summary sections from textbooks and study materials.

### Analyst + Trend Analysis
Focuses on data trends, growth patterns, and comparative analysis sections from business reports.

### Manager + Competitive Analysis
Extracts strategic insights, market positioning, and competitive advantage discussions from industry reports.

## Future Enhancements

The modular architecture supports:
- **Custom Personas**: User-defined keyword profiles
- **Advanced NLP**: Semantic similarity scoring
- **Batch Processing**: Parallel document analysis
- **API Integration**: RESTful service interface
- **Additional Languages**: Extended multilingual support