import pygame
from heat2d_dev import DISPATCHER

class Sprite:

    def __init__(self, stage = None, entity = None, background = False, scroll = None):
        self.surface = pygame.Surface((0, 0))
        self.width = 0
        self.height = 0
        self.center = (0, 0)

        self.stage = stage
        self.entity = entity
        self.background = background
        self.scroll = scroll

        self.init()

        self.colorkey = (255, 0, 255)
        self.frames = list()
        self.current_frame = 0
        self.has_animation = False
        self.animations = dict()
        self.default_animation = None
        self.current_animation = None
        self.animation_state = "playing"
        self.tick = 0

    def __repr__(self):
        return f"<heat2d.sprite.Sprite((Entity:{self.entity}, Background:{self.background}))>"

    def __str__(self):
        return self.__repr__()

    def init(self):
        if self.stage: DISPATCHER["engine"].sprites[self.stage.__class__.__name__ + str(len(DISPATCHER["engine"].sprites))] = {"sprite" : self, "entity" : self.entity, "background" : self.background, "scroll" : self.scroll}

    def set_image(self, filepath):
        self.surface = pygame.image.load(filepath).convert_alpha()
        self.width = self.surface.get_rect().width
        self.height = self.surface.get_rect().height
        self.center = (self.width / 2, self.height / 2)

    def set_background(self, scroll):
        self.background = True
        self.scroll = scroll

    def set_sheet(self, filepath, width, height):
        sheet = pygame.image.load(filepath).convert_alpha()
        cell_width = sheet.get_rect().width // width
        cell_height = sheet.get_rect().height // height

        self.frames = list()

        for y in range(height):
            for x in range(width):
                temp_surface = pygame.Surface((cell_width, cell_height))
                temp_surface.fill(self.colorkey)
                temp_surface.blit(sheet, (0, 0), area = (x * cell_width, y * cell_height, cell_width, cell_height))
                temp_surface.set_colorkey(self.colorkey)
                self.frames.append(temp_surface)

        self.set_frame(self.current_frame)
        self.has_animation = True

    def set_frame(self, frame):
        self.surface = self.frames[frame]
        self.width = self.surface.get_rect().width
        self.height = self.surface.get_rect().height
        self.center = (self.width / 2, self.height / 2)

    def next_frame(self):
        self.tick += 1
        if self.tick > self.animations[self.current_animation]["sequence"][self.current_frame - self.animations[self.current_animation]["sequence"][0][0]][1]:
            self.tick = 0
            self.current_frame += 1
            if self.current_frame > self.animations[self.current_animation]["sequence"][len(self.animations[self.current_animation]["sequence"]) - 1][0]:
                if self.animations[self.current_animation]["repeat"]: self.current_frame = self.animations[self.current_animation]["sequence"][0][0]
                else:
                    self.current_animation = self.default_animation
                    self.current_frame = self.animations[self.current_animation]["sequence"][0][0]
            self.set_frame(self.current_frame)

    #   TODO
    def prev_frame(self):
        pass

    def add_animation(self, name, sequence, repeat = False):
        self.animations[name] = {"sequence" : sequence, "repeat" : repeat}
        if len(self.animations) == 1:
            self.default_animation = name
            self.current_animation = name

    def play(self, name):
        self.animation_state = "playing"
        if self.current_animation != name: self.current_frame = self.animations[name]["sequence"][0][0]
        self.current_animation = name

    def stop(self, name = None):
        self.animation_state = "stopped"
        if name:
            if name == self.current_animation:
                if self.current_animation != self.default_animation: self.current_frame = self.animations[self.default_animation]["sequence"][0][0]
                self.current_animation = self.default_animation
        else:
            if self.current_animation != self.default_animation: self.current_frame = self.animations[self.default_animation]["sequence"][0][0]
            self.current_animation = self.default_animation

    def pause(self):
        self.animation_state = "paused"
