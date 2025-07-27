def get_resume_tips(extracted_skills):
    extracted_skills = [skill.lower().strip() for skill in extracted_skills]

    domain_skills = {
        "Data Science": [
            "pandas", "numpy", "matplotlib", "seaborn", "statistics", "excel", "data science", "machine learning"
        ],
        "AI/ML": [
            "deep learning", "nlp", "tensorflow", "pytorch", "computer vision", "scikit-learn"
        ],
        "Backend Development": [
            "nodejs", "sql", "flask", "django", "mongodb", "mysql", "postgresql", "expressjs"
        ],
        "Frontend Development": [
            "html", "css", "javascript", "react", "angular", "bootstrap", "tailwind", "jquery", "vue"
        ],
        "DevOps": [
            "docker", "kubernetes", "jenkins", "aws", "azure", "git", "linux", "terraform", "bash"
        ],
        "Mobile Development": [
            "flutter", "dart", "react native", "android", "swift", "kotlin", "ios"
        ],
        "Cloud Computing": [
            "gcp", "cloud computing", "cloud functions", "serverless"
        ],
        "Cybersecurity": [
            "network security", "penetration testing", "ethical hacking", "nmap", "kali linux", "burpsuite", "wireshark"
        ],
        "UI/UX Design": [
            "figma", "adobe xd", "sketch", "wireframing", "prototyping", "design thinking", "user research"
        ],
        "Database Management": [
            "database design", "firebase", "nosql"
        ]
    }

    tips = []
    matched_domains = {}

    for domain, skills in domain_skills.items():
        matched = [s for s in skills if s in extracted_skills]
        if matched:
            matched_domains[domain] = len(matched)

    if matched_domains:
        likely_domain = max(matched_domains, key=matched_domains.get)
        domain_line = f"You are most likely interested in: {likely_domain}"
    else:
        domain_line = "You are most likely interested in: Unknown (add more relevant skills)."

    # Generate learning tips based on matched domain
    for domain, skills in domain_skills.items():
        matched = [s for s in skills if s in extracted_skills]
        if len(matched) >= 2:
            missing_skills = [s for s in skills if s not in extracted_skills]
            if missing_skills:
                tips.append(f"For {domain}, consider learning: {', '.join(missing_skills[:5])}.")

    if not tips:
        tips.append("Add more skills or keywords relevant to your domain.")

    return domain_line, tips
