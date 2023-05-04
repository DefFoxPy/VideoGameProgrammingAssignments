import pygame 

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings

class PauseState(BaseState):

    def enter(self, **params: dict) -> None:
        self.player = params["player"]
        self.car_list = params["car_list"]
        self.datos = params["datos"]
        self.world = params["world"]
        InputHandler.register_listener(self)
    
    def exit(self) -> None:
        InputHandler.unregister_listener(self)
    
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter":
            self.state_machine.change("play", player=self.player, car_list=self.car_list, datos=self.datos, world = self.world)
        
    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        render_text(
            surface,
            "Pause",
            settings.FONTS["large"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2,
            settings.COLOR_BLACK,
            center = True,
        )
