import pygame
import time

from heat2d import DISPATCHER


master_volume = 1

class Sound:
    def __init__(self, filename):
        DISPATCHER.engine.sounds.append(self)

        self.volume = 1
        self.right = 1
        self.left = 1
        self.source_sound = pygame.mixer.Sound(filename)
        self.channel = pygame.mixer.find_channel()

        self.dynamic = False
        self.source_object = None
        self.focus_object = None
        self.max_distance = 200
        self.balance_factor = 200
        self.balance_max = 0.73

    def __repr__(self):
        return f"<heat2d.Sound({self.filename}, volume={int(self.volume * 100)}%)>"

    def play(self):
        self.channel.play(self.source_sound)

    def set_source(self, source, focus):
        self.source_object = source
        self.focus_object = focus

    def update(self):
        if self.dynamic and self.source_object and self.focus_object:
            b = (self.source_object.position.x - self.focus_object.position.x) / self.balance_factor
            dist = ((self.source_object.position.x - self.focus_object.position.x)**2 + (self.source_object.position.y - self.focus_object.position.y)**2) / self.max_distance**2
            if dist > 1: dist = 1
            volume = 1 - dist

            if b > 0:
                self.left = self.balance_max - b
                if self.left < 0: self.left = 0
                self.right = 1
            elif b < 0:
                self.left = 1
                self.right = self.balance_max - abs(b)
                if self.right < 0: self.right = 0
            else:
                self.left = 1
                self.right = 1

            self.channel.set_volume(self.left * self.volume * volume * master_volume, self.right * self.volume * volume * master_volume)
