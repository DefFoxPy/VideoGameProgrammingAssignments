
import pygame, random

from typing import Any

import settings

class Car:
    def __init__(self, posx: int, skin: int) -> None:
        self.x = posx
        self.y = -settings.CAR_HEIGHT
        self.width = settings.CAR_WIDTH
        self.height = settings.CAR_HEIGHT
        self.skin = skin
        self.set = random.randint(0,3)
        
        if self.x > 1:
            self.rotate = 0
            self.y = settings.VIRTUAL_WIDTH
            
        else:
            self.rotate = 180
    
    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(settings.POS_SET[self.x], self.y, self.width, self.height)
    
    def collides(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())
    
    def update(self, dt: float) -> None:
        if self.x > 1:
            self.vy = -settings.CAR_SPEED[self.skin]
        else:
            aux = list(reversed(settings.CAR_SPEED))
            self.vy = aux[self.skin]
            
        self.y += self.vy * dt

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(pygame.transform.rotate(settings.TEXTURES["Set_vehicle"+str(self.set)].convert_alpha(),self.rotate) , (settings.POS_SET[self.x], self.y), settings.FRAMES["list_cars"][self.skin])
    
