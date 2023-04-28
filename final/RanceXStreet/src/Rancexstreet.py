"""
This module was autogenerated by gale.
"""
import pygame

from gale.game import Game
from gale.input_handler import InputData, InputHandler, InputListener
from gale.state_machine import StateMachine

import settings

from src import states

class Rancexstreet(Game):
    def init(self) -> None:
        InputHandler.register_listener(self)
        self.state_machine = StateMachine(
            {   
                "start": states.StartState,
                "carSelect": states.CarSelectState,
                "play": states.PlayState,
                "gameOver": states.GameOverState,
                "pause": states.PauseState, 
            }
        )
        self.state_machine.change("start")
        InputHandler.register_listener(self)

    def update(self, dt: float) -> None:
        self.state_machine.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["background"],[0, 0])
        self.state_machine.render(surface)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if (input_id == 'quit' and input_data.pressed):
            self.quit()
