#  This file is a part of the Heat2D Project and  #
#  distributed under the GPL 3 license            #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


import os
import struct
from math import atan2, degrees
import pygame

from heat2d import DISPATCHER
from heat2d.libs.utils import source_path
from heat2d.gl import Texture, Shader
from heat2d.animation.spritesheet import SpriteSheet



class Sprite:
    def __init__(self, filepath=None, loader=None):
        self.engine = DISPATCHER.engine

        self.gameobject = None
        self.sheets = dict()

        self.has_animation = False
        self.current_animation = None
        self.anim_duration = 0
        self.current_frame = 0
        self.playing = False
        self.loop = False
        self.stopsig = 2 #2: Don't stop  3: Stop directly  4: Finish and stop

        self.angle  = 0
        self.width  = 0
        self.height = 0

        self.__palette = None
        self._palette_buffer = None

        if filepath:
            self.load_texture(filepath)

        self.shader = Shader(
                        vertex   = source_path("shaders/sprite.vsh"),
                        fragment = source_path("shaders/sprite.fsh")
                    )

    def __repr__(self):
        return f"<heat2d.Sprite({self.source_width}x{self.source_height})>"

    def load_texture(self, filepath, sheet=None):
        if sheet:
            source = pygame.image.load(filepath)
            source_image = pygame.Surface((source.get_width()+2, source.get_height()+2), pygame.SRCALPHA)
            source_image.blit(source, (1, 1))

            s = source_image.get_size()

            if self.width < s[0]: self.width = s[0]
            if self.height < s[1]: self.height = s[1]

            sheet.sources.append({"source":source_image, "size":source_image.get_size(), "texture":Texture(source_image)})

        else:
            source = pygame.image.load(filepath)
            self.source_image = pygame.Surface((source.get_width()+2, source.get_height()+2), pygame.SRCALPHA)
            self.source_image.blit(source, (1, 1))
            self.source_size = self.source_image.get_size()
            self.source_width, self.source_height = self.source_size

            self.width  = self.source_width
            self.height = self.source_height

            self.texture = Texture(self.source_image)

    def add_animation(self, sheet):
        if not self.has_animation: self.has_animation = True
        self.sheets[sheet.name] = sheet
        for filepath in sheet.filepaths: self.load_texture(filepath, sheet)

    def play_animation(self, animname, duration=None, loop=False):
        if not animname in self.sheets: raise NameError(f"animname is not found.")

        self.stopsig = 2
        self.playing = True
        self.loop = loop

        self.current_animation = animname
        self.current_frame = 0
        if duration:
            self.anim_duration = duration
        else:
            self.anim_duration = len(self.sheets[animname].sources)

    def stop_animation(self, wait=False):
        if wait: self.stopsig = 4
        else: self.stopsig = 3

    def get_current_frame(self):
        return self.sheets[self.current_animation].sources[self.current_frame]

    def scale(self, scale):
        self.width *= scale
        self.height *= scale

    def rotate(self, angle):
        self.angle += angle
        if self.angle < 0:
            self.angle = 360
        elif self.angle >= 360:
            self.angle = 0
        self.gameobject.hitarea.set_angle(self.angle)

    def rotate_to(self, vector):
        self.angle = degrees(atan2(self.gameobject.position.y - vector.y,  self.gameobject.position.x - vector.x))

    def update(self):
        if self.has_animation and self.playing and not self.stopsig in (3,4):

            self.current_frame += (len(self.sheets[self.current_animation].sources) / self.anim_duration) / self.engine.settings.graphics.max_fps

            if int(self.current_frame) > len(self.sheets[self.current_animation].sources)-1:
                self.current_frame = 0
                if not self.loop: self.stopsig = 3
                return


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
