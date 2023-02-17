"""
ISPPJ1 2023
Study Case: Breakout

Author: Mint and CarlosULA

This file contains the specialization of PowerUp to catch the ball to the game.
"""

from typing import TypeVar

from gale.factory import Factory

import settings
from src.powerups.PowerUp import PowerUp

class CatchBall(PowerUp):
    """
    Power-up to  catch the ball to the game.
    """
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 8)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()
        self.in_play = False