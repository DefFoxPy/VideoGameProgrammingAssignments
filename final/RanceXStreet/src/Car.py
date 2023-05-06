
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
        self.set = random.randint(0,3)
        if self.x > 1:
            self.rotate = 0
            self.y = settings.VIRTUAL_WIDTH
            if settings.CAR_SPEED[self.skin] == settings.MAX_CAR_SPEED:
                self.vy = -settings.MIN_CAR_SPEED
            elif settings.CAR_SPEED[self.skin] == settings.MIN_CAR_SPEED:
                self.vy = -settings.MAX_CAR_SPEED
            else:
                self.vy = -abs(settings.CAR_SPEED[self.skin] - settings.MIN_CAR_SPEED)
        else:
            self.rotate = 180
            aux = list(reversed(settings.CAR_SPEED))
            self.vy = aux[self.skin]
    
    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(settings.POS_SET[self.x], self.y, self.width, self.height)
    
    def collides(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())
    
    def update(self, dt: float) -> None:
        self.y += self.vy

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(pygame.transform.rotate(settings.TEXTURES["Set_vehicle"+str(self.set)],self.rotate) , (settings.POS_SET[self.x], self.y), settings.FRAMES["list_cars"][self.skin])
    
