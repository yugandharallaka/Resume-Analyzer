import re
import PyPDF2
import docx

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_info(file_path):
    basic_info = {}
    skills = []

    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")

    # Normalize lines
    text_lines = [line.strip() for line in text.splitlines() if line.strip()]
    text_full = "\n".join(text_lines)

    # Email & Phone
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text_full)
    phone_match = re.search(r'\+?\d[\d\s\-]{8,}', text_full)

    # Name
    name_match = re.search(r'Name[:\- ]+(.*)', text_full, re.IGNORECASE)
    probable_name = None
    for line in text_lines[:5]:
        if len(line.split()) <= 4 and not re.search(r'\d', line):
            probable_name = line
            break
    name = name_match.group(1).strip() if name_match else (probable_name or "Not found")

    basic_info['name'] = name
    basic_info['email'] = email_match.group() if email_match else "Not found"
    basic_info['phone'] = phone_match.group() if phone_match else "Not found"

    # Find skills section (from "Skills" to next heading)
    skills_text = ""
    skill_start = -1
    for i, line in enumerate(text_lines):
        if re.search(r'(technical skills|skills)', line, re.IGNORECASE):
            skill_start = i
            break

    if skill_start != -1:
        for i in range(skill_start + 1, len(text_lines)):
            if re.search(r'(education|experience|projects|certifications|achievements)', text_lines[i], re.IGNORECASE):
                break
            skills_text += text_lines[i] + "\n"

    known_skills = [
        'python', 'java', 'c++', 'c', 'r', 'scikit-learn', 'nltk',
        'pandas', 'numpy', 'matplotlib', 'seaborn',
        'supervised learning', 'unsupervised learning', 'data analysis',
        'data visualization', 'accuracy', 'precision', 'recall',
        'confusion matrix', 'jupyter notebook', 'google colab',
        'communication skills', 'team collaboration'
    ]

    extracted_skills = []
    for skill in known_skills:
        if re.search(rf'\b{re.escape(skill)}\b', skills_text, re.IGNORECASE):
            extracted_skills.append(skill.lower())

    # Recommend tips
    tips = []
    if 'data analysis' in extracted_skills or 'machine learning' in extracted_skills:
        tips.append("For Data Science, consider learning: statistics, excel, SQL.")
    if 'python' in extracted_skills and 'flask' not in extracted_skills:
        tips.append("Explore backend development with Flask or Django.")
    if 'communication skills' in extracted_skills:
        tips.append("Build leadership and project management experience.")

    return {
        "basic_info": basic_info,
        "skills": extracted_skills,
        "tips": tips,
        "text": text_full
    }
