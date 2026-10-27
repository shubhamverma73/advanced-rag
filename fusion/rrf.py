from hybrid_search.retrieval_document import RetrievalDocument


def reciprocal_rank_fusion( vector_results: list[RetrievalDocument], keyword_results: list[RetrievalDocument], k: int = 60, ):

    merged = {}

    # -----------------------------
    # Vector Search
    # -----------------------------
    for rank, doc in enumerate(vector_results, start=1):

        doc.rrf_score += 1 / (k + rank)

        merged[doc.id] = doc

    # -----------------------------
    # Keyword Search
    # -----------------------------
    for rank, doc in enumerate(keyword_results, start=1):

        score = 1 / (k + rank)

        if doc.id in merged:

            merged[doc.id].rrf_score += score
            merged[doc.id].bm25_score = doc.bm25_score

        else:

            doc.rrf_score = score

            merged[doc.id] = doc

    # -----------------------------
    # Set Retriever Type
    # -----------------------------
    for doc in merged.values():

        if doc.vector_score is not None and doc.bm25_score is not None:
            doc.retriever = "hybrid"

        elif doc.vector_score is not None:
            doc.retriever = "vector"

        elif doc.bm25_score is not None:
            doc.retriever = "keyword"

    # -----------------------------
    # Sort by RRF Score
    # -----------------------------
    return sorted(
        merged.values(),
        key=lambda x: x.rrf_score,
        reverse=True,
    )