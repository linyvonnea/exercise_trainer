from typing import Dict, Any

from .base import BaseExercise, ExerciseResult
from angles import knee_angle, torso_tilt_angle
import config
from feedback import combine_feedback


class FrontLungeExercise(BaseExercise):
    name = "Front Lunge"
    required_landmarks = [11, 12, 23, 24, 26, 28]

    def __init__(self):
        super().__init__()
        self.state = "up"

    def update(self, landmarks) -> ExerciseResult:
        fb_msgs = []
        metrics: Dict[str, Any] = {}

        if landmarks is None:
            return ExerciseResult(self.reps, "No person detected", metrics)

        if not self.has_required_landmarks(landmarks):
            return ExerciseResult(self.reps, self.missing_landmarks_feedback(), metrics)

        front_knee = knee_angle(landmarks, left=False)
        torso_tilt = torso_tilt_angle(landmarks)

        metrics["front_knee_angle"] = front_knee
        metrics["torso_tilt"] = torso_tilt

        if torso_tilt > 20:
            fb_msgs.append("Keep your chest lifted")

        if front_knee < config.LUNGE_FRONT_KNEE_DOWN_THRESHOLD:
            if self.state == "up":
                self.state = "down"
                fb_msgs.append("Hold the lunge, keep front knee over ankle.")
        elif front_knee > config.LUNGE_FRONT_KNEE_UP_THRESHOLD:
            if self.state == "down":
                self.reps += 1
                self.state = "up"
                fb_msgs.append(f"Strong lunge! Rep {self.reps}")

        stage_instruction = (
            "Step forward and bend both knees." if self.state == "up" else "Drive through the front heel to stand tall."
        )
        fb_msgs.append(stage_instruction)

        feedback = combine_feedback(fb_msgs)
        return ExerciseResult(self.reps, feedback, metrics)
