# src/angles.py

import numpy as np

# compute joint angle at point b
def angle_between_points(a, b, c): 

    # points to vectors
    ba = a - b
    bc = c - b

    # cosine formula
    denom = (np.linalg.norm(ba) * np.linalg.norm(bc)) + 1e-6
    cos_angle = np.dot(ba, bc) / denom # dot product
    cos_angle = np.clip(cos_angle, -1.0, 1.0)

    # radians to degrees
    return np.degrees(np.arccos(cos_angle)) 

# xy coordinates of landmark
def get_point(landmarks, idx):
    return np.array([landmarks[idx, 0], landmarks[idx, 1]], dtype=np.float32)


def knee_angle(landmarks, left=True):
    # left: hip(23) - knee(25) - ankle(27)
    # right: hip(24) - knee(26) - ankle(28)
    if left:
        hip_idx, knee_idx, ankle_idx = 23, 25, 27
    else:
        hip_idx, knee_idx, ankle_idx = 24, 26, 28
    
    # extract xy points
    hip = get_point(landmarks, hip_idx)
    knee = get_point(landmarks, knee_idx)
    ankle = get_point(landmarks, ankle_idx)
    return angle_between_points(hip, knee, ankle) # knee angle at knee joint


def shoulder_angle(landmarks, left=True):
    #sholder flexion: hip-shoulder-elbow angle
    # arm down ≈ 0-30°, arm overhead ≈ 150-180°
    if left:
        hip_idx, shoulder_idx, elbow_idx = 23, 11, 13
    else:
        hip_idx, shoulder_idx, elbow_idx = 24, 12, 14

    hip = get_point(landmarks, hip_idx)
    shoulder = get_point(landmarks, shoulder_idx)
    elbow = get_point(landmarks, elbow_idx)
    return angle_between_points(hip, shoulder, elbow)


def torso_tilt_angle(landmarks):
    # angle between hip, shoulder, vertical (0, -1)

    # midpoints of hips and shoulders
    left_sh, right_sh = get_point(landmarks, 11), get_point(landmarks, 12)
    left_hp, right_hp = get_point(landmarks, 23), get_point(landmarks, 24)
    shoulder_mid = (left_sh + right_sh) / 2.0
    hip_mid = (left_hp + right_hp) / 2.0

    # angle between torso vector (hips to shoulders) and vertical
    v = shoulder_mid - hip_mid # torso vector
    vertical = np.array([0.0, -1.0], dtype=np.float32) # upward vector

    denom = (np.linalg.norm(v) * np.linalg.norm(vertical)) + 1e-6
    cos_angle = np.dot(v, vertical) / denom
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    return np.degrees(np.arccos(cos_angle))