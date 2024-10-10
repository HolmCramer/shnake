from turtle import Turtle
from utils import SCREEN_COORDS

SCOREBOARD_POS = (SCREEN_COORDS[0][0]+25,SCREEN_COORDS[1][0]-15)


class Scoreboard(Turtle):
    def __init__(self, shape: str = "classic", undobuffersize: int = 1000, visible: bool = False) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.score : int = 0
        self.draw_scoreboard()
    
    def get_score_string(self) -> str:
        score_str = f"{(4-len(str(self.score)))*"0"}{str(self.score)}"
        return score_str

    def draw_scoreboard(self) -> None:
        self.teleport(SCOREBOARD_POS[0],SCOREBOARD_POS[1])
        score_string = self.get_score_string()
        self.write(score_string, font=("Arial", 16, "normal"))

    def increment_score(self) -> None:
        self.score += 10
        self.clear()
        self.draw_scoreboard()