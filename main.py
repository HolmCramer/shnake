from turtle import Screen, Turtle
from snake import Snake, Segment, DIRECTIONS
from scoreboard import Scoreboard, SCOREBOARD_POS
import time
from utils import SCREEN_RES, SCREEN_COORDS, BORDER_OFFSET, STEP_DIST
from threading import Thread
from time import sleep



screen = Screen()
screen.setup(width=SCREEN_RES[0], height=SCREEN_RES[1])
screen.screensize(canvwidth=SCREEN_RES[0],canvheight=SCREEN_RES[1])
screen.setworldcoordinates(SCREEN_COORDS[0][0], SCREEN_COORDS[1][0]-10, SCREEN_COORDS[0][1]+10, SCREEN_COORDS[1][1])
screen.mode("world")
screen.colormode(255)
screen.bgcolor(139,172,15)
screen.title("Snake")
screen.tracer(0)

def draw_border() -> None:
    pen = Turtle(visible=False)
    pen.teleport(SCREEN_COORDS[0][0] + BORDER_OFFSET, SCREEN_COORDS[1][1] - BORDER_OFFSET)
    pen.goto(SCREEN_COORDS[0][1] - BORDER_OFFSET, SCREEN_COORDS[1][1] - BORDER_OFFSET)
    pen.goto(SCREEN_COORDS[0][1] - BORDER_OFFSET, SCREEN_COORDS[1][0] + BORDER_OFFSET)
    pen.goto(SCREEN_COORDS[0][0] + BORDER_OFFSET, SCREEN_COORDS[1][0] + BORDER_OFFSET)
    pen.goto(SCREEN_COORDS[0][0] + BORDER_OFFSET, SCREEN_COORDS[1][1] - BORDER_OFFSET)

draw_border()

game_is_on = False
snake = Snake()
scoreboard = Scoreboard()

input_buffer = [DIRECTIONS.RIGHT]

def insert_into_input_buffer(direction : DIRECTIONS) -> None:
    if direction is not input_buffer[0]:
        input_buffer.insert(0, direction)
    if len(input_buffer) > 2:
        while True:
            input_buffer.pop()
            if len(input_buffer) <= 2:
                break

def up():
    snake.set_snake_direction(DIRECTIONS.UP)
    insert_into_input_buffer(DIRECTIONS.UP)

def right():
    snake.set_snake_direction(DIRECTIONS.RIGHT)
    insert_into_input_buffer(DIRECTIONS.RIGHT)

def down():
    snake.set_snake_direction(DIRECTIONS.DOWN)
    insert_into_input_buffer(DIRECTIONS.DOWN)

def left():
    snake.set_snake_direction(DIRECTIONS.LEFT)
    insert_into_input_buffer(DIRECTIONS.LEFT)

def event_handler() -> None:
        screen.onkeypress(up, "Up")
        screen.onkeypress(right, "Right")
        screen.onkeypress(down, "Down")
        screen.onkeypress(left, "Left")
        screen.listen()

def self_collision_check() -> bool:
    flag = True
    for i in range(3, len(snake.segments)):
        if snake.segments[i].pos() == snake.pos():
            flag = False
    return flag

def collision_check() -> bool:
    flag = True
    if snake.pos()[0] < SCREEN_COORDS[0][0] + STEP_DIST or snake.pos()[0] > SCREEN_COORDS[0][1] - STEP_DIST:
        flag = False
    elif snake.pos()[1] < SCREEN_COORDS[1][0] + STEP_DIST or snake.pos()[1] > SCREEN_COORDS[1][1] - STEP_DIST:
        flag = False
    elif self_collision_check() is False:
        flag = False        
    else:
        flag = True
    return flag

def eat_food(food : Segment):
    flag = False
    if food.pos() == snake.pos():
        flag = snake.add_segment(food)
        food = Segment(food_spawn=True, snake_positions=snake.get_snake_positions())
        scoreboard.increment_score()
    return flag, food

def waiter(frame_time) -> None:
    sleep(frame_time)

def thread_builder(frame_time) -> Thread:
    thread = Thread(target=waiter, args=(frame_time,))
    return thread

def main() -> None:
    food = Segment(food_spawn=True, snake_positions=snake.get_snake_positions())
    frame_time = 0.2
    scoreboard.get_score_string()
    game_is_on = True
    eat_flag = False
    while game_is_on:
        screen.update()
        event_handler()
        screen.update()
        eat_flag = snake.move_snake(eat_flag, input_buffer)
        eat_flag, food = eat_food(food)
        game_is_on = collision_check()
        if game_is_on is not True:
            break
        screen.update()
        thread = thread_builder(frame_time)
        thread.start()
        thread.join()
    print("You lost!")
    screen.exitonclick()

if __name__ == '__main__':
    main()