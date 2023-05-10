
import pygame, random

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.factory import AbstractFactory
from gale.factory import Factory
from gale.text import render_text
import settings
import src.powerups

from src.Car import Car
from src.World import World


class PlayState(BaseState):
    def enter(self, **params: dict) -> None:  
        self.player = params["player"]
        self.car_list = params["car_list"]
        self.score = params["datos"][0]
        self.time_car = params["datos"][1]
        self.old_skin_car = params["datos"][2]
        self.powerUp_limit_ghost = params["datos"][3]
        self.powerUp_limit_slowly = params["datos"][4]
        self.powerUpGhost = params["datos"][5]
        self.powerUpSlowly = params["datos"][6]
        self.powerups = params.get("powerups", [])
        self.player.rotate = 0
        self.displayX = 0
        self.displayY = 0
        self.time_game_over = 0
        self.world = World(0)
        self.powerups_abstract_factory = AbstractFactory("src.powerups")    
        
        InputHandler.register_listener(self)
    
    def exit(self)  -> None:
        InputHandler.unregister_listener(self)
        
    def update(self, dt: float) -> None:
        if not self.player.slowly:
            settings.PLAYER_SPEED = min(500, settings.PLAYER_SPEED + self.score//100 // 2)
        
        else:
            settings.PLAYER_SPEED = settings.PLAYER_INITIAL_SPEED
        
        settings.CAR_SPEED = [settings.PLAYER_SPEED//2, settings.PLAYER_SPEED, settings.PLAYER_SPEED//2, settings.PLAYER_SPEED//2, settings.PLAYER_SPEED//2, settings.PLAYER_SPEED//2, settings.PLAYER_SPEED//4, settings.PLAYER_SPEED//2, settings.PLAYER_SPEED//5] 
        
        self.world.update(dt, self.score / 100)
        self.player.update(dt)            
        self.time_car += dt
        self.score += (settings.PLAYER_SPEED * dt) // 7 
        
        if self.time_car >= settings.GENERATE_CAR + random.randint(1, max(1, 10-self.score//100)):
            aux_pos = random.randint(0,settings.NUM_VIAS-1)
            aux_skin = random.randint(0,settings.NUM_SKIN-1)
            old_posx_car = list()
        
            for car in self.car_list:
                old_posx_car.append(car.x)

            if len(old_posx_car) < 4: 
                while aux_pos in old_posx_car:
                    aux_pos = random.randint(0, settings.NUM_VIAS-1)
                
                while aux_skin in self.old_skin_car:
                    aux_skin = random.randint(0,settings.NUM_SKIN-1)
                
                if random.random() < 0.1:
                    name = random.choice(settings.LIST_POWERUP)
                    self.powerups.append(
                    self.powerups_abstract_factory.get_factory(name).create(
                        aux_pos, -10
                        )
                    )
                
                else:
                    car = Car(posx= aux_pos, skin= aux_skin)
                    self.car_list.append(car)
                    self.old_skin_car.append(aux_skin)
                    
                    if len(self.old_skin_car) == settings.NUM_SKIN // 2:
                        self.old_skin_car.pop(0)
                
                self.time_car = 0

        if self.player.ghost:
            self.powerUp_limit_ghost += dt
            self.player.set = 4
            
            if self.powerUp_limit_ghost >= settings.POWERUP_LIMIT_GHOST:
                self.player.ghost = False
                self.player.set = self.player.old_set
                self.powerUp_limit_ghost = 0

        if self.player.slowly:
            self.powerUp_limit_slowly += dt
            
            if self.powerUp_limit_slowly >= settings.POWERUP_LIMIT_SLOWLY:
                self.player.slowly = False
                self.powerUp_limit_slowly = 0

        for powerup in self.powerups:
            powerup.update(dt)

            if powerup.collides(self.player):
                settings.SOUNDS["powerUp"].play()
                powerup.take(self)

        # Remove powerups that are not in play
        self.powerups = [p for p in self.powerups if p.in_play]

        for car in self.car_list:
            car.update(dt)
            
            if car.y > settings.VIRTUAL_HEIGHT and car.vy > 0:
                indice = self.car_list.index(car)
                self.car_list.pop(indice)
            
            elif car.y < 0 - car.height and car.vy < 0:
                indice = self.car_list.index(car)
                self.car_list.pop(indice)

            if car.collides(self.player) and not self.player.ghost:
                self.time_game_over += 1
                if self.time_game_over == 2: ## para crear el efecto de humo
                    self.state_machine.change("enterHighScore",score = self.score / 100,world = self.world)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.player.render(surface)  
        
        for car in self.car_list:
            car.render(surface)
        
        for powerup in self.powerups:
            powerup.render(surface) 
        
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
        
        surface.blit(settings.TEXTURES["icons"].convert_alpha(), (1000, 10), settings.FRAMES["list_icons"][5])
        
        render_text(
            surface,
            "P",
            settings.FONTS["small"],
            1000 + settings.ICON_WIDTH - 10,
            settings.ICON_HEIGHT + 5,
            settings.COLOR_BLACK,
            center= False,
        )
        
        surface.blit(settings.TEXTURES["icons"].convert_alpha(), (1010 + settings.ICON_WIDTH , 10), settings.FRAMES["list_icons"][18])
        
        render_text(
            surface,
            "Q",
            settings.FONTS["small"],
            1010 + 2 * settings.ICON_WIDTH - 10,
            settings.ICON_HEIGHT + 5,
            settings.COLOR_BLACK,
            center= False,
        )

        surface.blit(settings.TEXTURES["icons"].convert_alpha(), (60 + settings.ICON_WIDTH , settings.VIRTUAL_HEIGHT - 140), settings.FRAMES["list_icons"][1])
        if self.powerUpGhost:
            surface.blit(settings.TEXTURES["icons"].convert_alpha(), (60 + settings.ICON_WIDTH , settings.VIRTUAL_HEIGHT - 140), settings.FRAMES["list_icons"][25])
        render_text(
            surface,
            "X",
            settings.FONTS["small"],
            60 + 2 * settings.ICON_WIDTH - 10,
            settings.VIRTUAL_HEIGHT - 70,
            settings.COLOR_BLACK,
            center= False,
        )
        surface.blit(settings.TEXTURES["icons"].convert_alpha(), (30, settings.VIRTUAL_HEIGHT - 140), settings.FRAMES["list_icons"][0])
        if self.powerUpSlowly:
            surface.blit(settings.TEXTURES["icons"].convert_alpha(), (30, settings.VIRTUAL_HEIGHT - 140), settings.FRAMES["list_icons"][24])
        render_text(
            surface,
            "Z",
            settings.FONTS["small"],
            30 + settings.ICON_WIDTH - 10,
            settings.VIRTUAL_HEIGHT - 70,
            settings.COLOR_BLACK,
            center= False,
        )
        pygame.display.flip()
            
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == 'pause':
            settings.SOUNDS["enter"].play()
            self.state_machine.change("pause", player=self.player ,score=self.score, car_list=self.car_list, datos=[self.score, self.time_car, self.old_skin_car, 
                self.powerUp_limit_ghost, self.powerUp_limit_slowly, self.powerUpGhost, self.powerUpSlowly], world = self.world, powerups=self.powerups, opc = 0)
        
        elif input_id == 'home':
            settings.SOUNDS["enter"].play()
            self.state_machine.change("pause", player=self.player ,score=self.score, car_list=self.car_list, datos=[self.score, self.time_car, self.old_skin_car, 
                self.powerUp_limit_ghost, self.powerUp_limit_slowly, self.powerUpGhost, self.powerUpSlowly], world = self.world, powerups=self.powerups, opc = 1)
        
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
        
        elif input_id == "powerup_1" and self.powerUpGhost:
            settings.SOUNDS["enter"].play()
            self.player.ghost = True
            self.powerUpGhost = False
        
        elif input_id == "powerup_2" and self.powerUpSlowly:
            settings.SOUNDS["enter"].play()
            self.player.slowly = True
            self.powerUpSlowly = False