from turtle import Turtle, Screen
from utils import SCREEN_COORDS, SCREEN_RES
import csv

SCOREBOARD_POS = (SCREEN_COORDS[0][0]+25,SCREEN_COORDS[1][0]-13.5)


class Scoreboard(Turtle):
    def __init__(self, shape: str = "classic", undobuffersize: int = 1000, visible: bool = False) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.player_name : str = "player_name"
        self.score : int = 0
        self.draw_scoreboard()
    
    def get_score_string(self) -> str:
        score_str = f"{(4-len(str(self.score)))*"0"}{str(self.score)}"
        return score_str

    def draw_scoreboard(self) -> None:
        self.teleport(SCOREBOARD_POS[0],SCOREBOARD_POS[1])
        score_string = self.get_score_string()
        self.write(score_string, font=("OCR A Extended", 16, "normal"))

    def increment_score(self) -> None:
        self.score += 10
        self.clear()
        self.draw_scoreboard()

    def input_player_name(self) -> None:
        self.player_name = self.screen.textinput("Enter Nickname", "Enter your Nickname(max 11 characters): ")
        self.player_name = self.player_name[:11]
        print(self.player_name)

    def get_scoreboard_list(self) -> list[dict]:
        with open('scoreboard.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            scoreboard_list = []
            for row in csv_reader:
                scoreboard_list.append(row)
        
        return scoreboard_list

    def get_score_item(self, rows) -> str:
        return int(rows[::][1])

    def insert_score_into_csv(self) -> None:
        scoreboard_list = self.get_scoreboard_list()
        fields = ['Name', 'Score']
        rows = []
        for score in scoreboard_list:
            field1, field2 = score.values()
            data = [field1, field2]
            rows.append(data)
        
        rows.append([self.player_name, self.score])
        rows.sort(key=self.get_score_item, reverse=True)
        
        while len(rows) > 5:
            rows.pop()
        
        filename = "scoreboard.csv"
        
        with open(filename, 'w', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)

    def display_scoreboard(self, screen : Screen) -> None:
        screen.clear()
        screen.setup(width=SCREEN_RES[0], height=SCREEN_RES[1])
        screen.screensize(canvwidth=SCREEN_RES[0],canvheight=SCREEN_RES[1])
        screen.setworldcoordinates(SCREEN_COORDS[0][0], SCREEN_COORDS[1][0]-10, SCREEN_COORDS[0][1]+10, SCREEN_COORDS[1][1])
        screen.mode("world")
        screen.colormode(255)
        screen.bgcolor(139,172,15)
        screen.title("Scoreboard")
        screen.tracer(0)
        
        self.teleport(0, 100)
        score_string = "__________"
        self.write(score_string, align="center", font=("OCR A Extended", 20, "bold"))
        score_string = "Scoreboard"
        self.write(score_string, align="center", font=("OCR A Extended", 20, "bold"))
        
        pos = 40
        place = 1
        scoreboard_list = self.get_scoreboard_list()
        
        for score in scoreboard_list:
            self.teleport(-170, pos)
            score_string = f"{place}. {score['Name']}"
            self.write(score_string, align="left", font=("OCR A Extended", 20, "normal"))
            self.teleport(170, pos)
            score_string = f"{(4-len(str(score['Score'])))*"0"}{str(score['Score'])}"
            self.write(score_string, align="right", font=("OCR A Extended", 20, "normal"))
            pos -= 30
            place += 1