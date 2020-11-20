import pygame


class Context:
    def __init__(self, position, size):
        self.x, self.y = position
        self.width, self.height = size
        self.layers = list()
        self.layers.append(Layer(self))
        self.visible = True
        self.effect = None

    def __repr__(self):
        return f"<heat2d.ui.Context(({self.x},{self.y}), {self.width}x{self.height})>"

    def new_layer(self, num=1):
        for i in range(0, num):
            self.layers.append(Layer(self))


class Layer:
    def __init__(self, context):
        self.context = context
        self.surface = pygame.Surface((self.context.width, self.context.height), pygame.SRCALPHA).convert_alpha()
        self._opacity = 255

    def __repr__(self):
        return f"<heat2d.ui.Layer()>"

    def clear(self, color=None):
        if color: self.surface.fill(color)
        else: self.surface.fill((0, 0, 0, 0))

    @property
    def opacity(self): return self._opacity

    @opacity.setter
    def opacity(self, val):
        self._opacity = val
        self.surface.set_alpha(self._opacity)
