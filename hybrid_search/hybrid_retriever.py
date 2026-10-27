from hybrid_search.vector_retriever import vector_search
from hybrid_search.keyword_retriever import keyword_search
from fusion.rrf import reciprocal_rank_fusion


def hybrid_search( index, query, query_vector, namespace="default", vector_top_k=5, keyword_top_k=5 ):

    # -----------------------------
    # Vector Search
    # -----------------------------
    vector_results = vector_search(
        index=index,
        query_vector=query_vector,
        namespace=namespace,
        top_k=vector_top_k,
    )

    # -----------------------------
    # Keyword Search
    # -----------------------------
    keyword_results = keyword_search(
        query=query,
        top_k=keyword_top_k,
    )

    # -----------------------------
    # Merge Results
    # -----------------------------
    results = reciprocal_rank_fusion(
        vector_results=vector_results,
        keyword_results=keyword_results,
    )

    return results