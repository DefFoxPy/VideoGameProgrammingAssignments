import pygame 

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings

class GameOverState(BaseState):
    def enter(self, score: float) -> None:
        self.score = score
        self.selected = 2
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
                self.state_machine.change("start")
            else:
                pygame.quit()
        
    def render(self, surface: pygame.Surface) -> None:
        render_text(
            surface,
            "Game Over",
            settings.FONTS["large"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2,
            (0,0,0),
            center = True,
        )
        render_text(
            surface,
            "Your score: " + str(self.score) + "km",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 + 50,
            (255, 175,37),
            center = True,
        )
        color = (206,173,139)
        font = settings.FONTS["small"]
        if self.selected == 1:
            color = (255, 175,37)
            font = settings.FONTS["smallPlus"]
        
        render_text(
            surface,
            "Restart",
            font,
            1030,
            480,
            color,
            center= False,
        )
        color = (206,173,139)
        font = settings.FONTS["small"]
        if self.selected == 2:
            color = (255, 175,37)
            font = settings.FONTS["smallPlus"]
        
        render_text(
            surface,
            "Home",
            font,
            1030,
            540,
            color,
            center= False,
        )

        color = (206,173,139)
        font = settings.FONTS["small"]
        if self.selected == 3:
            color = (255, 175,37)
            font = settings.FONTS["smallPlus"]
        
        render_text(
            surface,
            "Exit",
            font,
            1030,
            600,
            color,
            center= False,
        )
