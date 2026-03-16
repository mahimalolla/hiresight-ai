import io
import re
from PyPDF2 import PdfReader

COMMON_SKILLS = {
    "python", "java", "javascript", "typescript", "sql", "c++", "c#", "r",
    "react", "next.js", "node.js", "fastapi", "django", "flask",
    "postgresql", "mysql", "sqlite", "mongodb", "redis",
    "aws", "azure", "gcp", "docker", "kubernetes",
    "machine learning", "deep learning", "nlp", "llm", "rag",
    "pytorch", "tensorflow", "scikit-learn", "pandas", "numpy",
    "rest api", "graphql", "git", "linux"
}

def extract_skills_from_resume_text(text: str) -> list[str]:
    text_lower = text.lower()
    found_skills = []

    for skill in COMMON_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(set(found_skills))

def parse_resume(file_bytes):
    pdf = PdfReader(io.BytesIO(file_bytes))
    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    extracted_skills = extract_skills_from_resume_text(text)

    return {
        "raw_text": text,
        "skills": extracted_skills,
        "skill_count": len(extracted_skills)
    }
