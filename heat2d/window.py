#  This file is a part of the Heat2D Project and  #
#  distributed under the LGPL 3 license           #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


import pygame
import os

from heat2d import DISPATCHER
from heat2d.math import Vector2
from heat2d.color import Color
from heat2d.libs.utils import source_path
from heat2d.gl.texture import Texture



class Window:
    def __init__(self, size, title="Heat2D Game Project", icon=None, clear_color=(0, 0, 0)):
        self.engine = DISPATCHER.engine
        self.__width = size[0]
        self.__height = size[1]
        self.__size = size
        self.__title = title
        self.__icon = icon

        self.fullscreen = False

        if icon: self.icon = icon
        else: self.icon = source_path("favicon.png")
        self.__updategl = False
        self.size = size
        self.__updategl = True
        self.title = self.__title

        if isinstance(clear_color, Color):
            self.clear_color = clear_color
        else:
            self.clear_color = Color(clear_color)

        self.center = Vector2(self.width / 2, self.height / 2)

    def __repr__(self):
        return f"<heat2d.Window({self.width}x{self.height}, {self.title})>"

    def is_active(self):
        return pygame.display.get_active()

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
            pygame.display.set_mode((self.__width, self.__height), pygame.DOUBLEBUF|pygame.OPENGL)
            self.surface = pygame.Surface((self.__width, self.__height))
            self.fullscreen = False

        else:
            pygame.display.set_mode((self.__width, self.__height), pygame.DOUBLEBUF|pygame.OPENGL|pygame.FULLSCREEN|pygame.HWSURFACE)
            self.surface = pygame.Surface((self.__width, self.__height))
            self.fullscreen = True

    @property
    def width(self): return self.__width

    @width.setter
    def width(self, val):
        self.__width = val

        if self.fullscreen:
            self.toggle_fullscreen()

            pygame.display.set_mode((self.__width, self.__height), pygame.DOUBLEBUF|pygame.OPENGL)
            self.surface = pygame.Surface((self.__width, self.__height))

            if self.__updategl:
                self.engine.renderer.ctx.viewport = (0, 0, self.__width, self.__height)

                self.engine.renderer.texture = Texture(self.surface, ctx=self.engine.renderer.ctx)
                self.engine.renderer.gamefbo = self.engine.renderer.ctx.framebuffer((self.engine.renderer.texture.texobj,))

            self.toggle_fullscreen()

        else:
            pygame.display.set_mode((self.__width, self.__height), pygame.DOUBLEBUF|pygame.OPENGL)
            self.surface = pygame.Surface((self.__width, self.__height))

            if self.__updategl:
                self.engine.renderer.ctx.viewport = (0, 0, self.__width, self.__height)

                self.engine.renderer.texture = Texture(self.surface, ctx=self.engine.renderer.ctx)
                self.engine.renderer.gamefbo = self.engine.renderer.ctx.framebuffer((self.engine.renderer.texture.texobj,))

    @property
    def height(self): return self.__height

    @height.setter
    def height(self, val):
        self.__height = val

        if self.fullscreen:
            self.toggle_fullscreen()

            pygame.display.set_mode((self.__width, self.__height), pygame.DOUBLEBUF|pygame.OPENGL)
            self.surface = pygame.Surface((self.__width, self.__height))

            if self.__updategl:
                self.engine.renderer.ctx.viewport = (0, 0, self.__width, self.__height)

                self.engine.renderer.texture = Texture(self.surface, ctx=self.engine.renderer.ctx)
                self.engine.renderer.gamefbo = self.engine.renderer.ctx.framebuffer((self.engine.renderer.texture.texobj,))

            self.toggle_fullscreen()

        else:
            pygame.display.set_mode((self.__width, self.__height), pygame.DOUBLEBUF|pygame.OPENGL)
            self.surface = pygame.Surface((self.__width, self.__height))

            if self.__updategl:
                self.engine.renderer.ctx.viewport = (0, 0, self.__width, self.__height)

                self.engine.renderer.texture = Texture(self.surface, ctx=self.engine.renderer.ctx)
                self.engine.renderer.gamefbo = self.engine.renderer.ctx.framebuffer((self.engine.renderer.texture.texobj,))

    @property
    def size(self): return self.__size

    @size.setter
    def size(self, val):
        self.__size = val
        self.__width = self.__size[0]
        self.__height = self.__size[1]

        if self.fullscreen:
            self.toggle_fullscreen()

            pygame.display.set_mode((self.__width, self.__height), pygame.DOUBLEBUF|pygame.OPENGL)
            self.surface = pygame.Surface((self.__width, self.__height))

            if self.__updategl:
                self.engine.renderer.ctx.viewport = (0, 0, self.__width, self.__height)

                self.engine.renderer.texture = Texture(self.surface, ctx=self.engine.renderer.ctx)
                self.engine.renderer.gamefbo = self.engine.renderer.ctx.framebuffer((self.engine.renderer.texture.texobj,))

            self.toggle_fullscreen()

        else:
            pygame.display.set_mode((self.__width, self.__height), pygame.DOUBLEBUF|pygame.OPENGL)
            self.surface = pygame.Surface((self.__width, self.__height))

            if self.__updategl:
                self.engine.renderer.ctx.viewport = (0, 0, self.__width, self.__height)

                self.engine.renderer.texture = Texture(self.surface, ctx=self.engine.renderer.ctx)
                self.engine.renderer.gamefbo = self.engine.renderer.ctx.framebuffer((self.engine.renderer.texture.texobj,))

    @property
    def title(self): return self.__title

    @title.setter
    def title(self, val):
        self.__title = val
        pygame.display.set_caption(self.__title)

    @property
    def icon(self): return self.__icon

    @icon.setter
    def icon(self, val):
        self.__icon = val
        pygame.display.set_icon(pygame.image.load(self.__icon))
