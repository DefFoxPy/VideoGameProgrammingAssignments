
import pygame

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings
from src.utilities.highscores import read_highscores

class HighScoreState(BaseState):
    def enter(self) -> None:
        self.hs = read_highscores()
        self.retardo = False
        InputHandler.register_listener(self)
    
    def exit(self) -> None:
        InputHandler.unregister_listener(self)
    
    def update(self, dt: float) -> None:
        self.retardo = True

    def on_input(self, input_id: str, input_data: InputData):
        if input_id == "enter" and input_data.pressed and self.retardo:
            self.state_machine.change("start")
    
    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["cartel4"], (0, 0))
        render_text(
            surface,
            "High Scores",
            settings.FONTS["largePlus"],
            820,
            195,
            settings.COLOR_ORANGE_DARK,
            center=True,
        )

        for i in range(settings.NUM_HIGHSCORES):
            name = "***"
            score = "***"

            if i < len(self.hs):
                item = self.hs[i]
                name = item[0]
                score = str(item[1])
            
            color = settings.COLOR_ORANGE
            if i%2 == 0:
                color = settings.COLOR_BLACK

            render_text(
                surface,
                f"{i + 1}.",
                settings.FONTS["medium"],
                settings.VIRTUAL_WIDTH // 2 + 50,
                230 + i * 45,
                color,
                center = False,
            )

            render_text(
                surface,
                name,
                settings.FONTS["medium"],
                settings.VIRTUAL_WIDTH // 2 + 90,
                230 + i * 45,
                color,
                center = False,
            )
            render_text(
                surface,
                str(score) + "km",
                settings.FONTS["medium"],
                settings.VIRTUAL_WIDTH // 2 + 190,
                230 + i * 45,
                color,
                center = False,
            )

        render_text(
            surface,
            "Press enter for continue",
            settings.FONTS["mediumPlus"],
            820,
            650,
            settings.COLOR_BLACK,
            center=True,
        )

