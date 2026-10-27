import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from hybrid_search.keyword_retriever import keyword_search

results = keyword_search(
    query="What PPE rules are mentioned?",
    top_k=5
)

print("\n")
print("=" * 80)
print("BM25 RESULTS")
print("=" * 80)

for i, doc in enumerate(results, start=1):

    print(f"\nRank {i}")
    print(f"BM25 Score : {doc.bm25_score:.4f}")

    print("-" * 80)

    print(doc.content)

    print("-" * 80)