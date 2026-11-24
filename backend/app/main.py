from fastapi import FastAPI

from app.api.routes import jobs, resumes

app = FastAPI(
    title="Job Pilot",
    description=(
        "Plataforma de análise de oportunidades profissionais com IA. "
        "Analisa descrições de vagas e currículos, identifica compatibilidades e lacunas "
        "e recomenda ações de preparação."
    ),
    version="0.3.0",
)

app.include_router(jobs.router, prefix="/api/v1", tags=["Vagas"])
app.include_router(resumes.router, prefix="/api/v1/resumes", tags=["Currículos"])
