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
SCALE_FACTOR = 0.4  # For scaling down ship images.


ROTATE = {pg.K_RIGHT: 1, pg.K_LEFT: -1}
ACCELERATE = pg.K_UP
DECELERATE = pg.K_DOWN
FIRE = pg.K_LSHIFT
BOOST = pg.K_SPACE

# Set up environment.
os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.display.set_caption(CAPTION)
pg.display.set_mode(SCREEN_SIZE)


# Load all graphics.
GFX = tools.load_all_gfx("resources")
GFX["ships"] = tools.load_all_gfx(os.path.join("resources", "ships"))
GFX["bullets"] = tools.load_all_gfx(os.path.join("resources", "bullets"))
