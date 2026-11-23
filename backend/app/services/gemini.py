from google import genai
from google.genai import types

from app.core.config import get_settings
from app.models.job import JobAnalysis

# ---------------------------------------------------------------------------
# Prompt de extração
# ---------------------------------------------------------------------------
# O prompt instrui o modelo a agir apenas como extrator — sem inventar fatos,
# sem normalizar sinônimos e sem deduzir informações ausentes.
# As regras aqui espelham diretamente os princípios do contrato da API
# definidos em docs/contrato-da-api.md.
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


def analyze_job_description(descricao: str) -> JobAnalysis:
    """
    Envia a descrição da vaga ao Gemini e retorna a análise estruturada.

    Fluxo:
    1. Monta o prompt com as regras de extração + texto da vaga.
    2. Chama a API do Gemini pedindo resposta em JSON com o schema de JobAnalysis.
    3. Converte o JSON retornado em um objeto JobAnalysis validado pelo Pydantic.

    Raises:
        ValueError: se a chave da API não estiver configurada.
        Exception: propaga erros da API do Gemini para o handler da rota.
    """
    settings = get_settings()

    if not settings.gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY não configurada. "
            "Adicione a chave no arquivo backend/.env."
        )

    # Inicializa o cliente com a chave lida de forma segura via SecretStr
    client = genai.Client(
        api_key=settings.gemini_api_key.get_secret_value()
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=_EXTRACTION_PROMPT.format(descricao=descricao),
        config=types.GenerateContentConfig(
            # response_mime_type instrui o Gemini a retornar JSON puro,
            # sem texto adicional nem blocos de código markdown.
            response_mime_type="application/json",
            # response_schema passa o modelo Pydantic para que o Gemini
            # respeite exatamente os campos e tipos definidos no contrato.
            response_schema=JobAnalysis,
        ),
    )

    # model_validate_json valida e converte o JSON retornado pelo Gemini
    # para um objeto JobAnalysis, garantindo que o contrato foi respeitado.
    return JobAnalysis.model_validate_json(response.text)
