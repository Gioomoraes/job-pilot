from fastapi import FastAPI

from app.api.routes import jobs

app = FastAPI(
    title="Job Pilot",
    description=(
        "Plataforma de análise de oportunidades profissionais com IA. "
        "Analisa descrições de vagas e currículos, identifica compatibilidades e lacunas "
        "e recomenda ações de preparação."
    ),
    version="0.2.0",
)

app.include_router(jobs.router, prefix="/api/v1", tags=["Vagas"])
