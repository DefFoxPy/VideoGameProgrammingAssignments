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
        self.list_icons = [14, 18, 8]
        InputHandler.register_listener(self)
    
    def exit(self) -> None:
        InputHandler.unregister_listener(self)
    
    def update(self, dt: float) -> None:
        self.time_display += 1
        if self.time_display > 2:
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
                self.state_machine.change("highScore")
        
    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["EscenaGameOver"].convert_alpha(), (0, 0))
        surface.blit(settings.TEXTURES["cartel2"].convert_alpha(), (0, 0))
        render_text(
            surface,
            "Game Over",
            settings.FONTS["largePlus"],
            875,
            215,
            settings.COLOR_BLACK,
            center = True,
        )
        
        color_display = settings.COLOR_LIGHT
        font_display = settings.FONTS["medium"]
        if self.display:
            color_display = settings.COLOR_ORANGE
            font_display = settings.FONTS["mediumPlus"]

        render_text(
            surface,
            "Your score: " + str(self.score) + " km",
            font_display,
            875,
            290,
            color_display,
            center = True,
        )
       
        color = settings.COLOR_LIGHT
        font = settings.FONTS["small"]
        self.list_icons[0] = 14
        if self.selected == 1:
            color = settings.COLOR_BLACK
            font = settings.FONTS["smallPlus"]
            self.list_icons[0] = 38        
        render_text(
            surface,
            "Restart",
            font,
            850 - settings.ICON_WIDTH - 90,
            380 + settings.ICON_HEIGHT + 25,
            color,
            center= False,
        )

        color = settings.COLOR_LIGHT
        font = settings.FONTS["small"]
        self.list_icons[1] = 18
        if self.selected == 2:
            self.list_icons[1] = 42
            color = settings.COLOR_BLACK
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

        color = settings.COLOR_LIGHT
        font = settings.FONTS["small"]
        self.list_icons[2] = 8
        if self.selected == 3:
            color = color = settings.COLOR_BLACK
            font = settings.FONTS["smallPlus"]
            self.list_icons[2] = 32
        
        render_text(
            surface,
            "High Score",
            font,
            850 + settings.ICON_WIDTH + 30,
            380 + settings.ICON_HEIGHT + 25,
            color,
            center= False,
        )

        surface.blit(settings.TEXTURES["icons"].convert_alpha(), (850 - settings.ICON_WIDTH -70, 380), settings.FRAMES["list_icons"][self.list_icons[0]])
        surface.blit(settings.TEXTURES["icons"].convert_alpha(), (850,380), settings.FRAMES["list_icons"][self.list_icons[1]])
        surface.blit(settings.TEXTURES["icons"].convert_alpha(), (850 + settings.ICON_WIDTH + 70, 380), settings.FRAMES["list_icons"][self.list_icons[2]])
 