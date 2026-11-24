import io
from pypdf import PdfReader


def extract_text_from_pdf(pdf_bytes: bytes) -> tuple[str, int]:
    """
    Extrai o texto bruto e a quantidade de páginas de um arquivo PDF.

    Args:
        pdf_bytes: Conteúdo binário do arquivo PDF.

    Returns:
        tuple[str, int]: (texto_extraido, total_de_paginas)

    Raises:
        ValueError: Se o arquivo estiver corrompido, protegido por senha ou sem texto legível.
    """
    if not pdf_bytes:
        raise ValueError("O arquivo PDF enviado está vazio.")

    stream = io.BytesIO(pdf_bytes)

    try:
        reader = PdfReader(stream)
    except Exception as exc:
        raise ValueError(f"Não foi possível ler o arquivo como PDF: {exc}") from exc

    if reader.is_encrypted:
        raise ValueError("O arquivo PDF está protegido por senha e não pode ser processado.")

    total_pages = len(reader.pages)
    if total_pages == 0:
        raise ValueError("O arquivo PDF não contém páginas.")

    extracted_pages: list[str] = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            extracted_pages.append(text)

    full_text = "\n\n".join(extracted_pages).strip()

    if not full_text:
        raise ValueError(
            "Nenhum texto pôde ser extraído do PDF. "
            "Certifique-se de que o documento não é uma imagem digitalizada sem OCR."
        )

    return full_text, total_pages
