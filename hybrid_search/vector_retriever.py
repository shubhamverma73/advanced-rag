from pinecone import Pinecone, DenseVectorQuery
from hybrid_search.retrieval_document import RetrievalDocument

def vector_search(index, query_vector, namespace="default", top_k=5 ):

    response = index.documents.search(
        namespace=namespace,
        top_k=top_k,
        score_by=[
            DenseVectorQuery(
                field="embedding",
                values=query_vector,
            )
        ],
        include_fields=[
            "content"
        ]
    )

    results = []

    for doc in response.matches:

        results.append(
            RetrievalDocument(
                id=doc._id,
                content=doc.content,
                source=getattr(doc, "source", None),
                page=getattr(doc, "page", None),
                vector_score=float(doc.score),
                retriever="vector",
            )
        )

    return results