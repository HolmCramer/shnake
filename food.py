from turtle import Turtle
from random import randint
from utils import SCREEN_COORDS, SNAKE_COLOR


class Segment(Turtle):
    def __init__(self, shape: str = "circle", undobuffersize: int = 1000, visible: bool = True, food_spawn : bool = False, snake_positions : tuple = None) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.up()
        self.shapesize(0.8,0.8)
        self.color(SNAKE_COLOR)
        if food_spawn is True:
            self.set_rnd_pos(snake_positions)
    
    def set_rnd_pos(self, snake_positions) -> None:
        while True:
            x = randint(SCREEN_COORDS[0][0]//20, SCREEN_COORDS[0][1]//20) * 20
            y = randint(SCREEN_COORDS[1][0]//20, SCREEN_COORDS[1][1]//20) * 20
            coords = (x,y)
            if coords not in snake_positions:
                break
        self.setpos(coords)