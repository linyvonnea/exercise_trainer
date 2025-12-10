# src/exercises/squat.py

from typing import Dict, Any
from .base import BaseExercise, ExerciseResult
from angles import knee_angle, torso_tilt_angle
import config
from feedback import combine_feedback
from scoring import score_range, clamp_score


class SquatExercise(BaseExercise):
    name = "Squat"

    def __init__(self):
        super().__init__()
        self.state = "up"  # "up" or "down"

    def update(self, landmarks) -> ExerciseResult:
        fb_msgs = []
        metrics: Dict[str, Any] = {}

        if landmarks is None:
            return ExerciseResult(self.reps, "No person detected", self.last_form_score, metrics)

        # Use right knee (or left, but be consistent)
        knee = knee_angle(landmarks, left=False)
        torso_tilt = torso_tilt_angle(landmarks)

        metrics["knee_angle"] = knee
        metrics["torso_tilt"] = torso_tilt

        # --- form scoring for this frame ---
        # Knee: ideal 80–110 deg
        knee_score = score_range(knee, ideal_min=80.0, ideal_max=110.0, soft_margin=20.0)
        # Torso tilt: ideal near 0; treat 0–10 as perfect
        # We'll "invert" by mapping tilt to a pseudo-value (smaller is better)
        tilt_score = score_range(max(0.0, 10.0 - abs(torso_tilt)), 0.0, 10.0, soft_margin=10.0)
        frame_form_score = clamp_score(0.7 * knee_score + 0.3 * tilt_score)

        metrics["frame_form_score"] = frame_form_score

        # --- form feedback (not only when rep ends) ---
        if torso_tilt > 20:
            fb_msgs.append("Keep your back more upright")

        # --- rep logic ---
        if knee < config.SQUAT_KNEE_DOWN_THRESHOLD:
            if self.state == "up":
                self.state = "down"

        elif knee > config.SQUAT_KNEE_UP_THRESHOLD:
            if self.state == "down":
                # Rep completed → freeze current frame_form_score as rep score
                self.reps += 1
                self.state = "up"
                self.last_form_score = frame_form_score
                self.rep_scores.append(frame_form_score)
                fb_msgs.append(f"Nice squat! Rep {self.reps} (Form: {frame_form_score:.0f})")

        feedback = combine_feedback(fb_msgs)
        return ExerciseResult(self.reps, feedback, self.last_form_score, metrics)