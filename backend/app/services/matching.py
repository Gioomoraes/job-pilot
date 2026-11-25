import re
import unicodedata

from app.models.job import JobAnalysis
from app.models.matching import MatchResult
from app.models.resume import ResumeAnalysis


def _clean_str(text: str) -> str:
    """
    Normaliza a string: minúsculas, sem acentos e sem pontuação excessiva.
    """
    text = text.lower()
    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")
    return re.sub(r"[^\w\s\+/\.#-]", " ", text).strip()


# Equivalências comuns para match de termos técnicos
_SYNONYMS = {
    "postgres": "postgresql",
    "pgsql": "postgresql",
    "js": "javascript",
    "ts": "typescript",
    "reactjs": "react",
    "react.js": "react",
    "nodejs": "node.js",
    "node": "node.js",
    "rest": "apis rest",
    "api rest": "apis rest",
    "rest api": "apis rest",
    "restful": "apis rest",
}


def _build_candidate_corpus(curriculo: ResumeAnalysis) -> tuple[set[str], str]:
    """
    Gera o conjunto de competências explícitas e um texto unificado
    com todo o repertório do candidato (resumo, experiências, certificações).
    """
    terms: set[str] = set()

    for skill in curriculo.competencias_tecnicas:
        clean = _clean_str(skill)
        terms.add(clean)
        if clean in _SYNONYMS:
            terms.add(_SYNONYMS[clean])

    corpus_parts = [
        curriculo.resumo or "",
        curriculo.titulo_profissional or "",
        " ".join(curriculo.competencias_tecnicas),
        " ".join(curriculo.certificacoes),
    ]

    for exp in curriculo.experiencias:
        corpus_parts.append(exp.cargo)
        corpus_parts.extend(exp.descricao)

    corpus = _clean_str(" ".join(corpus_parts))
    return terms, corpus


def _is_matched(item: str, candidate_terms: set[str], candidate_corpus: str) -> bool:
    """
    Verifica de forma determinística se um requisito ou tecnologia da vaga
    está presente no perfil do candidato.
    """
    clean_item = _clean_str(item)

    if not clean_item:
        return False

    # 1. Checagem direta no conjunto de termos de competências
    if clean_item in candidate_terms:
        return True

    synonym = _SYNONYMS.get(clean_item)
    if synonym and synonym in candidate_terms:
        return True

    # 2. Busca exata de palavra/expressão no texto do currículo
    pattern = rf"(?<!\w){re.escape(clean_item)}(?!\w)"
    if re.search(pattern, candidate_corpus):
        return True

    # 3. Se for uma frase de requisito (ex: "experiência com Python e PostgreSQL"),
    # verifica se os termos-chave técnicos da frase estão no currículo
    words = [w for w in clean_item.split() if len(w) > 2]
    matched_words = [w for w in words if w in candidate_terms or re.search(rf"(?<!\w){re.escape(w)}(?!\w)", candidate_corpus)]

    # Se a maioria das palavras técnicas do requisito foi atendida
    if words and len(matched_words) == len(words):
        return True

    return False


def calculate_match(vaga: JobAnalysis, curriculo: ResumeAnalysis) -> MatchResult:
    """
    Calcula a compatibilidade entre uma vaga e um currículo de forma 100% determinística.

    Regras:
    - Requisitos obrigatórios e tecnologias essenciais compõem 75% da nota.
    - Diferenciais compõem 25% da nota.
    - A pontuação varia de 0.0 a 100.0%.
    """
    candidate_terms, candidate_corpus = _build_candidate_corpus(curriculo)

    # Coleta os requisitos essenciais (obrigatorios + tecnologias não diferenciais)
    diferenciais_set = {_clean_str(d) for d in vaga.diferenciais}
    essential_items: list[str] = []

    for req in vaga.requisitos_obrigatorios:
        if req not in essential_items:
            essential_items.append(req)

    for tech in vaga.tecnologias:
        if _clean_str(tech) not in diferenciais_set and tech not in essential_items:
            essential_items.append(tech)

    desirable_items = [d for d in vaga.diferenciais if d]

    # Avaliação dos requisitos essenciais
    skills_atendidas: list[str] = []
    gaps_obrigatorios: list[str] = []

    for item in essential_items:
        if _is_matched(item, candidate_terms, candidate_corpus):
            skills_atendidas.append(item)
        else:
            gaps_obrigatorios.append(item)

    # Avaliação dos diferenciais
    diferenciais_atendidos: list[str] = []
    gaps_diferenciais: list[str] = []

    for item in desirable_items:
        if _is_matched(item, candidate_terms, candidate_corpus):
            skills_atendidas.append(f"{item} (Diferencial)")
            diferenciais_atendidos.append(item)
        else:
            gaps_diferenciais.append(item)

    total_analisados = len(essential_items) + len(desirable_items)

    # Cálculo da pontuação
    if essential_items:
        peso_essencial = 75.0 if desirable_items else 100.0
        peso_desejavel = 25.0 if desirable_items else 0.0

        pct_essencial = len(skills_atendidas) / len(essential_items)
        score_essencial = min(pct_essencial, 1.0) * peso_essencial

        score_desejavel = 0.0
        if desirable_items:
            pct_desejavel = len(diferenciais_atendidos) / len(desirable_items)
            score_desejavel = min(pct_desejavel, 1.0) * peso_desejavel

        pontuacao = round(score_essencial + score_desejavel, 1)
    elif desirable_items:
        pct_desejavel = len(diferenciais_atendidos) / len(desirable_items)
        pontuacao = round(pct_desejavel * 100.0, 1)
    else:
        pontuacao = 100.0

    # Classificação do nível de aderência
    if pontuacao >= 75.0:
        nivel = "Alta"
        resumo = (
            f"Alta compatibilidade técnica ({pontuacao}%). O perfil atende à maioria dos "
            f"requisitos obrigatórios da vaga."
        )
    elif pontuacao >= 50.0:
        nivel = "Média"
        resumo = (
            f"Compatibilidade média ({pontuacao}%). O candidato possui parte das competências "
            f"exigidas, mas há lacunas importantes a desenvolver."
        )
    else:
        nivel = "Baixa"
        resumo = (
            f"Compatibilidade baixa ({pontuacao}%). Há uma quantidade expressiva de requisitos "
            f"obrigatórios não identificados no currículo."
        )

    return MatchResult(
        pontuacao_total=min(pontuacao, 100.0),
        nivel_aderencia=nivel,
        total_requisitos_analisados=total_analisados,
        skills_atendidas=skills_atendidas,
        gaps_obrigatorios=gaps_obrigatorios,
        gaps_diferenciais=gaps_diferenciais,
        resumo_aderencia=resumo,
    )
