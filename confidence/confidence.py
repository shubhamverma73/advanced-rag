from statistics import mean, stdev


def check_confidence(ranked_results):

    if not ranked_results:
        return False, []

    scores = [score for _, score in ranked_results]

    # Agar sirf ek hi document hai
    if len(scores) == 1:
        return True, ranked_results

    avg_score = mean(scores)
    std_score = stdev(scores)

    # Dynamic Threshold
    dynamic_threshold = avg_score - (0.75 * std_score)

    filtered = []

    for doc, score in ranked_results:

        if score >= dynamic_threshold:
            filtered.append((doc, score))

    # Safety: kam se kam Top-1 hamesha rahe
    if not filtered:
        filtered.append(ranked_results[0])

    # Debug Report
    print("\n")
    print("=" * 80)
    print("CONFIDENCE REPORT")
    print("=" * 80)
    print(f"Average Score    : {avg_score:.4f}")
    print(f"Std Deviation    : {std_score:.4f}")
    print(f"Dynamic Cutoff   : {dynamic_threshold:.4f}")
    print(f"Selected Chunks  : {len(filtered)}/{len(ranked_results)}")

    return True, filtered