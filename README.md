# Job Pilot

Plataforma de análise de oportunidades profissionais com IA. O objetivo é analisar descrições de vagas e currículos, identificar compatibilidades e lacunas e recomendar ações de preparação, sempre a partir do conteúdo fornecido, sem inventar informações.

Este é um projeto de portfólio e de estudo, desenvolvido em etapas pequenas e validadas.

## Estado atual

**Etapa 3 concluída (Marco 1: Análise de Vagas com LLM ativa e validada).**

Concluído até aqui:

- Estrutura do repositório e documentação inicial.
- Ambiente Python configurado (Python 3.13).
- Configuração por variáveis de ambiente, validada na inicialização.
- Contrato de dados da análise de vagas ([`docs/contrato-da-api.md`](docs/contrato-da-api.md)).
- API FastAPI criada com validação por Pydantic (`/api/v1/analyze`).
- Integração real com o Google Gemini (`google-genai` com modelo `gemini-3.5-flash`) para extração estruturada de descrições de vagas.
- Documentação interativa via Swagger UI (`/docs`).

Próximo passo: **Etapa 4 (Marco 2)** — Processamento e extração de texto de currículos em PDF.

## Tecnologias

Instaladas e em uso:

- Python 3.13.
- `fastapi` — framework da API REST.
- `uvicorn` — servidor ASGI.
- `pydantic-settings` — configuração validada por variáveis de ambiente.
- `google-genai` — SDK oficial do Gemini para LLM e embeddings.
- `chromadb` — banco de dados vetorial local para RAG (usado a partir da Etapa 6).

A instalar:

- `pypdf` — extração de texto de PDFs (Etapa 4).

## Estrutura do repositório

```text
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       └── jobs.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── job.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── gemini.py
│   ├── .env.example
│   └── requirements.txt
├── docs/
│   ├── contrato-da-api.md
│   └── escopo.md
├── frontend/
├── .gitignore
└── README.md
```

## Como executar

Pré-requisitos: Python 3.13 e Git. Os comandos abaixo usam PowerShell (Windows). Em macOS e Linux, use `python3` no lugar de `python` e ative o ambiente com `source .venv/bin/activate`.

```powershell
git clone https://github.com/Gioomoraes/job-pilot.git
cd job-pilot/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Se o PowerShell bloquear a execução de scripts, rode `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e tente a ativação de novo.

Para validar a configuração:

```powershell
python -c "from app.core.config import get_settings; s = get_settings(); print(s.app_env, s.log_level)"
```

O resultado esperado é `development INFO`. As variáveis aceitas estão documentadas em [`backend/.env.example`](backend/.env.example). O arquivo `.env` não é versionado.

## Documentação

- [`docs/escopo.md`](docs/escopo.md): escopo do produto e roadmap em marcos.
- [`docs/contrato-da-api.md`](docs/contrato-da-api.md): contrato de entrada e saída da análise de vagas.

## Privacidade

No plano gratuito da API do Gemini, os dados enviados podem ser usados pelo provedor para melhorar seus produtos. Não envie dados sensíveis nem informações pessoais de terceiros.