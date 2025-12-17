import re
import os

def parse_questions(file_path, output_dir):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    questions = {}
    current_q_num = 0
    current_q_text = []
    current_term = ""
    current_explanation = []
    
    state = "IDLE" # IDLE, QUESTION, WAITING_ANSWER, TERM, EXPLANATION
    
    for line in lines:
        line_stripped = line.strip()
        
        # Check for new Problem start
        match_problem = re.search(r'Problem (\d+) of 20', line)
        if match_problem:
            # If we were building a previous question, save it
            if current_q_num > 0:
                save_question(output_dir, current_q_num, current_q_text, current_term, current_explanation)
            
            # Reset for new question
            current_q_num = int(match_problem.group(1))
            current_q_text = []
            current_term = ""
            current_explanation = []
            state = "QUESTION"
            continue
            
        # Check for Industry Insight (to stop explanation capture)
        if "Industry Insight" in line:
            if state == "EXPLANATION":
                state = "IDLE"
            continue

        if state == "QUESTION":
            if "Solution?" in line:
                state = "WAITING_ANSWER"
            elif line_stripped:
                current_q_text.append(line_stripped)
        
        elif state == "WAITING_ANSWER":
            if "Answer:" in line:
                state = "TERM"
        
        elif state == "TERM":
            # Look for the term (next non-empty line)
            if line_stripped and "Answer:" not in line: # Avoid re-triggering if Answer line has text? No, Answer line usually just has "Answer: (X)"
                current_term = line_stripped
                state = "EXPLANATION"
            # Note: If "Answer:" line also had the term, we might miss it. 
            # But looking at the file, "Answer:" is usually on its own line or with the number.
            # The term is on the next non-empty line.
            
        elif state == "EXPLANATION":
            # Capture explanation until next Problem or Industry Insight
            # We already handle "Problem" and "Industry Insight" checks at the top.
            if line_stripped:
                current_explanation.append(line_stripped)

    # Save the last question
    if current_q_num > 0:
        save_question(output_dir, current_q_num, current_q_text, current_term, current_explanation)

def save_question(output_dir, q_num, q_text, term, explanation):
    filename = f"Question_{q_num:02d}.md"
    filepath = os.path.join(output_dir, filename)
    
    q_str = " ".join(q_text)
    exp_str = " ".join(explanation)
    
    md_content = f"""# Question
{q_str}

# Answer
{term}

# Explanation
{exp_str}
"""
    with open(filepath, 'w') as f:
        f.write(md_content)
    print(f"Created {filename}")

if __name__ == "__main__":
    os.makedirs('Extra_question/questions', exist_ok=True)
    parse_questions('Extra_question/extracted_content.txt', 'Extra_question/questions')
