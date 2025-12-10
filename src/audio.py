# src/audio.py

import os
import platform

def play_rep_sound():
    """Play a short sound when a rep is completed."""
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            os.system("afplay /System/Library/Sounds/Glass.aiff >/dev/null 2>&1 &")
        elif system == "Windows":
            import winsound
            winsound.MessageBeep()
        else:  # Linux or others: fallback to terminal bell
            print("\a", end="", flush=True)
    except Exception:
        # If anything fails, just ignore audio.
        pass