
import pygame
import settings

class Player:
    def __init__(self,x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 98
        self.height = 214

        self.vx = 0
        self.vy = 0

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
        
        if self.x < 460:
            self.x = 460
        if self.x + self.width > 1000:
            self.x = 1000 - self.width

        if self.y < 5:
            self.y = 5
        if self.y + self.height > settings.VIRTUAL_HEIGHT:
            self.y = self.y + self.height

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["car1"], (self.x, self.y))