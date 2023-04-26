
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
            frames.append(pygame.Rect(x,y, settings.ICON_WIDHT , settings.ICON_HEIGHT))
            x += settings.ICON_WIDHT + space_left_icon
        x = 0
        y += settings.ICON_HEIGHT + space_bottom_icon
    
    return frames
