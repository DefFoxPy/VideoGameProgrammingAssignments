
import string, pygame
from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings
from src.utilities.highscores import read_highscores, write_highscore

class EnterHighScorestate(BaseState):
    def enter(self, score: int) -> None:
        self.score = score
        self.hs = read_highscores()

        if self.score > 0 and ( len(self.hs) < settings.NUM_HIGHSCORES or self.score > self.hs[-1][1]):
            pass
        else:
            self.state_machine.change("gameOver")
        
        self.name = [0, 0, 0]
        self.selected = 0
        InputHandler.register_listener(self)
    
    def exit(self) -> None:
        InputHandler.unregister_listener(self)
    
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            name = "".join([string.ascii_uppercase[i] for i in self.name])
            self.hs.append([name, self.score])
            self.hs.sort(key=lambda item: item[-1], reverse = True)
            write_highscore(self.hs[: settings.NUM_HIGHSCORES])
            self.state_machine.change("gameOver", self.score)
        
        if input_id == "move_left" and input_data.pressed:
            self.selected = max(0, self.selected - 1)
        elif input_id == "move_right" and input_data.pressed:
            self.selected = min(2, self.selected + 1)
        elif input_id == "move_down" and input_data.pressed:
            self.name[self.selected] = max(0, self.name[self.selected] - 1)
        elif input_id == "move_up" and input_data.pressed:
            self.name[self.selected] = min(len(string.ascii_uppercase) - 1, self.name[self.selected] + 1)
    
    def render(self, surface: pygame.Surface) -> None:
        render_text(
            surface,
            f"Your score: {self.score}",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2,
            (0, 0, 0),
            center= True,
        )

        x = settings.VIRTUAL_WIDTH // 2 - 20

        for i in range(3):
            color = (0, 0, 0) if self.selected == i else (255, 255, 255)

            render_text(
                surface,
                string.ascii_uppercase[self.name[i]],
                settings.FONTS["medium"],
                x,
                settings.VIRTUAL_HEIGHT // 2 + 10,
                color, 
                center = True,
            )

            x += 20
