from pydantic import BaseModel, Field


class ResumeExtractionResponse(BaseModel):
    """
    Modelo de resposta para o upload e extração de texto de currículo.
    """
    filename: str = Field(..., description="Nome do arquivo enviado")
    tamanho_bytes: int = Field(..., description="Tamanho do arquivo em bytes")
    total_paginas: int = Field(..., description="Número total de páginas do documento")
    texto_extraido: str = Field(..., description="Texto limpo extraído do PDF")
