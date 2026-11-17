# Job Pilot

Plataforma de análise de oportunidades profissionais com agentes de IA. O objetivo é analisar descrições de vagas e currículos, identificar compatibilidades e lacunas e recomendar ações de preparação, sempre a partir do conteúdo fornecido, sem inventar informações.

Este é um projeto de portfólio e de estudo, desenvolvido em etapas pequenas e validadas.

## Estado atual

**Etapa 1 concluída (estrutura do projeto).**

Existe hoje:

- Estrutura do repositório e documentação inicial.
- Ambiente Python configurado (Python 3.13).
- Configuração por variáveis de ambiente, validada na inicialização.
- Contrato de dados da análise de vagas ([`docs/contrato-da-api.md`](docs/contrato-da-api.md)).

Ainda **não** existe: API, integração com LLM, processamento de currículos, base de conhecimento (RAG) ou agente. O que está planejado, e em qual ordem, está em [`docs/escopo.md`](docs/escopo.md).

## Tecnologias

Em uso:

- Python 3.13.
- pydantic-settings, para configuração validada.

Planejadas (entram na etapa em que forem usadas): FastAPI, Google Gemini (plano gratuito da API), ChromaDB, LangChain e LangGraph. Cada dependência só é registrada em `backend/requirements.txt` depois de instalada.

## Estrutura do repositório

```text
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── core/
│   │       ├── __init__.py
│   │       └── config.py
│   ├── .env.example
│   └── requirements.txt
├── docs/
│   ├── contrato-da-api.md
│   └── escopo.md
├── .gitignore
└── README.md
```

## Como executar

Pré-requisitos: Python 3.13 e Git. Os comandos abaixo usam PowerShell (Windows). Em macOS e Linux, use `python3` no lugar de `python` e ative o ambiente com `source .venv/bin/activate`.

```powershell
git clone https://github.com/Gioomoraes/prisma-agent.git
cd prisma-agent/backend
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