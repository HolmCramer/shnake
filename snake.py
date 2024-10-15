from turtle import Turtle
from enum import Enum
from utils import SNAKE_COLOR, STEP_DIST, NORTH, EAST, SOUTH, WEST, SCREEN_COORDS
from random import randint

class DIRECTIONS(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

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
            x = randint((SCREEN_COORDS[0][0]+STEP_DIST)//20, (SCREEN_COORDS[0][1]-STEP_DIST)//20) * 20
            y = randint((SCREEN_COORDS[1][0]+STEP_DIST)//20, (SCREEN_COORDS[1][1]-STEP_DIST)//20) * 20
            coords = (x,y)
            if coords not in snake_positions:
                break
        self.setpos(coords)

class Snake(Turtle):
    def __init__(self, shape: str = "square", undobuffersize: int = 1000, visible: bool = True) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.up()
        self.shapesize(0.8,0.8)
        self.color(SNAKE_COLOR)
        self.segments : Segment = []
        self.init_segments(2)
        self.init_pos()
    
    def init_pos(self):
        self.segments[0].teleport(-20,0)
        self.segments[1].teleport(-40,0)
    
    def init_segments(self, count=1) -> None:
        for _ in range(count):
            self.segments.append(Segment(shape="square"))
        return
    
    def get_number_of_segments(self) -> int:
        count = len(self.segments)
        return count

    def add_segment(self, segment : Segment) -> bool:
        segment.shape("square")
        self.segments.insert(0, segment)
        return True
    
    def move_to_snake_head(self) -> None:
        for i in range(len(self.segments)-1, -1, -1):
            if i == 0:
                self.segments[i].teleport(self.xcor(), self.ycor())
            else:
                self.segments[i].teleport(self.segments[i-1].xcor(), self.segments[i-1].ycor())

    def get_direction(self, input_buffer : list, eaten : bool) -> DIRECTIONS:
        if eaten is True:
            segment = self.segments[1]
        else:
            segment = self.segments[0]
        
        match input_buffer[0]:
            case DIRECTIONS.UP:
                if segment.ycor() == self.ycor() + STEP_DIST:
                    return input_buffer[1]
                else:
                    return input_buffer[0]
            case DIRECTIONS.RIGHT:
                if segment.xcor() == self.xcor() + STEP_DIST:
                    return input_buffer[1]
                else:
                    return input_buffer[0]
            case DIRECTIONS.DOWN:
                if segment.ycor() == self.ycor() - STEP_DIST:
                    return input_buffer[1]
                else:
                    return input_buffer[0]
            case DIRECTIONS.LEFT:
                if segment.xcor() == self.xcor() - STEP_DIST:
                    return input_buffer[1]
                else:
                    return input_buffer[0]
            case _:
                print("Error calculating Direction!")

    def teleport_in_direction(self, direction : DIRECTIONS) -> None:
        match direction:
            case DIRECTIONS.UP:
                self.teleport(self.xcor(), self.ycor() + STEP_DIST)
            case DIRECTIONS.RIGHT:
                self.teleport(self.xcor() + STEP_DIST, self.ycor())
            case DIRECTIONS.DOWN:
                self.teleport(self.xcor(), self.ycor() - STEP_DIST)
            case DIRECTIONS.LEFT:
                self.teleport(self.xcor() - STEP_DIST, self.ycor())


    def move_snake(self, eaten : bool, input_buffer : list) -> bool:
        direction = self.get_direction(input_buffer, eaten)
        if eaten is False:
            self.move_to_snake_head()
        else:
            eaten = False
        self.teleport_in_direction(direction)
        return eaten
    
    def get_snake_positions(self) -> tuple:
        snake_positions = [self.pos()]
        for segment in self.segments:
            snake_positions.append(segment.pos())
        return snake_positions