import pygame

class UILayer:

    def __init__(self, position, size):
        self.x, self.y = position
        self.width, self.height = size
        self.back_surface = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()
        self.front_surface = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()
        self.surface = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()

    def __repr__(self):
        return f"heat2d.ui.UILayer(({self.x},{self.y}), {self.width}x{self.height})"

    def render(self, clear=True):
        if clear: self.surface.fill((255, 255, 255, 255))
        self.surface.blit(self.back_surface, (0, 0))
        self.surface.blit(self.front_surface, (0, 0))
