from dataclasses import dataclass

@dataclass
class RetrievalDocument:

    id: str
    content: str

    source: str | None = None
    page: int | None = None

    vector_score: float | None = None
    bm25_score: float | None = None

    retriever: str = ""
    cross_score: float | None = None
    rrf_score: float = 0.0