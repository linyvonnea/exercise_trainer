# src/ui/countdown.py
import time
import cv2

def run_countdown(cap, detector, window_name, seconds=3, title="Get Ready"):

    start = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            return

        # draw pose if you want (optional)
        landmarks, annotated = detector.detect(frame, draw=True)

        h, w, _ = annotated.shape
        elapsed = time.time() - start
        remaining = int(seconds - elapsed) + 1

        # background panel
        cv2.rectangle(annotated, (0, 0), (w, 80), (20, 20, 20), -1)

        cv2.putText(annotated, title, (20, 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

        if remaining <= 0:
            cv2.putText(annotated, "GO!", (w//2 - 60, h//2),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 4)
            cv2.imshow(window_name, annotated)
            cv2.waitKey(250)
            break

        cv2.putText(annotated, str(remaining), (w//2 - 20, h//2),
                    cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 255), 4)

        cv2.imshow(window_name, annotated)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break