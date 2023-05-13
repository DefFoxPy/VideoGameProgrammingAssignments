import string, pygame
from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings
from src.utilities.highscores import read_highscores, write_highscore


class EnterHighScorestate(BaseState):
    def enter(self, **params: dict) -> None:
        self.score = params["score"]
        self.world = params["world"]
        self.time_display = 0
        self.display = True
        self.hs = read_highscores()

        if self.score > 0 and (
            len(self.hs) < settings.NUM_HIGHSCORES or self.score > self.hs[-1][1]
        ):
            pass
        else:
            self.state_machine.change("gameOver", self.score)

        self.name = [0, 0, 0]
        self.selected = 0
        InputHandler.register_listener(self)

    def exit(self) -> None:
        InputHandler.unregister_listener(self)

    def update(self, dt: float) -> None:
        self.time_display += 1
        if self.time_display > 2:
            self.display = not self.display
            self.time_display = 0

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            settings.SOUNDS["enter"].play()
            name = "".join([string.ascii_uppercase[i] for i in self.name])
            self.hs.append([name, self.score])
            self.hs.sort(key=lambda item: item[-1], reverse=True)
            write_highscore(self.hs[: settings.NUM_HIGHSCORES])
            self.state_machine.change("gameOver", self.score)

        if input_id == "move_left" and input_data.pressed:
            settings.SOUNDS["select"].play()
            self.selected = max(0, self.selected - 1)
        elif input_id == "move_right" and input_data.pressed:
            settings.SOUNDS["select"].play()
            self.selected = min(2, self.selected + 1)
        elif input_id == "move_down" and input_data.pressed:
            settings.SOUNDS["select2"].play()
            self.name[self.selected] = max(0, self.name[self.selected] - 1)
        elif input_id == "move_up" and input_data.pressed:
            settings.SOUNDS["select2"].play()
            self.name[self.selected] = min(
                len(string.ascii_uppercase) - 1, self.name[self.selected] + 1
            )

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        surface.blit(
            settings.TEXTURES["cartel3"].convert_alpha(),
            (
                (settings.VIRTUAL_WIDTH - settings.TEXTURES["cartel3"].get_width())
                // 2,
                (settings.VIRTUAL_HEIGHT - settings.TEXTURES["cartel3"].get_height())
                // 2,
            ),
        )

        render_text(
            surface,
            "Congratulations",
            settings.FONTS["largePlus"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 - 100,
            settings.COLOR_BLACK,
            center=True,
        )

        color_display = settings.COLOR_LIGHT
        color_display2 = settings.COLOR_ORANGE_DARK
        font_display = settings.FONTS["medium"]
        font_display2 = settings.FONTS["small"]
        if self.display:
            color_display = settings.COLOR_ORANGE
            color_display = settings.COLOR_ORANGE_DARK
            font_display = settings.FONTS["mediumPlus"]
            font_display2 = settings.FONTS["smallPlus"]

        render_text(
            surface,
            f"New score: {self.score} km",
            font_display,
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2,
            color_display,
            center=True,
        )

        render_text(
            surface,
            "NickName: ",
            settings.FONTS["mediumPlus"],
            settings.VIRTUAL_WIDTH // 2 - 50,
            settings.VIRTUAL_HEIGHT // 2 + 100,
            settings.COLOR_BLACK,
            center=True,
        )

        x = settings.VIRTUAL_WIDTH // 2 + 60
        for i in range(3):
            color = (
                settings.COLOR_LIGHT if self.selected == i else settings.COLOR_ORANGE
            )
            render_text(
                surface,
                string.ascii_uppercase[self.name[i]],
                settings.FONTS["medium"],
                x,
                settings.VIRTUAL_HEIGHT // 2 + 100,
                color,
                center=True,
            )
            x += 35

        render_text(
            surface,
            "enter to continue",
            font_display2,
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 + 220,
            color_display2,
            center=True,
        )
