from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
from collections import OrderedDict
from resume_parser import extract_info
from tips import get_resume_tips

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join("backend")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def calculate_resume_score(text, extracted_skills):
    score = 0

    # 1. Contact Info (10 points)
    contact_present = any([
        re.search(r'\b[A-Za-z]+\s[A-Za-z]+\b', text),  # name pattern
        re.search(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', text),
        re.search(r'(\+91)?[6-9]\d{9}', text)
    ])
    if contact_present:
        score += 10

    # 2. Skill Relevance (20 points)
    data_science_keywords = {"python", "pandas", "numpy", "matplotlib", "seaborn", "nltk", "machine learning", "data analysis"}
    matched_skills = data_science_keywords.intersection(set(s.lower() for s in extracted_skills))
    score += min(20, len(matched_skills) * 2)

    # 3. Projects or Experience (15 points)
    if any(word in text.lower() for word in ["project", "experience", "internship"]):
        score += 15

    # 4. Education Info (15 points)
    if re.search(r"(B\.?Tech|M\.?Tech|Bachelor|Master|Degree|University|College)", text, re.IGNORECASE):
        score += 15

    # 5. Tools & Technologies (10 points)
    tools = {"jupyter", "tableau", "git", "colab", "excel", "vscode"}
    found_tools = tools.intersection(set(text.lower().split()))
    score += min(10, len(found_tools) * 2)

    # 6. Soft Skills (10 points)
    soft_skills = {"communication", "teamwork", "leadership", "collaboration", "adaptability"}
    found_soft = soft_skills.intersection(set(text.lower().split()))
    if found_soft:
        score += 10

    # 7. Formatting / Length (10 points)
    if 100 < len(text.split()) < 1000:  # decent length
        score += 10

    # 8. Certifications (10 points)
    if any(word in text.lower() for word in ["coursera", "certification", "certified", "udemy", "kaggle"]):
        score += 10

    return min(score, 100)

@app.route('/')
def home():
    return 'Resume Analyzer Backend is Running'

@app.route('/upload', methods=['POST'])
def upload_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filepath = os.path.join(UPLOAD_FOLDER, "uploaded_resume.pdf")
        file.save(filepath)

        # Extract basic info, skills, and full text
        result = extract_info(filepath)
        basic_info = result.get("basic_info", {})
        skills = result.get("skills", [])
        full_text = result.get("text", "")

        # Get domain and tips
        domain_line, tips = get_resume_tips(skills)

        # Calculate resume score using logic
        score = calculate_resume_score(full_text, skills)

        # Return ordered response
        ordered_response = OrderedDict()
        ordered_response['basic_info'] = basic_info
        ordered_response['skills'] = skills
        ordered_response['domain'] = domain_line
        ordered_response['tips'] = tips
        ordered_response['score'] = score

        return jsonify(ordered_response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
