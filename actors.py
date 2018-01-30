"""
This module contains the Player class for the user controlled character.
"""

import math
import pygame as pg

import prepare


class Player(pg.sprite.Sprite):
    """
    This class represents our user controlled character.
    """

    def __init__(self, pos, image, speed=100, *groups):  # instantiate player
        super(Player, self).__init__(*groups)
        self.top_speed = speed  # set top speed
        self.acceleration = 12  # set max acceleration
        self.velocity = [0.0, 0.0]  # set velocity to 0 on both axis
        self.original = pg.transform.rotozoom(image, 0, prepare.SCALE_FACTOR)
        self.angle = 90.0  # player orientation at the start of the game (facing up)
        self.image = pg.transform.rotozoom(self.original, -self.angle, 1)  # Rotate image to right direction
        self.rect = self.image.get_rect(center=pos)  # get rectangle for player
        self.true_pos = list(self.rect.center)  # assign the center of the rectangle to the true position
        self.angular_speed = 30.0  # set rotation speed of player
        self.thrust_strength = 0
        self.health = 100
        self.energy = 100

    def update(self, keys, bounding, dt, entities):
        """
        Updates the players position based on currently held keys.
        """

        self.check_keys(keys, dt)  # run function check_keys that checks if keys are pressed
        self.true_pos[0] += self.velocity[0] * dt  # update x-position by horizontal velocity * delta time variable
        self.true_pos[1] += self.velocity[1] * dt  # update y-position by vertical velocity * delta time variable
        self.rect.center = self.true_pos  # update the center of the rectangle
        self.recharge_energy()
        if not bounding.contains(self.rect):  # if the rectangle touches any boundaries
            self.on_boundary_collision(bounding)  # then prevent the player from going any further in that direction

    def on_boundary_collision(self, bounding):
        """
        If the ship hits the edge of the map, zero acceleration in that
        direction.
        """
        if self.rect.x < bounding.x or self.rect.right > bounding.right:
            self.velocity[0] = 0.0
        if self.rect.y < bounding.y or self.rect.bottom > bounding.bottom:
            self.velocity[1] = 0.0
        self.rect.clamp_ip(bounding)
        self.true_pos = list(self.rect.center)

    def check_keys(self, keys, dt):
        """
        Call methods to check keys for both rotation and thrust.
        """
        self.rotate(keys, dt)
        self.thrust(keys, dt)
        self.shoot(keys, dt)
        self.boost(keys, dt)

    def boost(self, keys, dt):
        if keys[prepare.BOOST] and self.energy > 0:
            self.top_speed = 350
            self.acceleration = 20
            self.energy -= 20 / 60
        else:
            self.top_speed = 100

    # def energy_use(self, keys):
    #     if keys[prepare.BOOST]:
    #        # if not
    def recharge_energy(self):
        if self.energy < 100:
            self.energy += 3 / 60

    def rotate(self, keys, dt):
        """
        If either rotation key is held adjust angle, image,
        and rect appropriately.
        """
        for key in prepare.ROTATE:
            if keys[key]:
                self.angle += self.angular_speed * prepare.ROTATE[
                    key] * dt  # set angle to multiplication of angular speed, direction and delta time
                self.angle %= 360
                self.image = pg.transform.rotozoom(self.original, -self.angle, 1)
                self.rect = self.image.get_rect(center=self.rect.center)

    def thrust(self, keys, dt):
        """
        Adjust velocity if the thrust key is held.
        """

        # This function has been altered by Lars van Scheijndel on 24-01-2018 at 16:11
        # The change was necessary to ensure the player would turn when not accelerating

        if keys[prepare.ACCELERATE]:  # if thrust key (up-arrow, pg.K_UP) is held
            self.thrust_strength += self.acceleration
        if keys[prepare.DECELERATE]:  # if brake key (down-arrow, pg.K_DOWN) is held
            self.thrust_strength -= self.acceleration

        rads = math.radians(self.angle)  # get angle in radians
        self.velocity[0] = math.sin(rads) * dt * self.thrust_strength  # set horizontal velocity to acceleration * cosine of angle * delta time
        self.velocity[1] = -math.cos(rads) * dt * self.thrust_strength  # set vertical velocity to acceleration * cosine of angle * delta time
        self.restrict_speed()  # restrict the speed

    def restrict_speed(self):
        """
        Restricts the velocity components so that the top speed is never
        exceeded.
        """
        adj, op = self.velocity
        if math.hypot(adj, op) > self.top_speed:
            angle = math.atan2(op, adj)  # Angle of movement; not ship direction
            self.velocity[0] = self.top_speed * math.cos(angle)
            self.velocity[1] = self.top_speed * math.sin(angle)

    def shoot(self, keys, dt):
        if keys[prepare.FIRE]:
            bullet = Bullet(self.rect.centerx, self.rect.top)

    def draw(self, surface):
        """
        Basic draw function. (not used if drawing via groups)
        """
        surface.blit(self.image, self.rect)


