import random
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Player import Player
from src.powerups.PowerUp import PowerUp


class Ghost(PowerUp):
    """
    Power-up to make player immunity
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 0)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.powerUpGhost = True
        self.in_play = False
