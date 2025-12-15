# src/feedback.py

def combine_feedback(messages):
    msgs = [m for m in messages if m]
    if not msgs:
        return "Good form!"
    return " | ".join(msgs)