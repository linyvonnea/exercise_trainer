# src/config.py

# Angles in degrees
SQUAT_KNEE_DOWN_THRESHOLD = 100   # below = going down
SQUAT_KNEE_UP_THRESHOLD = 140     # above + coming from down = rep

ARM_RAISE_UP_THRESHOLD = 140      # shoulder angle, above = raised
ARM_RAISE_DOWN_THRESHOLD = 80     # below = down

SIDE_BEND_TILT_THRESHOLD = 15     # torso tilt angle in degrees

# FPS smoothing for rep detection
SMOOTHING_WINDOW = 5