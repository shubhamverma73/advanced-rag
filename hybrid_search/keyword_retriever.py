import json
from hybrid_search.retrieval_document import RetrievalDocument
from rank_bm25 import BM25Okapi

def keyword_search(query: str, top_k: int = 5):

    # -----------------------------
    # Load BM25 Corpus
    # -----------------------------
    with open("data/bm25_corpus.json", "r", encoding="utf-8") as file:
        corpus = json.load(file)

    # -----------------------------
    # Tokenize Corpus
    # -----------------------------
    tokenized_corpus = [
        doc["content"].lower().split()
        for doc in corpus
    ]

    # -----------------------------
    # Create BM25 Index
    # -----------------------------
    bm25 = BM25Okapi(tokenized_corpus)

    # -----------------------------
    # Tokenize Query
    # -----------------------------
    tokenized_query = query.lower().split()

    # -----------------------------
    # BM25 Scores
    # -----------------------------
    scores = bm25.get_scores(tokenized_query)

    # -----------------------------
    # Sort Results
    # -----------------------------
    ranked_results = sorted(
        zip(corpus, scores),
        key=lambda x: x[1],
        reverse=True
    )

    # -----------------------------
    # Remove Irrelevant Results
    # -----------------------------
    ranked_results = [
        (doc, score)
        for doc, score in ranked_results
        if score > 0
    ]

    # -----------------------------
    # Convert to RetrievalDocument 
    # -----------------------------
    results = []

    for doc, score in ranked_results[:top_k]:

        results.append(
            RetrievalDocument(
                id=doc["id"],
                content=doc["content"],
                source=doc.get("source"),
                page=doc.get("page"),
                vector_score=None,
                bm25_score=float(score),
                retriever="keyword",
            )
        )

    return results