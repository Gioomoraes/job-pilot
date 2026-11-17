# Escopo do produto

## Visão geral

O Job Pilot é uma plataforma de análise de oportunidades profissionais com agentes de IA. Ele analisa descrições de vagas e currículos, identifica compatibilidades e lacunas e recomenda ações de preparação. Toda análise deve refletir somente o conteúdo fornecido e não pode inventar informações.

## Roadmap

| Marco | Entrega | Etapas do plano |
|---|---|---|
| 1 | Análise de vaga em texto (extração estruturada) | 1 a 3 |
| 2 | Processamento de currículos em PDF | 4 |
| 3 | Compatibilidade com pontuação determinística | 5 |
| 4 | Base de conhecimento (RAG) e recomendações de estudo | 6 |
| 5 | Agente com LangGraph e ferramentas | 7 |
| 6 | Persistência, testes, segurança e Docker | 8 a 11 |
| Evolução | Frontend, autenticação, comparação de vagas, deploy | 12 |

Cada marco só começa depois que o anterior foi validado.

## Marco 1: análise de vaga em texto

### Objetivo

Ajudar uma pessoa a compreender e comparar descrições de vagas, organizando o texto colado em campos estruturados.

### Fluxo previsto

1. A pessoa cola uma descrição de vaga.
2. O cliente (inicialmente a documentação interativa da API; interface própria em marco posterior) envia o texto ao backend.
3. O backend solicita a análise a uma API de LLM seguindo o contrato definido.
4. A resposta estruturada é apresentada à pessoa.

### Incluído

- Entrada manual de descrição em texto.
- Extração dos campos definidos no contrato inicial.
- Indicação de ambiguidades, lacunas relevantes e contradições explícitas presentes no texto.
- Representação previsível de dados ausentes.

### Fica para marcos posteriores

- Currículos e comparação com vagas (Marcos 2 e 3).
- RAG e recomendações de estudo (Marco 4).
- Agente com ferramentas (Marco 5).
- Banco de dados e persistência de análises (Marco 6).
- Interface própria, login e gestão de usuários (Evolução).
- Importação automática de vagas por URL e enriquecimento com dados externos, que não dependem de scraping na primeira versão (Evolução).

## Princípios da análise

- Usar somente a descrição recebida como fonte de informação.
- Não normalizar sinônimos de senioridade.
- Listar em `tecnologias` todas as tecnologias mencionadas, inclusive as citadas como diferenciais.
- Registrar em `pontos_de_atencao` ambiguidades, lacunas relevantes e contradições explícitas, sem inferir fatos sobre a empresa ou a vaga.
- Não incluir trechos de origem no contrato inicial; rastreabilidade fica para uma evolução futura.

## Princípios gerais do projeto

- O LLM extrai e explica; o código decide. Pontuações são calculadas por regras explícitas, nunca pelo modelo.
- Currículos e descrições de vagas são dados não confiáveis, nunca instruções para o agente.
- Dados sensíveis não são enviados ao provedor de LLM enquanto o plano gratuito estiver em uso.