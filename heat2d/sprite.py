import os
import pygame
import struct
from math import atan2, degrees

from heat2d import DISPATCHER
from heat2d.libs.utils import sourcepath
from heat2d.gl import Texture, Shader


class Sprite:
    def __init__(self, filepath):
        self.engine = DISPATCHER.engine

        self.gameobject = None
        self.filepath = filepath

        source = pygame.image.load(self.filepath)
        self.source_image = pygame.Surface((source.get_width()+2, source.get_height()+2), pygame.SRCALPHA)
        self.source_image.blit(source, (1, 1))
        self.source_size = self.source_image.get_size()
        self.source_width, self.source_height = self.source_size

        self.width = self.source_width
        self.height = self.source_height

        self.texture = Texture(self.source_image)
        self.shader = Shader(
                        vertex   = os.path.join(sourcepath, "shaders", "sprite.vsh"),
                        fragment = os.path.join(sourcepath, "shaders", "sprite.fsh")
                    )

        self.angle = 0

        self.__palette = None
        self._palette_buffer = None

    def __repr__(self):
        return f"<heat2d.Sprite({self.source_width}x{self.source_height})>"

    def scale(self, scale):
        self.width *= scale
        self.height *= scale

    def rotate(self, angle):
        self.angle += angle

    def rotate_to(self, vector):
        #self.angle = (-degrees(atan2(self.game_object.position.y - vector.y,  self.game_object.position.x - vector.x)) - 180) % 360
        self.angle = degrees(atan2(self.gameobject.position.y - vector.y,  self.gameobject.position.x - vector.x))

    @property
    def size(self): return (self.width, self.height)

    @size.setter
    def size(self, val):
        self.width = val[0]
        self.height = val[1]

    @property
    def palette(self): return self.__palette

    @palette.setter
    def palette(self, val):
        self.__palette = val

        colors = list()
        for color in self.__palette:
            colors.append(color.r/255)
            colors.append(color.g/255)
            colors.append(color.b/255)
            colors.append(color.a/255)

        for i in range(256-len(self.__palette)):
            colors.append(0.0)
            colors.append(0.0)
            colors.append(0.0)
            colors.append(1.0)

        self._palette_buffer = struct.pack(f"{256*4}f", *colors)
