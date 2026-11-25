# Job Pilot ✈️

O **Job Pilot** é uma plataforma inteligente para análise de oportunidades profissionais e currículos utilizando **Inteligência Artificial Generativa (Google Gemini)** e **FastAPI**.

O objetivo do projeto é ajudar profissionais a compreenderem os requisitos reais de vagas de emprego, mapearem suas competências e identificarem com precisão as lacunas técnicas (gaps) para se prepararem melhor para processos seletivos.

---

## 🎯 Funcionalidades Principais

- **Análise Estruturada de Vagas:** Recebe a descrição bruta de qualquer vaga de emprego e extrai de forma padronizada: cargo, nível de senioridade, modalidade, requisitos obrigatórios, diferenciais, tecnologias exigidas e pontos de atenção.
- **Processamento de Currículos em PDF:** Realiza o upload e extração de texto de arquivos PDF de currículos preservando as seções originais.
- **Estruturação Semântica do Currículo com IA:** Mapeia e organiza em JSON todas as competências técnicas, histórico de experiências, formação acadêmica, certificações, idiomas e links do candidato.
- **Motor de Compatibilidade (Match & Gaps):** Cruzamento determinístico entre as exigências da vaga e o perfil do candidato, calculando o percentual de aderência e apontando exatamente quais requisitos faltam para a vaga.

---

## 📐 Princípios do Projeto

1. **O LLM extrai e explica; o código decide:** A inteligência artificial é utilizada estritamente para leitura e compreensão semântica de textos não estruturados. Pontuações, métricas e decisões de compatibilidade são calculadas deterministicamente por regras em Python, evitando alucinações.
2. **Fidelidade estrita aos dados:** O sistema nunca inventa, deduz ou completa informações ausentes nem na vaga, nem no currículo.
3. **Arquitetura Limpa:** Separação clara entre camadas de configuração (`core`), modelos de dados (`models`), serviços de negócio/IA (`services`) e endpoints HTTP (`api`).

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.13
- **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/) com documentação interativa automática (Swagger UI)
- **Servidor ASGI:** [Uvicorn](https://www.uvicorn.org/)
- **Modelos de Linguagem (LLM):** [Google Gemini API](https://ai.google.dev/) via SDK oficial `google-genai` (modelo `gemini-3.5-flash`)
- **Validação de Dados:** [Pydantic](https://docs.pydantic.dev/) e `pydantic-settings`
- **Manipulação de Documentos:** `pypdf` e `python-multipart`
- **Banco Vetorial (Planejado para RAG):** `chromadb`

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.13+ instalado
- Git
- Chave de API do Google Gemini ([obter gratuitamente no Google AI Studio](https://aistudio.google.com/))

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Gioomoraes/job-pilot.git
   cd job-pilot/backend
   ```

2. **Crie e ative o ambiente virtual:**
   ```powershell
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   ```powershell
   Copy-Item .env.example .env
   ```
   Abra o arquivo `.env` e adicione sua chave:
   ```env
   GEMINI_API_KEY=sua_chave_do_gemini_aqui
   ```

5. **Inicie o servidor de desenvolvimento:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Acesse a documentação interativa:**
   Abra o navegador em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📁 Estrutura do Projeto

```text
job-pilot/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # Endpoints da API (vagas, currículos, match)
│   │   ├── core/            # Configurações e variáveis de ambiente
│   │   ├── models/          # Esquemas de validação Pydantic
│   │   ├── services/        # Serviços (Gemini, extração de PDF, matching)
│   │   └── main.py          # Ponto de entrada do FastAPI
│   ├── .env.example
│   └── requirements.txt
├── docs/                    # Documentação detalhada e contratos
│   ├── contrato-da-api.md
│   └── escopo.md
└── README.md
```

---

## 📄 Documentação Adicional

- [Escopo do Produto e Roadmap](docs/escopo.md)
- [Contrato da API de Vagas](docs/contrato-da-api.md)
