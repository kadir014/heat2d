import pygame
from heat2d import DISPATCHER
from heat2d.window import Window
from heat2d.renderer import Renderer
from heat2d.stage import Stage
from heat2d.gameobject import GameObject
from heat2d.libs.keys import key_dictionary, button_dictionary, inv_key_dictionary, inv_button_dictionary
from heat2d.errors import NoStageDeclared
from heat2d.ui.context import Context
from heat2d import ui
from heat2d.timer import Timer, TickTimer


class Engine:

    def __init__(self):
        DISPATCHER["engine"] = self
        pygame.init()

        self.window = Window((800, 600))
        self.renderer = Renderer()

        self.timers = list()

        #working with a dictionary might be better than 3 lists
        self.key_states = {k: [0, 0, 0] for k in key_dictionary}
        self.mouse_states = {b: [0, 0, 0] for b in button_dictionary}
        self.mouse_x, self.mouse_y = 0, 0

        self.current_stage = None
        self.stages = dict()
        self.gameobjects = list()

        self.__is_running = False

        #Initialize modules
        ui.init()

    def __repr__(self):
        return f"<heat2d.Engine({self.window})>"

    #   @engine.event decorator function to store input calls
    def event(self, *args):
        def wrapper(func):
            self.event_funcs[func.__name__].append(func)
            if func.__name__ == "every_tick": self.timers.append(TickTimer(func, args[0]))
            elif func.__name__ == "every_time": self.timers.append(Timer(func, args[0]))

        return wrapper

    #   @engine.add decorator to add components into engine
    def add(self, comp):
        self._add(comp)
        #if any(tuple(parent == Stage for parent in cls.__bases__)):
        #    self.add(cls)
        #else:
        #    raise ValueError(f"{cls} is not a Stage")

    def _add(self, *args):
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

    def key_pressed(self, key):
        if self.key_states[key][1]: return True
        return False

    def key_released(self, key):
        if self.key_states[key][2]: return True
        return False

    def key_held(self, key):
        if self.key_states[key][0]: return True
        return False

    def mouse_pressed(self, button):
        if self.mouse_states[button][1]: return True
        return False

    def mouse_released(self, button):
        if self.mouse_states[button][2]: return True
        return False

    def mouse_held(self, button):
        if self.mouse_states[button][0]: return True
        return False

    def mouse_wheel_up(self):
        if self.mouse_states["wheelup"][1]: return True
        return False

    def mouse_wheel_down(self):
        if self.mouse_states["wheeldown"][1]: return True
        return False

    def handle_events(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        for k in self.key_states:
            self.key_states[k][1] = 0
            self.key_states[k][2] = 0

        for b in self.mouse_states:
            self.mouse_states[b][1] = 0
            self.mouse_states[b][2] = 0

        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT: self.__is_running = False

            elif event.type == pygame.KEYDOWN:
                self.key_states[inv_key_dictionary[event.key]][0] = 1
                self.key_states[inv_key_dictionary[event.key]][1] = 1

            elif event.type == pygame.KEYUP:
                self.key_states[inv_key_dictionary[event.key]][0] = 0
                self.key_states[inv_key_dictionary[event.key]][1] = 0
                self.key_states[inv_key_dictionary[event.key]][2] = 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_states[inv_button_dictionary[event.button]][0] = 1
                self.mouse_states[inv_button_dictionary[event.button]][1] = 1

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_states[inv_button_dictionary[event.button]][0] = 0
                self.mouse_states[inv_button_dictionary[event.button]][1] = 0
                self.mouse_states[inv_button_dictionary[event.button]][2] = 1

    def stop(self):
        self.__is_running = False

    def run(self):
        self.__is_running = True

        if not self.current_stage: raise NoStageDeclared("You have to declare at least one stage to run the engine.")

        while self.__is_running:
            self.window.clock.tick(self.window.max_fps)
            self.window.fps = self.window.clock.get_fps()

            self.handle_events()
            self.stages[self.current_stage].update()

            for timer in self.timers: timer.update()
            self.renderer.draw()

        pygame.quit()
