import requests
from collections import Counter

GITHUB_API_BASE = "https://api.github.com"


def extract_username(github_input: str) -> str:
    github_input = github_input.strip().rstrip("/")
    if "github.com/" in github_input:
        return github_input.split("github.com/")[-1].split("/")[0]
    return github_input


def analyze_github_profile(github_input: str) -> dict:
    username = extract_username(github_input)

    user_url = f"{GITHUB_API_BASE}/users/{username}"
    repos_url = f"{GITHUB_API_BASE}/users/{username}/repos?per_page=100&sort=updated"

    user_resp = requests.get(user_url, timeout=15)
    if user_resp.status_code != 200:
        return {
            "status": "error",
            "message": f"Could not fetch GitHub user '{username}'"
        }

    repos_resp = requests.get(repos_url, timeout=15)
    if repos_resp.status_code != 200:
        return {
            "status": "error",
            "message": f"Could not fetch repos for '{username}'"
        }

    user_data = user_resp.json()
    repos_data = repos_resp.json()

    language_counter = Counter()
    ai_keywords = {
        "llm", "rag", "ai", "ml", "machine-learning", "deep-learning",
        "nlp", "transformer", "fastapi", "langchain", "vector", "embedding",
        "neural", "pytorch", "tensorflow", "chatbot", "computer-vision"
    }

    ai_signal_repos = []
    notable_repos = []

    total_stars = 0
    total_forks = 0

    for repo in repos_data:
        repo_name = (repo.get("name") or "").lower()
        description = (repo.get("description") or "").lower()
        language = repo.get("language")
        stargazers_count = repo.get("stargazers_count", 0)
        forks_count = repo.get("forks_count", 0)

        total_stars += stargazers_count
        total_forks += forks_count

        if language:
            language_counter[language] += 1

        text_blob = f"{repo_name} {description}"
        matched_keywords = [kw for kw in ai_keywords if kw in text_blob]

        if matched_keywords:
            ai_signal_repos.append({
                "name": repo.get("name"),
                "description": repo.get("description"),
                "language": language,
                "stars": stargazers_count,
                "html_url": repo.get("html_url"),
                "matched_keywords": matched_keywords
            })

        notable_repos.append({
            "name": repo.get("name"),
            "description": repo.get("description"),
            "language": language,
            "stars": stargazers_count,
            "forks": forks_count,
            "html_url": repo.get("html_url"),
            "updated_at": repo.get("updated_at")
        })

    notable_repos = sorted(
        notable_repos,
        key=lambda r: (r["stars"], r["forks"]),
        reverse=True
    )[:5]

    top_languages = [
        {"language": lang, "count": count}
        for lang, count in language_counter.most_common(5)
    ]

    ai_signal_score = "Low"
    if len(ai_signal_repos) >= 5:
        ai_signal_score = "High"
    elif len(ai_signal_repos) >= 2:
        ai_signal_score = "Medium"

    return {
        "status": "success",
        "username": user_data.get("login"),
        "name": user_data.get("name"),
        "bio": user_data.get("bio"),
        "profile_url": user_data.get("html_url"),
        "followers": user_data.get("followers"),
        "following": user_data.get("following"),
        "public_repos": user_data.get("public_repos"),
        "top_languages": top_languages,
        "total_repo_stars": total_stars,
        "total_repo_forks": total_forks,
        "ai_signal_score": ai_signal_score,
        "ai_signal_repo_count": len(ai_signal_repos),
        "ai_signal_repos": ai_signal_repos[:5],
        "notable_repos": notable_repos
    }