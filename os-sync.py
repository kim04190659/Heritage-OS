import os
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Configuration
WATCH_DIR = "knowledge-assets"
INDEX_FILE = "knowledge-assets/index-for-ai.md"
POLL_INTERVAL = 10  # Seconds

def generate_index():
    """Scans knowledge-assets and generates an index file for AI."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating index...")
    
    lines = ["# Heritage-OS Knowledge Index", "", "This file is auto-generated for NotebookLM scanning.", ""]
    
    root_path = Path(".")
    target_path = root_path / WATCH_DIR
    
    if not target_path.exists():
        print(f"Error: {WATCH_DIR} not found.")
        return False

    for file_path in target_path.rglob("*"):
        if file_path.name == "index-for-ai.md" or file_path.name.startswith("."):
            continue
        
        if file_path.is_file() and file_path.suffix in ['.md', '.txt', '.pdf']:
            relative_path = file_path.relative_to(root_path)
            lines.append(f"## {file_path.name}")
            lines.append(f"- Path: `{relative_path}`")
            lines.append(f"- Last Modified: {datetime.fromtimestamp(file_path.stat().st_mtime)}")
            
            # Read snippet for markdown/text
            if file_path.suffix in ['.md', '.txt']:
                try:
                    content = file_path.read_text(encoding='utf-8')[:200].replace('\n', ' ')
                    lines.append(f"- Preview: {content}...")
                except Exception:
                    lines.append("- Preview: (Binary or unreadable content)")
            
            lines.append("")

    try:
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return True
    except Exception as e:
        print(f"Error writing index: {e}")
        return False

def git_sync():
    """Commits and pushes changes if any."""
    try:
        # Check for changes
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not status.stdout.strip():
            return  # No changes

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Changes detected. Syncing...")
        
        # Add all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit
        msg = f"Auto-sync: knowledge-assets update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        
        # Push (Requires upstream to be set, suppressing error if not set)
        # Note: In a fresh init, remote might not be configured.
        result = subprocess.run(["git", "push"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Git Push Warning: Remote may not be configured or reachable.")
            print(f"Details: {result.stderr.strip()}")
        else:
            print("Push successful.")
            
    except subprocess.CalledProcessError as e:
        print(f"Git Error: {e}")

def main():
    print("Heritage-OS Sync & Monitor started.")
    print(f"Watching: {WATCH_DIR}")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            # 1. Update Index
            if generate_index():
                # 2. Sync if index update caused changes (or other file changes)
                git_sync()
            
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopping monitor.")

if __name__ == "__main__":
    main()
