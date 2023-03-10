"""
ISPPJ1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class to define the Play state.
"""
import random

import pygame

from gale.factory import AbstractFactory
from gale.state_machine import BaseState
from gale.input_handler import InputHandler, InputData, InputData
from gale.text import render_text
from gale.factory import Factory
from src.Missile import Missile

import settings
import src.powerups


class PlayState(BaseState):
    def enter(self, **params: dict):
        self.level = params["level"]
        self.score = params["score"]
        self.lives = params["lives"]
        self.paddle = params["paddle"]
        self.balls = params["balls"]
        self.missiles = params["missiles"]
        self.brickset = params["brickset"]
        self.live_factor = params["live_factor"]
        self.points_to_next_live = params["points_to_next_live"]
        self.points_to_next_grow_up = (
            self.score
            + settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
        )
        self.powerups = params.get("powerups", [])
        self.catchBall = False
        self.cannons = False
        self.active = False

        if not params.get("resume", False):
            self.balls[0].vx = random.randint(-80, 80)
            self.balls[0].vy = random.randint(-170, -100)
            settings.SOUNDS["paddle_hit"].play()

        self.powerups_abstract_factory = AbstractFactory("src.powerups")

        InputHandler.register_listener(self)

    def exit(self) -> None:
        InputHandler.unregister_listener(self)

    def update(self, dt: float) -> None:
        self.paddle.update(dt)
        self.catchBall = self.paddle.catchBall
        self.cannons = self.paddle.cannons

        for ball in self.balls:
            ball.update(dt)
            ball.solve_world_boundaries()
            
            # Check collision with the paddle
            if ball.collides(self.paddle):
                
                if not self.catchBall:
                    settings.SOUNDS["paddle_hit"].stop()
                    settings.SOUNDS["paddle_hit"].play()
                    
                    if ball.vy == 0:
                        ball.vy = random.randint(-170, -100)
                        ball.vx = random.randint(-80,80)
                    
                    ball.rebound(self.paddle)
                    ball.push(self.paddle)
                    
                else:
                    ball.vy = 0
                    
                    # Holds the ball attached to the paddle
                    if self.paddle.x != 0 and (self.paddle.x + self.paddle.width) < settings.VIRTUAL_WIDTH: 
                        ball.vx = self.paddle.vx
                    else:
                        ball.vx = 0

            # Check collision with brickset
            if not ball.collides(self.brickset):
                continue

            brick = self.brickset.get_colliding_brick(ball.get_collision_rect())

            if brick is None:
                continue

            brick.hit()
            self.score += brick.score()
            ball.rebound(brick)

            # Check earn life
            if self.score >= self.points_to_next_live:
                settings.SOUNDS["life"].play()
                self.lives = min(3, self.lives + 1)
                self.live_factor += 0.5
                self.points_to_next_live += settings.LIVE_POINTS_BASE * self.live_factor

            # Check growing up of the paddle
            if self.score >= self.points_to_next_grow_up:
                settings.SOUNDS["grow_up"].play()
                self.points_to_next_grow_up += (
                    settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
                )
                self.paddle.inc_size()

            # Chance to generate two more balls
            if random.random() < 0.1:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("TwoMoreBall").create(
                        r.centerx - 8, r.centery - 8
                    )
                )

            # Chance to generate CatchBall
            elif random.random() < 0.1:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("CatchBall").create(
                        r.centerx - 8, r.centery - 8
                    )
                )
            
            # Chance to generate Cannons
            elif random.random() < 0.1:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("Cannons").create(
                        r.centerx - 8, r.centery - 8
                    )
                )

        # update missile
        for missile in self.missiles:
            missile.update(dt)
            missile.solve_world_boundaries()

            #Check collision with brickset
            if not missile.collides(self.brickset):
                continue

            brick = self.brickset.get_colliding_brick(missile.get_collision_rect())

            if brick is None:
                continue

            brick.hit()
            self.score += brick.score()
            missile.in_play = False

        # Removing all balls that are not in play
        self.balls = [ball for ball in self.balls if ball.in_play]
        self.missiles = [missile for missile in self.missiles if missile.in_play]

        self.brickset.update(dt)

        if not self.balls:
            self.lives -= 1
            self.paddle.catchBall = False
            self.paddle.cannons = False
            if self.lives == 0:
                self.state_machine.change("game_over", score=self.score)
            else:
                self.paddle.dec_size()
                self.state_machine.change(
                    "serve",
                    level=self.level,
                    score=self.score,
                    lives=self.lives,
                    paddle=self.paddle,
                    brickset=self.brickset,
                    points_to_next_live=self.points_to_next_live,
                    live_factor=self.live_factor,
                )

        # Update powerups
        for powerup in self.powerups:
            powerup.update(dt)

            if powerup.collides(self.paddle):
                powerup.take(self)

        # Remove powerups that are not in play
        self.powerups = [p for p in self.powerups if p.in_play]

        # Check victory
        if self.brickset.size == 1 and next(
            (True for _, b in self.brickset.bricks.items() if b.broken), False
        ):
            self.state_machine.change(
                "victory",
                lives=self.lives,
                level=self.level,
                score=self.score,
                paddle=self.paddle,
                balls=self.balls,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
            )

    def render(self, surface: pygame.Surface) -> None:
        heart_x = settings.VIRTUAL_WIDTH - 120

        i = 0
        # Draw filled hearts
        while i < self.lives:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][0]
            )
            heart_x += 11
            i += 1

        # Draw empty hearts
        while i < 3:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][1]
            )
            heart_x += 11
            i += 1

        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["tiny"],
            settings.VIRTUAL_WIDTH - 80,
            5,
            (255, 255, 255),
        )

        self.brickset.render(surface)

        self.paddle.render(surface)

        for ball in self.balls:
            ball.render(surface)

        for powerup in self.powerups:
            powerup.render(surface)

        for missile in self.missiles:
            missile.render(surface)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "move_left":
            if input_data.pressed:
                self.paddle.vx = -settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx < 0:
                self.paddle.vx = 0
        elif input_id == "move_right":
            if input_data.pressed:
                self.paddle.vx = settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx > 0:
                self.paddle.vx = 0
        elif input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "pause",
                level=self.level,
                score=self.score,
                lives=self.lives,
                paddle=self.paddle,
                balls=self.balls,
                missiles=self.missiles,
                brickset=self.brickset,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
                powerups=self.powerups,
            )
        if input_id == "enter" and self.catchBall:
            self.paddle.catchBall = False

        if input_id == "shot" and self.cannons:
            missil = Missile(self.paddle.x + self.paddle.width//2, self.paddle.y - 8)
            self.missiles.append(missil) 
            self.paddle.cannons = False
