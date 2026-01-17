import os
import glob
from datetime import datetime, timedelta
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
STRUCTURED_DIR = BASE_DIR / "knowledge-assets" / "structured"
README_FILE = BASE_DIR / "README.md"

def get_weekly_stats():
    """Calculates stats for the past 7 days."""
    files = glob.glob(str(STRUCTURED_DIR / "*.md"))
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    
    weekly_count = 0
    total_count = len(files)
    highlights = []
    
    for f in files:
        path = Path(f)
        # Check modification time (simulate creation time)
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        
        if mtime > week_ago:
            weekly_count += 1
            # Simple extraction of title for highlight
            try:
                content = path.read_text(encoding="utf-8")
                # Assume title is first line starting with #
                lines = content.split('\n')
                for line in lines:
                    if line.startswith("# "):
                        highlights.append(line[2:].strip())
                        break
            except:
                pass
                
    return weekly_count, total_count, highlights[:3] # Top 3

def update_readme():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Updating README with Weekly Digest...")
    
    if not README_FILE.exists():
        print("Error: README.md not found.")
        return

    weekly_count, total_count, highlights = get_weekly_stats()
    
    # Format the digest section
    digest_md = f"""
## 🌿 今週の知恵 (Weekly Digest)
*最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

- **週間ナレッジ蓄積数**: `{weekly_count}` 件
- **ナレッジ総資産**: `{total_count}` 件

### 💡 特筆すべき成功パターン (Highlights)
"""
    for h in highlights:
        digest_md += f"- {h}\n"
    
    if not highlights:
        digest_md += "- (今週の更新はありません)\n"

    digest_md += "\n---"

    try:
        content = README_FILE.read_text(encoding="utf-8")
        
        # Replace or Append
        marker = "## 🌿 今週の知恵 (Weekly Digest)"
        if marker in content:
            # Replace existing section (Naive split implementation)
            parts = content.split(marker)
            # Find end of section (next H2 or ---)
            after_section = ""
            rest = parts[1]
            if "\n---" in rest:
                after_section = rest.split("\n---", 1)[1]
            elif "\n## " in rest:
                 # Find first occurrence of next header
                 import re
                 match = re.search(r'\n## ', rest)
                 if match:
                     after_section = rest[match.start():]
            
            new_content = parts[0].strip() + "\n" + digest_md + "\n" + after_section.strip()
        else:
            # Append to top or bottom? Let's append after title for visibility or bottom
            # Appending to bottom for now
            new_content = content + "\n" + digest_md

        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print("README.md updated successfully.")
        
    except Exception as e:
        print(f"Error updating README: {e}")

if __name__ == "__main__":
    update_readme()
