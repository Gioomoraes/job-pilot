# Escopo do produto

## Objetivo

Ajudar uma pessoa a compreender e comparar descrições de vagas organizando o texto colado em campos estruturados. A análise deve refletir somente o conteúdo fornecido e não pode inventar informações.

## Fluxo previsto

1. A pessoa cola uma descrição de vaga.
2. O frontend envia o texto ao backend.
3. O backend solicita a análise a uma API de LLM seguindo o contrato definido.
4. A resposta estruturada é apresentada à pessoa.

O provedor da API de LLM e o tratamento operacional de suas credenciais ainda precisam ser definidos antes da integração.

## Incluído na primeira versão

- Entrada manual de descrição em texto.
- Extração dos campos definidos no contrato inicial.
- Indicação de ambiguidades, lacunas relevantes e contradições explícitas presentes no texto.
- Representação previsível de dados ausentes.

## Fora da primeira versão

- Login ou gestão de usuários.
- Banco de dados ou persistência de análises.
- RAG ou consulta a bases de conhecimento.
- Importação automática de vagas por URL.
- Enriquecimento com dados externos.

## Princípios da análise

- Usar somente a descrição recebida como fonte de informação.
- Não normalizar sinônimos de senioridade.
- Listar em `tecnologias` todas as tecnologias mencionadas, inclusive as citadas como diferenciais.
- Registrar em `pontos_de_atencao` ambiguidades, lacunas relevantes e contradições explícitas, sem inferir fatos sobre a empresa ou a vaga.
- Não incluir trechos de origem no contrato inicial; rastreabilidade fica para uma evolução futura.
