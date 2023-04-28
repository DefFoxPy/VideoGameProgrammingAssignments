import pygame 

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings

class GameOverState(BaseState):
    def enter(self, score: float) -> None:
        self.score = score
        self.selected = 2
        self.time_display = 0
        self.display = True
        InputHandler.register_listener(self)
    
    def exit(self) -> None:
        InputHandler.unregister_listener(self)
    
    def update(self, dt: float) -> None:
        self.time_display += 1
        if self.time_display > 1:
            self.display = not self.display
            self.time_display = 0
            
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
        surface.blit(settings.TEXTURES["EscenaGameOver"], (0, 0))
        surface.blit(settings.TEXTURES["cartel2"], (0, 0))
        render_text(
            surface,
            "Game Over",
            settings.FONTS["largePlus"],
            875,
            215,
            (0,0,0),
            center = True,
        )
        
        color_display = (206,173,139)
        font_display = settings.FONTS["medium"]
        if self.display:
            color_display = (255, 175,37)
            font_display = settings.FONTS["mediumPlus"]

        render_text(
            surface,
            "Your score: " + str(self.score) + "km",
            font_display,
            875,
            290,
            color_display,
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
            850 - settings.ICON_WIDHT - 90,
            380 + settings.ICON_HEIGHT + 25,
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
            850,
            380 + settings.ICON_HEIGHT + 25,
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
            850 + settings.ICON_WIDHT + 80,
            380 + settings.ICON_HEIGHT + 25,
            color,
            center= False,
        )

        if self.selected == 1:
            surface.blit(settings.TEXTURES["icons"], (850 - settings.ICON_WIDHT -70, 380), settings.FRAMES["list_icons"][38])
        else:
            surface.blit(settings.TEXTURES["icons"], (850 - settings.ICON_WIDHT -70, 380), settings.FRAMES["list_icons"][14])

        if self.selected == 2:
            surface.blit(settings.TEXTURES["icons"], (850,380), settings.FRAMES["list_icons"][42])
        else:
            surface.blit(settings.TEXTURES["icons"], (850,380), settings.FRAMES["list_icons"][18])

        if self.selected == 3:
            surface.blit(settings.TEXTURES["icons"], (850 + settings.ICON_WIDHT + 70, 380), settings.FRAMES["list_icons"][33])
        else:
            surface.blit(settings.TEXTURES["icons"], (850 + settings.ICON_WIDHT + 70, 380), settings.FRAMES["list_icons"][9])

