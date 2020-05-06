import pygame


class Context:

    def __init__(self, position, size):
        self.x, self.y = position
        self.width, self.height = size
        self.back_surface = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()
        self.front_surface = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()
        self.effect = None

    def __repr__(self):
        return f"<heat2d.ui.Context(({self.x},{self.y}), {self.width}x{self.height})>"

    def set_effect(self, effect):
        self.effect = effect
