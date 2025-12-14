# src/exercises/base.py

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

import numpy as np


@dataclass
class ExerciseResult:
    reps: int
    feedback: str
    raw_metrics: Dict[str, Any] = field(default_factory=dict)


class BaseExercise:
    """Abstract base class for an exercise."""
    name: str = "BaseExercise"
    required_landmarks: List[int] = []
    visibility_threshold: float = 0.5

    def __init__(self):
        self.reps: int = 0
        self.state: Optional[str] = None  # e.g., "up", "down"

    def reset(self):
        self.reps = 0
        self.state = None

    def has_required_landmarks(self, landmarks) -> bool:
        """Return True only if all required landmarks have visibility >= threshold."""
        if landmarks is None:
            return False
        if not self.required_landmarks:
            return True
        if landmarks.shape[1] <= 3:
            # No visibility info (legacy input) → assume visible
            return True
        if landmarks.shape[0] <= max(self.required_landmarks):
            return False
        vis = landmarks[self.required_landmarks, 3]
        return bool(np.all(vis >= self.visibility_threshold))

    def missing_landmarks_feedback(self) -> str:
        return "Move so the camera sees all needed joints."

    def update(self, landmarks) -> ExerciseResult:
        """Given landmarks for current frame, update state, reps, and feedback.
        Must be implemented by subclasses.
        """
        raise NotImplementedError