# src/exercises/side_bend.py

from typing import Dict, Any
from .base import BaseExercise, ExerciseResult
from angles import torso_tilt_angle
import config
from feedback import combine_feedback


class SideBendExercise(BaseExercise):
    name = "Side Bend"
    required_landmarks = [11, 12, 23, 24]

    def __init__(self):
        super().__init__()
        self.state = "center"  # "center" -> "tilt"

    def update(self, landmarks) -> ExerciseResult:
        fb_msgs = []
        metrics: Dict[str, Any] = {}

        if landmarks is None:
            return ExerciseResult(self.reps, "No person detected", metrics)

        if not self.has_required_landmarks(landmarks):
            return ExerciseResult(self.reps, self.missing_landmarks_feedback(), metrics)

        tilt = torso_tilt_angle(landmarks)
        metrics["torso_tilt"] = tilt

        tilt_amount = abs(tilt)

        # Rep logic: center → tilt past threshold → back to center
        if tilt_amount > config.SIDE_BEND_TILT_THRESHOLD:
            if self.state == "center":
                self.state = "tilt"
                fb_msgs.append("Hold briefly, then return to center.")
        else:
            if self.state == "tilt":
                self.reps += 1
                self.state = "center"
                fb_msgs.append(f"Nice bend! Rep {self.reps}")
                fb_msgs.append("Stand tall, then bend again.")

        stage_instruction = (
            "Slide your hand down your leg to the side." if self.state == "center" else "Return to the starting position."
        )
        fb_msgs.append(stage_instruction)

        feedback = combine_feedback(fb_msgs)
        return ExerciseResult(self.reps, feedback, metrics)