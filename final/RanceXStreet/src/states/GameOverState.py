import pygame 

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings

class GameOverState(BaseState):
    def enter(self, score: float) -> None:
        self.socre = score
        self.selected = 1
        InputHandler.register_listener(self)
    
    def exit(self) -> None:
        InputHandler.unregister_listener(self)
    
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "move_right" and input_data.pressed:
            self.selected = min(3, self.selected + 1)

        elif input_id == "move_left" and input_data.pressed:
            self.selected = max(1, self.selected - 1) 

        elif input_id == "enter" and input_data.pressed:

            if self.selected == 1:
                self.state_machine.change("carSelect")
            elif self.selected == 2:
                pass
            else:
                pygame.quit()