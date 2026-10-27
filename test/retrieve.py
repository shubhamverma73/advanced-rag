from langchain_ollama import OllamaEmbeddings
from pinecone import DenseVectorQuery, Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

# -------------------------
# User Question
# -------------------------
query = "What is Python?"

# -------------------------
# Embedding Model
# -------------------------
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

query_vector = embeddings.embed_query(query)

# -------------------------
# Pinecone
# -------------------------
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.index("simple-rag")

# -------------------------
# Search
# -------------------------
response = index.documents.search(
    namespace="default",
    top_k=1,
    score_by=[
        DenseVectorQuery(
            field="embedding",
            values=query_vector
        )
    ],
    include_fields=["content", "page", "source"]
)

# -------------------------
# Print Results
# -------------------------
for i, doc in enumerate(response.matches, start=1):

    print(f"\nResult {i}")
    print(f"Similarity : {doc.score:.3f}")

    print("-"*80)

    print(doc.content)

    print("-"*80)