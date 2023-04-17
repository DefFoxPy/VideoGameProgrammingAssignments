import pygame

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings

class StartState(BaseState):
    def enter(self) -> None:
        self.selected = 1
        InputHandler.register_listener(self)
    
    def exit(self)  -> None:
        InputHandler.unregister_listener(self)
    
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "move_down" and input_data.pressed:
            self.selected = min(3, self.selected + 1)

        elif input_id == "move_up" and input_data.pressed:
            self.selected = max(1, self.selected - 1) 

        elif input_id == "enter" and input_data.pressed:

            if self.selected == 1:
                print("Play")
                self.state_machine.change("play")
            elif self.selected == 2:
                print("Higt_score")
            else:
                pygame.quit()
    
    def render(self, surface: pygame.surface) -> None:
        surface.blit(settings.TEXTURES["startstate"], (0, 0))

        color = (206,173,139)
        font = settings.FONTS["medium"]
        if self.selected == 1:
            color = (255, 175,37)
            font = settings.FONTS["mediumPlus"]
        
        render_text(
            surface,
            "Play Game",
            font,
            1050,
            480,
            color,
            center= False,
        )

        color = (206,173,139)
        font = settings.FONTS["medium"]
        if self.selected == 2:
            color = (255, 175,37)
            font = settings.FONTS["mediumPlus"]
        
        render_text(
            surface,
            "High scores",
            font,
            1030,
            540,
            color,
            center= False,
        )

        color = (206,173,139)
        font = settings.FONTS["medium"]
        if self.selected == 3:
            color = (255, 175,37)
            font = settings.FONTS["mediumPlus"]
        
        render_text(
            surface,
            "Exit",
            font,
            1160,
            600,
            color,
            center= False,
        )
        
            
        
        