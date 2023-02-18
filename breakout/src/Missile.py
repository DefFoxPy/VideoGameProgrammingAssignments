"""
ISPPJ1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Missile.
"""
import random
from typing import Any, Tuple, Optional

import pygame

import settings
from src.Paddle import Paddle


class Missile:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 20
        self.height = 16

        self.vy = 0

        self.texture = settings.TEXTURES["spritesheet"]
        self.frame = 7
        self.in_play = True

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collides(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())

    def update(self, dt: float) -> None:
        self.y += self.vy * dt

    def render(self, surface):
        surface.blit(
            self.texture, (self.x, self.y), settings.FRAMES["missile"][1]
        )

    @staticmethod
    def get_intersection(r1: pygame.Rect, r2: pygame.Rect) -> Optional[Tuple[int, int]]:
        """
        Compute, if exists, the intersection between two
        rectangles.
        """
        if r1.x > r2.right or r1.right < r2.x or r1.bottom < r2.y or r1.y > r2.bottom:
            # There is no intersection
            return None

        # Compute x shift
        if r1.centerx < r2.centerx:
            x_shift = r2.x - r1.right
        else:
            x_shift = r2.right - r1.x

        # Compute y shift
        if r1.centery < r2.centery:
            y_shift = r2.y - r1.bottom
        else:
            y_shift = r2.bottom - r1.y

        return (x_shift, y_shift)

    

