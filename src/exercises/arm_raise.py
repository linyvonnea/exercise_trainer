# src/exercises/arm_raise.py

from typing import Dict, Any
from .base import BaseExercise, ExerciseResult
from angles import shoulder_angle
import config
from feedback import combine_feedback


class ArmRaiseExercise(BaseExercise):
    name = "Arm Raise"
    required_landmarks = [11, 12, 13, 14, 23, 24]

    def __init__(self):
        super().__init__()
        self.state = "down"

    def update(self, landmarks) -> ExerciseResult:
        fb_msgs = []
        metrics: Dict[str, Any] = {}

        if landmarks is None:
            return ExerciseResult(self.reps, "No person detected", metrics)

        if not self.has_required_landmarks(landmarks):
            return ExerciseResult(self.reps, self.missing_landmarks_feedback(), metrics)

        left_sh = shoulder_angle(landmarks, left=True)
        right_sh = shoulder_angle(landmarks, left=False)

        metrics["left_shoulder_angle"] = left_sh
        metrics["right_shoulder_angle"] = right_sh

        avg_sh_angle = (left_sh + right_sh) / 2.0

        # Rep logic: down → up → down
        if avg_sh_angle > config.ARM_RAISE_UP_THRESHOLD:
            if self.state == "down":
                self.state = "up"
        elif avg_sh_angle < config.ARM_RAISE_DOWN_THRESHOLD:
            if self.state == "up":
                self.reps += 1
                self.state = "down"
                fb_msgs.append(f"Good raise! Rep {self.reps}")

        stage_instruction = (
            "Raise both arms overhead." if self.state == "down" else "Lower your arms to reset for the next rep."
        )
        fb_msgs.append(stage_instruction)

        feedback = combine_feedback(fb_msgs)
        return ExerciseResult(self.reps, feedback, metrics)