
import pygame

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings

class Car:
    def __init__(self, posx: int, skin: int) -> None:
        self.x = posx
        self.y = -settings.TEXTURES["car1"].get_height() +40
        self.width = settings.TEXTURES["car1"].get_width()
        self.height = settings.TEXTURES["car1"].get_height()
        self.skin = skin
        self.vy = 0
        self.rotate = 180
        self.posSet = [470, 610, 745, 883]
    
    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(pygame.transform.rotate(settings.TEXTURES["car"+str(self.skin)],self.rotate) , (self.posSet[self.x], self.y))

    
