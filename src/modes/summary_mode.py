# src/modes/summary_mode.py

import os
import csv
from datetime import datetime
from exercises.base import BaseExercise

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
LOG_PATH = os.path.join(LOG_DIR, "workouts.csv")


def ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def append_log(exercise: BaseExercise):
    ensure_log_dir()
    file_exists = os.path.exists(LOG_PATH) and os.path.getsize(LOG_PATH) > 0

    avg_score = None
    if exercise.rep_scores:
        avg_score = sum(exercise.rep_scores) / len(exercise.rep_scores)

    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                ["timestamp", "exercise", "total_reps", "avg_form_score"]
            )
        writer.writerow(
            [
                datetime.now().isoformat(timespec="seconds"),
                exercise.name,
                exercise.reps,
                f"{avg_score:.1f}" if avg_score is not None else "",
            ]
        )


def show_summary(exercise: BaseExercise):
    print("========== Workout Summary ==========")
    print(f"Exercise: {exercise.name}")
    print(f"Total reps: {exercise.reps}")
    if exercise.rep_scores:
        avg_score = sum(exercise.rep_scores) / len(exercise.rep_scores)
        best = max(exercise.rep_scores)
        worst = min(exercise.rep_scores)
        print(f"Average form score: {avg_score:.1f}/100")
        print(f"Best rep score:     {best:.1f}")
        print(f"Worst rep score:    {worst:.1f}")
    else:
        print("No form scores recorded.")
    print("Log file:", LOG_PATH)
    print("=====================================")

    append_log(exercise)