from fastapi import APIRouter, UploadFile, File, Form, Body
from pydantic import BaseModel

from app.services.resume_parser import parse_resume
from app.services.github_analyzer import analyze_github_profile
from app.services.job_parser import parse_job_description
from app.services.scoring import compute_match_score
from app.services.profile_builder import build_candidate_skill_profile

router = APIRouter(
    prefix="/analyze",
    tags=["Candidate Analysis"]
)


class MatchRequest(BaseModel):
    github_url: str
    job_description: str
    candidate_skills: list[str] = []


@router.post("/resume")
async def analyze_resume(file: UploadFile = File(...)):
    content = await file.read()
    parsed = parse_resume(content)

    return {
        "status": "success",
        "resume_analysis": parsed
    }


@router.post("/github")
async def analyze_github(github_url: str = Body(..., embed=True)):
    return analyze_github_profile(github_url)


@router.post("/job")
async def analyze_job(job_description: str = Body(..., embed=True)):
    return parse_job_description(job_description)


@router.post("/match")
async def analyze_match(payload: MatchRequest):
    github_result = analyze_github_profile(payload.github_url)
    job_result = parse_job_description(payload.job_description)

    candidate_profile = build_candidate_skill_profile(
        manual_skills=payload.candidate_skills,
        github_languages=github_result.get("top_languages", []),
        resume_skills=[]
    )

    score_result = compute_match_score(
        candidate_skills=candidate_profile["combined_skills"],
        required_skills=job_result["required_skills"]
    )

    return {
        "status": "success",
        "github_summary": github_result,
        "job_summary": job_result,
        "candidate_profile": candidate_profile,
        "match_result": score_result
    }


@router.post("/full-match")
async def analyze_full_match(
    file: UploadFile = File(...),
    github_url: str = Form(...),
    job_description: str = Form(...)
):
    content = await file.read()

    resume_result = parse_resume(content)
    github_result = analyze_github_profile(github_url)
    job_result = parse_job_description(job_description)

    candidate_profile = build_candidate_skill_profile(
        manual_skills=[],
        github_languages=github_result.get("top_languages", []),
        resume_skills=resume_result.get("skills", [])
    )

    score_result = compute_match_score(
        candidate_skills=candidate_profile["combined_skills"],
        required_skills=job_result["required_skills"]
    )

    return {
        "status": "success",
        "resume_summary": {
            "skills": resume_result.get("skills", []),
            "skill_count": resume_result.get("skill_count", 0)
        },
        "github_summary": github_result,
        "job_summary": job_result,
        "candidate_profile": candidate_profile,
        "match_result": score_result
    }
