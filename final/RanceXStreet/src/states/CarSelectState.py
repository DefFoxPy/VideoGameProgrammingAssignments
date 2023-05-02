
import pygame 

from gale.state_machine import BaseState
from gale.input_handler import InputHandler, InputData
from gale.text import render_text

import settings
from src.Player import Player

class CarSelectState(BaseState):
    def enter(self) -> None:
        self.player = Player((settings.VIRTUAL_WIDTH - settings.CAR_WIDTH) // 2 , (settings.VIRTUAL_HEIGHT - settings.CAR_HEIGHT) // 2)
        self.player.rotate = 0
        self.retardo = False
        self.displayX = 0.0
        self.display = True
        self.time_display = 0
        InputHandler.register_listener(self)
  
    def exit(self) -> None:
        InputHandler.unregister_listener(self)

    def update(self, dt: float) -> None:
        self.retardo = True
        if self.displayX < settings.VIRTUAL_WIDTH * 2:
            self.displayX += (settings.VIRTUAL_WIDTH // 10.0) * 2
        self.time_display += 1
        if self.time_display > 1:
            self.display = not self.display
            self.time_display = 0

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "move_right" and input_data.pressed:           
            self.player.skin = min(8, self.player.skin + 1)
        elif input_id == "move_left" and input_data.pressed:
            self.player.skin = max(0, self.player.skin - 1)
        elif input_id == "move_down" and input_data.pressed:
            self.player.set = min(3, self.player.set + 1)
        elif input_id == "move_up" and input_data.pressed:
            self.player.set = max(0, self.player.set - 1)
        elif input_id == "enter" and input_data.pressed and self.retardo:
            self.state_machine.change("play", player=self.player, car_list=[], datos=[0, 0, [], []])

    def render(self, surface: pygame.Surface) -> None:    
        if self.displayX < settings.VIRTUAL_WIDTH:
            surface.blit(settings.TEXTURES["EscenaStar"], [self.displayX,0])
        elif self.displayX < settings.VIRTUAL_WIDTH * 2:
            surface.blit(settings.TEXTURES["EscenaSelect"], (self.displayX - settings.VIRTUAL_WIDTH *2, 0))
        else:    
            surface.blit(settings.TEXTURES["EscenaSelect"], (0, 0))
            surface.blit(settings.TEXTURES["cartel1"], ((settings.VIRTUAL_WIDTH - settings.TEXTURES["cartel1"].get_width()) // 2, (settings.VIRTUAL_HEIGHT - settings.TEXTURES["cartel1"].get_height()) // 2))
            
            render_text(
            surface,
            "Select your car",
            settings.FONTS["largePlus"],
            settings.VIRTUAL_WIDTH // 2,
            110,
            (0, 0, 0),
            center= True,
            )

            color_display = (206,173,139)
            font_display = settings.FONTS["medium"]
            if self.display:
                color_display = (255, 175,37)
                font_display = settings.FONTS["mediumPlus"]

            render_text(
                surface,
                "Press enter for play",
                font_display,
                settings.VIRTUAL_WIDTH // 2,
                (settings.VIRTUAL_HEIGHT + settings.TEXTURES["cartel1"].get_height()) // 2 + 45,
                color_display,
                center = True,
            )

            #icon left           
            if self.player.skin == 0:
                surface.blit(settings.TEXTURES["icons"], ((settings.VIRTUAL_WIDTH) // 2 - 130 - settings.ICON_WIDHT, (settings.VIRTUAL_HEIGHT) // 2 - 45), settings.FRAMES["list_icons"][2])
            else:
                surface.blit(settings.TEXTURES["icons"], ((settings.VIRTUAL_WIDTH) // 2 - 130 - settings.ICON_WIDHT, (settings.VIRTUAL_HEIGHT) // 2 - 40), settings.FRAMES["list_icons"][26])

            #icon right                        
            self.player.render(surface)
            if self.player.skin == 8:
                surface.blit(settings.TEXTURES["icons"], ((settings.VIRTUAL_WIDTH) // 2 + 130, (settings.VIRTUAL_HEIGHT) // 2 - 45), settings.FRAMES["list_icons"][3]) 
            else:
                surface.blit(settings.TEXTURES["icons"], ((settings.VIRTUAL_WIDTH) // 2 + 130, (settings.VIRTUAL_HEIGHT) // 2 - 40), settings.FRAMES["list_icons"][27]) 
            self.player.render(surface)
        