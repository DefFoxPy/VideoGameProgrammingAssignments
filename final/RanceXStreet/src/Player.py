
import pygame
import settings


class Player:
    def __init__(self,x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = settings.TEXTURES["car1"].get_width()
        self.height = settings.TEXTURES["car1"].get_height()
        self.skin = 0
        self.set = 0
        self.vx = 0
        self.vy = 0
        self.rotate = 0

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)
   
    def update(self, dt: float) -> None:
        next_x = self.x + self.vx * dt
        next_y = self.y + self.vy * dt

        if self.vx < 0:
            self.x = max(0, next_x)
        else:
            self.x = min(settings.VIRTUAL_WIDTH - self.width, next_x)
        
        if self.vy < 0:
            self.y = max(0, next_y)
        else:
            self.y = min(settings.VIRTUAL_HEIGHT - self.height, next_y)
        
        if self.x < settings.POS_SET[0]:
            self.x = settings.POS_SET[0]
        if self.x > settings.POS_SET[3]:
            self.x = settings.POS_SET[3]

        if self.y < 5:
            self.y = 5
        if self.y + self.height > settings.VIRTUAL_HEIGHT:
            self.y = self.y + self.height

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(pygame.transform.rotate(settings.TEXTURES["Set_vehicle"+str(self.set)],self.rotate) , (self.x, self.y), settings.FRAMES["list_cars"][self.skin])
        #surface.blit(pygame.transform.rotate(settings.TEXTURES["Set_vehicle0"],self.rotate) , (self.x, self.y), settings.FRAMES["list_cars"][1])
        #surface.blit(settings.TEXTURES["Set_vehicle"+str(self.set)], (self.x, self.y), settings.FRAMES["list_cars"][self.skin])
    