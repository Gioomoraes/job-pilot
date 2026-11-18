from pydantic import BaseModel, Field


class JobInput(BaseModel):
    """Entrada da análise: texto bruto da descrição da vaga."""

    descricao: str = Field(
        ...,
        min_length=10,
        description="Texto integral da descrição da vaga colada pelo usuário.",
        examples=["Pessoa Desenvolvedora Backend Pleno — Acme Tecnologia. Modelo híbrido em São Paulo..."],
    )


class JobAnalysis(BaseModel):
    """Saída estruturada da análise, conforme contrato definido em docs/contrato-da-api.md."""

    cargo: str | None = Field(None, description="Título da posição conforme aparece na descrição.")
    empresa: str | None = Field(None, description="Nome da empresa, se informado.")
    nivel: str | None = Field(None, description="Senioridade conforme aparece na descrição, sem normalizar sinônimos.")
    modalidade: str | None = Field(None, description="Regime de trabalho: remoto, presencial ou híbrido.")
    localizacao: str | None = Field(None, description="Localização informada: cidade, estado ou país.")
    responsabilidades: list[str] = Field(default_factory=list, description="Atividades e atribuições da função.")
    requisitos_obrigatorios: list[str] = Field(default_factory=list, description="Requisitos obrigatórios.")
    diferenciais: list[str] = Field(default_factory=list, description="Qualificações desejáveis ou diferenciais.")
    tecnologias: list[str] = Field(default_factory=list, description="Todas as tecnologias citadas na descrição.")
    beneficios: list[str] = Field(default_factory=list, description="Benefícios explicitamente oferecidos.")
    pontos_de_atencao: list[str] = Field(
        default_factory=list,
        description="Ambiguidades, lacunas relevantes e contradições explícitas na descrição.",
    )
