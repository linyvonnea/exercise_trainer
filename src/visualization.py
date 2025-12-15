# src/visualization.py

import cv2
import numpy as np

HEADER_H = 95          # top HUD height
FOOTER_H = 70          # bottom feedback bar height
MARGIN = 12

COLOR_BG = (20, 20, 20)
COLOR_TEXT = (255, 255, 255)
COLOR_ACCENT = (0, 255, 255)
COLOR_WARN = (0, 0, 255)

COLOR_BAR_BORDER = (90, 90, 90)
COLOR_BAR_FILL = (0, 200, 0)


def draw_hud(
    frame,
    exercise_name: str,
    reps: int,
    feedback: str,
    target_reps: int | None = None,
    mode_label: str | None = None,
    color=COLOR_TEXT,
):

    h, w, _ = frame.shape

    # --- header background ---
    cv2.rectangle(frame, (0, 0), (w, HEADER_H), COLOR_BG, -1)

    # --- left header text: exercise + reps ---
    cv2.putText(
        frame,
        f"Exercise: {exercise_name}",
        (MARGIN, 32),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        color,
        2,
    )
    cv2.putText(
        frame,
        f"Reps: {reps}",
        (MARGIN, 68),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        color,
        2,
    )

    # --- right header text: mode label ---
    if mode_label:
        # Right-align by estimating text width
        (tw, th), _ = cv2.getTextSize(mode_label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.putText(
            frame,
            mode_label,
            (w - MARGIN - tw, 32),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            COLOR_TEXT,
            2,
        )

    # --- progress bar  ---
    if target_reps is not None and target_reps > 0:
        bar_x1, bar_y1 = MARGIN, 74
        bar_x2, bar_y2 = w - MARGIN, 92

        # outline
        cv2.rectangle(frame, (bar_x1, bar_y1), (bar_x2, bar_y2), COLOR_BAR_BORDER, 2)

        # fill
        progress = min(1.0, max(0.0, reps / float(target_reps)))
        filled_x2 = int(bar_x1 + (bar_x2 - bar_x1) * progress)

        
        if filled_x2 > bar_x1 + 2:
            cv2.rectangle(
                frame,
                (bar_x1 + 2, bar_y1 + 2),
                (filled_x2 - 2, bar_y2 - 2),
                COLOR_BAR_FILL,
                -1,
            )

        # show "reps/target"
        prog_text = f"{reps}/{target_reps}"
        (ptw, pth), _ = cv2.getTextSize(prog_text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
        cv2.putText(
            frame,
            prog_text,
            (w - MARGIN - ptw, 82),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            COLOR_TEXT,
            2,
        )

    # --- Feedback ---
    if feedback:
        if "No person detected" in feedback:
            # Big centered warning
            (tw, th), _ = cv2.getTextSize(feedback, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 3)
            x = max(MARGIN, (w - tw) // 2)
            y = (h // 2)
            cv2.putText(
                frame,
                feedback,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                COLOR_WARN,
                3,
            )
        else:
            # Footer bar + text
            cv2.rectangle(frame, (0, h - FOOTER_H), (w, h), COLOR_BG, -1)
            cv2.putText(
                frame,
                feedback,
                (MARGIN, h - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                COLOR_ACCENT,
                2,
            )

    return frame


def render_summary_overlay(summary: dict, target_reps: int | None = None, size=None):

    if size is None:
        width, height = 800, 520
    else:
        width, height = size

    frame = np.zeros((height, width, 3), dtype=np.uint8)
    frame[:] = (18, 18, 18)

    # border card
    cv2.rectangle(frame, (20, 20), (width - 20, height - 20), (80, 80, 80), 2)

    lines = [
        "Workout Summary",
        f"Exercise: {summary.get('exercise', 'N/A')}",
        f"Total reps: {summary.get('total_reps', 0)}",
    ]

    if target_reps is not None:
        lines.append(f"Target reps: {target_reps}")

    log_path = summary.get("log_path")
    if log_path:
        lines.append(f"Log saved to: {log_path}")

    lines.append("Press q or Esc to close")

    y = 110
    for i, text in enumerate(lines):
        is_title = (i == 0)
        scale = 1.05 if is_title else 0.85
        color = (0, 255, 255) if is_title else (255, 255, 255)
        thickness = 3 if is_title else 2

        cv2.putText(
            frame,
            text,
            (50, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            scale,
            color,
            thickness,
        )
        y += 55 if is_title else 45

    return frame