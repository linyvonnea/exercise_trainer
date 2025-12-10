# src/exercises/arm_raise.py

from typing import Dict, Any
from .base import BaseExercise, ExerciseResult
from angles import shoulder_angle
import config
from feedback import combine_feedback
from scoring import score_range, clamp_score


class ArmRaiseExercise(BaseExercise):
    name = "Arm Raise"

    def __init__(self):
        super().__init__()
        self.state = "down"

    def update(self, landmarks) -> ExerciseResult:
        fb_msgs = []
        metrics: Dict[str, Any] = {}

        if landmarks is None:
            return ExerciseResult(self.reps, "No person detected", self.last_form_score, metrics)

        left_sh = shoulder_angle(landmarks, left=True)
        right_sh = shoulder_angle(landmarks, left=False)

        metrics["left_shoulder_angle"] = left_sh
        metrics["right_shoulder_angle"] = right_sh

        avg_sh_angle = (left_sh + right_sh) / 2.0

        # Form scoring: want arms roughly overhead, say 150–180
        angle_score = score_range(avg_sh_angle, ideal_min=150.0, ideal_max=180.0, soft_margin=20.0)
        frame_form_score = clamp_score(angle_score)
        metrics["frame_form_score"] = frame_form_score

        # Rep logic: down → up → down
        if avg_sh_angle > config.ARM_RAISE_UP_THRESHOLD:
            if self.state == "down":
                self.state = "up"
        elif avg_sh_angle < config.ARM_RAISE_DOWN_THRESHOLD:
            if self.state == "up":
                self.reps += 1
                self.state = "down"
                self.last_form_score = frame_form_score
                self.rep_scores.append(frame_form_score)
                fb_msgs.append(f"Good raise! Rep {self.reps} (Form: {frame_form_score:.0f})")

        feedback = combine_feedback(fb_msgs)
        return ExerciseResult(self.reps, feedback, self.last_form_score, metrics)