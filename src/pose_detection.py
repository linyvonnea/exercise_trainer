# src/pose_detection.py

import cv2
import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose

class PoseDetector:
    def __init__(self,
                 static_image_mode=False,
                 model_complexity=1,
                 enable_segmentation=False,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.pose = mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            enable_segmentation=enable_segmentation,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def detect(self, frame, draw=True):
        # return landmarks and annotated frame
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb) # run the model

        landmarks = None
        if results.pose_landmarks:
            h, w, _ = frame.shape
            lm_list = []
            for lm in results.pose_landmarks.landmark:
                lm_list.append([lm.x, lm.y, lm.z, lm.visibility])
            landmarks = np.array(lm_list, dtype=np.float32)
            if draw:
                self.mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
                )

        return landmarks, frame