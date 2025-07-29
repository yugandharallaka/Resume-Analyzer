from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import traceback
import uuid
from collections import OrderedDict
from resume_parser import extract_info
from tips import get_resume_tips

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join("backend", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def calculate_resume_score(text, extracted_skills):
    score = 0
    text_lower = text.lower()
    skills_lower = set(s.lower() for s in extracted_skills)

    # 1. Contact Info (10 points)
    if re.search(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', text_lower) and re.search(r'(\+91)?[6-9]\d{9}', text_lower):
        score += 10
    else:
        score -= 5  # penalty if missing

    # 2. Skill Relevance (20 points)
    important_skills = {"python", "pandas", "numpy", "matplotlib", "seaborn", "nltk", "machine learning", "data analysis"}
    matched_skills = important_skills.intersection(skills_lower)
    score += min(20, len(matched_skills) * 2)

    # 3. Projects or Experience (15 points)
    if any(word in text_lower for word in ["project", "experience", "internship"]):
        score += 15

    # 4. Education (10 points)
    if re.search(r"(b\\.?tech|m\\.?tech|bachelor|master|degree|university|college)", text_lower):
        score += 10

    # 5. Certifications (10 points)
    if any(word in text_lower for word in ["certification", "certified", "coursera", "udemy", "kaggle"]):
        score += 10

    # 6. Tools & Platforms (10 points)
    tools = {"jupyter", "tableau", "colab", "excel", "git", "vscode"}
    matched_tools = tools.intersection(set(text_lower.split()))
    score += min(10, len(matched_tools) * 2)

    # 7. Soft Skills (5 points)
    soft_skills = {"communication", "leadership", "teamwork", "adaptability"}
    matched_soft = soft_skills.intersection(set(text_lower.split()))
    if matched_soft:
        score += 5

    # 8. Resume Length (5 points)
    word_count = len(text.split())
    if 150 <= word_count <= 1000:
        score += 5
    elif word_count < 100:
        score -= 5

    return max(min(score, 100), 0)

@app.route('/')
def home():
    return '✅ Resume Analyzer Backend is Running'

@app.route('/upload', methods=['POST'])
def upload_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        ext = file.filename.rsplit('.', 1)[-1].lower()
        if ext not in ['pdf', 'docx']:
            return jsonify({'error': 'Unsupported file format. Only PDF and DOCX allowed.'}), 400

        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        result = extract_info(filepath)
        basic_info = result.get("basic_info", {})
        skills = result.get("skills", [])
        full_text = result.get("text", "")

        domain_line, tips = get_resume_tips(skills)
        score = calculate_resume_score(full_text, skills)

        ordered_response = OrderedDict()
        ordered_response['basic_info'] = basic_info
        ordered_response['skills'] = skills
        ordered_response['domain'] = domain_line
        ordered_response['tips'] = tips
        ordered_response['score'] = score

        return jsonify(ordered_response), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
