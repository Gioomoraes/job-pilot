from fastapi import APIRouter

from app.models.job import JobAnalysis, JobInput

router = APIRouter()


@router.post(
    "/analyze",
    response_model=JobAnalysis,
    summary="Analisar descrição de vaga",
    description=(
        "Recebe o texto bruto de uma descrição de vaga e retorna os campos estruturados "
        "conforme o contrato definido em `docs/contrato-da-api.md`. "
        "**Etapa 2:** retorna dados de exemplo. A análise real via Gemini será adicionada na Etapa 3."
    ),
)
def analyze_job(body: JobInput) -> JobAnalysis:
    """
    Rota de análise de vaga.

    Por enquanto retorna um mock estático para validar o contrato de dados.
    A integração com o Gemini será implementada na Etapa 3.
    """
    return JobAnalysis(
        cargo="[Pendente — integração com Gemini na Etapa 3]",
        empresa=None,
        nivel=None,
        modalidade=None,
        localizacao=None,
        responsabilidades=[],
        requisitos_obrigatorios=[],
        diferenciais=[],
        tecnologias=[],
        beneficios=[],
        pontos_de_atencao=[
            "Esta rota retorna dados de exemplo. "
            "A análise real com extração via LLM será implementada na Etapa 3."
        ],
    )
