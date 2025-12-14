# src/config.py

# Angles in degrees
SQUAT_KNEE_DOWN_THRESHOLD = 95    # below = going down (stricter requires deeper squat)
SQUAT_KNEE_UP_THRESHOLD = 155     # above + coming from down = rep (stricter lockout)

ARM_RAISE_UP_THRESHOLD = 160      # shoulder flexion angle, above = raised
ARM_RAISE_DOWN_THRESHOLD = 45     # below = down

SIDE_BEND_TILT_THRESHOLD = 25     # torso tilt angle in degrees

LUNGE_FRONT_KNEE_DOWN_THRESHOLD = 90   # below = in lunge (front knee deeply bent)
LUNGE_FRONT_KNEE_UP_THRESHOLD = 165    # above + coming from down = rep

# FPS smoothing for rep detection
SMOOTHING_WINDOW = 5