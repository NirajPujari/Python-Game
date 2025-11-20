# constants.py
import os

# Game grid
N = 5

# Window size
WINDOW_SIZE = 620
SPACING = 14

# Assets path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

# Colors
COLORS = {
    'back': (189, 172, 161),
    0: (204, 192, 179),
    2: (238, 228, 219),
    4: (240, 226, 202),
    8: (242, 177, 121),
    16: (236, 141, 85),
    32: (250, 123, 92),
    64: (234, 90, 56),
    128: (237, 207, 114),
    256: (242, 208, 75),
    512: (237, 200, 80),
    1024: (227, 186, 19),
    2048: (236, 196, 2)
}

FPS = 60
TITLE = "2048 - Modular"
