from typing import Dict, Any

from .base import BaseExercise, ExerciseResult
from angles import knee_angle, torso_tilt_angle
import config
from feedback import combine_feedback


class FrontLungeExercise(BaseExercise):
    name = "Front Lunge"
    required_landmarks = [11, 12, 23, 24, 25, 26, 27, 28]

    def __init__(self):
        super().__init__()
        self.state = "up"
        self.lead_leg = "right"  # alternate every rep

    def update(self, landmarks) -> ExerciseResult:
        fb_msgs = []
        metrics: Dict[str, Any] = {}

        if landmarks is None:
            return ExerciseResult(self.reps, "No person detected", metrics)

        if not self.has_required_landmarks(landmarks):
            return ExerciseResult(self.reps, self.missing_landmarks_feedback(), metrics)

        right_knee = knee_angle(landmarks, left=False)
        left_knee = knee_angle(landmarks, left=True)
        torso_tilt = torso_tilt_angle(landmarks)

        metrics["right_knee_angle"] = right_knee
        metrics["left_knee_angle"] = left_knee
        metrics["torso_tilt"] = torso_tilt
        metrics["lead_leg"] = self.lead_leg

        if torso_tilt > 20:
            fb_msgs.append("Keep your chest lifted")

        lead_knee = right_knee if self.lead_leg == "right" else left_knee

        if lead_knee < config.LUNGE_FRONT_KNEE_DOWN_THRESHOLD:
            if self.state == "up":
                self.state = "down"
                fb_msgs.append(
                    f"Hold the {self.lead_leg} lunge, keep front knee over the ankle."
                )
        elif lead_knee > config.LUNGE_FRONT_KNEE_UP_THRESHOLD:
            if self.state == "down":
                completed_leg = self.lead_leg
                self.reps += 1
                self.state = "up"
                fb_msgs.append(f"Strong {completed_leg} lunge! Rep {self.reps}")
                # Alternate legs for the next rep
                self.lead_leg = "left" if completed_leg == "right" else "right"
                fb_msgs.append(f"Next rep: step forward with your {self.lead_leg} leg.")

        stage_instruction = (
            f"Step forward with your {self.lead_leg} leg and bend both knees."
            if self.state == "up"
            else f"Drive through your {self.lead_leg} heel to stand tall."
        )
        fb_msgs.append(stage_instruction)

        feedback = combine_feedback(fb_msgs)
        return ExerciseResult(self.reps, feedback, metrics)
