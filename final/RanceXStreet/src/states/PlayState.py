
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
    
    def exit(self)  -> None:
        InputHandler.unregister_listener(self)
        
    def update(self, dt: float) -> None:
        self.world.update(dt, self.score/100)
        self.player.update(dt)            
        self.time_car += 1
        self.score += 1
        if self.time_car >= settings.GENERATE_CAR * random.randint(1, max(1, 10-self.score//100)):
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
            if len(self.old_posx_car) == settings.NUM_VIAS:
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
                    self.state_machine.change("enterHighScore",score = self.score / 100,world = self.world)
            if car.y > settings.VIRTUAL_HEIGHT:
                self.car_list.pop(0)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.player.render(surface)  
        for car in self.car_list:
            car.render(surface)
        render_text(
            surface,
            "Score:",
            settings.FONTS["mediumPlus"],
            100,
            90,
            settings.COLOR_BLACK,
            center= True,
        )
        render_text(
            surface,
            "Km: " + str(self.score/100),
            settings.FONTS["medium"],
            100,
            133,
            settings.COLOR_LIGHT,
            center= False,
        )
        surface.blit(settings.TEXTURES["icons"], (1000, 10), settings.FRAMES["list_icons"][5])
        surface.blit(settings.TEXTURES["icons"], (1010 + settings.ICON_WIDHT , 10), settings.FRAMES["list_icons"][18])

        pygame.display.flip()
            
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == 'pause':
            self.state_machine.change("pause", player=self.player ,score=self.score, car_list=self.car_list, datos=[self.score, self.time_car, self.old_posx_car, self.old_skin_car], world = self.world, opc = 0)
        elif input_id == 'home':
            self.state_machine.change("pause", player=self.player ,score=self.score, car_list=self.car_list, datos=[self.score, self.time_car, self.old_posx_car, self.old_skin_car], world = self.world, opc = 1)
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

        
        
        
        
        