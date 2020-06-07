from creatures.physical_engine import *
from creatures.sprites_tree.bat import Bat
from creatures.sprites_tree.bird import Bird
from creatures.sprites_tree.chicken import Chicken
from creatures.sprites_tree.cow import Cow
from creatures.sprites_tree.sheep import Sheep
from creatures.sprites_tree.skeleton import Skeleton
from creatures.sprites_tree.skeletonboss import SkeletonBoss
from creatures.sprites_tree.walking_test import WalkingTest
from creatures.sprites_tree.zombie import Zombie
from creatures.vector import PVector
from pygame.sprite import Group
from settings import FPS


BARD_RANGE = 120
FREEZE_RANGE = 120
SPAWN_RANGE = 100

LIMITS = {
    "walking_test": 1,
    "birds": 0,
    "skeletons": 0,
    "skeletons_boss": 0,
    "zombies": 0,
    "cows": 0,
    "sheeps": 0,
    "bats": 0,
    "chickens": 0,
}

FREQUENCIES = {
    "walking_test": 1,
    "birds": 1,
    "skeletons": 1,
    "skeletons_boss": 1,
    "zombies": 1,
    "cows": 1,
    "sheeps": 1,
    "bats": 1,
    "chickens": 1,
}

CREATURES = {
    "walking_test": WalkingTest,
    "bird": Bird,
    "skeleton": Skeleton,
    "skeletons_boss": SkeletonBoss,
    "zombies": Zombie,
    "cows": Cow,
    "sheep": Sheep,
    "bats": Bat,
    "chickens": Chicken,
}

NAMES = {
    "walking_test": "walking_test",
    "bird": "birds",
    "skeleton": "skeletons",
    "skeletons_boss": "skeletons_boss",
    "zombies": "zombie",
    "cows": "cow",
    "sheeps": "sheep",
    "bats": "bat",
    "chickens": "chicken",
}


class CreaturesEngine:
    def __init__(self, game):

        # window, clock, main position
        self.game = game
        self.window = game.screen
        self.items_factory = game.factory
        self.clock = 0
        self.map_position = PVector(0, 0)
        self.map_position_init = PVector(0, 0)

        # map, player, arrows
        self.platforms = game.platforms
        self.player = game.player

        # creatures, arrows
        self.all_creatures = game.all_creatures
        self.arrows = game.arrows

        # groups
        self.groups = {
            "walking_test": Group(),
            "birds": Group(),
            "skeletons": Group(),
            "skeletons_boss": Group(),
            "zombies": Group(),
            "cows": Group(),
            "sheeps": Group(),
            "bats": Group(),
            "chickens": Group(),
        }

    def update(self):
        # update main position
        self.update_map_position()

        # clock
        self.clock += 1

        # bites player (if doesn't bite nothing happens)
        for creature in self.all_creatures:
            creature.bite(self.player)

        # hits player (if doesn't hit nothing happens)
        for arrow in self.arrows:
            arrow.bite(self.player)

        # shot (if doesn't shoot nothing happens)
        for archer in self.all_creatures:
            archer.shoot(self.player, self.arrows)

        # update creatures
        for creature in self.all_creatures:
            creature.update(self.player, self.platforms,
                            self.map_position, self.items_factory)

        # update arrows
        for arrow in self.arrows:
            print(self.player)
            print(self.platforms)
            print(self.map_position)
            print(self.items_factory)

            arrow.update(self.player, self.platforms, self.map_position, self.items_factory)

        # spawn
        self.spawn()

        # print stats
        # self.print_stats()

    def draw(self):
        # redraw creatures
        for creature in self.all_creatures:
            creature.draw(self.window)

        # redraw arrows
        for arrow in self.arrows:
            arrow.draw(self.window)

    def spawn(self):
        for group, frequency, limit, Creature in zip(
            self.groups.values(), FREQUENCIES.values(), LIMITS.values(), CREATURES.values()
        ):

            if len(group) >= limit:
                continue

            if self.clock % (frequency * FPS) != 0:
                continue

            new_creature = Creature(self.player.position.x, self.player.position.y)
            group.add(new_creature)
            self.all_creatures.add(new_creature)

    def update_map_position(self):
        dx, dy = self.game.get_main_stage_position()
        self.map_position.set(dx - self.map_position_init.x, dy - self.map_position_init.y)

    def freeze(self, freeze_duration):
        # freeze_duration is in range(50, ...)
        for creature in self.all_creatures:
            distance = (self.player.position - creature.position).mag()
            if distance < FREEZE_RANGE:
                creature.freeze_count = freeze_duration

    def bard(self, bard_power):
        # bard power is in range(0.0, 1.0)
        for creature in self.all_creatures:
            distance = (self.player.position - creature.position).mag()
            if distance < BARD_RANGE:
                push_away(creature, self.player, bard_power)

    def print_stats(self):
        for group, name in zip(self.groups.values(), NAMES):
            print(f"{name:10}:{len(group)}")
        print()
