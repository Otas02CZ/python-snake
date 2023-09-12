from DisplayServer import DisplayServer, OBSTACLE, HEAD, BODY, FOOD, EMPTY
from MusicServer import MusicServer
from random import randint
import math

class Position:
    x: int
    y: int
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
UP = Position(0, -1)
DOWN = Position(0, 1)
LEFT = Position(-1, 0)
RIGHT = Position(1, 0)
NONE = Position(0, 0)

class SnakeGame:
    snakePieces: list[Position]
    obstacles: list[Position]
    food: Position
    score: int
    running: bool
    display: DisplayServer
    music: MusicServer
    base_length: int
    direction: Position

    def __init__(self, display: DisplayServer, music: MusicServer, base_length: int):
        self.running = False
        self.display = display
        self.music = music
        self.obstacles = []
        self.snakePieces = []
        self.food = None
        self.score = 0
        self.base_length = base_length
        self.direction = Position(-1, 0)
        
    def reset_game(self):
        self.direction = Position(-1, 0)
        self.snakePieces = []
        self.obstacles = []
        self.score = 0
        self.display.clear()
        
    def create_food(self):
        while True:
            y_cor = randint(1, self.display.height-1)
            x_cor = randint(0, self.display.width-1)
            will_continue = False
            for obstacle in self.obstacles:
                if obstacle.x == x_cor and obstacle.y == y_cor:
                    will_continue = True
            if will_continue:
                continue
            for snakePiece in self.snakePieces:
                if snakePiece.x == x_cor and snakePiece.y == y_cor:
                    will_continue = True
            if will_continue:
                continue
            self.food = Position(x_cor, y_cor)
            self.display.setPixel(x_cor, y_cor, FOOD)
            break
    
    def change_direction(self, direction: Position):
        if self.running:
            if direction.x + self.direction.x == 0 and direction.y + self.direction.y == 0:
                return
            self.direction = direction
    
    def change_running_state(self, running):
        self.running = running;                
    
    def prepare_game(self):
        y_cor : int = self.display.height-1
        x_cor : int = self.display.width-1
        for x in range(self.display.width):
            self.obstacles.append(Position(x, 1))
            self.obstacles.append(Position(x, y_cor))
            self.display.setPixel(x, 1, OBSTACLE)
            self.display.setPixel(x, y_cor, OBSTACLE)
        for y in range(1, self.display.height):
            self.obstacles.append(Position(0, y))
            self.obstacles.append(Position(x_cor, y))
            self.display.setPixel(0, y, OBSTACLE)
            self.display.setPixel(x_cor, y, OBSTACLE)
        y_cor = math.ceil(self.display.height/2)
        x_cor = math.ceil(self.display.width/2)
        for i in range(self.base_length):
            self.snakePieces.append(Position(x_cor, y_cor))
            if (i == 0):
                self.display.setPixel(x_cor, y_cor, HEAD)
            else:
                self.display.setPixel(x_cor, y_cor, BODY)
            x_cor += 1
        self.create_food()
        
    def obstacle_hit(self, next_position: Position) -> bool:
        for obstacle in self.obstacles:
            if obstacle.x == next_position.x and obstacle.y == next_position.y:
                return True
        return False
    
    def snake_hit(self, next_position: Position) -> bool:
        for snakePiece in self.snakePieces:
            if snakePiece.x == next_position.x and snakePiece.y == next_position.y:
                return True
        return False
    
    def food_eaten(self, next_position: Position) -> bool:
        return self.food.x == next_position.x and self.food.y == next_position.y
    
    def run_game(self) -> bool:
        next_position : Position = Position(self.snakePieces[0].x + self.direction.x, self.snakePieces[0].y + self.direction.y)
        if self.obstacle_hit(next_position) or self.snake_hit(next_position):
            return False
        if self.food_eaten(next_position):
            self.score += 1
            self.snakePieces.insert(0, next_position)
            self.display.setPixel(next_position.x, next_position.y, HEAD)
            self.display.setPixel(self.snakePieces[1].x, self.snakePieces[1].y, BODY)
            self.create_food()
        else:
            self.snakePieces.insert(0, next_position)
            last_piece : Position = self.snakePieces.pop()
            self.display.setPixel(last_piece.x, last_piece.y, EMPTY)
            self.display.setPixel(next_position.x, next_position.y, HEAD)
            self.display.setPixel(self.snakePieces[1].x, self.snakePieces[1].y, BODY)
        self.display.setArea(0, self.display.width-1, 0, 1, EMPTY)
        self.display.setText(0, 0, f"Score: {self.score}", True)
        return True