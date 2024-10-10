from turtle import Turtle
from utils import SCREEN_COORDS

SCOREBOARD_POS = (SCREEN_COORDS[0][0]+25,SCREEN_COORDS[1][0]-15)


class Scoreboard(Turtle):
    def __init__(self, shape: str = "classic", undobuffersize: int = 1000, visible: bool = False) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.score : int = 0
        self.draw_scoreboard()
    
    def draw_scoreboard(self) -> None:
        self.teleport(SCOREBOARD_POS[0],SCOREBOARD_POS[1])
        self.write("0000", font=("Arial", 16, "normal"))

    def draw_updated_score(self) -> None:
        pass
        #self.write(score, font=("Arial", 16, "normal"))

    def increment_score(self) -> None:
        self.score += 10
        self.draw_updated_score()