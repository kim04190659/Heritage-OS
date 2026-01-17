import os
import json
import glob
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
RAW_DIR = BASE_DIR / "knowledge-assets" / "raw-logs"
STRUCTURED_DIR = BASE_DIR / "knowledge-assets" / "structured"

# Mock AI Logic
def mock_ai_inference(text):
    """
    Simulates AI inference to extract judgment logic and emotional context.
    """
    logic = "Based on standard procedure, but adapted for specific circumstances."
    emotion = "Neutral professional demeanor."
    
    if "住民" in text or "resident" in text:
        emotion = "High sensitivity due to resident concerns. Empathy required."
    if "判断" in text or "decision" in text:
        logic = "Decision made based on long-term trust building rather than immediate efficiency."
    if "怒り" in text or "anger" in text:
        emotion = "Tense situation requiring de-escalation."
        
    return logic, emotion

def process_logs():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Scanning raw logs...")
    
    # 1. Find all JSON logs
    log_files = glob.glob(str(RAW_DIR / "*.json"))
    
    processed_count = 0
    for log_file in log_files:
        path = Path(log_file)
        
        # Load Raw Data
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading {path.name}: {e}")
            continue

        # Check if already processed (simple check: if markdown exists)
        target_md = STRUCTURED_DIR / f"{path.stem}.md"
        if target_md.exists():
            continue
            
        print(f"Processing new log: {path.name}")
        
        # 2. Mock AI Inference
        raw_text = data.get("content", {}).get("raw_text", "")
        logic, emotion = mock_ai_inference(raw_text)
        
        # 3. Generate Markdown Content
        md_content = f"""# {data.get('title', 'Untitled Knowledge')}

## Metadata
- **ID**: `{data.get('id')}`
- **Source**: {data.get('source_metadata', {}).get('type')}
- **Captured By**: {data.get('source_metadata', {}).get('captured_by')}
- **Date**: {data.get('created_at')}

## Content Summary
{data.get('content', {}).get('summary', 'No summary provided.')}

## AI Analysis (Context Structure)
### Judgment Logic (Why)
{logic}

### Emotional Context
{emotion}

## Raw Content
{raw_text}
"""
        
        # 4. Save Structured Data
        try:
            with open(target_md, "w", encoding="utf-8") as f:
                f.write(md_content)
            print(f"Generated structured knowledge: {target_md.name}")
            processed_count += 1
        except Exception as e:
            print(f"Error writing markdown: {e}")
            
    if processed_count == 0:
        print("No new logs to process.")
    else:
        print(f"Successfully processed {processed_count} logs.")

if __name__ == "__main__":
    # Ensure directories exist
    STRUCTURED_DIR.mkdir(parents=True, exist_ok=True)
    process_logs()
