"""
ISPPJ1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""
from typing import Dict, Any, List

import pygame

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Board import Board



class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params["level"]
        self.board = enter_params["board"]
        self.score = enter_params["score"]

        # Position in the grid which we are highlighting
        self.board_highlight_i1 = -1
        self.board_highlight_j1 = -1
        self.board_highlight_i2 = -1
        self.board_highlight_j2 = -1

        self.highlighted_i1 = 0
        self.highlighted_j1 = 0
        self.highlighted_i2 = 0
        self.highlighted_j2 = 0
        self.temp_x = 0
        self.temp_y = 0
        self.highlighted_tile = False
        self.block = False

        self.active = True

        self.timer = settings.LEVEL_TIME

        self.goal_score = self.level * 1.25 * 1000

        # A surface that supports alpha to highlight a selected tile
        self.tile_alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.tile_alpha_surface,
            (255, 255, 255, 96),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )

        # A surface that supports alpha to draw behind the text.
        self.text_alpha_surface = pygame.Surface((212, 136), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (56, 56, 56, 234), pygame.Rect(0, 0, 212, 136)
        )

        def decrement_timer():
            self.timer -= 1

            # Play warning sound on timer if we get low
            if self.timer <= 5:
                settings.SOUNDS["clock"].play()

        Timer.every(1, decrement_timer)

        InputHandler.register_listener(self)

    def exit(self) -> None:
        InputHandler.unregister_listener(self)

    def update(self, _: float) -> None:

        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

        if self.score >= self.goal_score:
            Timer.clear()
            settings.SOUNDS["next-level"].play()
            self.state_machine.change("begin", level=self.level + 1, score=self.score)

        # actualiza el tablero si no hay match posibles
        if not self.board.calculate_match_rec_pre():
                print("No hay match")
                self.board = Board(settings.VIRTUAL_WIDTH - 272, 16)

    def render(self, surface: pygame.Surface) -> None:
        self.board.render(surface)

        if self.highlighted_tile:
            x = self.highlighted_j1 * settings.TILE_SIZE + self.board.x
            y = self.highlighted_i1 * settings.TILE_SIZE + self.board.y
            surface.blit(self.tile_alpha_surface, (x, y))

        surface.blit(self.text_alpha_surface, (16, 16))
        render_text(
            surface,
            f"Level: {self.level}",
            settings.FONTS["medium"],
            30,
            24,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Goal: {self.goal_score}",
            settings.FONTS["medium"],
            30,
            80,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            30,
            108,
            (99, 155, 255),
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not self.active:
            return
        

        if input_id == "click" and input_data.pressed:
            pos_x, pos_y = input_data.position
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
            i = (pos_y - self.board.y) // settings.TILE_SIZE
            j = (pos_x - self.board.x) // settings.TILE_SIZE

            if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH:
                if not self.highlighted_tile:
                    self.highlighted_tile = True
                    self.highlighted_i1 = i
                    self.highlighted_j1 = j
                    self.temp_x = j * settings.TILE_SIZE
                    self.temp_y = i * settings.TILE_SIZE

        elif input_id in "mup" and self.highlighted_tile and self.block == False:
            self.block = True
            self.board.tiles[self.highlighted_i1][self.highlighted_j1].y = self.temp_y - settings.TILE_SIZE

        elif input_id in "mdown" and self.highlighted_tile and self.block == False:
            self.block = True
            self.board.tiles[self.highlighted_i1][self.highlighted_j1].y = self.temp_y + settings.TILE_SIZE

        elif input_id in "mright" and self.highlighted_tile and self.block == False:
            self.block = True
            self.board.tiles[self.highlighted_i1][self.highlighted_j1].x = self.temp_x + settings.TILE_SIZE

        elif input_id in "mleft" and self.highlighted_tile and self.block == False:
            self.block = True
            self.board.tiles[self.highlighted_i1][self.highlighted_j1].x = self.temp_x - settings.TILE_SIZE

        elif input_id == "click" and input_data.released:
            self.block = False
            pos_x, pos_y = self.board.tiles[self.highlighted_i1][self.highlighted_j1].x, self.board.tiles[self.highlighted_i1][self.highlighted_j1].y
            i = pos_y // settings.TILE_SIZE
            j = pos_x // settings.TILE_SIZE

            if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH:
                self.highlighted_i2 = i
                self.highlighted_j2 = j
                di = abs(self.highlighted_i2 - self.highlighted_i1)
                dj = abs(self.highlighted_j2 - self.highlighted_j1)

                if di <= 1 and dj <= 1 and di != dj:
                    self.active = False
                    tile1 = self.board.tiles[self.highlighted_i1][
                        self.highlighted_j1
                    ]
                    tile2 = self.board.tiles[self.highlighted_i2][
                        self.highlighted_j2
                    ]

                    def arrive():
                        tile1 = self.board.tiles[self.highlighted_i1][
                            self.highlighted_j1
                        ]
                        tile2 = self.board.tiles[self.highlighted_i2][
                            self.highlighted_j2
                        ]
                        (
                            self.board.tiles[tile1.i][tile1.j],
                            self.board.tiles[tile2.i][tile2.j],
                        ) = (
                            self.board.tiles[tile2.i][tile2.j],
                            self.board.tiles[tile1.i][tile1.j],
                        )
                        tile1.i, tile1.j, tile2.i, tile2.j = (
                            tile2.i,
                            tile2.j,
                            tile1.i,
                            tile1.j,
                        )
                        if not (self.__calculate_matches([tile1, tile2])): #revertir cambios
                            
                            tile1 = self.board.tiles[self.highlighted_i1][
                            self.highlighted_j1
                            ]
                            tile2 = self.board.tiles[self.highlighted_i2][
                                self.highlighted_j2
                            ]
                            (
                                self.board.tiles[tile1.i][tile1.j],
                                self.board.tiles[tile2.i][tile2.j],
                            ) = (
                                self.board.tiles[tile2.i][tile2.j],
                                self.board.tiles[tile1.i][tile1.j],
                            )
                            tile1.i, tile1.j, tile2.i, tile2.j = (
                                tile2.i,
                                tile2.j,
                                tile1.i,
                                tile1.j,
                            )
                            Timer.tween(
                                0.25,
                                [
                                    (tile1, {"x": tile2.x, "y": tile2.y}),
                                    (tile2, {"x": self.temp_x, "y": self.temp_y}),
                                ],
                            ) 

                    # Swap tiles
                    Timer.tween(
                        0.25,
                        [
                            (tile1, {"x": tile2.x, "y": tile2.y}),
                            (tile2, {"x": self.temp_x, "y": self.temp_y}),
                        ],
                        on_finish=arrive,
                    )
                else:
                    self.board.tiles[self.highlighted_i1][self.highlighted_j1].x = self.temp_x 
                    self.board.tiles[self.highlighted_i1][self.highlighted_j1].y = self.temp_y
            else:
                self.board.tiles[self.highlighted_i1][self.highlighted_j1].x = self.temp_x
                self.board.tiles[self.highlighted_i1][self.highlighted_j1].y = self.temp_y

            self.highlighted_tile = False

    def __calculate_matches(self, tiles: List) -> bool:
        
        matches = self.board.calculate_matches_for(tiles)

        if matches is None:
            self.active = True
            return False

        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()

        for match in matches:
            self.score += len(match) * 50

        self.board.remove_matches()

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self.__calculate_matches(
                [item[0] for item in falling_tiles]
            ),
        )

        return True
