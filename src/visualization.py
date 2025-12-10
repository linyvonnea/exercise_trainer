# src/visualization.py

import cv2


def form_label(score: float) -> str:
    if score is None:
        return ""
    if score >= 85:
        return "Excellent form"
    if score >= 70:
        return "Good form"
    if score >= 50:
        return "Okay, can improve"
    return "Needs improvement"


def draw_hud(
    frame,
    exercise_name,
    reps,
    feedback,
    form_score=None,
    target_reps=None,
    color=(255, 255, 255),
):
    h, w, _ = frame.shape

    # Top bar background
    cv2.rectangle(frame, (0, 0), (w, 60), (0, 0, 0), -1)

    # Left side: exercise + reps
    cv2.putText(
        frame,
        f"Exercise: {exercise_name}",
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2,
    )
    cv2.putText(
        frame,
        f"Reps: {reps}",
        (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2,
    )

    # Right side: form score + label
    if form_score is not None:
        text = f"Last Form: {form_score:.0f}/100"
        cv2.putText(
            frame,
            text,
            (w - 280, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )
        label = form_label(form_score)
        if label:
            cv2.putText(
                frame,
                label,
                (w - 280, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 200, 255),
                2,
            )

    # Progress bar (if target reps known)
    if target_reps is not None and target_reps > 0:
        bar_x1, bar_y1 = 10, 70
        bar_x2, bar_y2 = w - 10, 90
        cv2.rectangle(frame, (bar_x1, bar_y1), (bar_x2, bar_y2), (80, 80, 80), 2)
        progress = min(1.0, reps / float(target_reps))
        filled_x2 = int(bar_x1 + (bar_x2 - bar_x1) * progress)
        cv2.rectangle(
            frame, (bar_x1 + 2, bar_y1 + 2), (filled_x2 - 2, bar_y2 - 2), (0, 200, 0), -1
        )

    # Bottom feedback bar OR big "no person" text
    if feedback:
        if "No person detected" in feedback:
            # Big centered warning
            cv2.putText(
                frame,
                feedback,
                (int(w * 0.1), int(h * 0.5)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),
                3,
            )
        else:
            cv2.rectangle(frame, (0, h - 60), (w, h), (0, 0, 0), -1)
            cv2.putText(
                frame,
                feedback,
                (10, h - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
            )

    return frame