from PyRarria.creatures.physical_engine import *
from PyRarria.creatures.sprites_attributes import SKELETON
from PyRarria.creatures.sprites_animations import SKELETON_ANIMATION
from PyRarria.creatures.sprites_tree.arrow import Arrow
from PyRarria.creatures.sprites_tree.walking_sprite import WalkingSprite
from PyRarria.creatures.test_global_settings import FPS

import math

ANIMATION = SKELETON_ANIMATION
OBJECT = SKELETON


class Skeleton(WalkingSprite):

    # static variables
    animation = [ANIMATION['left'], ANIMATION['right']]
    frames = ANIMATION['frames']
    width = ANIMATION['width']
    height = ANIMATION['height']
    radius = min(width, height)
    animation_ticks = math.floor(FPS * ANIMATION['speed'])
    frame_ticks = math.ceil(FPS * ANIMATION['speed'] / ANIMATION['frames'])

    def __init__(self, x, y):
        super(Skeleton, self).__init__(x, y)
        self.create(x, y, **OBJECT)

    def update_forces(self, player, platforms):
        gravity(self)
        if (player.location - self.location).mag() > 200:
            run_after(self, player)
        else:
            self.velocity.zero()
        jump_from_platform(self, platforms)

    def bite(self, player):
        pass

    def shoot(self, player, arrows):
        if self.shot_count > 0:
            self.shot_count -= 1
        else:
            arrow = Arrow(self.location.x, self.location.y)
            bullet(arrow, self.location, player.location)

            arrows.add(arrow)
            self.shot_count = 10