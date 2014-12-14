#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sfml as sf
import sys
from animation import *

WWIDTH, WHEIGHT = 800, 480
WTITLE = "PySFML - Tappy Plane"
GROUND_SPEED = 200
SETTINGS = sf.ContextSettings()
SETTINGS.antialiasing_level = 8
GRAVITY = 10.0


class Game:
    def __init__(self):
        # Window
        self.window = sf.RenderWindow(sf.VideoMode(WWIDTH, WHEIGHT), WTITLE, sf.Style.CLOSE | sf.Style.TITLEBAR,
                                      SETTINGS)
        self.window.framerate_limit = 60

        # Clock
        self.clock = sf.Clock()

        # View
        self.view = sf.View(sf.Rectangle((0, 0), (WWIDTH, WHEIGHT)))
        self.window.view = self.view

        # Loading assets
        self.load_assets()

        self.backgrounds = [sf.Sprite(self.bg_texture) for i in xrange(2)]
        self.grounds = [sf.Sprite(self.ground_texture) for i in xrange(2)]

        self.grounds[0].position = 0, 409
        self.grounds[1].position = 0, 409

        # Plane
        fly_anim = Animation()
        fly_anim.texture = self.plane_sheet
        fly_anim.add_frame(sf.Rectangle((0, 0), (88, 73)))
        fly_anim.add_frame(sf.Rectangle((88, 0), (88, 73)))
        fly_anim.add_frame(sf.Rectangle((176, 0), (88, 73)))
        fly_anim.add_frame(sf.Rectangle((88, 0), (88, 73)))

        self.plane = AnimatedSprite(sf.seconds(0.2), False, True)
        self.plane.play(fly_anim)
        self.plane.origin = self.plane.global_bounds.width / 2.0, self.plane.global_bounds.height / 2.0

        self.plane.position = sf.Vector2(150, 200)

        self.plane_speed = sf.Vector2(0.0, 0.0)

        self.jump_time = None

        self.plane_jumped = False

        # Rocks
        self.rocks = []
        self.spawn_rocks()

    def run(self):
        while self.window.is_open:
            for event in self.window.events:
                self.handle_events(event)

            elapsed = self.clock.elapsed_time.seconds
            self.clock.restart()
            self.update(elapsed)

            self.render()

    def handle_events(self, event):
        if type(event) is sf.CloseEvent:
            self.window.close()
        if type(event) is sf.KeyEvent and event.code is sf.Keyboard.SPACE:
            self.plane_jumped = True
            self.jump_time = sf.Clock()

    def update(self, elapsed_time):
        # Backgrounds
        self.backgrounds[0].move(sf.Vector2(-GROUND_SPEED / 10.0, 0.0) * elapsed_time)
        self.backgrounds[1].position = self.backgrounds[0].position + \
                                       sf.Vector2(self.backgrounds[0].global_bounds.width, 0)

        if self.backgrounds[0].position.x <= -WWIDTH:
            self.backgrounds[0], self.backgrounds[1] = self.backgrounds[1], self.backgrounds[0]

        # Grounds
        self.grounds[0].move(sf.Vector2(-GROUND_SPEED, 0) * elapsed_time)
        self.grounds[1].position = self.grounds[0].position + sf.Vector2(self.grounds[0].global_bounds.width, 0)

        if self.grounds[0].position.x <= -WWIDTH:
            self.grounds[0], self.grounds[1] = self.grounds[1], self.grounds[0]

        # Plane
        if not self.plane_jumped and (self.plane.rotation <= 60 or self.plane.rotation >= 300):
            self.plane.rotate(1.25)

        if self.plane_jumped:
            self.plane_speed = sf.Vector2(0.0, -150.0)

            if self.jump_time.elapsed_time.seconds < 0.25:
                self.plane.rotate(-2.5)
            else:
                self.plane_jumped = False
                self.jump_time = None
            if self.plane.rotation % 300 > 60:
                self.plane.rotation = (300, 60)[self.plane.rotation > 300]

        if self.plane_speed.y <= 50 * GRAVITY:
            self.plane_speed += sf.Vector2(0.0, GRAVITY)

        self.plane.move(self.plane_speed * elapsed_time)
        self.plane.update(sf.seconds(elapsed_time))

        # Rocks
        if len(self.rocks) > 0:
            self.rocks[0].move(sf.Vector2(-GROUND_SPEED, 0.0) * elapsed_time)
            self.rocks[1].position = sf.Vector2(self.rocks[0].position.x + 300,
                                                WHEIGHT - self.rocks[0].global_bounds.height)

            if self.rocks[1].position.x <= -self.rocks[1].global_bounds.width:
                for i in xrange(2):
                    self.rocks.pop(0)
                self.spawn_rocks()

    def spawn_rocks(self):
        if len(self.rocks) == 0:
            rock_down = sf.Sprite(self.rock_down)
            rock_down.position = sf.Vector2(float(WWIDTH), 0.0)
            self.rocks.append(rock_down)

            rock_up = sf.Sprite(self.rock_up)
            rock_up.position = sf.Vector2(rock_up.position.x + 300.0, float(WHEIGHT - rock_up.global_bounds.height))
            self.rocks.append(rock_up)
        else:
            print("Boş değil")

    def render(self):
        self.window.clear()

        for i in self.backgrounds:
            self.window.draw(i)

        for i in self.rocks:
            self.window.draw(i)

        for i in self.grounds:
            self.window.draw(i)

        self.window.draw(self.plane)

        self.window.display()

    def load_assets(self):
        try:
            self.bg_texture = sf.Texture.from_file("assets/images/background.png")
            self.ground_texture = sf.Texture.from_file("assets/images/ground.png")
            self.plane_sheet = sf.Texture.from_file("assets/images/plane_sheet.png")
            self.rock_up = sf.Texture.from_file("assets/images/rock-up.png")
            self.rock_down = sf.Texture.from_file("assets/images/rock-down.png")
        except IOError:
            sys.exit(1)


if __name__ == '__main__':
    Game().run()