import pygame 

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings

class PauseState(BaseState):

    def enter(self, **params: dict) -> None:
        self.score = params["score"]
        self.player = params["player"]
        self.car_list = params["car_list"]
        self.datos = params["datos"]
        InputHandler.register_listener(self)
    
    def exit(self) -> None:
        InputHandler.unregister_listener(self)
    
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter":
            self.state_machine.change("play", player=self.player, score=self.score, car_list=self.car_list, datos=self.datos)
        
    def render(self, surface: pygame.Surface) -> None:
        render_text(
            surface,
            "Pause",
            settings.FONTS["large"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2,
            (0,0,0),
            center = True,
        )
