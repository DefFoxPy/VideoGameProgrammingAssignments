import random
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Player import Player
from src.powerups.PowerUp import PowerUp


class Slowly(PowerUp):
    """
    Power-up to make player slow
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 6)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.powerUpSlowly = True
        self.in_play = False
