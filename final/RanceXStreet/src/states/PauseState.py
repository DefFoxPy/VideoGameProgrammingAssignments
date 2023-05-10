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
        self.opc = params["opc"]
        self.powerups = params["powerups"]
        self.retardo = False
        self.list_icons = [9, 10]
        self.selected = 1
        InputHandler.register_listener(self)
    
    def exit(self) -> None:
        InputHandler.unregister_listener(self)
    
    def update(self,  dt: float) -> None:
        self.retardo = True

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "move_right" and input_data.pressed:
            self.selected = min(2, self.selected + 1)

        elif input_id == "move_left" and input_data.pressed:
            self.selected = max(1, self.selected - 1) 

        elif input_id == "enter" and input_data.pressed and self.retardo:
            if self.selected == 1:
                self.state_machine.change("play", player=self.player, car_list=self.car_list, powerups=self.powerups, datos=self.datos, world = self.world)
            else:
                self.state_machine.change("start")
        
    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
                  
        if self.opc == 0:
            surface.blit(settings.TEXTURES["cartel5"].convert_alpha(), ((settings.VIRTUAL_WIDTH - settings.TEXTURES["cartel5"].get_width()) // 2, (settings.VIRTUAL_HEIGHT - settings.TEXTURES["cartel5"].get_height()) // 2))  
            render_text(
                surface,
                "Pause",
                settings.FONTS["large"],
                settings.VIRTUAL_WIDTH // 2,
                settings.VIRTUAL_HEIGHT // 2,
                settings.COLOR_BLACK,
                center = True,
            )

            render_text(
                surface,
                "Press enter for continue",
                settings.FONTS["medium"],
                settings.VIRTUAL_WIDTH // 2,
                settings.VIRTUAL_HEIGHT // 2 + 200,
                settings.COLOR_BLACK,
                center=True,
            )
        if self.opc == 1:
            surface.blit(settings.TEXTURES["cartel1"].convert_alpha(), ((settings.VIRTUAL_WIDTH - settings.TEXTURES["cartel1"].get_width()) // 2, (settings.VIRTUAL_HEIGHT - settings.TEXTURES["cartel1"].get_height()) // 2)) 

            render_text(
                surface,
                "do you want to go home?",
                settings.FONTS["large"],
                settings.VIRTUAL_WIDTH // 2,
                settings.VIRTUAL_HEIGHT // 2,
                settings.COLOR_BLACK,
                center = True,
            )
            surface.blit(settings.TEXTURES["icons"], (settings.VIRTUAL_WIDTH // 2 - 100, settings.VIRTUAL_HEIGHT // 2 + 33), settings.FRAMES["list_icons"][self.list_icons[0]])
            if self.selected == 1:
                surface.blit(settings.TEXTURES["icons"], (settings.VIRTUAL_WIDTH // 2 - 100, settings.VIRTUAL_HEIGHT // 2 + 33), settings.FRAMES["list_icons"][self.list_icons[0]+24])

            surface.blit(settings.TEXTURES["icons"], (settings.VIRTUAL_WIDTH // 2 + 100 - settings.ICON_WIDTH, settings.VIRTUAL_HEIGHT // 2 + 33), settings.FRAMES["list_icons"][self.list_icons[1]])
            if self.selected == 2:
                surface.blit(settings.TEXTURES["icons"], (settings.VIRTUAL_WIDTH // 2 + 100 - settings.ICON_WIDTH, settings.VIRTUAL_HEIGHT // 2 + 33), settings.FRAMES["list_icons"][self.list_icons[1]+24])
            

