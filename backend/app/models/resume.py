from pydantic import BaseModel, Field


class ResumeExtractionResponse(BaseModel):
    """
    Modelo de resposta para o upload e extração de texto bruto de currículo.
    """
    filename: str = Field(..., description="Nome do arquivo enviado")
    tamanho_bytes: int = Field(..., description="Tamanho do arquivo em bytes")
    total_paginas: int = Field(..., description="Número total de páginas do documento")
    texto_extraido: str = Field(..., description="Texto limpo extraído do PDF")


class ExperienceItem(BaseModel):
    """
    Representa uma experiência profissional extraída do currículo.
    """
    cargo: str = Field(..., description="Cargo ou título da função")
    empresa: str = Field(..., description="Nome da empresa ou instituição")
    periodo: str | None = Field(default=None, description="Período de atuação")
    descricao: list[str] = Field(
        default_factory=list,
        description="Principais atividades, responsabilidades ou realizações",
    )


class EducationItem(BaseModel):
    """
    Representa uma formação acadêmica ou técnica extraída do currículo.
    """
    curso: str = Field(..., description="Nome do curso ou graduação")
    instituicao: str = Field(..., description="Instituição de ensino")
    periodo: str | None = Field(default=None, description="Período ou ano de conclusão")
    status: str | None = Field(
        default=None,
        description="Situação do curso (ex: Concluído, Em andamento, Trancado)",
    )


class ResumeAnalysis(BaseModel):
    """
    Estruturação completa dos dados de um currículo extraído por LLM.
    """
    nome: str | None = Field(default=None, description="Nome completo da pessoa")
    titulo_profissional: str | None = Field(
        default=None,
        description="Título profissional ou objetivo declarado",
    )
    resumo: str | None = Field(
        default=None,
        description="Resumo profissional ou apresentação pessoal",
    )
    competencias_tecnicas: list[str] = Field(
        default_factory=list,
        description="Linguagens, frameworks, ferramentas, cloud, bancos de dados citados",
    )
    experiencias: list[ExperienceItem] = Field(
        default_factory=list,
        description="Lista de experiências profissionais",
    )
    formacao: list[EducationItem] = Field(
        default_factory=list,
        description="Lista de formações acadêmicas ou técnicas",
    )
    certificacoes: list[str] = Field(
        default_factory=list,
        description="Cursos, eventos relevantes e certificações listadas",
    )
    idiomas: list[str] = Field(
        default_factory=list,
        description="Idiomas informados e seus níveis de proficiência",
    )
    links: list[str] = Field(
        default_factory=list,
        description="Links encontrados (LinkedIn, GitHub, portfólio, etc.)",
    )
