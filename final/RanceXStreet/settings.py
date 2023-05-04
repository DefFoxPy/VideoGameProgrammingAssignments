"""
This module was autogenerated by gale.
"""
import pathlib

import pygame

from gale import frames
from gale import input_handler

from src.utilities.frames import generate_icons_frames, generate_cars_frames

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_ESCAPE, 'quit')
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RETURN, "enter")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_UP, "move_up")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_DOWN, "move_down")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RIGHT, "move_right")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_LEFT, "move_left")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_p, "pause")

# Size we want to emulate
VIRTUAL_WIDTH = 1280
VIRTUAL_HEIGHT = 720
# Size of our actual window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

PLAYER_SPEED = 300
CAR_SPEED = [60, 45, 45, 45, 20, 45, 45, 20]
MAX_CAR_SPEED = max(CAR_SPEED)
MIN_CAR_SPEED = min(CAR_SPEED)
GENERATE_CAR = 15
NUM_SKIN = 8
NUM_VIAS = 4
POS_SET = [462, 575, 701, 822]
BASE_DIR = pathlib.Path(__file__).parent
ICON_HEIGTH = 81.8
ICON_WIDHT = 80.9
CAR_HEIGHT = 164
CAR_WIDTH = 75
NUM_HIGHSCORES = 7

COLOR_BLACK = (0 , 0, 0)
COLOR_ORANGE = (249, 154, 2)
COLOR_ORANGE_DARK = (240, 38, 10)
COLOR_LIGHT = (206,173,139)

# Register your textures from the graphics folder, for instance:
# TEXTURES = {
#     'my_texture': pygame.image.load(BASE_DIR / "assets" / "graphics" / "my_texture.png")
# }

TEXTURES = {
    "road_0_left": pygame.image.load(BASE_DIR / "graphics" / "object" / "road_0_left.png"),
    "road_0_right": pygame.image.load(BASE_DIR / "graphics" / "object" / "road_0_right.png"),
    "Soil_Tile": pygame.image.load(BASE_DIR / "graphics" / "object" / "Soil_Tile.png"),
    "background": pygame.image.load(BASE_DIR / "graphics" / "background.png"),
    "EscenaStar": pygame.image.load(BASE_DIR / "graphics" / "EscenaStar.png"),
    "EscenaSelect": pygame.image.load(BASE_DIR / "graphics" / "EscenaSelect.png"),
    "EscenaGameOver": pygame.image.load(BASE_DIR / "graphics" / "EscenaGameOver.png"),
    "cartel1": pygame.image.load(BASE_DIR / "graphics" / "cartel1.png"),
    "cartel2": pygame.image.load(BASE_DIR / "graphics" / "cartel2.png"),
    "cartel3": pygame.image.load(BASE_DIR / "graphics" / "cartel3.png"),
    "cartel4": pygame.image.load(BASE_DIR / "graphics" / "cartel4.png"),
    "carSelectState": pygame.image.load(BASE_DIR / "graphics" / "carSelectState.png"),
    "startate": pygame.image.load(BASE_DIR / "graphics" / "startstate.png"),
    "icons": pygame.image.load(BASE_DIR / "graphics" / "icons.png"),
    "Set_vehicle0": pygame.image.load(BASE_DIR / "graphics" / "vehicle" / "Set_vehicle.png"),
    "Set_vehicle1": pygame.image.load(BASE_DIR / "graphics" / "vehicle" / "Set_vehicle2.png"),
    "Set_vehicle2": pygame.image.load(BASE_DIR / "graphics" / "vehicle" / "Set_vehicle3.png"),
    "Set_vehicle3": pygame.image.load(BASE_DIR / "graphics" / "vehicle" / "Set_vehicle4.png"),
    "car0": pygame.image.load(BASE_DIR / "graphics" / "vehicle" / "Audi.png"),
    "car1": pygame.image.load(BASE_DIR / "graphics" / "vehicle" / "Black_viper.png"),
    "car2": pygame.image.load(BASE_DIR / "graphics" / "vehicle" / "Car.png"),
    "car3": pygame.image.load(BASE_DIR / "graphics" / "vehicle" / "Mini_truck.png"),
    "car4": pygame.image.load(BASE_DIR / "graphics" / "vehicle" / "Mini_van.png"),
    "car5": pygame.image.load(BASE_DIR / "graphics" / "vehicle" / "Police.png"),
    "car6": pygame.image.load(BASE_DIR / "graphics" / "vehicle" / "taxi.png"),
    "car7": pygame.image.load(BASE_DIR / "graphics" / "vehicle" / "truck.png"),    
}

# Register your frames, for instance:
# FRAMES = {
#     'my_frames': frames.generate_frames(TEXTURES['my_texture'], 16, 16)
# }
FRAMES = {
    "list_icons": generate_icons_frames(),
    "list_cars" : generate_cars_frames(),
}

pygame.mixer.init()

# Register your sound from the sounds folder, for instance:
# SOUNDS = {
#     'my_sound': pygame.mixer.Sound(BASE_DIR / "assets"  / "sounds" / "my_sound.wav"),
# }
SOUNDS = {}

pygame.font.init()

# Register your fonts from the fonts folder, for instance:
# FONTS = {
#     'small': pygame.font.Font(BASE_DIR / "assets"  / "fonts" / "font.ttf", 8)
# }
FONTS = {
    "tiny": pygame.font.Font(BASE_DIR / "fonts" / "Supersonic Rocketship.ttf", 20),
    "small": pygame.font.Font(BASE_DIR / "fonts" / "Supersonic Rocketship.ttf", 32),
    "smallPlus": pygame.font.Font(BASE_DIR / "fonts" / "Supersonic Rocketship.ttf", 35),
    "medium": pygame.font.Font(BASE_DIR / "fonts" / "Supersonic Rocketship.ttf", 40),
    "mediumPlus": pygame.font.Font(BASE_DIR / "fonts" / "Supersonic Rocketship.ttf", 43),
    "large": pygame.font.Font(BASE_DIR / "fonts" / "Supersonic Rocketship.ttf", 50),
    "largePlus": pygame.font.Font(BASE_DIR / "fonts" / "Supersonic Rocketship.ttf", 60),
}
