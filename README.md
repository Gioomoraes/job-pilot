# Analisador de Vagas

Projeto de portfólio para organizar, em JSON, as informações presentes em uma descrição de vaga colada pelo usuário. A análise deve preservar o que o texto diz, indicar lacunas relevantes e não inventar dados.

## Escopo da primeira versão

- Receber uma descrição de vaga em texto.
- Usar uma API de LLM para estruturar as informações de acordo com o contrato em [`docs/contrato-da-api.md`](docs/contrato-da-api.md).
- Apresentar uma resposta estruturada ao usuário.
- Representar informações singulares ausentes com `null` e listas sem itens com `[]`.

Ficam fora da primeira versão: login, banco de dados, RAG e importação automática de links. O sistema não deve consultar fontes externas para completar a descrição.

## Tecnologias planejadas

- Frontend: React + TypeScript.
- Backend: Python + FastAPI.
- Análise: API de LLM; provedor ainda a definir.

## Estrutura inicial

```text
.
├── backend/
│   ├── README.md
│   └── app/
├── docs/
│   ├── contrato-da-api.md
│   └── escopo.md
├── frontend/
│   ├── README.md
│   └── src/
├── .gitignore
└── README.md
```

## Estado atual

Este repositório contém apenas a estrutura e documentação iniciais. A aplicação e as integrações ainda não foram implementadas, e não há comandos de execução configurados.
