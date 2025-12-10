# src/modes/workout_mode.py

import cv2
from typing import Optional
from pose_detection import PoseDetector
from visualization import draw_hud
from exercises.base import BaseExercise
from audio import play_rep_sound


def run_workout_mode(
    exercise: BaseExercise,
    camera_index: int = 0,
    target_reps: Optional[int] = None,
):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"[Workout Mode] ERROR: Could not open camera index {camera_index}.")
        return 0

    detector = PoseDetector()

    print(f"[Workout Mode] Starting exercise: {exercise.name}")
    if target_reps is not None:
        print(f"Target reps: {target_reps}")
    print("Press 'q' to quit.")

    prev_reps = exercise.reps

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[Workout Mode] Camera frame read failed, exiting.")
            break

        landmarks, annotated = detector.detect(frame, draw=True)
        result = exercise.update(landmarks)

        # Play sound when a new rep is completed
        if exercise.reps > prev_reps:
            play_rep_sound()
            prev_reps = exercise.reps

        hud = draw_hud(
            annotated,
            exercise.name,
            result.reps,
            result.feedback,
            form_score=result.form_score,
            target_reps=target_reps,
        )
        cv2.imshow("Workout Mode", hud)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        if target_reps is not None and exercise.reps >= target_reps:
            print("Target reps reached!")
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"[Workout Mode] Finished {exercise.name}. Total reps: {exercise.reps}")
    return exercise.reps