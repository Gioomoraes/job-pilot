from fastapi import APIRouter, HTTPException, status

from app.models.job import JobAnalysis, JobInput
from app.services.gemini import analyze_job_description

router = APIRouter()


@router.post(
    "/analyze",
    response_model=JobAnalysis,
    summary="Analisar descrição de vaga",
    description=(
        "Recebe o texto bruto de uma descrição de vaga e retorna os campos estruturados "
        "extraídos pelo Gemini, conforme o contrato definido em `docs/contrato-da-api.md`. "
        "A análise usa apenas o conteúdo fornecido — nenhuma informação é inventada."
    ),
)
def analyze_job(body: JobInput) -> JobAnalysis:
    """
    Rota de análise de vaga.

    Delega a extração ao GeminiService e trata dois cenários de erro:
    - ValueError: chave da API ausente (503 Service Unavailable).
    - Qualquer outro erro: falha na comunicação com o Gemini (502 Bad Gateway).
    """
    try:
        return analyze_job_description(body.descricao)

    except ValueError as exc:
        # Chave da API não configurada — problema de configuração local
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )

    except Exception as exc:
        # Erro de rede, timeout ou resposta inesperada do Gemini
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro ao chamar a API do Gemini: {exc}",
        )
