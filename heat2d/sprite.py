import pygame
from math import cos, sin, pi, atan2, degrees
from heat2d.visuals import Rectangle


class Sprite:
    def __init__(self, filename):
        if isinstance(filename, Rectangle):
            self.__source_image = pygame.Surface((filename.width, filename.height)).convert()
            self.__source_image.fill(filename.color)
        else:
            self.__source_image = pygame.image.load(filename)

        self.__calc(self.__source_image)

        self.angle = 0

        self.__blit(False)

    def __calc(self, source_surface):
        self.source_image = source_surface.convert_alpha()
        self.source_size = source_surface.get_size()
        self.width, self.height = self.source_size

        if self.width != self.height:
            max_size = max(self.source_size)

            temp_surf = pygame.Surface((max_size, max_size), pygame.SRCALPHA)
            temp_surf.blit(self.source_image, (max_size / 2 - self.width / 2,
                                               max_size / 2 - self.height / 2))

            self.__calc(temp_surf)
            return

        self.width_constant = abs(self.width - (cos(pi / 4) * self.width) * 2)
        self.height_constant = abs(self.height - (cos(pi / 4) * self.height) * 2)

        self.surface = pygame.Surface((self.width + self.width_constant,
                                       self.height + self.height_constant),
                                       pygame.SRCALPHA).convert_alpha()

        self.size = self.surface.get_size()
        self.surface_width, self.surface_height = self.size

        self.flip_horizontal = False
        self.flip_vertical = False

    def __blit(self, rotated=True):
        self.surface.fill((255, 255, 255, 255))

        if rotated:
            self.rotated_surface = pygame.transform.rotate(self.source_image, self.angle)

            self.surface.blit(self.rotated_surface, (-self.rotated_surface.get_width() / 2 + (self.width + self.width_constant) / 2,
                                                     -self.rotated_surface.get_height() / 2 + (self.height + self.height_constant) / 2))

        else:
            self.surface.blit(self.source_image, (-self.width / 2 + (self.width + self.width_constant) / 2,
                                                  -self.height / 2 + (self.height + self.height_constant) / 2))

    def get_hitbox(self):
        return (-self.rotated_surface.get_width() / 2 + (self.width + self.width_constant) / 2,
                -self.rotated_surface.get_height() / 2 + (self.height + self.height_constant) / 2,
                self.rotated_surface.get_width(), self.rotated_surface.get_height())

    def scale(self, scale):
        self.__calc(pygame.transform.scale(self.__source_image, (self.width * scale, self.height * scale)))
        self.__blit(False)

    def set_size(self, size):
        self.__calc(pygame.transform.scale(self.__source_image, size))
        self.__blit(False)

    def rotate(self, angle):
        self.angle = (self.angle + angle) % 360
        self.__blit()

    def rotate_to(self, x, y, tx, ty):
        self.angle = (-degrees(atan2(y - ty,  x - tx)) - 180) % 360
        self.__blit()

    def flip(self, horizontal=False, vertical=False):
        if horizontal:
            if self.flip_horizontal: self.flip_horizontal = False
            else: self.flip_horizontal = True
            self.source_image = pygame.transform.flip(self.source_image, True, False)
            self.__blit(False)

        elif vertical:
            if self.flip_vertical: self.flip_vertical = False
            else: self.flip_vertical = True
            self.source_image = pygame.transform.flip(self.source_image, False, True)
            self.__blit(False)

    def orient(self, orientation):
        if orientation.lower() == "east" and self.flip_horizontal:
            self.flip(horizontal=True)

        elif orientation.lower() == "west" and not self.flip_horizontal:
            self.flip(horizontal=True)

        elif orientation.lower() == "north" and self.flip_vertical:
            self.flip(vertical=True)

        elif orientation.lower() == "south" and not self.flip_vertical:
            self.flip(vertical=True)
