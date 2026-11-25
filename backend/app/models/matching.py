from pydantic import BaseModel, Field

from app.models.job import JobAnalysis
from app.models.resume import ResumeAnalysis


class MatchRequest(BaseModel):
    """
    Entrada para a rota de compatibilidade: recebe os dados estruturados da vaga e do currículo.
    """
    vaga: JobAnalysis = Field(..., description="Dados estruturados da vaga extraídos pela IA")
    curriculo: ResumeAnalysis = Field(..., description="Dados estruturados do currículo extraídos pela IA")


class MatchResult(BaseModel):
    """
    Resultado detalhado da análise de aderência e cálculo de gaps.
    """
    pontuacao_total: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Pontuação percentual calculada matematicamente (0.0 a 100.0)",
    )
    nivel_aderencia: str = Field(
        ...,
        description="Classificação textual da compatibilidade (Alta, Média ou Baixa)",
    )
    total_requisitos_analisados: int = Field(
        ...,
        description="Quantidade total de requisitos e tecnologias avaliadas",
    )
    skills_atendidas: list[str] = Field(
        default_factory=list,
        description="Competências e requisitos da vaga encontrados no perfil do candidato",
    )
    gaps_obrigatorios: list[str] = Field(
        default_factory=list,
        description="Requisitos essenciais exigidos pela vaga que não constam no currículo",
    )
    gaps_diferenciais: list[str] = Field(
        default_factory=list,
        description="Requisitos desejáveis ou diferenciais que o candidato não possui",
    )
    resumo_aderencia: str = Field(
        ...,
        description="Diagnóstico objetivo gerado pelo sistema sobre a compatibilidade",
    )
