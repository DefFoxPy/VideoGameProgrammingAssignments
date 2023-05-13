import pygame

from typing import List
from gale.frames import generate_frames
import settings


def generate_icons_frames() -> List[pygame.Rect]:
    space_left_icon = 28
    space_bottom_icon = 32
    x = 0
    y = 0
    frames = []
    for f in range(4):
        for c in range(12):
            frames.append(pygame.Rect(x, y, settings.ICON_WIDTH, settings.ICON_HEIGHT))
            x += settings.ICON_WIDTH + space_left_icon
        x = 0
        y += settings.ICON_HEIGHT + space_bottom_icon
    return frames


def generate_frames(cant: int, width: int, height) -> List[pygame.Rect]:
    x = 0
    y = 0
    frames = []
    for _ in range(cant):
        frames.append(pygame.Rect(x, y, width, height))
        x += width
    return frames


def generate_powerUp_frames() -> List[pygame.Rect]:
    x = 0
    y = 0
    frames = []
    for f in range(2):
        for c in range(6):
            frames.append(pygame.Rect(x, y, 50, 50))
            x += 50
        x = 0
        y += 50
    return frames
