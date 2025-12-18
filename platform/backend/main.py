from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import glob
import re

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUESTION_DIR_KR = os.path.join(BASE_DIR, "question")
QUESTION_DIR_KR = os.path.join(BASE_DIR, "question")
SOLVE_DIR = os.path.join(BASE_DIR, "solve")
SOLUTION_DIR = os.path.join(BASE_DIR, "model_solutions")
SOURCE_DIR = os.path.join(BASE_DIR, "source")

app.mount("/source", StaticFiles(directory=SOURCE_DIR), name="source")

class Answer(BaseModel):
    id: str
    code: str
    language: str

class SolutionSubmission(BaseModel):
    answers: List[Answer]

def parse_markdown(content):
    lines = content.split('\n')
    intro_lines = []
    questions = []
    current_question = None
    file_source_info = None
    
    for line in lines:
        # Check for Question Header (e.g., "### Q1.", "### Q2")
        match = re.match(r'^###\s*(Q\d+)', line)
        if match:
            if current_question:
                questions.append(current_question)
            
            q_id = match.group(1)
            current_question = {
                "id": q_id,
                "title": line.strip(),
                "content": "",
                "source": None
            }
            continue

        # Check for Source line
        source_match = re.match(r'^Source:\s*(.+)', line)
        if source_match:
            source_text = source_match.group(1).strip()
            # Try to parse markdown link [label](path)
            link_match = re.match(r'\[(.*?)\]\((.*?)\)', source_text)
            source_data = None
            if link_match:
                source_data = {
                    "label": link_match.group(1),
                    "path": link_match.group(2)
                }
            else:
                source_data = {
                    "label": "Source",
                    "path": source_text
                }
            
            if current_question:
                current_question["source"] = source_data
            else:
                file_source_info = source_data
            # Don't add Source line to content/intro
            continue

        if current_question:
            current_question["content"] += line + "\n"
        else:
            intro_lines.append(line)
            
    if current_question:
        questions.append(current_question)
        
    return {
        "intro": "\n".join(intro_lines),
        "questions": questions,
        "source": file_source_info
    }

