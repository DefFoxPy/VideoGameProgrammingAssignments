
import os
from typing import List, Any


USER_HOME = os.path.expanduser("~")

RANCEXSTREET_DIR = os.path.join(USER_HOME, ".RanceXStreet")

HIGHSCORES_PATH = os.path.join(RANCEXSTREET_DIR, "highscores.dat")

def read_highscores() -> List[List[Any]]:
    if not os.path.exists(RANCEXSTREET_DIR):
        os.mkdir(RANCEXSTREET_DIR)
    
    with open(HIGHSCORES_PATH, "a"):
        pass
    
    highscores = []

    with open(HIGHSCORES_PATH, "r") as f:
        for line in f:
            line = line[:-1]
            line = line.split(":")
            line[-1] = float(line[-1])
            highscores.append(line)
    
    return highscores

def write_highscore(highscores: List[List[Any]]) -> None:
    with open(HIGHSCORES_PATH, "w") as f:
        for line in highscores:
            line[-1] = str(line[-1])
            line = ":".join(line)
            f.write(f"{line}\n")