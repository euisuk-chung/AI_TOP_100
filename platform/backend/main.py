from fastapi import FastAPI, HTTPException
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
QUESTION_DIR_EN = os.path.join(BASE_DIR, "question_en")
SOLVE_DIR = os.path.join(BASE_DIR, "solve")
SOLUTION_DIR = os.path.join(BASE_DIR, "model_solutions")

def get_question_dir(lang="kr"):
    return QUESTION_DIR_EN if lang == "en" else QUESTION_DIR_KR

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
    
    for line in lines:
        # Check for Question Header (e.g., "### Q1.", "### Q2")
        # The format in the files seems to be "### Q1. ..." or "### Q1 ..."
        match = re.match(r'^###\s*(Q\d+)', line)
        if match:
            if current_question:
                questions.append(current_question)
            
            q_id = match.group(1)
            current_question = {
                "id": q_id,
                "title": line.strip(),
                "content": ""
            }
        elif current_question:
            current_question["content"] += line + "\n"
        else:
            intro_lines.append(line)
            
    if current_question:
        questions.append(current_question)
        
    return {
        "intro": "\n".join(intro_lines),
        "questions": questions
    }

@app.get("/api/questions")
def list_questions(lang: str = "kr"):
    question_dir = get_question_dir(lang)
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
def get_question(filename: str, lang: str = "kr"):
    question_dir = get_question_dir(lang)
    filepath = os.path.join(question_dir, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Question not found")
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    parsed = parse_markdown(content)
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
def get_solution(filename: str, lang: str = "kr"):
    """Get model solution for a question"""
    # Extract the question number from filename (e.g., "1_AI_TOP_100.md" -> "1")
    match = re.match(r'^(\d+)_', filename)
    if not match:
        raise HTTPException(status_code=404, detail="Solution not found")

    question_num = match.group(1)
    lang_suffix = "ko" if lang == "kr" else "en"
    solution_filename = f"{question_num}_AI_TOP_100_solution_{lang_suffix}.md"
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
