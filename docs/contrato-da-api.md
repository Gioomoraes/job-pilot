# Contrato inicial da análise de vagas

## Objetivo

Receber uma descrição de vaga em texto e organizar apenas as informações presentes nela. A análise não deve inventar, completar ou deduzir fatos ausentes.

## Entrada

```json
{
  "descricao": "Texto integral da descrição da vaga"
}
```

`descricao` é o texto fornecido pelo usuário.

## Saída

```json
{
  "cargo": null,
  "empresa": null,
  "nivel": null,
  "modalidade": null,
  "localizacao": null,
  "responsabilidades": [],
  "requisitos_obrigatorios": [],
  "diferenciais": [],
  "tecnologias": [],
  "beneficios": [],
  "pontos_de_atencao": []
}
```

## Campos

| Campo | Tipo | Significado |
|---|---|---|
| `cargo` | string ou `null` | Título da posição, conforme aparece na descrição. |
| `empresa` | string ou `null` | Nome da empresa, se informado. |
| `nivel` | string ou `null` | Senioridade conforme aparece na descrição, sem normalizar sinônimos. |
| `modalidade` | string ou `null` | Regime de trabalho explicitamente indicado, como remoto, presencial ou híbrido. |
| `localizacao` | string ou `null` | Localização explicitamente informada, como cidade, estado ou país. |
| `responsabilidades` | lista de strings | Atividades e atribuições descritas para a função. |
| `requisitos_obrigatorios` | lista de strings | Requisitos apresentados como necessários ou obrigatórios. |
| `diferenciais` | lista de strings | Qualificações apresentadas como desejáveis, diferenciais ou equivalentes. |
| `tecnologias` | lista de strings | Todas as tecnologias citadas na descrição, inclusive as citadas como diferenciais. |
| `beneficios` | lista de strings | Benefícios explicitamente oferecidos. |
| `pontos_de_atencao` | lista de strings | Ambiguidades, lacunas relevantes e contradições explícitas na descrição, sem inferir fatos sobre a empresa ou a vaga. |

## Informações ausentes

Use `null` para um campo singular cuja informação não esteja disponível. Use uma lista vazia (`[]`) quando não houver itens daquele tipo no texto. Não use expressões como `"não informado"` e não deduza informações com base em contexto externo ou suposições.

## Regras de extração

- Preserve o nível de senioridade conforme escrito; não normalize sinônimos.
- Inclua em `tecnologias` todas as tecnologias nomeadas, ainda que também apareçam em `diferenciais`.
- Use `pontos_de_atencao` para ambiguidades, lacunas relevantes e contradições explícitas.
- Não inclua trechos de origem nesta versão do contrato.
- Não acrescente fatos obtidos fora da descrição.

## Exemplo

### Entrada

```json
{
  "descricao": "Pessoa Desenvolvedora Backend Pleno — Acme Tecnologia. Modelo híbrido em São Paulo, SP. Você desenvolverá e manterá APIs e participará de revisões de código. Requisitos: experiência com Python e PostgreSQL. É um diferencial conhecer AWS. Oferecemos vale-refeição e plano de saúde."
}
```

### Saída

```json
{
  "cargo": "Pessoa Desenvolvedora Backend",
  "empresa": "Acme Tecnologia",
  "nivel": "Pleno",
  "modalidade": "Híbrido",
  "localizacao": "São Paulo, SP",
  "responsabilidades": [
    "Desenvolver e manter APIs",
    "Participar de revisões de código"
  ],
  "requisitos_obrigatorios": [
    "Experiência com Python",
    "Experiência com PostgreSQL"
  ],
  "diferenciais": [
    "Conhecimento de AWS"
  ],
  "tecnologias": [
    "Python",
    "PostgreSQL",
    "AWS"
  ],
  "beneficios": [
    "Vale-refeição",
    "Plano de saúde"
  ],
  "pontos_de_atencao": [
    "A descrição informa que o modelo é híbrido, mas não especifica a frequência presencial."
  ]
}
```

## Decisões tomadas

- Provedor: Google Gemini, começando pelo plano gratuito da API. O modelo exato será definido na integração (Etapa 3).
- Restrição de privacidade: no plano gratuito, os dados enviados podem ser usados pelo Google para melhorar seus produtos. Não enviar dados sensíveis nem informações pessoais de terceiros.

## Decisões ainda pendentes

- Rota HTTP e formato de erros da API (Etapa 2).
- Tratamento de competências comportamentais, hoje não separadas das técnicas (Etapa 3).