#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sfml as sf


class Animation:
    def __init__(self):
        self.texture = None
        self.frames = []

    def add_frame(self, rect):
        self.frames.append(rect)


class AnimatedSprite(sf.TransformableDrawable):
    def __init__(self, frametime=sf.seconds(0.2), paused=False, looped=True):
        super(AnimatedSprite, self).__init__()

        self.animation = None
        self.frametime = frametime
        self.paused = paused
        self.looped = looped

        self.current_time = None
        self.current_frame = 0

        self.texture = None

        self.vertices = sf.VertexArray(sf.PrimitiveType.QUADS, 4)

    def set_animation(self, animation):
        self.animation = animation
        self.texture = animation.texture
        self.current_frame = 0
        self.set_frame(0)

    def play(self, animation=None):
        if animation and self.animation is not animation:
            self.set_animation(animation)
        self.paused = False

    def pause(self):
        self.paused = True

    def stop(self):
        self.paused = True
        self.current_frame = 0
        self.set_frame(self.current_frame)

    def set_color(self, color):
        for i in self.vertices:
            i.color = color

    def local_bounds(self):
        rect = self.animation[self.current_frame]

        width = abs(rect.width)
        height = abs(rect.height)
        return sf.Rectangle((0.0, 0.0), (width, height))

    def global_bounds(self):
        self.transform.transform_rectangle(self.local_bounds())

    def set_frame(self, frame, reset_time=True):
        if self.animation:
            rect = self.animation.frames[frame]

            self.vertices[0].position = sf.Vector2(0.0, 0.0)
            self.vertices[1].position = sf.Vector2(0.0, rect.height)
            self.vertices[2].position = sf.Vector2(rect.width, rect.height)
            self.vertices[3].position = sf.Vector2(rect.width, 0.0)

            left = rect.left + 0.0001
            right = left + rect.width
            top = rect.top
            bottom = top + rect.height

            self.vertices[0].tex_coords = sf.Vector2(left, top)
            self.vertices[1].tex_coords = sf.Vector2(left, bottom)
            self.vertices[2].tex_coords = sf.Vector2(right, bottom)
            self.vertices[3].tex_coords = sf.Vector2(right, top)

        if reset_time:
            self.current_time = sf.Time.ZERO

    def update(self, delta):
        if not self.paused and self.animation:
            self.current_time += delta

            if self.current_time >= self.frametime:
                self.current_time -= self.frametime

                if self.current_frame + 1 < len(self.animation.frames):
                    self.current_frame += 1

                else:
                    self.current_frame = 0

                    if not self.looped:
                        self.paused = True

                self.set_frame(self.current_frame, False)

    def draw(self, target, states):
        if self.animation and self.texture:
            states.transform *= self.transform
            states.texture = self.texture
            target.draw(self.vertices, states)


def main():
    window = sf.RenderWindow(sf.VideoMode(800, 600), "PySFML Animation")
    window.framerate_limit = 60

    texture = sf.Texture.from_file("assets/images/player.png")

    walking_down = Animation()
    walking_down.texture = texture
    walking_down.add_frame(sf.Rectangle((32, 0), (32, 32)))
    walking_down.add_frame(sf.Rectangle((64, 0), (32, 32)))
    walking_down.add_frame(sf.Rectangle((32, 0), (32, 32)))
    walking_down.add_frame(sf.Rectangle((0, 0), (32, 32)))

    walking_up = Animation()
    walking_up.texture = texture
    walking_up.add_frame(sf.Rectangle((32, 96), (32, 32)))
    walking_up.add_frame(sf.Rectangle((64, 96), (32, 32)))
    walking_up.add_frame(sf.Rectangle((32, 96), (32, 32)))
    walking_up.add_frame(sf.Rectangle((0, 96), (32, 32)))

    walking_left = Animation()
    walking_left.texture = texture
    walking_left.add_frame(sf.Rectangle((32, 32), (32, 32)))
    walking_left.add_frame(sf.Rectangle((64, 32), (32, 32)))
    walking_left.add_frame(sf.Rectangle((32, 32), (32, 32)))
    walking_left.add_frame(sf.Rectangle((0, 32), (32, 32)))

    walking_right = Animation()
    walking_right.texture = texture
    walking_right.add_frame(sf.Rectangle((32, 64), (32, 32)))
    walking_right.add_frame(sf.Rectangle((64, 64), (32, 32)))
    walking_right.add_frame(sf.Rectangle((32, 64), (32, 32)))
    walking_right.add_frame(sf.Rectangle((0, 64), (32, 32)))

    current_anim = walking_down
    anim_sprite = AnimatedSprite(sf.seconds(0.2), True, False)
    anim_sprite.position = sf.Vector2(400, 300)

    frame_clock = sf.Clock()

    speed = 80.0

    no_key_pressed = True

    while window.is_open:
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()

        delta = frame_clock.elapsed_time
        frame_clock.restart()

        movement = sf.Vector2(0.0, 0.0)

        if sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN):
            current_anim = walking_down
            movement += sf.Vector2(0.0, speed)
            no_key_pressed = False

        if sf.Keyboard.is_key_pressed(sf.Keyboard.UP):
            current_anim = walking_up
            movement += sf.Vector2(0.0, -speed)
            no_key_pressed = False

        if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
            current_anim = walking_left
            movement += sf.Vector2(-speed, 0.0)
            no_key_pressed = False

        if sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
            current_anim = walking_right
            movement += sf.Vector2(speed, 0.0)
            no_key_pressed = False

        anim_sprite.play(current_anim)
        anim_sprite.move(movement * delta.seconds)

        if no_key_pressed:
            anim_sprite.stop()
        no_key_pressed = True

        anim_sprite.update(delta)

        window.clear()
        window.draw(anim_sprite)
        window.display()


if __name__ == '__main__':
    main()