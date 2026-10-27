from sentence_transformers import CrossEncoder

# Model sirf ek baar load hoga
model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(query, matches, top_k=1):
    """
    Re-rank retrieved Pinecone documents.

    Parameters
    ----------
    query : str
        User question

    matches : list
        response.matches from Pinecone

    top_k : int
        Number of best chunks to return

    Returns
    -------
    str
        Final context for LLM
    """

    # ------------------------
    # Prepare (query, chunk) pairs
    # ------------------------

    pairs = [ (query, match.content) for match in matches ]

    # ------------------------
    # CrossEncoder Scores
    # ------------------------

    scores = model.predict(pairs)

    # ------------------------
    # Combine Match + Score
    # ------------------------

    ranked = list(zip(matches, scores))
    ranked.sort(key=lambda x: x[1], reverse=True )

    print("\n")
    print("=" * 80)
    print("AFTER RE-RANKING")
    print("=" * 80)

    for i, (match, score) in enumerate(ranked, start=1):

        print(f"\nRank {i}")
        print(f"CrossEncoder Score : {score:.4f}")

        print("-" * 80)

        print(match.content)

        print("-" * 80)

    # ------------------------
    # Return Top Ranked Documents
    # ------------------------

    return ranked[:top_k]



# Pinecone is used for similarity score
# CrossEncoder is used for relevance score