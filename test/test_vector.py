import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from pinecone import Pinecone

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from hybrid_search.vector_retriever import vector_search

load_dotenv()

query = "What PPE rules are mentioned?"

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

query_vector = embeddings.embed_query(query)

pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.index("simple-rag-md")

results = vector_search( index=index, query_vector=query_vector, top_k=5 )

print("\n")
print("=" * 80)
print("DENSE SEARCH RESULTS")
print("=" * 80)

for i, doc in enumerate(results, start=1):

    print(f"\nRank {i}")
    print(f"Vector Score : {doc.vector_score:.4f}")

    print("-" * 80)

    print(doc.content)

    print("-" * 80)