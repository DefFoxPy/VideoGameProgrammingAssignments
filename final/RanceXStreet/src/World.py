import pygame
import settings

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

class World:
    def __init__(self) -> None:
        self.displayX = 0
        self.displayY = 0

    def update(self, dt: float, score: float) -> None:
        self.score = score
        self.yRelativa = self.displayY % settings.VIRTUAL_HEIGHT
        self.displayY += 50         

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["Soil_Tile"],[self.displayX, self.yRelativa - settings.VIRTUAL_HEIGHT])        
        surface.blit(settings.TEXTURES["road_0_left"],[380, self.yRelativa - settings.VIRTUAL_HEIGHT])
        surface.blit(settings.TEXTURES["road_0_right"],[681, self.yRelativa - settings.VIRTUAL_HEIGHT])
        if self.yRelativa < settings.VIRTUAL_HEIGHT:
            surface.blit(settings.TEXTURES["Soil_Tile"],[self.displayX, self.yRelativa])
            surface.blit(settings.TEXTURES["road_0_left"],[380, self.yRelativa])
            surface.blit(settings.TEXTURES["road_0_right"],[681, self.yRelativa])
        
        