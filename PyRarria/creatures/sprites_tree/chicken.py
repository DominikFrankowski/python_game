from creatures.sprites_attributes import CHICKEN
from creatures.sprites_animations import CHICKEN_ANIMATION
from creatures.sprites_tree.walking_sprite import WalkingSprite
from settings import FPS

import math

ANIMATION = CHICKEN_ANIMATION
OBJECT = CHICKEN


class Chicken(WalkingSprite):

    # static variables
    animation = [ANIMATION["left"], ANIMATION["right"]]
    frames = ANIMATION["frames"]
    width = ANIMATION["width"]
    height = ANIMATION["height"]
    radius = min(width, height)
    animation_ticks = math.floor(FPS * ANIMATION["speed"])
    frame_ticks = math.ceil(FPS * ANIMATION["speed"] / ANIMATION["frames"])

    def __init__(self, x, y):
        super(Chicken, self).__init__(x, y)
        self.create(x, y, **OBJECT)
        self.is_enemy = False
