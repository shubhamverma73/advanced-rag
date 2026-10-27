import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from pinecone import Pinecone

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from hybrid_search.hybrid_retriever import hybrid_search

load_dotenv()

query = "Noise exposure"

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

query_vector = embeddings.embed_query(query)

pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.index("simple-rag-md")

results = hybrid_search( index=index, query=query, query_vector=query_vector )

print("\n")
print("=" * 80)
print("HYBRID RESULTS")
print("=" * 80)

for i, doc in enumerate(results, start=1):

    print(f"\nRank {i}")

    print(f"Retriever    : {doc.retriever}")

    print(f"Vector Score : {doc.vector_score}")

    print(f"BM25 Score   : {doc.bm25_score}")

    print(f"RRF Score    : {doc.rrf_score:.6f}")

    print("-"*80)

    print(doc.content)