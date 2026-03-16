LANGUAGE_TO_SKILL_MAP = {
    "python": "python",
    "javascript": "javascript",
    "typescript": "typescript",
    "jupyter notebook": "python",
    "html": "html",
    "css": "css",
    "dart": "dart",
    "java": "java",
    "c++": "c++",
    "c#": "c#",
    "sql": "sql"
}

IGNORE_FOR_MATCHING = {
    "html",
    "css",
    "jupyter notebook"
}


def normalize_github_languages(top_languages: list[dict]) -> list[str]:
    normalized = []

    for item in top_languages:
        lang = item.get("language")
        if not lang:
            continue

        lang_lower = lang.lower().strip()
        mapped = LANGUAGE_TO_SKILL_MAP.get(lang_lower, lang_lower)

        if mapped not in IGNORE_FOR_MATCHING:
            normalized.append(mapped)

    return sorted(set(normalized))


def build_candidate_skill_profile(
    manual_skills: list[str],
    github_languages: list[dict],
    resume_skills: list[str] | None = None
) -> dict:
    manual = [skill.lower().strip() for skill in manual_skills]
    github = normalize_github_languages(github_languages)
    resume = [skill.lower().strip() for skill in (resume_skills or [])]

    combined = sorted(set(manual + github + resume))

    return {
        "manual_skills": sorted(set(manual)),
        "github_normalized_skills": github,
        "resume_skills": sorted(set(resume)),
        "combined_skills": combined
    }
