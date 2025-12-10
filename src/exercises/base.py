# src/exercises/base.py

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class ExerciseResult:
    reps: int
    feedback: str
    form_score: Optional[float] = None  # score for latest rep (0–100)
    raw_metrics: Dict[str, Any] = field(default_factory=dict)


class BaseExercise:
    """Abstract base class for an exercise."""
    name: str = "BaseExercise"

    def __init__(self):
        self.reps: int = 0
        self.state: Optional[str] = None  # e.g., "up", "down"
        self.last_form_score: Optional[float] = None
        self.rep_scores: List[float] = []  # all completed rep scores

    def reset(self):
        self.reps = 0
        self.state = None
        self.last_form_score = None
        self.rep_scores.clear()

    def update(self, landmarks) -> ExerciseResult:
        """Given landmarks for current frame, update state, reps, and feedback.
        Must be implemented by subclasses.
        """
        raise NotImplementedError