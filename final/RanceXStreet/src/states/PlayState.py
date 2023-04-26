
import pygame, random

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text
from typing import Dict, Tuple

import settings

from src.Car import Car

class PlayState(BaseState):
    def enter(self, **params: dict) -> None:  
        self.player = params["player"]
        self.player.rotate = 0
        self.player.x = settings.POS_SET[1]
        self.player.y = settings.VIRTUAL_HEIGHT - settings.TEXTURES["car1"].get_height()
        self.displayX = 0
        self.displayY = 0
        self.car_list = []
        self.time_car = 0
        self.time_game_over = 0
        
        InputHandler.register_listener(self)
        
    def update(self, dt: float) -> None:
        self.player.update(dt)
        self.yRelativa = self.displayY % settings.VIRTUAL_HEIGHT
        self.displayY += 50         
        self.time_car += 1 
        if self.time_car == 8:
            car = Car(posx = random.randint(0,settings.NUM_VIAS-1), skin= random.randint(0,settings.NUM_SKIN-1))
            self.car_list.append(car)
            self.time_car = 0

        for car in self.car_list:
            car.update(dt)
            if car.collides(self.player):
                print("colision")
                self.time_game_over += 1
                if self.time_game_over == 2: ## para crear el efecto de humo
                    self.state_machine.change("carSelect")
            if car.y > settings.VIRTUAL_HEIGHT:
                self.car_list.pop(0)
            
    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["Soil_Tile"],[self.displayX, self.yRelativa - settings.VIRTUAL_HEIGHT])        
        surface.blit(settings.TEXTURES["road_0_left"],[380, self.yRelativa - settings.VIRTUAL_HEIGHT])
        surface.blit(settings.TEXTURES["road_0_right"],[681, self.yRelativa - settings.VIRTUAL_HEIGHT])
        if self.yRelativa < settings.VIRTUAL_HEIGHT:
            surface.blit(settings.TEXTURES["Soil_Tile"],[self.displayX, self.yRelativa])
            surface.blit(settings.TEXTURES["road_0_left"],[380, self.yRelativa])
            surface.blit(settings.TEXTURES["road_0_right"],[681, self.yRelativa])
        self.player.render(surface)  
        for car in self.car_list:
            car.render(surface)

        pygame.display.flip()
            
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "move_left":
            if input_data.pressed:
                self.player.vx = -settings.PLAYER_SPEED
            elif input_data.released and self.player.vx < 0:
                self.player.vx = 0
        elif input_id == "move_right":
            if input_data.pressed:
                self.player.vx = settings.PLAYER_SPEED
            elif input_data.released and self.player.vx > 0:
                self.player.vx = 0
        elif input_id == "move_up":
            if input_data.pressed:
                self.player.vy = -settings.PLAYER_SPEED
            elif input_data.released and self.player.vy < 0:
                self.player.vy = 0
        elif input_id == "move_down":
            if input_data.pressed:
                self.player.vy = settings.PLAYER_SPEED
            elif input_data.released and self.player.vy > 0:
                self.player.vy = 0

        
        
        
        
        