# src/exercises/__init__.py

from .squat import SquatExercise
from .arm_raise import ArmRaiseExercise
from .side_bend import SideBendExercise

EXERCISE_CLASSES = {
    "squat": SquatExercise,
    "arm_raise": ArmRaiseExercise,
    "side_bend": SideBendExercise,
}

def get_exercise(name: str):
    name = name.lower()
    if name not in EXERCISE_CLASSES:
        raise ValueError(f"Unknown exercise: {name}")
    return EXERCISE_CLASSES[name]()