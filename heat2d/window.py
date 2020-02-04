import pygame
import os


class Window:

    def __init__(self, size, title="Heat2D Game Project", icon=None, clear_color=(0, 0, 0)):
        self._width = size[0]
        self._height = size[1]
        self._size = size
        self._title = title
        self._icon = icon
        self.clear_color = clear_color

        if icon: self.icon = icon
        else: self.icon = os.path.join(__file__[:len(__file__) - len("window.py")], "favicon.png")
        self.size = size
        self.title = self._title

        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.center = (self.center_x, self.center_y)

        self.clock = pygame.time.Clock()
        self.max_fps = 60
        self.fps = self.max_fps

    def __repr__(self):
        return f"<heat2d.Window({self.size}, {self.title})>"

    @property
    def width(self): return self._width

    @width.setter
    def width(self, val):
        self._width = val
        self.surface = pygame.display.set_mode((self._width, self._height))

    @property
    def height(self): return self._height

    @height.setter
    def height(self, val):
        self._height = val
        self.surface = pygame.display.set_mode((self._width, self._height))

    @property
    def size(self): return self._size

    @size.setter
    def size(self, val):
        self._size = val
        self.surface = pygame.display.set_mode(self._size)

    @property
    def title(self): return self._title

    @title.setter
    def title(self, val):
        self._title = val
        pygame.display.set_caption(self._title)

    @property
    def icon(self): return self._icon

    @icon.setter
    def icon(self, val):
        self._icon = val
        pygame.display.set_icon(pygame.image.load(self._icon))
