import pygame
from heat2d import DISPATCHER
from heat2d.window import Window
from heat2d.renderer import Renderer
from heat2d.stage import Stage
from heat2d.gameobject import GameObject
from heat2d.libs.keys import key_dictionary
from heat2d.exceptions import NoStageDeclared
from heat2d.ui.context import Context
from heat2d import ui
from heat2d.timer import Timer, TickTimer


class Engine:

    def __init__(self):
        DISPATCHER["engine"] = self
        pygame.init()

        self.window = Window((800, 600))
        self.renderer = Renderer()

        self.events = None
        self.inp_funcs = {"key_held" : list(), "key_pressed" : list(), "key_released" : list(), "mouse_held" : list(), "mouse_pressed" : list(), "mouse_released" : list()}
        self.event_funcs = {"update" : list(), "every_tick" : list(), "every_time" : list()}
        self.timers = list()

        self.key_used = list()
        self.mouse_x, self.mouse_y = 0, 0

        self.current_stage = None
        self.stages = dict()
        self.gameobjects = list()

        self.__is_running = False

        #Initialize modules
        ui.init()

    def __repr__(self):
        return f"<heat2d.Engine({self.window})>"

    #   @engine.input decorator function to store input calls
    def input(self, func):
        self.inp_funcs[func.__name__].append(func)

    #   @engine.event decorator function to store input calls
    def event(self, *args):
        def wrapper(func):
            self.event_funcs[func.__name__].append(func)
            if func.__name__ == "every_tick": self.timers.append(TickTimer(func, args[0]))
            elif func.__name__ == "every_time": self.timers.append(Timer(func, args[0]))

        return wrapper

    def remove_by_id(self, inpfunc, id):
        for func in self.inp_funcs[inp_func]:
            if id(func) == id:
                self.inp_funcs[inp_func].remove(func)
                return

    def add(self, *args):
        for arg in args:
            if isinstance(arg, Context):
                self.renderer.ui_layers.append(arg)

            else:
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

        if not self.current_stage: raise NoStageDeclared("You have to declare at least one stage to run the engine.")

        while self.__is_running:
            self.window.clock.tick(self.window.max_fps)
            self.window.fps = self.window.clock.get_fps()

            self.handle_events()
            self.stages[self.current_stage].update()

            for timer in self.timers: timer.update()
            for func in self.event_funcs["update"]: func()
            self.renderer.draw()

        pygame.quit()
