# src/modes/workout_mode.py

import cv2
from typing import Optional
from pose_detection import PoseDetector
from visualization import draw_hud, render_summary_overlay
from exercises.base import BaseExercise
from audio import play_rep_sound
from .summary_mode import show_summary


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
    last_frame = None

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
            target_reps=target_reps,
        )
        last_frame = hud.copy()
        cv2.imshow("Workout Mode", hud)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        if target_reps is not None and exercise.reps >= target_reps:
            print("Target reps reached!")
            break

    cap.release()

    summary = show_summary(exercise, print_summary=False)

    if last_frame is not None:
        frame_size = (last_frame.shape[1], last_frame.shape[0])
    else:
        frame_size = None

    summary_frame = render_summary_overlay(summary, target_reps=target_reps, size=frame_size)
    cv2.imshow("Workout Mode", summary_frame)

    while True:
        key = cv2.waitKey(0) & 0xFF
        if key in (ord("q"), 27):
            break

    cv2.destroyAllWindows()
    return exercise.reps