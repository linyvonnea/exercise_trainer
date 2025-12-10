# src/scoring.py
"""
Simple helpers to turn angles / metrics into 0–100 form scores.
You can tweak the ranges per exercise.
"""

def score_range(value: float, ideal_min: float, ideal_max: float,
                soft_margin: float = 15.0) -> float:
    """
    Score is 100 if value is inside [ideal_min, ideal_max].
    It drops linearly to 0 at (ideal_min - soft_margin) and (ideal_max + soft_margin).
    """
    if ideal_min <= value <= ideal_max:
        return 100.0

    if value < ideal_min - soft_margin or value > ideal_max + soft_margin:
        return 0.0

    if value < ideal_min:
        # value in (ideal_min-soft_margin, ideal_min)
        return 100.0 * (value - (ideal_min - soft_margin)) / soft_margin
    else:
        # value in (ideal_max, ideal_max+soft_margin)
        return 100.0 * ((ideal_max + soft_margin) - value) / soft_margin


def clamp_score(score: float) -> float:
    return max(0.0, min(100.0, score))