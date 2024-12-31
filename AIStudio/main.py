import subprocess
import threading
from AIStudio import wakeup
from icecream import ic as cout
import pygame

pygame.mixer.init()
pygame.mixer.music.load(r"C:/Users/DUBEM/Desktop/New Horizon/Dictionary/AIStudio/001.mp3")


class AI:
    def expand_window_condition(self):
        if wakeup.wakeword():
            return True
        else:
            return False

    def play_intro(self):
        pygame.mixer.music.play()

    def expand_window(self, app_ins):
        if self.expand_window_condition():
            self.app_ins = app_ins
            self.app_ins._expand_(self.app_ins.screen)
            self.app_ins.screen.update()
            # self.play_intro()
            threading.Thread(target=AI().play_intro).start()

