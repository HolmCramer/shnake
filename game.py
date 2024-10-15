from turtle import Screen, Turtle
from snake import Snake, Segment, DIRECTIONS
from scoreboard import Scoreboard, SCOREBOARD_POS
from utils import SCREEN_RES, SCREEN_COORDS, BORDER_OFFSET, STEP_DIST
from threading import Thread
from time import sleep
from math import log


class Game():
    def __init__(self) -> None:
        self.screen = Screen()
        self.screen.setup(width=SCREEN_RES[0], height=SCREEN_RES[1])
        self.screen.screensize(canvwidth=SCREEN_RES[0],canvheight=SCREEN_RES[1])
        self.screen.setworldcoordinates(SCREEN_COORDS[0][0], SCREEN_COORDS[1][0]-10, SCREEN_COORDS[0][1]+10, SCREEN_COORDS[1][1])
        self.screen.mode("world")
        self.screen.colormode(255)
        self.screen.bgcolor(139,172,15)
        self.screen.title("Shnake")
        self.screen.tracer(0)
        self.draw_border()
        self.game_is_on = False
        self.snake = Snake()
        self.scoreboard = Scoreboard()
        self.input_buffer = [DIRECTIONS.RIGHT]
        self.frame_time = 0.3

    def draw_border(self) -> None:
        pen = Turtle(visible=False)
        pen.teleport(SCREEN_COORDS[0][0] + BORDER_OFFSET, SCREEN_COORDS[1][1] - BORDER_OFFSET)
        pen.goto(SCREEN_COORDS[0][1] - BORDER_OFFSET, SCREEN_COORDS[1][1] - BORDER_OFFSET)
        pen.goto(SCREEN_COORDS[0][1] - BORDER_OFFSET, SCREEN_COORDS[1][0] + BORDER_OFFSET)
        pen.goto(SCREEN_COORDS[0][0] + BORDER_OFFSET, SCREEN_COORDS[1][0] + BORDER_OFFSET)
        pen.goto(SCREEN_COORDS[0][0] + BORDER_OFFSET, SCREEN_COORDS[1][1] - BORDER_OFFSET)


    def insert_into_input_buffer(self, direction : DIRECTIONS) -> None:
        if direction is not self.input_buffer[0]:
            self.input_buffer.insert(0, direction)
        while len(self.input_buffer) > 2:
            self.input_buffer.pop()

    def up(self):
        self.snake.set_snake_direction(DIRECTIONS.UP)
        self.insert_into_input_buffer(DIRECTIONS.UP)

    def right(self):
        self.snake.set_snake_direction(DIRECTIONS.RIGHT)
        self.insert_into_input_buffer(DIRECTIONS.RIGHT)

    def down(self):
        self.snake.set_snake_direction(DIRECTIONS.DOWN)
        self.insert_into_input_buffer(DIRECTIONS.DOWN)

    def left(self):
        self.snake.set_snake_direction(DIRECTIONS.LEFT)
        self.insert_into_input_buffer(DIRECTIONS.LEFT)

    def update_speed(self, snake : Snake, frame_time : float) -> float:
        if int(log(frame_time/0.3, 0.99)) < snake.get_number_of_segments() - 2:
            frame_time *= 0.99
        return frame_time

    def event_handler(self) -> None:
            self.screen.onkeypress(self.up, "Up")
            self.screen.onkeypress(self.right, "Right")
            self.screen.onkeypress(self.down, "Down")
            self.screen.onkeypress(self.left, "Left")
            self.screen.listen()

    def self_collision_check(self) -> bool:
        flag = True
        for i in range(3, len(self.snake.segments)):
            if self.snake.segments[i].pos() == self.snake.pos():
                flag = False
        return flag

    def collision_check(self) -> bool:
        flag = True
        if self.snake.pos()[0] < SCREEN_COORDS[0][0] + STEP_DIST or self.snake.pos()[0] > SCREEN_COORDS[0][1] - STEP_DIST:
            flag = False
        elif self.snake.pos()[1] < SCREEN_COORDS[1][0] + STEP_DIST or self.snake.pos()[1] > SCREEN_COORDS[1][1] - STEP_DIST:
            flag = False
        elif self.self_collision_check() is False:
            flag = False        
        else:
            flag = True
        return flag

    def eat_food(self, food : Segment):
        flag = False
        if food.pos() == self.snake.pos():
            flag = self.snake.add_segment(food)
            food = Segment(food_spawn=True, snake_positions=self.snake.get_snake_positions())
            self.scoreboard.increment_score()
        return flag, food

    def waiter(self) -> None:
        sleep(self.frame_time)

    def thread_builder(self) -> Thread:
        thread = Thread(target=self.waiter, args=())
        return thread

    def gameloop(self) -> None:
        food = Segment(food_spawn=True, snake_positions=self.snake.get_snake_positions())
        self.scoreboard.get_score_string()
        game_is_on = True
        eat_flag = False
        self.scoreboard.input_player_name()
        while game_is_on:
            self.screen.update()
            self.event_handler()
            self.screen.update()
            eat_flag = self.snake.move_snake(eat_flag, self.input_buffer)
            eat_flag, food = self.eat_food(food)
            game_is_on = self.collision_check()
            if game_is_on is not True:
                break
            self.screen.update()
            self.frame_time = self.update_speed(self.snake, self.frame_time)
            thread = self.thread_builder()
            thread.start()
            thread.join()
        print("You lost!")
        self.scoreboard.get_scoreboard_list()
        self.scoreboard.insert_score_into_csv()
        self.scoreboard.display_scoreboard(self.screen)
        self.screen.exitonclick()