# src/angles.py

import numpy as np

def angle_between_points(a, b, c):
    """
    Compute angle ABC (in degrees) given three 2D points (x, y).
    a, b, c are np.array([x, y]).
    """
    ba = a - b
    bc = c - b
    denom = (np.linalg.norm(ba) * np.linalg.norm(bc)) + 1e-6
    cos_angle = np.dot(ba, bc) / denom
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    return np.degrees(np.arccos(cos_angle))


def get_point(landmarks, idx):
    """Return (x, y) as np.array from normalized landmarks array."""
    return np.array([landmarks[idx, 0], landmarks[idx, 1]], dtype=np.float32)


def knee_angle(landmarks, left=True):
    # Left: hip(23) - knee(25) - ankle(27)
    # Right: hip(24) - knee(26) - ankle(28)
    if left:
        hip_idx, knee_idx, ankle_idx = 23, 25, 27
    else:
        hip_idx, knee_idx, ankle_idx = 24, 26, 28
    hip = get_point(landmarks, hip_idx)
    knee = get_point(landmarks, knee_idx)
    ankle = get_point(landmarks, ankle_idx)
    return angle_between_points(hip, knee, ankle)


def shoulder_angle(landmarks, left=True):
    # angle between torso vertical and upper arm: shoulder-elbow-wrist
    if left:
        shoulder_idx, elbow_idx, wrist_idx = 11, 13, 15
    else:
        shoulder_idx, elbow_idx, wrist_idx = 12, 14, 16
    shoulder = get_point(landmarks, shoulder_idx)
    elbow = get_point(landmarks, elbow_idx)
    wrist = get_point(landmarks, wrist_idx)
    return angle_between_points(shoulder, elbow, wrist)


def torso_tilt_angle(landmarks):
    """Angle between vector hip→shoulder and vertical (0,-1)."""
    # Use midpoints of hips and shoulders
    left_sh, right_sh = get_point(landmarks, 11), get_point(landmarks, 12)
    left_hp, right_hp = get_point(landmarks, 23), get_point(landmarks, 24)
    shoulder_mid = (left_sh + right_sh) / 2.0
    hip_mid = (left_hp + right_hp) / 2.0

    v = shoulder_mid - hip_mid
    vertical = np.array([0.0, -1.0], dtype=np.float32)
    denom = (np.linalg.norm(v) * np.linalg.norm(vertical)) + 1e-6
    cos_angle = np.dot(v, vertical) / denom
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    return np.degrees(np.arccos(cos_angle))