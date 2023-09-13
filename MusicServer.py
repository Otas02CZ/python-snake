import pygame
import time
import threading

GAME_OVER : str = "./sounds/error.mp3"
EAT: str = "./sounds/apple_bite.mp3"
THEME: str = "./sounds/theme.mp3"
WIN: str = "./sounds/round_end.mp3"

THEME_NAME: str = "THEME"
GAME_OVER_NAME: str = "GAME_OVER"
EAT_NAME: str = "EAT"
WIN_NAME: str = "WIN"

class MusicServer:
    channels: int
    can_continue: bool
    emptyChannels: list[int]
    sounds: dict[str, pygame.mixer.Sound] = {}
    
    def __init__(self) -> None:
        self.channels = 8
        self.can_continue = True
        pygame.mixer.init(channels=self.channels)
        self.emptyChannels = [i for i in range(self.channels)]
    
    def load_sound(self, sound_path: str, sound_name: str):
        self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
     
    def _play(self, sound_name: str, repeat):
        try:
            channel = self.emptyChannels.pop(0)
        except:
            return
        while True:
            pygame.mixer.Channel(channel).play(self.sounds[sound_name])
            while pygame.mixer.Channel(channel).get_busy() and self.can_continue:
                time.sleep(0.1)
            if not self.can_continue:
                break
            if not repeat:
                break
        self.emptyChannels.append(channel)
    
    def play(self, sound, repeat):
        play_thread = threading.Thread(target=self._play, args=[sound, repeat], name=sound)
        play_thread.start()