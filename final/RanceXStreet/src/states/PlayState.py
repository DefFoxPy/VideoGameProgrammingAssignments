
import pygame

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings

class PlayState(BaseState):
    def render(self, surface: pygame.Surface) -> None:
        #surface.fill([150, 255, 20])
        surface.blit(settings.TEXTURES["Soil_Tile"],[0,0])
        surface.blit(settings.TEXTURES["road_0_left"],[380,0])
        surface.blit(settings.TEXTURES["road_0_right"],[730,0])
        pygame.display.flip()
        