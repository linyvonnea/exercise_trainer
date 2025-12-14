# src/visualization.py

import cv2
import numpy as np


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


def render_summary_overlay(summary, target_reps=None, size=None):
    if size is None:
        width, height = 640, 480
    else:
        width, height = size

    frame = np.zeros((height, width, 3), dtype=np.uint8)
    frame[:] = (20, 20, 20)

    cv2.rectangle(frame, (15, 15), (width - 15, height - 15), (80, 80, 80), 2)

    lines = [
        "Workout Summary",
        f"Exercise: {summary['exercise']}",
        f"Total reps: {summary['total_reps']}",
    ]

    if target_reps is not None:
        lines.append(f"Target reps: {target_reps}")

    log_path = summary.get("log_path")
    if log_path:
        lines.append(f"Log saved to: {log_path}")

    lines.append("Press q or Esc to close")

    y_start = 100
    line_spacing = 45
    for idx, text in enumerate(lines):
        y = y_start + idx * line_spacing
        cv2.putText(
            frame,
            text,
            (40, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9 if idx == 0 else 0.8,
            (0, 255, 255) if idx == 0 else (255, 255, 255),
            2,
        )

    return frame