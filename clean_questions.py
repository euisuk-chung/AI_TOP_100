import os
import glob
import re

def clean_content(content):
    lines = content.split('\n')
    
    # 1. Find the start: Look for "문제 설명" or the first header after the title
    # We'll keep the title (first line usually) and Source.
    
    start_index = 0
    # Skip the first few lines which are usually Title and Source
    # We want to remove the blog intro text.
    # A good heuristic for these specific files seems to be finding "### **문제 설명**" or just "### 문제 설명"
    # Or sometimes just the first header that isn't the title.
    
    # Let's try to find "문제 설명"
    for i, line in enumerate(lines):
        if "문제 설명" in line and line.strip().startswith("#"):
            start_index = i
            break
    
    if start_index == 0:
        # Fallback: look for the first H1/H2/H3 after line 5 (skipping title/source/metadata)
        for i, line in enumerate(lines):
            if i > 5 and line.strip().startswith("#"):
                start_index = i
                break
    
    # 2. Find the end: Look for "어떠신가요?" or "다른 문제도 살펴보고 싶다면?"
    end_index = len(lines)
    for i, line in enumerate(lines):
        if i > start_index and ("어떠신가요?" in line or "다른 문제도 살펴보고 싶다면?" in line):
            end_index = i
            break
            
    # Extract the core content
    # We want to keep the Title and Source at the top if possible, or just re-add them.
    # The original files have Title at line 0 (index 0) and Source at line 2.
    
    header = lines[:4] # Keep first 4 lines (Title, blank, Source, blank)
    body = lines[start_index:end_index]
    
    return '\n'.join(header + body)

def main():
    question_dir = "question"
    files = glob.glob(os.path.join(question_dir, "*.md"))
    
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        cleaned = clean_content(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)
            
        print(f"Cleaned {filepath}")

if __name__ == "__main__":
    main()
