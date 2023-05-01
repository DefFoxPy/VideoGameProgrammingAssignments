
import pygame 

from typing import List
from gale.frames import generate_frames
import settings

def generate_icons_frames() ->List[pygame.Rect]:
    space_left_icon = 28
    space_bottom_icon = 32
    x = 0
    y = 0
    frames = []
    for f in range(4):
        for c in range(12):
            frames.append(pygame.Rect(x,y, settings.ICON_WIDHT , settings.ICON_HEIGTH))
            x += settings.ICON_WIDHT + space_left_icon
        x = 0
        y += settings.ICON_HEIGTH + space_bottom_icon    
    return frames

def generate_cars_frames() ->List[pygame.Rect]:
    x = 0
    y = 0
    frames = []
    for f in range(8):
        frames.append(pygame.Rect(x,y, settings.CAR_WIDTH , settings.CAR_HEIGHT))
        x += settings.CAR_WIDTH    
    return frames