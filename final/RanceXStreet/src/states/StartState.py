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
        if input_id == "move_down" and input_data.pressed and self.selected == 1:
            self.selected = 2
        elif input_id == "move_down" and input_data.pressed and self.selected == 2:
            self.selected = 3
        elif input_id == "move_up" and input_data.pressed and self.selected == 3:
            self.selected = 2
        elif input_id == "move_up" and input_data.pressed and self.selected == 2:
            self.selected = 1
        elif input_id == "enter" and input_data.pressed:

            if self.selected == 1:
                print("Play")
                self.state_machine.change("play")
            elif self.selected == 2:
                print("Higt_score")
            else:
                print("Exit")
    
    def render(self, surface: pygame.surface) -> None:
        surface.fill([0, 255, 0])
        render_text(
            surface,
            "RanceXStreet",
            settings.FONTS["large"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 3,
            (255, 0, 0),
            center=True
        )
        color = (52, 235, 216)
        if self.selected == 1:
            color = (255, 255, 255)
        
        render_text(
            surface,
            "Play Game",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT - 90,
            color,
            center= True,
        )

        color = (52, 235, 216)
        if self.selected == 2:
            color = (255, 255, 255)
        
        render_text(
            surface,
            "High scores",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT - 75,
            color,
            center= True,
        )

        color = (52, 235, 216)
        if self.selected == 3:
            color = (255, 255, 255)
        
        render_text(
            surface,
            "Exit",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT - 60,
            color,
            center= True,
        )
        
            
        
        