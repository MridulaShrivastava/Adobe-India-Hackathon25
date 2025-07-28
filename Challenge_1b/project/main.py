#!/usr/bin/env python3
"""
Persona-Driven Document Intelligence System
Analyzes multiple PDFs and extracts relevant sections based on user persona and job.
"""

import os
import json
import sys
import argparse
from typing import List, Dict
from pathlib import Path
from document_intelligence import DocumentIntelligenceSystem
json_files = list(input_dir.glob("**/*.json"))


def find_persona_json_files(input_dir: Path) -> List[Dict]:
    """Find and parse persona JSON files recursively inside input directory."""
    json_files = list(input_dir.glob("**/*.json"))
    persona_configs = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            persona_role = config.get("persona", {}).get("role", "researcher")
            job_task = config.get("job_to_be_done", {}).get("task", "literature review")
            documents = config.get("documents", [])
            
            persona_configs.append({
                "config_file": json_file.name,
                "persona": persona_role,
                "job": job_task,
                "documents": documents,
                "config": config,
                "folder": json_file.parent
            })
        except Exception as e:
            print(f"[ERROR] Failed to read {json_file.name}: {e}")
            continue
    
    return persona_configs

def process_persona_config(system: DocumentIntelligenceSystem, 
                           config: Dict, 
                           output_dir: Path) -> str:
    """Process a single persona configuration."""
    persona = config["persona"]
    job = config["job"]
    documents = config["documents"]
    folder = config["folder"]
    
    print(f"\n🔍 Processing config: {config['config_file']}")
    print(f"👤 Persona: {persona}")
    print(f"🎯 Job: {job}")
    print(f"📄 Documents listed: {len(documents)}")
    print("-" * 50)
    
    pdf_paths = []
    for doc in documents:
        filename = doc.get("filename", "")
        path = folder / filename
        if path.exists():
            pdf_paths.append(str(path))
            print(f"✓ Found: {filename}")
        else:
            print(f"✗ Missing: {filename}")
    
    if not pdf_paths:
        print("⚠️ No valid PDFs found for this config.")
        return None

    import tempfile, shutil
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        for pdf_path in pdf_paths:
            shutil.copy2(pdf_path, temp_path)

        result = system.analyze_documents(str(temp_path), persona, job)
        result["metadata"]["config_file"] = config["config_file"]
        result["metadata"]["specified_documents"] = len(documents)
        result["metadata"]["found_documents"] = len(pdf_paths)

        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        persona_safe = persona.replace(" ", "_")
        output_file = output_dir / f"{persona_safe}_{timestamp}_analysis.json"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Completed for: {persona}")
        print(f"⏱ Time: {result['metadata']['processing_time_seconds']}s")
        print(f"📁 Output saved: {output_file.name}")

        return output_file.name

def main():
    parser = argparse.ArgumentParser(description='Persona-Driven Document Intelligence')
    parser.add_argument('--input-dir', default='/app/input',
                        help='Input folder with persona configs and PDFs')
    parser.add_argument('--output-dir', default='/app/output',
                        help='Output directory for JSON results')
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    system = DocumentIntelligenceSystem()

    configs = find_persona_json_files(input_dir)

    if not configs:
        print("❌ No persona JSON configuration files found")
        print("📌 Place JSON and PDFs inside folders like /input/Persona1/")
        return 1

    print(f"🔧 Found {len(configs)} configuration file(s). Starting analysis...")

    results = []
    for config in configs:
        result = process_persona_config(system, config, output_dir)
        if result:
            results.append(result)

    print(f"\n🏁 All Done. Processed {len(results)} config(s).")
    print("📄 Output files:")
    for r in results:
        print(f"✅ {r}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
