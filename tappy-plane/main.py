#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sfml as sf
import sys

WWIDTH, WHEIGHT = 800, 480
WTITLE = "PySFML - Tappy Plane"
GROUND_SPEED = 200
SETTINGS = sf.ContextSettings()
SETTINGS.antialiasing_level = 8
GRAVITY = 90


class Game:
    def __init__(self):
        # Window
        self.window = sf.RenderWindow(sf.VideoMode(WWIDTH, WHEIGHT), WTITLE, sf.Style.CLOSE | sf.Style.TITLEBAR, SETTINGS)
        self.window.framerate_limit = 60

        # Clock
        self.clock = sf.Clock()

        # View
        self.view = sf.View(sf.Rectangle((0, 0), (WWIDTH, WHEIGHT)))
        self.window.view = self.view

        # Loading assets
        self.load_assets()

        self.background = sf.Sprite(self.bg_texture)
        self.grounds = [sf.Sprite(self.ground_texture) for i in xrange(2)]

        self.grounds[0].position = 0, 409
        self.grounds[1].position = 0, 409

        self.plane = sf.Sprite(self.plane_texture)
        self.plane.origin = self.plane.global_bounds.width / 2.0, self.plane.global_bounds.height / 2.0

        self.plane.position = sf.Vector2(150, 200)

        self.jumped = False

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
            self.jumped = True

    def update(self, elapsed_time):
        # Grounds
        self.grounds[0].move(sf.Vector2(-GROUND_SPEED, 0) * elapsed_time)
        self.grounds[1].position = self.grounds[0].position + sf.Vector2(self.grounds[0].global_bounds.width, 0)

        if self.grounds[0].position.x <= -WWIDTH:
            self.grounds[0], self.grounds[1] = self.grounds[1], self.grounds[0]

        # Plane
        if self.jumped:
            self.plane.move(sf.Vector2(0.0, 10 * -GRAVITY) * elapsed_time)
            self.jumped = False

        self.plane.move(sf.Vector2(0.0, GRAVITY) * elapsed_time)

        if self.plane.rotation <= 85:
            self.plane.rotate(1)

    def render(self):
        self.window.clear()

        self.window.draw(self.background)

        for i in self.grounds:
            self.window.draw(i)

        self.window.draw(self.plane)

        self.window.display()

    def load_assets(self):
        try:
            self.bg_texture = sf.Texture.from_file("assets/images/background.png")
            self.ground_texture = sf.Texture.from_file("assets/images/ground.png")
            self.plane_texture = sf.Texture.from_file("assets/images/plane.png")
        except IOError:
            sys.exit(1)


if __name__ == '__main__':
    Game().run()