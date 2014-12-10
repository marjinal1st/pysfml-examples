#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sfml as sf
from random import randint

WWIDTH, WHEIGHT = 800, 600
WTITLE = "PySFML Pong"
PADDLE_SPEED = 10.0
MAX_BALL_SPEED = 2500.0

def run():
    window = sf.RenderWindow(sf.VideoMode(WWIDTH, WHEIGHT), WTITLE)
    window.framerate_limit = 60

    # Background
    bg_texture = sf.Texture.from_file("assets/images/background.png")
    background = sf.Sprite(bg_texture)

    # Ball
    b_texture = sf.Texture.from_file("assets/images/ball.png")
    ball = sf.CircleShape(35)
    ball.texture = b_texture
    ball.origin = 35, 35
    ball.position = WWIDTH / 2.0, WHEIGHT / 2.0

    speed = sf.Vector2(randint(-5, 5), randint(-5, 5)) * 50.0

    # Paddle 1
    paddle_1 = sf.RectangleShape((50, 175))
    paddle_1.origin = 25.0, 82.5
    paddle_1.position = 50, WHEIGHT / 2.0

    # Paddle 2
    paddle_2 = sf.RectangleShape((50, 175))
    paddle_2.origin = 25.0, 82.5
    paddle_2.position = WWIDTH - 50, WHEIGHT / 2.0

    # Scores
    scored = False
    p1_score, p2_score = 0, 0

    # Font
    font = sf.Font.from_file("assets/fonts/kenvector.ttf")
    
    # Texts
    p1_score_text = sf.Text(str(p1_score))
    p1_score_text.font = font
    p1_score_text.character_size = 72
    p1_score_text.color = sf.Color.WHITE
    p1_score_text.position = 170, 100

    p2_score_text = sf.Text(str(p2_score))
    p2_score_text.font = font
    p2_score_text.character_size = 72
    p2_score_text.color = sf.Color.WHITE
    p2_score_text.position = 570, 100

    # Sound
    s_buffer = sf.SoundBuffer.from_file("assets/sounds/tone1.ogg")

    sound = sf.Sound(s_buffer)

    # Clock
    clock = sf.Clock()

    while window.is_open:
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()
        # Close
        if sf.Keyboard.is_key_pressed(sf.Keyboard.ESCAPE):
            window.close()

        elapsed = clock.elapsed_time.seconds
        clock.restart()

        # Inputs
        if sf.Keyboard.is_key_pressed(sf.Keyboard.W):
            paddle_1.move(sf.Vector2(0, -PADDLE_SPEED))
            
            if paddle_1.position.y < paddle_1.origin.y:
                paddle_1.position = sf.Vector2(paddle_1.position.x, paddle_1.origin.y)

        if sf.Keyboard.is_key_pressed(sf.Keyboard.S):
            paddle_1.move(sf.Vector2(0, PADDLE_SPEED))

            if paddle_1.position.y > WHEIGHT - paddle_1.origin.y:
                paddle_1.position = sf.Vector2(paddle_1.position.x, WHEIGHT - paddle_1.origin.y)

        if sf.Keyboard.is_key_pressed(sf.Keyboard.UP):
            paddle_2.move(sf.Vector2(0, -PADDLE_SPEED))

            if paddle_2.position.y < paddle_2.origin.y:
                paddle_2.position = sf.Vector2(paddle_2.position.x, paddle_2.origin.y)

        if sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN):
            paddle_2.move(sf.Vector2(0, PADDLE_SPEED))

            if paddle_2.position.y > WHEIGHT - paddle_2.origin.y:
                paddle_2.position = sf.Vector2(paddle_2.position.x, WHEIGHT - paddle_2.origin.y)

        if scored:
            speed = sf.Vector2(randint(-5, 5), randint(-5, 5)) * 50.0
            ball.position = WWIDTH / 2.0, WHEIGHT / 2.0
            paddle_1.position = 50, WHEIGHT / 2.0
            paddle_2.position = WWIDTH - 50, WHEIGHT / 2.0
            scored = False

        ball.move(speed * elapsed)

        if ball.position.x < ball.origin.x or ball.position.x > WWIDTH - ball.origin.x:
            #speed = sf.Vector2(speed.x * -1.0, speed.y)
            scored = True

            if ball.position.x < ball.origin.x:
                p2_score += 1
            else:
                p1_score += 1

            p1_score_text.string = str(p1_score)
            p2_score_text.string = str(p2_score)

        if ball.position.y < ball.origin.y or ball.position.y > WHEIGHT - ball.origin.y:
            speed = sf.Vector2(speed.x, speed.y * -1.0)

        p1_col = ball.global_bounds.intersects(paddle_1.global_bounds)
        if p1_col:
            sound.play()            
            if p1_col.top + p1_col.height / 2.0 > paddle_1.position.y:
                y = (-1.0, 1.0)[speed.y > 0]
            else:
                y = (1.0, -1.0)[speed.y > 0]

            x_factor = (1.0, 1.05)[-MAX_BALL_SPEED < speed.x < MAX_BALL_SPEED]
            
            speed = sf.Vector2(speed.x * -1.0 * x_factor, speed.y * y)


        p2_col = ball.global_bounds.intersects(paddle_2.global_bounds)
        if p2_col:
            sound.play()
            if p2_col.top + p2_col.height / 2.0 > paddle_2.position.y:
                y = (-1.0, 1.0)[speed.y > 0]
            else:
                y = (1.0, -1.0)[speed.y > 0]

            x_factor = (1.0, 1.05)[-MAX_BALL_SPEED < speed.x < MAX_BALL_SPEED]

            speed = sf.Vector2(speed.x * -1.0 * x_factor, speed.y * y)

        # Rendering
        window.clear(sf.Color.BLACK)

        window.draw(background)
        window.draw(ball)
        window.draw(paddle_1)
        window.draw(paddle_2)
        window.draw(p1_score_text)
        window.draw(p2_score_text)
        
        window.display()

if __name__ == '__main__':
    run()