# src/exercises/side_bend.py

from typing import Dict, Any
from .base import BaseExercise, ExerciseResult
from angles import torso_tilt_angle
import config
from feedback import combine_feedback
from scoring import score_range, clamp_score


class SideBendExercise(BaseExercise):
    name = "Side Bend"

    def __init__(self):
        super().__init__()
        self.state = "center"  # "center" -> "tilt"

    def update(self, landmarks) -> ExerciseResult:
        fb_msgs = []
        metrics: Dict[str, Any] = {}

        if landmarks is None:
            return ExerciseResult(self.reps, "No person detected", self.last_form_score, metrics)

        tilt = torso_tilt_angle(landmarks)
        metrics["torso_tilt"] = tilt

        # Form scoring: we want a noticeable, but controlled, tilt.
        # Let's say ideal is 20–40 degrees of tilt.
        tilt_amount = abs(tilt)
        tilt_score = score_range(tilt_amount, ideal_min=20.0, ideal_max=40.0, soft_margin=15.0)
        frame_form_score = clamp_score(tilt_score)
        metrics["frame_form_score"] = frame_form_score

        # Rep logic: center → tilt past threshold → back to center
        if tilt_amount > config.SIDE_BEND_TILT_THRESHOLD:
            if self.state == "center":
                self.state = "tilt"
                fb_msgs.append("Hold briefly, then return to center.")
        else:
            if self.state == "tilt":
                self.reps += 1
                self.state = "center"
                self.last_form_score = frame_form_score
                self.rep_scores.append(frame_form_score)
                fb_msgs.append(f"Nice bend! Rep {self.reps} (Form: {frame_form_score:.0f})")
                fb_msgs.append("Stand tall, then bend again.")

        feedback = combine_feedback(fb_msgs)
        return ExerciseResult(self.reps, feedback, self.last_form_score, metrics)