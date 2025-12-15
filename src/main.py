# src/main.py

from exercises import get_exercise, EXERCISE_CLASSES
from modes import run_learn_mode, run_workout_mode, show_summary

USE_GUI_MENU = True

EXERCISE_INFO = {
    "squat": {
        "title": "Squat",
        "description": "Lower-body strength exercise. Bend knees and hips while keeping your chest up.",
    },
    "arm_raise": {
        "title": "Arm Raise",
        "description": "Shoulder mobility and strength. Raise both arms overhead with straight elbows.",
    },
    "side_bend": {
        "title": "Side Bend",
        "description": "Lateral flexibility exercise. Bend sideways at the waist while staying tall.",
    },
    "front_lunge": {
        "title": "Front Lunge",
        "description": "Lower-body strength exercise. Step forward, drop into a right-leg lunge, and return to standing.",
    },
}


def choose_exercise() -> str:
    print("Choose exercise:")
    keys = list(EXERCISE_CLASSES.keys())
    for i, key in enumerate(keys, start=1):
        title = EXERCISE_INFO.get(key, {}).get("title", key)
        print(f"{i}. {title} ({key})")

    choice = input("Enter number: ").strip()
    try:
        idx = int(choice) - 1
        return keys[idx]
    except Exception:
        print("Invalid choice, defaulting to 'squat'.")
        return "squat"


def choose_mode() -> str:
    print("\nChoose mode:")
    print("1. Learn Mode")
    print("2. Workout Mode")
    choice = input("Enter number: ").strip()

    if choice == "1":
        return "learn"
    if choice == "2":
        return "workout"

    print("Invalid choice, defaulting to Workout Mode.")
    return "workout"


def show_exercise_info(exercise_key: str, mode: str, pause: bool = True):
    info = EXERCISE_INFO.get(exercise_key, {})
    title = info.get("title", exercise_key)
    desc = info.get("description", "")

    print("\n========== Exercise Info ==========")
    print(f"Exercise: {title} ({exercise_key})")
    if desc:
        print("Description:", desc)
    print(f"Mode: {mode.capitalize()} Mode")
    print("Controls: Press 'q' in the video window to quit.")
    print("===================================")

    if pause:
        input("Press Enter to start...")


def main():
    print("=== Pose-Based Exercise Trainer ===")

    used_gui = False
    exercise_key = None
    mode = None
    gui_target_reps = None  # comes from GUI menu 

    # ---- select exercise + mode (+ target reps ) ----
    if USE_GUI_MENU:
        try:
            from ui.menu import run_menu

            keys = list(EXERCISE_CLASSES.keys())
            chosen = run_menu(keys)

            if not chosen.get("exercise") or not chosen.get("mode"):
                print("No selection made. Exiting.")
                return

            exercise_key = chosen["exercise"]
            mode = chosen["mode"]
            gui_target_reps = chosen.get("target_reps", None)  # may be None for unlimited
            used_gui = True

        except Exception as e:
            print(f"[Main] GUI menu failed ({e}). Falling back to terminal menu.")
            exercise_key = choose_exercise()
            mode = choose_mode()
    else:
        exercise_key = choose_exercise()
        mode = choose_mode()

    # show info; pause only if NOT using GUI
    show_exercise_info(exercise_key, mode, pause=not used_gui)

    # ---- workout settings ----
    target_reps = None
    if mode == "workout":
        if used_gui:
            # fully GUI-driven: no terminal input
            target_reps = gui_target_reps
        else:
            try:
                reps_in = input("Target reps (leave blank for unlimited): ").strip()
                if reps_in:
                    target_reps = int(reps_in)
            except ValueError:
                print("Invalid number, using unlimited.")

    # ---- run ----
    exercise = get_exercise(exercise_key)

    if mode == "workout":
        run_workout_mode(exercise, camera_index=0, target_reps=target_reps)
    else:
        run_learn_mode(exercise, camera_index=0)
        show_summary(exercise)


if __name__ == "__main__":
    main()