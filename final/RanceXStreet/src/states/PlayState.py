
import pygame, random

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text
import settings

from src.Car import Car
from src.World import World

class PlayState(BaseState):
    def enter(self, **params: dict) -> None:  
        self.player = params["player"]
        self.car_list = params["car_list"]
        self.score = params["datos"][0]
        self.time_car = params["datos"][1]
        self.old_posx_car = params["datos"][2]
        self.old_skin_car = params["datos"][3]
        self.player.rotate = 0
        self.displayX = 0
        self.displayY = 0
        self.time_game_over = 0
        self.world = World()        
        InputHandler.register_listener(self)
        
    def update(self, dt: float) -> None:
        self.world.update(dt, self.score/100)
        self.player.update(dt)            
        self.time_car += 1
        self.score += 1
        if self.time_car >= settings.GENERATE_CAR * random.randint(1, max(1, 1-self.score//100)):
            aux_pos = random.randint(0,settings.NUM_VIAS-1)
            aux_skin = random.randint(0,settings.NUM_SKIN-1)
            while aux_pos in self.old_posx_car:
                aux_pos = random.randint(0, settings.NUM_VIAS-1)
            while aux_skin in self.old_skin_car:
                aux_skin = random.randint(0,settings.NUM_SKIN-1)
            car = Car(posx = aux_pos, skin= aux_skin)
            self.car_list.append(car)
            self.old_posx_car.append(aux_pos)
            self.old_skin_car.append(aux_skin)
            if len(self.old_posx_car) == 4:
                self.old_posx_car.pop(0)
            if len(self.old_skin_car) == settings.NUM_SKIN//2:
                self.old_skin_car.pop(0)
            self.time_car = 0

        for car in self.car_list:
            car.update(dt)
            if car.collides(self.player):
                print("colision")
                self.time_game_over += 1
                if self.time_game_over == 2: ## para crear el efecto de humo
                    self.state_machine.change("gameOver",self.score / 100)
            if car.y > settings.VIRTUAL_HEIGHT:
                self.car_list.pop(0)
            
    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.player.render(surface)  
        for car in self.car_list:
            car.render(surface)
               
        pygame.display.flip()
            
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == 'pause':
            self.state_machine.change("pause", player=self.player ,score=self.score, car_list=self.car_list, datos=[self.score, self.time_car, self.old_posx_car, self.old_skin_car], world = self.world)
        elif input_id == "move_left":
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

        
        
        
        
        