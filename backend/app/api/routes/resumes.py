from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.models.resume import ResumeAnalysis, ResumeExtractionResponse
from app.services.gemini import analyze_resume_text
from app.services.pdf import extract_text_from_pdf

router = APIRouter()

# Limite de tamanho de arquivo seguro (10 MB)
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024


async def _read_and_validate_pdf(file: UploadFile) -> str:
    """
    Função auxiliar para validar o arquivo e extrair o texto em string.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas arquivos no formato .pdf são aceitos.",
        )

    content = await file.read()
    file_size = len(content)

    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="O arquivo excede o tamanho máximo permitido de 10 MB.",
        )

    try:
        texto, _ = extract_text_from_pdf(content)
        return texto
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.post(
    "/upload",
    response_model=ResumeExtractionResponse,
    summary="Upload e extração de texto de currículo em PDF",
    description=(
        "Recebe um arquivo PDF contendo um currículo, valida o formato e extrai "
        "todo o texto legível das páginas, preparando os dados para posterior análise."
    ),
)
async def upload_resume(
    file: UploadFile = File(..., description="Arquivo PDF do currículo"),
) -> ResumeExtractionResponse:
    """
    Recebe o arquivo de currículo, valida a extensão e tipo MIME e extrai o texto.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas arquivos no formato .pdf são aceitos.",
        )

    content = await file.read()
    file_size = len(content)

    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="O arquivo excede o tamanho máximo permitido de 10 MB.",
        )

    try:
        texto, total_paginas = extract_text_from_pdf(content)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return ResumeExtractionResponse(
        filename=file.filename,
        tamanho_bytes=file_size,
        total_paginas=total_paginas,
        texto_extraido=texto,
    )


@router.post(
    "/analyze",
    response_model=ResumeAnalysis,
    summary="Upload e estruturação completa do currículo via IA",
    description=(
        "Recebe um arquivo PDF de currículo, extrai o texto bruto e utiliza o Gemini "
        "para estruturar todos os dados (experiências, competências, formação, etc.) em JSON."
    ),
)
async def analyze_resume(
    file: UploadFile = File(..., description="Arquivo PDF do currículo"),
) -> ResumeAnalysis:
    """
    Extrai o texto do PDF e envia ao Gemini para análise e estruturação semântica.
    """
    texto = await _read_and_validate_pdf(file)

    try:
        return analyze_resume_text(texto)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro ao chamar a API do Gemini para análise do currículo: {exc}",
        )
