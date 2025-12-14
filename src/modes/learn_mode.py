# src/modes/learn_mode.py

import cv2
from pose_detection import PoseDetector
from visualization import draw_hud
from exercises.base import BaseExercise

EXERCISE_TIPS = {
    "Squat": "Feet shoulder-width. Bend knees, keep chest up.",
    "Arm Raise": "Raise both arms overhead. Keep elbows straight.",
    "Side Bend": "Stand tall. Slide hand down leg on one side.",
    "Front Lunge": "Step forward, drop both knees, keep front knee over ankle.",
}


def run_learn_mode(exercise: BaseExercise, camera_index: int = 0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"[Learn Mode] ERROR: Could not open camera index {camera_index}.")
        return 0

    detector = PoseDetector()

    print(f"[Learn Mode] Practicing exercise: {exercise.name}")
    print("Press 'q' to quit.")

    base_tip = EXERCISE_TIPS.get(
        exercise.name, f"Practice controlled movement for {exercise.name}."
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[Learn Mode] Camera frame read failed, exiting.")
            break

        landmarks, annotated = detector.detect(frame, draw=True)
        result = exercise.update(landmarks)

        # Prefer exercise feedback; fall back to tip only if feedback is neutral
        text = result.feedback or base_tip
        if text == "Good form!":
            text = base_tip

        hud = draw_hud(
            annotated,
            f"{exercise.name} (Learn)",
            exercise.reps,
            text,
            target_reps=None,
        )
        cv2.imshow("Learn Mode", hud)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(
        f"[Learn Mode] Finished practice for {exercise.name}. Reps detected: {exercise.reps}"
    )
    return exercise.reps