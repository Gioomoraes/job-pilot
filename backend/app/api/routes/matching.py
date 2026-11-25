from fastapi import APIRouter

from app.models.matching import MatchRequest, MatchResult
from app.services.matching import calculate_match

router = APIRouter()


@router.post(
    "/match",
    response_model=MatchResult,
    summary="Calcular compatibilidade entre vaga e currículo",
    description=(
        "Cruza os dados estruturados de uma vaga e de um currículo de forma determinística, "
        "calculando a pontuação percentual de aderência, os requisitos atendidos e as lacunas (gaps)."
    ),
)
def match_job_and_resume(body: MatchRequest) -> MatchResult:
    """
    Recebe os objetos validados de vaga e currículo e executa o cálculo de compatibilidade.
    """
    return calculate_match(vaga=body.vaga, curriculo=body.curriculo)
