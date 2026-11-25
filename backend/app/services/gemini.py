from google import genai
from google.genai import types

from app.core.config import get_settings
from app.models.job import JobAnalysis
from app.models.resume import ResumeAnalysis

# ---------------------------------------------------------------------------
# Prompt de extração de vaga
# ---------------------------------------------------------------------------
_EXTRACTION_PROMPT = """\
Você é um assistente especializado em análise de descrições de vagas de emprego.
Sua única função é extrair e organizar as informações presentes no texto recebido.

REGRAS OBRIGATÓRIAS:
- Use apenas as informações presentes no texto. Não invente, complete ou deduza fatos ausentes.
- Use null para campos singulares cuja informação não esteja disponível.
- Use lista vazia [] quando não houver itens daquele tipo no texto.
- Preserve o nível de senioridade exatamente como escrito; não normalize sinônimos.
- Inclua em "tecnologias" todas as tecnologias nomeadas, mesmo as que já aparecem em outros campos.
- Use "pontos_de_atencao" exclusivamente para ambiguidades, lacunas relevantes e contradições \
explícitas presentes no texto — sem inferir fatos sobre a empresa ou a vaga.
- Não acrescente informações obtidas fora da descrição.

DESCRIÇÃO DA VAGA:
{descricao}
"""

# ---------------------------------------------------------------------------
# Prompt de extração de currículo
# ---------------------------------------------------------------------------
_RESUME_EXTRACTION_PROMPT = """\
Você é um assistente especializado em análise e estruturação de currículos profissionais.
Sua única função é extrair e organizar os dados presentes no texto do currículo fornecido.

REGRAS OBRIGATÓRIAS:
- Use apenas as informações presentes no texto. Não invente, complete ou deduza fatos ausentes.
- Use null para campos singulares cuja informação não esteja declarada no texto.
- Use lista vazia [] quando não houver itens daquele tipo no texto.
- Em "competencias_tecnicas", liste todas as linguagens, frameworks, bibliotecas, ferramentas, \
bancos de dados, plataformas de nuvem e metodologias citadas explicitamente no currículo.
- Em "links", inclua URLs ou perfis mencionados (como LinkedIn, GitHub, portfólio).
- Em "experiencias", extraia cargo, empresa, período e a lista de atividades/realizações declaradas.
- Em "formacao", extraia curso, instituição, período e status (ex: "Em andamento", "Concluído").
- Não acrescente informações de fontes externas.

TEXTO DO CURRÍCULO:
{texto}
"""


def _get_gemini_client() -> genai.Client:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY não configurada. "
            "Adicione a chave no arquivo backend/.env."
        )
    return genai.Client(api_key=settings.gemini_api_key.get_secret_value())


def analyze_job_description(descricao: str) -> JobAnalysis:
    """
    Envia a descrição da vaga ao Gemini e retorna a análise estruturada.
    """
    client = _get_gemini_client()

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=_EXTRACTION_PROMPT.format(descricao=descricao),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=JobAnalysis,
        ),
    )

    return JobAnalysis.model_validate_json(response.text)


def analyze_resume_text(texto_curriculo: str) -> ResumeAnalysis:
    """
    Envia o texto bruto do currículo ao Gemini e retorna a estrutura padronizada em JSON.
    """
    client = _get_gemini_client()

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=_RESUME_EXTRACTION_PROMPT.format(texto=texto_curriculo),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ResumeAnalysis,
        ),
    )

    return ResumeAnalysis.model_validate_json(response.text)
