# src/feedback.py

def combine_feedback(messages):
    """Given a list of short feedback strings, combine nicely."""
    msgs = [m for m in messages if m]
    if not msgs:
        return "Good form!"
    return " | ".join(msgs)