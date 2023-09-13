from MusicServer import MusicServer, THEME, THEME_NAME, GAME_OVER, GAME_OVER_NAME, EAT, EAT_NAME, WIN, WIN_NAME
from SnakeGame import SnakeGame, UP, DOWN, LEFT, RIGHT
from DisplayServer import DisplayServer, EMPTY
from threading import Thread
from pynput import keyboard
from time import sleep, time
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
    frame_time_list: list[float]
    
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
        self.frame_time_list = []
        self.display = DisplayServer(self.height, self.width, self.clearing, EMPTY)
        self.music = MusicServer()
        self.music.load_sound(THEME, THEME_NAME)
        self.music.load_sound(GAME_OVER, GAME_OVER_NAME)
        self.music.load_sound(EAT, EAT_NAME)
        self.music.load_sound(WIN, WIN_NAME)
        self.snake = SnakeGame(self.display, self.music, self.base_length)
        self.music.play(THEME_NAME, True)

    def fps_displayer(self):
        while self.run_display:
            self.display.setArea(0, self.display.width, 1, 2, EMPTY)
            average_frame_time = sum(self.frame_time_list) / len(self.frame_time_list)
            try:
                self.display.setText(0, 1, f"AVERAGE FPS: {round(1000000/average_frame_time, 2)}", True)
            except:
                pass
            sleep(self.game_sleep)
    
    def display_runner(self):
        while self.run_display:
            timestamp = time() * 1000000
            self.display.draw()
            self.frame_time_list.append(time() * 1000000 - timestamp)
            if (len(self.frame_time_list) > 100):
                self.frame_time_list.pop(0)
            #sleep(self.draw_sleep)

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
        self.clear_input_buffer()
        
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
    
    def clear_input_buffer(slef):
        try:
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        except ImportError:
            import sys, termios
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    
    def prepare_game(self):
        self.snake.prepare_game()
        self.display.setArea(0, self.display.width-1, 0, 1, EMPTY)
        self.display.setText(0, 0, "Press Enter to start the game", True)
        
    def runner(self):
        render_thread = Thread(target=self.display_runner, name="RENDER")
        game_thread = Thread(target=self.game_runner, name="GAME")
        input_thread = keyboard.Listener(on_press=self.process_input)
        fps_display_thread = Thread(target=self.fps_displayer, name="FPS DISPLAYER")

        input_thread.start()
        render_thread.start()
        game_thread.start()
        fps_display_thread.start()
        self.prepare_game()
        input_thread.join()

HEIGHT = 50
WIDTH = 50
CLEARING = True
DRAW_SLEEP = 0.001
GAME_SLEEP = 0.1
BASE_LENGTH = 4
RUN_GAME = True
RUN_DISPLAY = True

runner : Runner = Runner(HEIGHT, WIDTH, CLEARING, DRAW_SLEEP, GAME_SLEEP, BASE_LENGTH)
runner.runner()