class Enemy(pg.sprite.Sprite):
    """
    This class represents our user controlled character.
    """

    def __init__(self, pos, entity, *groups):  # instantiate player
        super(Enemy, self).__init__(*groups)
        self.top_speed = entity["speed"]  # set top speed
        self.acceleration = entity["speed"] / 6  # set max acceleration
        self.velocity = [0.0, 0.0]  # set velocity to 0 on both axis
        self.original = pg.transform.rotozoom(entity["image"], 0, prepare.SCALE_FACTOR)
        self.angle = 270.0  # player orientation at the start of the game
        self.image = pg.transform.rotozoom(self.original, -self.angle, 1)  # Rotate image to right direction
        self.rect = self.image.get_rect(center=pos)  # get rectangle for player
        self.true_pos = [0, 0]  # list(self.rect.center)  # assign the center of the rectangle to the true position
        self.angular_speed = entity["angular"]  # set rotation speed of player
        self.thrust_strength = 0
        self.status = "agressive"
        self.distancetoplayer = 0
        self.directiontoplayer = 0
        self.rotatedirection = 0

    def update(self, keys, bounding, dt, entities):
        """
        Updates the players position based on currently held keys.
        """

        self.finddistancetoplayer(entities["player"])
        self.finddirectiontoplayer(entities["player"])

        if self.status == "agressive" or self.status == "kamikaze":
            self.movetoplayer()
        if self.status == "neutral" or self.status == "friendly":
            self.idle()

        self.thrust(dt)
        self.rotate(dt)

        self.true_pos[0] += self.velocity[0] * dt  # update x-position by horizontal velocity * delta time variable
        self.true_pos[1] += self.velocity[1] * dt  # update y-position by vertical velocity * delta time variable
        self.rect.center = self.true_pos  # update the center of the rectangle
        if not bounding.contains(self.rect):  # if the rectangle touches any boundaries
            self.on_boundary_collision(bounding)  # then prevent the player from going any further in that direction

    def finddistancetoplayer(self, player):
        relativex = self.true_pos[0] - player.true_pos[0]
        relativey = self.true_pos[1] - player.true_pos[1]
        self.distancetoplayer = math.sqrt(math.pow(relativex, 2) + math.pow(relativey, 2))

    def finddirectiontoplayer(self, player):
        relativex = self.true_pos[0] - player.true_pos[0]
        relativey = self.true_pos[1] - player.true_pos[1]
        if self.distancetoplayer == 0:
            self.distancetoplayer = 0.000001  # can't divide by zero

        angle = math.degrees(-math.acos(relativey / self.distancetoplayer)) * -1

        if relativex > 0:
            angle = (angle - 90) * -1 + 270

        self.directiontoplayer = angle - self.angle

        if self.directiontoplayer < 0:
            self.directiontoplayer += 360

    def movetoplayer(self):
        if self.distancetoplayer > 100:
            if 90 > self.directiontoplayer or self.directiontoplayer > 270:
                self.thrust_strength += self.acceleration
            elif self.thrust_strength > 0:
                self.thrust_strength -= self.acceleration

            if 0 < self.directiontoplayer < 180:
                self.rotatedirection = 1
            elif 180 <= self.directiontoplayer:
                self.rotatedirection = -1
        elif self.distancetoplayer < 50:
            if (90 < self.directiontoplayer or self.directiontoplayer < 270) and self.thrust_strength > 500:
                self.thrust_strength -= self.acceleration
            elif self.thrust_strength < 500:
                self.thrust_strength += self.acceleration

            if self.directiontoplayer < 180:
                self.rotatedirection = -1
            else:
                self.rotatedirection = 1
        else:
            if 90 > self.directiontoplayer or self.directiontoplayer > 270:
                self.thrust_strength += self.acceleration
            elif self.thrust_strength > 0:
                self.thrust_strength -= self.acceleration

    def idle(self):
        if self.distancetoplayer < 100:
            if (90 < self.directiontoplayer or self.directiontoplayer < 270) and self.thrust_strength < 500:
                self.thrust_strength += self.acceleration
            elif self.thrust_strength > 500:
                self.thrust_strength -= self.acceleration

            if self.directiontoplayer < 180:
                self.rotatedirection = -1
            else:
                self.rotatedirection = 1
        else:
            if self.thrust_strength < 500:
                self.thrust_strength += self.acceleration
            else:
                self.thrust_strength -= self.acceleration

            self.rotatedirection = 0.3

    def on_boundary_collision(self, bounding):
        """
        If the ship hits the edge of the map, zero acceleration in that
        direction.
        """
        if self.rect.x < bounding.x or self.rect.right > bounding.right:
            self.velocity[0] = 0.0
        if self.rect.y < bounding.y or self.rect.bottom > bounding.bottom:
            self.velocity[1] = 0.0
        self.rect.clamp_ip(bounding)
        self.true_pos = list(self.rect.center)

    def rotate(self, dt):
        """
        If either rotation key is held adjust angle, image,
        and rect appropriately.
        """

        self.angle += self.angular_speed * self.rotatedirection * dt  # set angle to multiplication of angular speed, direction and delta time
        self.angle %= 360
        self.image = pg.transform.rotozoom(self.original, -self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def thrust(self, dt):
        """
        Adjust velocity if the thrust key is held.
        """

        # if keys[prepare.ACCELERATE]:  # if thrust key (up-arrow, pg.K_UP) is held
        #     self.thrust_strength += self.acceleration
        # if keys[prepare.DECELERATE]:  # if brake key (down-arrow, pg.K_DOWN) is held
        #     self.thrust_strength -= self.acceleration

        rads = math.radians(self.angle)  # get angle in radians
        self.velocity[0] = math.sin(rads) * dt * self.thrust_strength  # set horizontal velocity to acceleration * cosine of angle * delta time
        self.velocity[1] = -math.cos(rads) * dt * self.thrust_strength  # set vertical velocity to acceleration * cosine of angle * delta time
        self.restrict_speed()  # restrict the speed

    def restrict_speed(self):
        """
        Restricts the velocity components so that the top speed is never
        exceeded.
        """
        adj, op = self.velocity
        if math.hypot(adj, op) > self.top_speed:
            angle = math.atan2(op, adj)  # Angle of movement; not ship direction
            self.velocity[0] = self.top_speed * math.cos(angle)
            self.velocity[1] = self.top_speed * math.sin(angle)

    def draw(self, surface):
        """
        Basic draw function. (not used if drawing via groups)
        """
        surface.blit(self.image, self.rect)


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 20))
        self.image.fill((138, 43, 226))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        print(self.rect.x, self.rect.y)
        self.rect.y = self.speedy


