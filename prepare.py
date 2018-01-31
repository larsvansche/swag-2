"""
This module initializes useful constants, initializes the display,
and loads necessary resources.
"""

import os
import pygame as pg
import tools


CAPTION = "Space"
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = (700, 500)
BACKGROUND_COLOR = (10, 20, 30)
SCALE_FACTOR = 0.3  # For scaling down ship images.


ROTATE = {pg.K_RIGHT: 1, pg.K_LEFT: -1}
ACCELERATE = pg.K_UP
DECELERATE = pg.K_DOWN
FIRE = pg.K_d
BOOST = pg.K_SPACE

# Set up environment.
os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.display.set_caption(CAPTION)
pg.display.set_mode(SCREEN_SIZE)


# Load all graphics.
GFX = tools.load_all_gfx("resources")
GFX["ships"] = tools.load_all_gfx(os.path.join("resources", "ships"))

# All enemy types
ENEMIES = {
    "destroyer": {"image": GFX["ships"]["destroyer"], "guns": 3, "speed": 40, "angular": 20, "value": 3},
    "cruiser": {"image": GFX["ships"]["cruiser"], "guns": 2, "speed": 60, "angular": 40, "value": 2},
    "shuttle": {"image": GFX["ships"]["shuttle"], "guns": 1, "speed": 80, "angular": 100, "value": 1}
}

GFX["bullets"] = tools.load_all_gfx(os.path.join("resources", "bullets"))
