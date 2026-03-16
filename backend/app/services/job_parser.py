import re

COMMON_SKILLS = {
    "python", "java", "javascript", "typescript", "sql", "c++", "c#", "r",
    "react", "next.js", "node.js", "fastapi", "django", "flask",
    "postgresql", "mysql", "sqlite", "mongodb", "redis",
    "aws", "azure", "gcp", "docker", "kubernetes",
    "machine learning", "deep learning", "nlp", "llm", "rag",
    "pytorch", "tensorflow", "scikit-learn", "pandas", "numpy",
    "rest api", "graphql", "git", "linux"
}

def extract_skills_from_text(text: str) -> list[str]:
    text_lower = text.lower()
    found_skills = []

    for skill in COMMON_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(set(found_skills))

def parse_job_description(job_text: str) -> dict:
    skills = extract_skills_from_text(job_text)

    return {
        "job_text": job_text,
        "required_skills": skills,
        "skill_count": len(skills)
    }
