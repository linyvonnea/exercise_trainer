# src/ui/menu.py

import cv2
import numpy as np


class Button:
    def __init__(self, x1, y1, x2, y2, text, key):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.text = text
        self.key = key

    def contains(self, x, y):
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

    def draw(self, frame, active=False):
        # highlight active buttons
        border = (0, 255, 255) if active else (255, 255, 255)
        cv2.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2), border, 2)
        cv2.putText(
            frame,
            self.text,
            (self.x1 + 15, self.y1 + 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.85,
            border,
            2,
        )


def run_menu(exercise_keys):
    clicked = {"key": None}

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            for b in param:
                if b.contains(x, y):
                    clicked["key"] = b.key

    W, H = 900, 560
    window = "Exercise Trainer - Menu"
    cv2.namedWindow(window)

    buttons = []

    # --- exercise buttons (left) ---
    x1, x2 = 40, 420
    y = 110
    for k in exercise_keys:
        buttons.append(Button(x1, y, x2, y + 60, k, f"ex:{k}"))
        y += 75

    # --- mode buttons (right) ---
    buttons.append(Button(480, 150, 860, 210, "LEARN MODE", "mode:learn"))
    buttons.append(Button(480, 240, 860, 300, "WORKOUT MODE", "mode:workout"))

    # --- target reps controls (right, lower) ---
    buttons.append(Button(480, 330, 560, 390, "-", "reps:minus"))
    buttons.append(Button(780, 330, 860, 390, "+", "reps:plus"))
    buttons.append(Button(580, 330, 760, 390, "UNLIMITED", "reps:unlimited"))

    # --- start button ---
    buttons.append(Button(480, 430, 860, 500, "START", "start"))

    cv2.setMouseCallback(window, on_mouse, buttons)

    chosen = {"exercise": None, "mode": None, "target_reps": 10, "unlimited": False}

    def clamp_reps(n: int) -> int:
        return max(1, min(200, n))  # keep it sensible for demos

    while True:
        frame = np.zeros((H, W, 3), dtype=np.uint8)
        frame[:] = (18, 18, 18)

        cv2.putText(
            frame, "EXERCISE TRAINER", (40, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 3
        )

        cv2.putText(
            frame, "Choose Exercise", (40, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2
        )
        cv2.putText(
            frame, "Choose Mode", (480, 120),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2
        )

        # target reps label
        cv2.putText(
            frame, "Target Reps (Workout)", (480, 325),
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2
        )

        # draw all buttons
        for b in buttons:
            if b.key.startswith("mode:"):
                b.draw(frame, active=(chosen["mode"] == b.key.split("mode:")[1]))
            elif b.key == "reps:unlimited":
                b.draw(frame, active=chosen["unlimited"])
            else:
                b.draw(frame)

        # show current selections
        cv2.putText(
            frame, f"Selected exercise: {chosen['exercise']}", (40, 525),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
        )
        cv2.putText(
            frame, f"Selected mode: {chosen['mode']}", (480, 525),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
        )

        # Show reps value in the middle box
        reps_display = "Unlimited" if chosen["unlimited"] else str(chosen["target_reps"])
        cv2.putText(
            frame, reps_display, (635, 375),
            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3
        )

        key = clicked["key"]
        if key:
            if key.startswith("ex:"):
                chosen["exercise"] = key.split("ex:")[1]

            elif key.startswith("mode:"):
                chosen["mode"] = key.split("mode:")[1]
                # Unlimited reps makes sense only in workout; keep it but harmless in learn

            elif key == "reps:minus":
                if not chosen["unlimited"]:
                    chosen["target_reps"] = clamp_reps(chosen["target_reps"] - 1)

            elif key == "reps:plus":
                if not chosen["unlimited"]:
                    chosen["target_reps"] = clamp_reps(chosen["target_reps"] + 1)

            elif key == "reps:unlimited":
                chosen["unlimited"] = not chosen["unlimited"]

            elif key == "start":
                if chosen["exercise"] and chosen["mode"]:
                    break

            clicked["key"] = None

        cv2.imshow(window, frame)
        k = cv2.waitKey(16) & 0xFF
        if k in (ord("q"), 27):  # q or ESC
            chosen = {"exercise": None, "mode": None, "target_reps": 10, "unlimited": False}
            break

    cv2.destroyWindow(window)

    # finalize target reps
    if chosen["unlimited"]:
        chosen["target_reps"] = None

    return chosen