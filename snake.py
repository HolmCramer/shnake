from turtle import Turtle
from enum import Enum
from utils import SNAKE_COLOR, STEP_DIST, NORTH, EAST, SOUTH, WEST, SCREEN_COORDS
from random import randint
from food import Segment

class DIRECTIONS(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class Snake(Turtle):
    def __init__(self, shape: str = "square", undobuffersize: int = 1000, visible: bool = True) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.up()
        self.color(SNAKE_COLOR)
        self.segments : Segment = []
        self.init_segments(2)
        self.init_pos()
    
    def init_pos(self):
        self.segments[0].teleport(-20,0)
        self.segments[1].teleport(-40,0)
    
    def init_segments(self, count=1) -> None:
        for _ in range(count):
            self.segments.append(Segment())
        return
    
    def add_segment(self, segment : Segment) -> bool:
        self.segments.insert(0, segment)
        return True
    
    def move_to_snake_head(self) -> None:
        for i in range(len(self.segments)-1, -1, -1):
            if i == 0:
                self.segments[i].teleport(self.xcor(), self.ycor())
            else:
                self.segments[i].teleport(self.segments[i-1].xcor(), self.segments[i-1].ycor())
    
    def set_snake_direction(self, direction: DIRECTIONS) -> None:
        match direction:
            case DIRECTIONS.UP:
                if self.heading() == SOUTH:
                    return
                else:
                    self.setheading(NORTH)
                    return
            case DIRECTIONS.RIGHT:
                if self.heading() == WEST:
                    return
                else:
                    self.setheading(EAST)
                    return
            case DIRECTIONS.DOWN:
                if self.heading() == NORTH:
                    return
                else:
                    self.setheading(SOUTH)
                    return
            case DIRECTIONS.LEFT:
                if self.heading() == EAST:
                    return
                else:
                    self.setheading(WEST)
                    return

    def get_direction(self, input_buffer : list) -> DIRECTIONS:
        match input_buffer[0]:
            case DIRECTIONS.UP:
                if self.segments[0].ycor() == self.ycor() + STEP_DIST:
                    return input_buffer[1]
                else:
                    return input_buffer[0]
            case DIRECTIONS.RIGHT:
                if self.segments[0].xcor() == self.xcor() + STEP_DIST:
                    return input_buffer[1]
                else:
                    return input_buffer[0]
            case DIRECTIONS.DOWN:
                if self.segments[0].ycor() == self.ycor() - STEP_DIST:
                    return input_buffer[1]
                else:
                    return input_buffer[0]
            case DIRECTIONS.LEFT:
                if self.segments[0].xcor() == self.xcor() - STEP_DIST:
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
        direction = self.get_direction(input_buffer)
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