def evaluate_collaboration(results):
    false_escalations = [
        r for r in results
        if r["tier2_used"] and r["confidence"] > 0.7
    ]

    print("False escalations:", len(false_escalations))
