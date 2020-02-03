import pygame
from math import ceil
from heat2d import DISPATCHER
from heat2d.window import Window
from heat2d.renderer import Renderer
from heat2d.stage import Stage
from heat2d.gameobject import GameObject
from heat2d.visuals.rectangle import Rectangle
from heat2d.libs.keys import key_dictionary
from heat2d.exceptions import warn


class Engine:

    def __init__(self):
        DISPATCHER["engine"] = self
        pygame.init()

        self.window = Window((800, 600))
        self.renderer = Renderer()

        self.events = None
        self.inp_funcs = {"key_held" : list(), "key_pressed" : list(), "key_released" : list(), "mouse_held" : list(), "mouse_pressed" : list(), "mouse_released" : list()}
        self.key_used = list()
        self.mouse_x, self.mouse_y = 0, 0

        self.current_stage = None
        self.stages = dict()
        self.gameobjects = list()

        self.__is_running = False

    def __repr__(self):
        return f"<heat2d.Engine({self.window})>"

    #   @engine.input decorator function to store input calls
    def input(self, func):
        self.inp_funcs[func.__name__].append(func)

    def add(self, *args):
        for arg in args:
            #Initialize objects
            inst = arg()

            if isinstance(inst, Stage):
                self.stages[inst.__class__.__name__] = inst
                if len(self.stages) == 1: self.current_stage = inst.__class__.__name__

            elif isinstance(inst, GameObject):
                self.gameobjects.append(inst)

    def change_stage(self, stage):
        if stage in self.stages: self.current_stage = stage
        else: raise NameError(f"{stage} is not found on stages.")

    def handle_events(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        for key in self.key_used:
            for func in self.inp_funcs["key_held"]:
                func(list(key_dictionary.keys())[list(key_dictionary.values()).index(key)])

        for func in self.inp_funcs["mouse_held"]:
            m = pygame.mouse.get_pressed()
            b = None
            if m[0]: b = "left"
            elif m[1]: b = "middle"
            elif m[2]: b = "right"
            for func in self.inp_funcs["mouse_held"]: func(b)

        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT: self.__is_running = False

            elif event.type == pygame.KEYDOWN:
                self.key_used.append(event.key)
                for func in self.inp_funcs["key_pressed"]:
                    func(list(key_dictionary.keys())[list(key_dictionary.values()).index(event.key)])

            elif event.type == pygame.KEYUP:
                self.key_used.remove(event.key)
                for func in self.inp_funcs["key_released"]:
                    func(list(key_dictionary.keys())[list(key_dictionary.values()).index(event.key)])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                b = None
                if event.button == 1: b = "left"
                elif event.button == 2 : b = "middle"
                elif event.button == 3 : b = "right"
                for func in self.inp_funcs["mouse_pressed"]: func(b)

            elif event.type == pygame.MOUSEBUTTONUP:
                b = None
                if event.button == 1: b = "left"
                elif event.button == 2 : b = "middle"
                elif event.button == 3 : b = "right"
                for func in self.inp_funcs["mouse_released"]: func(b)


        self.inp_funcs = {"key_held" : list(), "key_pressed" : list(), "key_released" : list(), "mouse_held" : list(), "mouse_pressed" : list(), "mouse_released" : list()}

    def run(self):
        self.__is_running = True

        stage_warn = False
        if not self.current_stage:
            warn("No stage has been declared.")
            stage_warn = True

        while self.__is_running:
            self.window.clock.tick(self.window.max_fps)
            self.window.fps = self.window.clock.get_fps()

            self.handle_events()
            if not stage_warn: self.stages[self.current_stage].update()

            self.renderer.draw()

        pygame.quit()
