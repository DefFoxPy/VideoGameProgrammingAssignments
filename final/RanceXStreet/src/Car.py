
import pygame, random

from typing import Any

import settings

class Car:
    def __init__(self, posx: int, skin: int) -> None:
        self.x = posx
        self.y = -settings.TEXTURES["car1"].get_height()
        self.width = settings.TEXTURES["car1"].get_width()
        self.height = settings.TEXTURES["car1"].get_height()
        self.skin = skin
        if self.x > 1:
            self.rotate = 0
            if settings.CAR_SPEED[self.skin] == settings.MAX_CAR_SPEED:
                self.vy = settings.MIN_CAR_SPEED
            elif settings.CAR_SPEED[self.skin] == settings.MIN_CAR_SPEED:
                self.vy = settings.MAX_CAR_SPEED
            else:
                self.vy = settings.CAR_SPEED[self.skin] - settings.MIN_CAR_SPEED
        else:
            self.rotate = 180
            self.vy = settings.CAR_SPEED[self.skin]
    
    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(settings.POS_SET[self.x], self.y, self.width, self.height)
    
    def collides(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())
    
    def update(self, dt: float) -> None:
        self.y += self.vy

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(pygame.transform.rotate(settings.TEXTURES["car"+str(self.skin)],self.rotate) , (settings.POS_SET[self.x], self.y))

    