def expand_source_path(source_data):
    if not source_data:
        return None
    
    path = source_data["path"]
    # Remove leading slash if present
    if path.startswith("/"):
        path = path[1:]
        
    # Check if it starts with "source/"
    if path.startswith("source/"):
        abs_path = os.path.join(BASE_DIR, path)

        # Check for glob pattern matching (if contains wildcards and not a direct directory/file exists)
        if any(char in path for char in ['*', '?', '[']) and not os.path.exists(abs_path):
             # Use glob to find matching files
            search_path = abs_path
            matches = glob.glob(search_path)
            
            images = []
            exts = ['.png', '.jpg', '.jpeg', '.gif']
            
            for m in matches:
                # Get relative path for frontend
                 # os.path.relpath might be safer
                rel_path = os.path.relpath(m, BASE_DIR).replace("\\", "/")
                
                if any(m.lower().endswith(ext) for ext in exts):
                    images.append(rel_path)
            
            if images:
                source_data["type"] = "gallery"
                source_data["images"] = sorted(images)
            else:
                 # If no matches or no images, fall back to link or text
                 pass

        elif os.path.isdir(abs_path):
            # It's a directory. List images and files.
            images = []
            files_list = []
            exts = ['.png', '.jpg', '.jpeg', '.gif']
            # List all files in directory
            try:
                dir_contents = os.listdir(abs_path)
                for f in dir_contents:
                    if any(f.lower().endswith(ext) for ext in exts):
                        images.append(os.path.join(path, f).replace("\\", "/"))
                    else:
                        # Is a non-image file
                        files_list.append(os.path.join(path, f).replace("\\", "/"))
                
                if images:
                    source_data["type"] = "gallery"
                    source_data["images"] = sorted(images)
                elif files_list:
                    source_data["type"] = "directory"
                    source_data["files"] = sorted(files_list)
                else:
                    source_data["type"] = "directory"
                    source_data["files"] = []
            except Exception as e:
                print(f"Error listing directory {abs_path}: {e}")
                source_data["type"] = "file"
        else:
            # Check if it is an image file
            if any(path.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                source_data["type"] = "image"
            else:
                source_data["type"] = "file"
    else:
        source_data["type"] = "link"
        
    return source_data

@app.get("/api/questions")
def list_questions():
    question_dir = QUESTION_DIR_KR
    files = glob.glob(os.path.join(question_dir, "*.md"))
    questions = []
    for f in files:
        filename = os.path.basename(f)
        questions.append({
            "filename": filename,
            "title": filename.replace(".md", "")
        })
    # Sort by filename to keep order
    questions.sort(key=lambda x: x["filename"])
    return questions

@app.get("/api/questions/{filename}")
def get_question(filename: str):
    question_dir = QUESTION_DIR_KR
    filepath = os.path.join(question_dir, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Question not found")
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    parsed = parse_markdown(content)
    
    # Expand source paths
    if parsed.get("source"):
        parsed["source"] = expand_source_path(parsed["source"])
        
    for q in parsed.get("questions", []):
        if q.get("source"):
            q["source"] = expand_source_path(q["source"])
            
    return parsed

@app.post("/api/solve/{filename}")
def save_solution(filename: str, submission: SolutionSubmission):
    # Create a directory for the solution based on the question name
    question_name = filename.replace(".md", "")
    solution_dir = os.path.join(SOLVE_DIR, question_name)
    os.makedirs(solution_dir, exist_ok=True)
    
    saved_files = []
    
    for answer in submission.answers:
        # Determine extension
        ext = "txt"
        if answer.language == "python":
            ext = "py"
        elif answer.language == "javascript":
            ext = "js"
        elif answer.language == "c":
            ext = "c"
        elif answer.language == "cpp":
            ext = "cpp"
        elif answer.language == "markdown":
            ext = "md"
        
        # Save as Q1.py, Q2.js, etc.
        solution_file = os.path.join(solution_dir, f"{answer.id}.{ext}")
        
        with open(solution_file, "w", encoding="utf-8") as f:
            f.write(answer.code)
        
        saved_files.append(solution_file)
        
    return {"message": "Solutions saved", "paths": saved_files}

@app.get("/api/solve/{filename}")
def get_user_solution(filename: str):
    # Determine solution directory
    question_name = filename.replace(".md", "")
    solution_dir = os.path.join(SOLVE_DIR, question_name)
    
    if not os.path.exists(solution_dir):
        return {"answers": []}
    
    answers = []
    # List all files
    try:
        files = os.listdir(solution_dir)
        for f in files:
            # Parse id and extension
            name, ext = os.path.splitext(f)
            # ext has dot, e.g. .py
            
            # Determine language from extension
            language = "python" # default
            if ext == ".py":
                language = "python"
            elif ext == ".js":
                language = "javascript"
            elif ext == ".c":
                language = "c"
            elif ext == ".cpp":
                language = "cpp"
            elif ext == ".md":
                language = "markdown"
            elif ext == ".txt":
                language = "python" # Fallback or plain text?
            
            with open(os.path.join(solution_dir, f), "r", encoding="utf-8") as file:
                code = file.read()
                
            answers.append({
                "id": name,
                "code": code,
                "language": language
            })
    except Exception as e:
        print(f"Error reading solutions: {e}")
        return {"answers": []}
        
    return {"answers": answers}

def parse_solution_by_questions(content):
    """Parse solution markdown into per-question sections"""
    lines = content.split('\n')
    solutions = {}
    current_q_id = None
    current_content = []
    intro_content = []

    for line in lines:
        # Match ### Q1. or ### Q2 etc.
        match = re.match(r'^###\s*(Q\d+)', line)
        if match:
            # Save previous question content
            if current_q_id:
                solutions[current_q_id] = '\n'.join(current_content).strip()

            current_q_id = match.group(1)
            current_content = [line]
        elif current_q_id:
            # Check if we hit a new ## section (end of questions)
            if line.startswith('## ') and not line.startswith('### '):
                solutions[current_q_id] = '\n'.join(current_content).strip()
                current_q_id = None
                current_content = []
            else:
                current_content.append(line)
        else:
            intro_content.append(line)

    # Save last question
    if current_q_id:
        solutions[current_q_id] = '\n'.join(current_content).strip()

    return {
        "intro": '\n'.join(intro_content).strip(),
        "questions": solutions
    }

@app.get("/api/solutions/{filename}")
def get_solution(filename: str):
    """Get model solution for a question"""
    # Extract the question number from filename (e.g., "1_AI_TOP_100.md" -> "1")
    match = re.match(r'^(\d+)_', filename)
    if not match:
        raise HTTPException(status_code=404, detail="Solution not found")

    question_num = match.group(1)
    solution_filename = f"{question_num}_AI_TOP_100_solution_ko.md"
    solution_path = os.path.join(SOLUTION_DIR, solution_filename)

    if not os.path.exists(solution_path):
        raise HTTPException(status_code=404, detail="Solution not found")

    with open(solution_path, "r", encoding="utf-8") as f:
        content = f.read()

    parsed = parse_solution_by_questions(content)
    return {"content": content, "parsed": parsed}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
