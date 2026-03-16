from fastapi import FastAPI
from app.routers import analyze

app = FastAPI(
    title="HireSight AI",
    description="AI-powered candidate intelligence platform",
    version="0.1"
)

app.include_router(analyze.router)

@app.get("/")
def root():
    return {"message": "HireSight API running"}
