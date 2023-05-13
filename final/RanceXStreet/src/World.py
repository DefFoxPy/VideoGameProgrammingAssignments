import pygame
import settings

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text


class World:
    def __init__(self, map: int) -> None:
        self.displayX = 0
        self.displayY = 0
        self.map = map

    def update(self, dt: float, score: float) -> None:
        self.yRelativa = self.displayY % settings.VIRTUAL_HEIGHT
        self.displayY += settings.PLAYER_SPEED * dt

        self.map = int(score // settings.NEXT_MAP)
        while self.map >= len(settings.LIST_MAP):
            self.map -= len(settings.LIST_MAP)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(
            settings.TEXTURES[settings.LIST_MAP[self.map]].convert_alpha(),
            [self.displayX, self.yRelativa - settings.VIRTUAL_HEIGHT],
        )
        surface.blit(
            settings.TEXTURES["road_0_left"].convert_alpha(),
            [380, self.yRelativa - settings.VIRTUAL_HEIGHT],
        )
        surface.blit(
            settings.TEXTURES["road_0_right"].convert_alpha(),
            [681, self.yRelativa - settings.VIRTUAL_HEIGHT],
        )
        if self.yRelativa < settings.VIRTUAL_HEIGHT:
            surface.blit(
                settings.TEXTURES[settings.LIST_MAP[self.map]].convert_alpha(),
                [self.displayX, self.yRelativa],
            )
            surface.blit(
                settings.TEXTURES["road_0_left"].convert_alpha(), [380, self.yRelativa]
            )
            surface.blit(
                settings.TEXTURES["road_0_right"].convert_alpha(), [681, self.yRelativa]
            )
