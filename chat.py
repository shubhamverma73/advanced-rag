from langchain_ollama import OllamaEmbeddings, ChatOllama
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from reranker.reranker import rerank
from confidence.confidence import check_confidence
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from query_rewriter.query_rewriter import expand_query
from hybrid_search.hybrid_retriever import hybrid_search

load_dotenv()

# ---------------------------------
# User Question
# ---------------------------------
query = input("Ask Question: ")

# ---------------------------------
# Embedding Model
# ---------------------------------
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


# ---------------------------------
# Query Expansion
# ---------------------------------
#query_vector = embeddings.embed_query(query)
expanded_query = expand_query(query)
query_vector = embeddings.embed_query(expanded_query)

# ---------------------------------
# Query Expansion Debug
# ---------------------------------
print("\n")
print("=" * 80)
print("QUERY EXPANSION")
print("=" * 80)

print("\nOriginal Query:\n")
print(query)

print("\nExpanded Query:\n")
print(expanded_query)

# ---------------------------------
# Pinecone
# ---------------------------------
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.index("simple-rag-md")


# ---------------------------------
# Hybrid Search
# ---------------------------------
results = hybrid_search( index=index, query=expanded_query, query_vector=query_vector )

# ---------------------------------
# Reranking Results
# ---------------------------------
ranked_docs = rerank(query=expanded_query, matches=results, top_k=3) # Use reranker to get the best context from top 5 matches

# ---------------------------------
# Check Confidence
# ---------------------------------
passed, ranked_docs = check_confidence(ranked_docs)

if not passed:
    print("\nNo relevant information found in the provided documents.")
    exit()

# ---------------------------------
# Context Preparation
# ---------------------------------
# context = response.matches[0].content # Use only the top match
# context = "\n\n".join( match.content for match, score in ranked_docs )
context_text = "\n\n".join( doc.content for doc, score in ranked_docs )

# ---------------------------------
# Final Context Sent To LLM
# ---------------------------------
print("\n")
print("=" * 80)
print("HYBRID SEARCH")
print("=" * 80)

for i, doc in enumerate(results, start=1):

    print(f"\nRank {i}")
    print(f"Retriever    : {doc.retriever}")
    print(f"Vector Score : {doc.vector_score}")
    print(f"BM25 Score   : {doc.bm25_score}")
    print(f"RRF Score    : {doc.rrf_score:.6f}")
    print("-" * 80)
    print(doc.content)
    print("-" * 80)

# ---------------------------------
# Prompt
# ---------------------------------
prompt = f"""
You are a Retrieval QA assistant.

Use ONLY the information present in CONTEXT.

Rules:

- Never use outside knowledge.
- Never assume anything.
- Never summarize.
- Include ALL relevant information found in the context.
- If the context contains multiple points, list every point.
- If the context contains tables, include the relevant table rows.
- Do not omit details.
- If the same information appears multiple times in the retrieved context, include it only once.
- If the answer is unavailable, reply exactly:
"I don't know based on the provided context."

CONTEXT:
{context_text}

QUESTION:
{query}

ANSWER:
"""

# ---------------------------------
# LLM
# ---------------------------------
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

response = llm.invoke(prompt)

print("\n")
print("=" * 80)
print("FINAL ANSWER")
print("=" * 80)
print(response.content)