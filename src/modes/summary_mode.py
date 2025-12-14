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

    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                ["timestamp", "exercise", "total_reps"]
            )
        writer.writerow(
            [
                datetime.now().isoformat(timespec="seconds"),
                exercise.name,
                exercise.reps,
            ]
        )


def show_summary(exercise: BaseExercise, print_summary: bool = True):
    summary = {
        "exercise": exercise.name,
        "total_reps": exercise.reps,
        "log_path": LOG_PATH,
    }

    if print_summary:
        print("========== Workout Summary ==========")
        print(f"Exercise: {summary['exercise']}")
        print(f"Total reps: {summary['total_reps']}")
        print("Log file:", summary["log_path"])
        print("=====================================")

    append_log(exercise)
    return summary