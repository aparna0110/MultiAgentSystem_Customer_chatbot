CONFIDENCE_THRESHOLD = 0.6


def route_based_on_confidence(state):
    if state["confidence"] < CONFIDENCE_THRESHOLD:
        return "tier2"
    return "manager"
