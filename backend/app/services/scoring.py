def compute_match_score(candidate_skills: list[str], required_skills: list[str]) -> dict:
    candidate_set = set(skill.lower() for skill in candidate_skills)
    required_set = set(skill.lower() for skill in required_skills)

    matched = sorted(list(candidate_set.intersection(required_set)))
    missing = sorted(list(required_set - candidate_set))

    if len(required_set) == 0:
        score = 0
    else:
        score = round((len(matched) / len(required_set)) * 100)

    if score >= 80:
        recommendation = "Strong Match"
    elif score >= 55:
        recommendation = "Moderate Match"
    else:
        recommendation = "Weak Match"

    strengths = [f"Candidate demonstrates {skill}" for skill in matched]
    gaps = [f"Candidate lacks evidence of {skill}" for skill in missing]

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendation": recommendation,
        "strengths": strengths,
        "gaps": gaps
    }
