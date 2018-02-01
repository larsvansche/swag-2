"""
This module contains the Level class.
Drawing and updating of actors should occur here.
"""
import random
import time
import math
import pygame as pg

import prepare
import tools
import actors

level_width = 700
level_height = 500

BIG_STARS = tools.tile_surface((level_width, level_height), prepare.GFX["stars"], True)


class Level(object):
    """
    This class represents the whole starscape.  The starscape consists of
    three star layers.  The player is drawn and updated by this class.
    The player is contained in a pg.sprite.GroupSingle group.
    """
    def __init__(self, viewport, player):

        self.image = BIG_STARS.copy()
        self.rect = self.image.get_rect()

        self.entities = {"player": player}
        self.entities["player"].rect.midbottom = self.rect.centerx, self.rect.centery  # set position of the player
        self.entities["player"].true_pos = list(player.rect.center)
        self.groupsingles = {"player": pg.sprite.GroupSingle(self.entities["player"])}

        self.totalentities = len(self.entities)

        self.make_layers()
        self.viewport = viewport
        self.update_viewport(True)
        self.mid_viewport = self.viewport.copy()
        self.mid_true = list(self.mid_viewport.topleft)
        self.base_viewport = self.viewport.copy()
        self.base_true = list(self.base_viewport.topleft)
        self.level = 3

        self.makewave()

    def makewave(self):  # method has not been tested yet
        wantedlevel = self.level
        for enemy in prepare.ENEMIES:
            while wantedlevel >= prepare.ENEMIES[enemy]["value"]:
                self.createenemy(prepare.ENEMIES[enemy], (random.randint(0, level_width), random.randint(0, level_height)))
                wantedlevel -= prepare.ENEMIES[enemy]["value"]

    def createenemy(self, enemy, position):  # method has not been tested yet
        self.totalentities += 1
        identifier = self.totalentities

        self.entities[identifier] = actors.Enemy(position, enemy)
        self.entities[identifier].rect.midbottom = position[0], position[1]  # set entity position
        self.entities[identifier].true_pos = list(self.entities[identifier].rect.center)

        self.groupsingles[identifier] = pg.sprite.GroupSingle(self.entities[identifier])

    def createbullet(self, position, angle):  # method has not been tested yet
        self.totalentities += 1
        identifier = self.totalentities

        self.entities[identifier] = actors.Bullet(position, angle)
        self.entities[identifier].rect.midbottom = position[0], position[1]  # set entity position
        self.entities[identifier].true_pos = list(self.entities[identifier].rect.center)

        self.groupsingles[identifier] = pg.sprite.GroupSingle(self.entities[identifier])

    def make_layers(self):
        """
        Create the middle and base image of the stars.
        self.image scrolls with the player, self.mid_image scrolls at
        half the speed, and self.base always stays fixed. 
        """
        w, h = self.image.get_size()
        shrink = pg.transform.smoothscale(self.image, (w//2, h//2))
        self.mid_image = tools.tile_surface((w, h), shrink, True)
        shrink = pg.transform.smoothscale(self.image, (w//4, h//4))
        self.base = tools.tile_surface((w, h), shrink, True)

    def update(self, keys, dt):
        """
        Updates the player and then adjusts the viewport with respect to the player's new position.
        """

        dead = list()

        for entity in self.entities:  # for loop that updates all instantiated entities
            self.entities[entity].update(keys, self.rect, dt, self.entities)
            if self.entities[entity].health <= 0:
                self.entities[entity].kill()
                dead.append(entity)

        self.detectcolissions()
        self.update_viewport()

        for kill in dead:
            del self.entities[kill]

        del dead

        self.firebullet()

    def firebullet(self):
        if self.entities["player"].fire:
            if time.time() >= self.entities["player"].timeatshot + self.entities["player"].firerate:
                player = self.entities["player"]
                rads = math.radians(player.angle)  # change to firing angle when ready

                bulletx = math.sin(rads) * (player.colissionsize + 10) + player.true_pos[0]
                bullety = -math.cos(rads) * (player.colissionsize + 10) + player.true_pos[1]

                self.createbullet((bulletx, bullety), player.angle)
                player.timeatshot = time.time()

    def detectcolissions(self):
        for entity in self.entities:
            for entity2 in self.entities:
                if entity != entity2:
                    tracked = self.entities[entity]
                    target = self.entities[entity2]
                    radius = target.colissionsize
                    trackedx = tracked.true_pos[0]
                    trackedy = tracked.true_pos[1]
                    targetx = target.true_pos[0]
                    targety = target.true_pos[1]

                    if (trackedx - targetx) ** 2 + (trackedy - targety) ** 2 < radius ** 2:
                        damage = min(target.health, tracked.health)
                        target.health -= damage
                        tracked.health -= damage

    def update_viewport(self, start=False):
        """
        The viewport will stay centered on the player unless the player
        approaches the edge of the map.
        """
        old_center = self.viewport.center
        self.viewport.center = self.groupsingles["player"].sprite.rect.center
        self.viewport.clamp_ip(self.rect)
        change = (self.viewport.centerx-old_center[0], self.viewport.centery-old_center[1])
        if not start:
            self.mid_true[0] += change[0] * 0.5
            self.mid_true[1] += change[1] * 0.5
            self.mid_viewport.topleft = self.mid_true
            self.base_true[0] += change[0] * 0.1
            self.base_true[1] += change[1] * 0.1
            self.base_viewport.topleft = self.base_true

    def draw(self, surface):
        """
        Blit and clear actors on the self.image layer.
        Then blit appropriate viewports of all layers.
        """

        for entity in self.entities:
            self.groupsingles[entity].clear(self.image, clear_callback)
            self.groupsingles[entity].draw(self.image)

        surface.blit(self.base, (0, 0), self.base_viewport)
        surface.blit(self.mid_image, (0, 0), self.mid_viewport)
        surface.blit(self.image, (0, 0), self.viewport)


def clear_callback(surface, rect):
    """
    We need this callback because the clearing background contains
    transparency.  We need to fill the rect with transparency first.
    """

    surface.fill((0, 0, 0, 0), rect)
    surface.blit(BIG_STARS, rect, rect)


