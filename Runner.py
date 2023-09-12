from MusicServer import MusicServer, THEME
from SnakeGame import SnakeGame, UP, DOWN, LEFT, RIGHT
from DisplayServer import DisplayServer, EMPTY
from threading import Thread
from pynput import keyboard
from time import sleep
from os import system

class GAME_STATE:
    game_inner: bool
    
class Runner:
    running: bool
    run_display: bool
    run_game: bool
    height: int
    width: int
    base_length: int
    clearing: bool
    display: DisplayServer
    snake: SnakeGame
    music: MusicServer
    draw_sleep: float
    game_sleep: float
    game_ender: bool
    
    def __init__(self, height: int, width: int, clearing: bool, draw_sleep: float, game_sleep: float, base_length: int):
        self.running = False
        self.game_ended = False
        self.run_display = True
        self.run_game = True
        self.height = height
        self.width = width
        self.base_length = base_length
        self.clearing = clearing
        self.draw_sleep = draw_sleep
        self.game_sleep = game_sleep
        self.display = DisplayServer(self.height, self.width, self.clearing)
        self.music = MusicServer()
        self.snake = SnakeGame(self.display, self.music, self.base_length)
        self.music.play(THEME, True)

    def display_runner(self):
        while self.run_display:
            self.display.draw()
            sleep(self.draw_sleep)

    def game_runner(self):
        while self.run_game:
            if self.running:
                if not self.snake.run_game():
                    self.game_over()
            sleep(GAME_SLEEP)

    def exit_game(self):
        self.run_display = False
        self.run_game = False
        self.music.can_continue = False
        system("cls")
        
    def game_over(self):
        self.running = False
        self.game_ended = True
        self.snake.change_running_state(False)
        if self.snake.won:
            self.display.setArea(0, self.display.width-1, 0, 1, EMPTY)
            self.display.setText(0, 0, f"You have won. Score: {self.snake.score} Press Enter to reload or esc to end", True)
        else:
            self.display.setArea(0, self.display.width-1, 0, 1, EMPTY)
        self.display.setText(0, 0, f"Game over. Score: {self.snake.score} Press Enter to reload or esc to end", True)
        
    def pause_game(self):
        if self.running:
            self.snake.change_running_state(False)
            self.running = False
            self.display.setArea(0, self.display.width-1, 0, 1, EMPTY)
            self.display.setText(0, 0, "Game paused. press enter to continue or esc to end", True)
           
    def continue_game(self):
        if self.game_ended:
            self.snake.reset_game()
            self.prepare_game()
            self.game_ended = False
        else:
            self.running = True
            self.snake.change_running_state(True)

    def process_input(self, key):
        match key:
            case keyboard.Key.enter:
                self.continue_game()
            case keyboard.Key.esc:
                if not self.running:
                    self.exit_game()
                    return False
                self.pause_game()
            case keyboard.Key.left:
                self.snake.change_direction(LEFT)
            case keyboard.Key.right:
                self.snake.change_direction(RIGHT)
            case keyboard.Key.up:
                self.snake.change_direction(UP)
            case keyboard.Key.down:
                self.snake.change_direction(DOWN)
    
    def prepare_game(self):
        self.snake.prepare_game()
        self.display.setArea(0, self.display.width-1, 0, 1, EMPTY)
        self.display.setText(0, 0, "Press Enter to start the game", True)
        
    def runner(self):
        render_thread = Thread(target=self.display_runner, name="RENDER")
        game_thread = Thread(target=self.game_runner, name="GAME")
        input_thread = keyboard.Listener(on_press=self.process_input)

        input_thread.start()
        render_thread.start()
        game_thread.start()
        self.prepare_game()
        input_thread.join()

HEIGHT = 40
WIDTH = 40
CLEARING = True
DRAW_SLEEP = 0.035
GAME_SLEEP = 0.1
BASE_LENGTH = 4
RUN_GAME = True
RUN_DISPLAY = True

runner : Runner = Runner(HEIGHT, WIDTH, CLEARING, DRAW_SLEEP, GAME_SLEEP, BASE_LENGTH)
runner.runner()