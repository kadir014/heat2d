import pygame
import os
import struct

from heat2d import DISPATCHER
from heat2d.math import Vector2
from heat2d.libs.color import Color
from heat2d.libs.utils import sourcepath


class Window:
    def __init__(self, size, title="Heat2D Game Project", icon=None, clear_color=(0, 0, 0)):
        self.engine = DISPATCHER.engine
        self._width = size[0]
        self._height = size[1]
        self._size = size
        self._title = title
        self._icon = icon

        if icon: self.icon = icon
        else: self.icon = os.path.join(sourcepath, "favicon.png")
        self.size = size
        self.title = self._title

        self.fullscreen = False

        if isinstance(clear_color, Color):
            self.clear_color = clear_color
        else:
            self.clear_color = Color(clear_color)

        self.center = Vector2(self.width / 2, self.height / 2)

        self.clock = pygame.time.Clock()
        self.max_fps = 60
        self.fps = self.max_fps
        self.deltatime = 0

    def __repr__(self):
        return f"<heat2d.Window({self.width}x{self.height}, {self.title})>"

    def take_screenshot(self, filepath, area=None):
        snap = pygame.image.fromstring(self.engine.renderer.ctx.screen.read(), self.size, "RGB")
        if area:
            surf = pygame.Surface((area[2]-area[0], area[3]-area[1]))
            surf.blit(snap, (-area[0], -area[1]))
            pygame.image.save(surf, filepath)
        else:
            pygame.image.save(snap, filepath)

    def toggle_fullscreen(self):
        if self.fullscreen:
            pygame.display.set_mode((self._width, self._height), pygame.DOUBLEBUF|pygame.OPENGL)
            self.surface = pygame.Surface((self._width, self._height))
            self.fullscreen = False

        else:
            pygame.display.set_mode((self._width, self._height), pygame.DOUBLEBUF|pygame.OPENGL|pygame.FULLSCREEN)
            self.surface = pygame.Surface((self._width, self._height))
            self.fullscreen = True

    @property
    def width(self): return self._width

    @width.setter
    def width(self, val):
        self._width = val
        pygame.display.set_mode((self._width, self._height), pygame.DOUBLEBUF|pygame.OPENGL)
        self.surface = pygame.Surface((self._width, self._height))

    @property
    def height(self): return self._height

    @height.setter
    def height(self, val):
        self._height = val
        pygame.display.set_mode((self._width, self._height), pygame.DOUBLEBUF|pygame.OPENGL)
        self.surface = pygame.Surface((self._width, self._height))

    @property
    def size(self): return self._size

    @size.setter
    def size(self, val):
        self._size = val
        self._width = self._size[0]
        self._height = self._size[1]
        pygame.display.set_mode((self._width, self._height), pygame.DOUBLEBUF|pygame.OPENGL)
        self.surface = pygame.Surface((self._width, self._height))

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
