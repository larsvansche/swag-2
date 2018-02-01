#!/usr/bin/env python 
import sys
import pygame as pg

# Importing prepare initializes the display.
import prepare
import actors
import level


class App(object):
    def __init__(self):
        """
        This is the main class that runs t he program.
        """
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.keys = pg.key.get_pressed()
        self.done = False
        # ship = random.choice(list(prepare.GFX["ships"].values()))
        ship = list(prepare.GFX["ships"].values())[7]  # pick first ship available
        self.player = actors.Player((0, 0), ship)
        self.level = level.Level(self.screen_rect.copy(), self.player)

        self.energyloss_counter = 0
        self.energygain_counter = 0

    def receive(self, msg):
        print("message: " + msg)

    # Creates health bar for player
    def health_bar(self):
        if self.player.health >= 75:
            health_color = (0, 128, 0)  # Health above or equal to 75 = green
        elif self.player.health > 25:
            health_color = (255, 255, 0)  # Health above 25 = yellow
        else:
            health_color = (255, 0, 0)  # Health beneath 25 = red

        pg.draw.rect(self.screen, health_color, (10, 20, self.player.health, 15))  # Shape and location of health bar

    # Creates health bar for enemies
    def enemy_health(self):
        for entity in self.level.entities:
            if entity != "player" and self.level.entities[entity].__class__.__name__ != "Bullet":  # check if entity is not player or bullet
                if self.level.entities[entity].health >= 75:
                    health_color = (0, 128, 0)  # Health above or equal to 75 = green
                elif self.level.entities[entity].health > 25:
                    health_color = (255, 255, 0)  # Health above 25 = yellow
                else:
                    health_color = (255, 0, 0)  # Health beneath 25 = red

                # self.level.image.clear()
                # self.level.createhealthbar(pg.draw.rect(self.level.image, health_color, (self.level.entities[entity].true_pos[0], self.level.entities[entity].true_pos[1] + 50, 30, 10), 0))

    # Creates energy bar for player
    def energy_bar(self):
        if self.player.energy >= 75:
            energy_color = (0, 0, 255)  # Energy above or equal to 75 = blue
        elif self.player.energy > 25:
            energy_color = (30, 144, 255)  # Energy above 25 = dodgerblue1
        else:
            energy_color = (0, 238, 238)  # Energy beneath 25 = cyan2
        pg.draw.rect(self.screen, energy_color, (10, 40, self.player.energy, 10))

    def event_loop(self):
        """
        End the program on quit event and update held keys on keyup or keydown.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type in (pg.KEYDOWN, pg.KEYUP):
                self.keys = pg.key.get_pressed()

    def display_fps(self):
        """
        Show the program's FPS in the window handle.
        """
        template = "{} - FPS: {:.2f}"
        caption = template.format(prepare.CAPTION, self.clock.get_fps())
        pg.display.set_caption(caption)

    def update(self, dt):
        """
        Update necessary elements; currently only the level.
        """
        self.level.update(self.keys, dt)
        
    def render(self):
        """
        Draw all elements. Individual actor drawing handled by level instance.
        """
        self.screen.fill(prepare.BACKGROUND_COLOR)
        self.health_bar()
        # self.enemy_health()
        self.energy_bar()
        self.level.draw(self.screen)
        pg.display.update()

    def main_loop(self):
        """
        The main game loop.
        """
        dt = 0.3
        self.clock.tick(self.fps)
        while not self.done:
            self.event_loop()
            self.update(dt)
            self.render()
            dt = self.clock.tick(self.fps)/1000.0  # create delta time variable to multiply with movement and rotation
            self.display_fps()
            self.health_bar()
            self.enemy_health()
            self.energy_bar()


def main():
    """
    Create an App and start the program.
    """
    App().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
