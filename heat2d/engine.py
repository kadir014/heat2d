#  This file is a part of the Heat2D Project and  #
#  distributed under the LGPL 3 license           #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


import time
import pygame

from heat2d import DISPATCHER
from heat2d.camera import Camera
from heat2d.window import Window
from heat2d.renderer import Renderer
from heat2d.stage import Stage
from heat2d.gameobject import GameObject
from heat2d.libs.keys import key_dictionary, inv_key_dictionary
from heat2d.libs.keys import button_dictionary, inv_button_dictionary
from heat2d.libs.keys import controller_dictionary, inv_controller_dictionary
from heat2d.libs.controller import Controller
from heat2d.errors import NoStageDeclared, UnknownKey, UnknownMouseButton, DeviceNotFound
from heat2d.ui.context import Context
from heat2d import ui
from heat2d.timer import Timer
from heat2d.math.vector import Vector2



class Engine:
    def __init__(self):
        DISPATCHER.engine = self
        pygame.init()

        self.camera = Camera()
        self.window = Window((800, 600))
        self.clock = pygame.time.Clock()
        self.renderer = Renderer()

        self.timers = list()
        self.sounds = list()

        self.master_volume = 1.0
        self.master_volume_left = 1.0
        self.master_volume_right = 1.0

        self._lps = 0
        self.lps = 0

        self.max_fps = 60
        self.fps = self.max_fps
        self.deltatime = 1 / self.max_fps

        self.update_elapsed = 0
        self.render_elapsed = 0
        self.__init_time = time.time()
        self.init_elapsed = 0

        #working with a dictionary might be better than 3 lists
        self.key_states = {k: [0, 0, 0] for k in key_dictionary}
        self.mouse_states = {b: [0, 0, 0] for b in button_dictionary}
        self.cached_key_combs = dict()
        self.controllers = list()

        self.current_stage = None
        self.stages = dict()
        self.gameobjects = list()

        self.__is_running = False
        self.__stop_sig = False
        self._pause = False

        #Initialize modules
        ui.init()

    def __repr__(self):
        return f"<heat2d.Engine({self.window})>"

    def pause(self):
        self._pause = True

    def resume(self):
        self._pause = False

    def add(self, comp, *args, **kwargs):
        if isinstance(comp, Context):
            self.renderer.ui_contexts.append(comp)

            return comp

        else:
            st = comp()

            if isinstance(st, Stage):
                self.stages[st.__class__.__name__] = st
                if len(self.stages) == 1: self.current_stage = st.__class__.__name__
                st.created()

                return st

    def change_stage(self, stage):
        if stage in self.stages: self.current_stage = stage
        else: raise NameError(f"{stage} is not found on stages.")

    def get_current_stage(self):
        return self.stages[self.current_stage]

    def get_stage(self, name):
        for stage in self.stages:
            if stage == name: return self.stages[stage]

    def __parse_key_parameter(self, keypar):
        if keypar in self.cached_key_combs:
            return self.cached_key_combs[keypar]

        keys = []
        k = ""
        i = 0
        while i <= len(keypar)-1:
            b = i == len(keypar)-1
            if keypar[i] == "+" or b:
                if b: k += keypar[i]
                keys.append(k.lower().strip())
                k = ""
                i += 1
                continue
            k += keypar[i]
            i += 1

        self.cached_key_combs[keypar] = keys
        return keys

    def key_pressed(self, key=None, numpad=False, left=False, right=False):
        key = key.lower().strip()
        if not key in key_dictionary: raise UnknownKey(f"'{key}' is not a key")

        if key == None:
            for k in self.key_states:
                if self.key_states[k][1]: return True
            return False

        if "+" in key:
            keys = self.__parse_key_parameter(key)

            flag = False
            for i, k in enumerate(keys):
                if i == len(keys) - 1:
                    if flag and self.key_states[k][1]: return True

                if self.key_states[k][0]:
                    flag = True
                else:
                    return False

            return False

        else:
            if self.key_states[key.lower().strip()][1]: return True
            return False

    def key_released(self, key=None, numpad=False, left=False, right=False):
        key = key.lower().strip()
        if not key in key_dictionary:
            raise UnknownKey(f"'{key}' is not a key")

        if key == None:
            for k in self.key_states:
                if self.key_states[k][2]: return True
            return False

        if "+" in key:
            keys = self.__parse_key_parameter(key)

            flag = False
            for i, k in enumerate(keys):
                if i == len(keys) - 1:
                    if flag and self.key_states[k][2]: return True

                if not self.key_states[k][0]:
                    flag = True
                else:
                    return False

            return False

        else:
            if self.key_states[key][2]: return True
            return False

    def key_held(self, key=None, numpad=False, left=False, right=False):
        key = key.lower().strip()

        if key == None:
            for k in self.key_states:
                if self.key_states[k][0]: return True
            return False

        if "+" in key:
            keys = self.__parse_key_parameter(key)

            for k in keys:
                if not self.key_states[k][0]: return False

            return True

        else:
            if not key in key_dictionary: raise UnknownKey(f"'{key}' is not a key")
            if self.key_states[key][0]: return True
            return False

    def mouse_pressed(self, button):
        button = button.lower().strip()
        if not button in button_dictionary:
            raise UnknownMouseButton(f"'{button}' is not a mouse button")

        if self.mouse_states[button][1]: return True
        return False

    def mouse_released(self, button):
        button = button.lower().strip()
        if not button in button_dictionary:
            raise UnknownMouseButton(f"'{button}' is not a mouse button")

        if self.mouse_states[button][2]: return True
        return False

    def mouse_held(self, button):
        button = button.lower().strip()
        if not button in button_dictionary:
            raise UnknownMouseButton(f"'{button}' is not a mouse button")

        if self.mouse_states[button][0]: return True
        return False

    def mouse_wheel_up(self):
        if self.mouse_states["wheelup"][1]: return True
        return False

    def mouse_wheel_down(self):
        if self.mouse_states["wheeldown"][1]: return True
        return False

    def get_controller(self, _id=0):
        if pygame.joystick.get_count() == 0:
            raise DeviceNotFound("there is no controllers connected or detected in system")

        if len(self.controllers) > 0:
            for cc in self.controllers:
                if cc.id == _id: return cc

        c = Controller(_id)
        self.controllers.append(c)
        return c

    def handle_events(self):
        self.mouse = Vector2(pygame.mouse.get_pos())

        for k in self.key_states:
            self._lps += 1
            self.key_states[k][1] = 0
            self.key_states[k][2] = 0

        for b in self.mouse_states:
            self._lps += 1
            self.mouse_states[b][1] = 0
            self.mouse_states[b][2] = 0

        for c in self.controllers:
            self._lps += 1
            for b in c.button_states:
                c.button_states[b][1] = 0
                c.button_states[b][2] = 0

        self.events = pygame.event.get()
        for event in self.events:
            self._lps += 1

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

            elif event.type == pygame.JOYBUTTONDOWN:
                for c in self.controllers:
                    if c.id == event.instance_id:

                        c.button_states[inv_controller_dictionary[event.button]][0] = 1
                        c.button_states[inv_controller_dictionary[event.button]][1] = 1

            elif event.type == pygame.JOYBUTTONUP:
                for c in self.controllers:
                    if c.id == event.instance_id:

                        c.button_states[inv_controller_dictionary[event.button]][0] = 0
                        c.button_states[inv_controller_dictionary[event.button]][1] = 0
                        c.button_states[inv_controller_dictionary[event.button]][2] = 1

            elif event.type == pygame.JOYAXISMOTION:
                for c in self.controllers:
                    if c.id == event.instance_id:

                        if   event.axis == 0: c.left_stick.axis.x  = event.value
                        elif event.axis == 1: c.left_stick.axis.y  = event.value
                        elif event.axis == 2: c.right_stick.axis.x = event.value
                        elif event.axis == 3: c.right_stick.axis.y = event.value

    def stop(self):
        self.__stop_sig = True

    def run(self):
        if not self.current_stage:
            raise NoStageDeclared("You have to declare at least one stage to run the engine.")

        self.init_elapsed = (time.time() - self.__init_time) * 1000

        for stage in self.stages.values():
            stage.engine_init_finished()
            for gameobject in stage.gameobjects:
                gameobject.engine_init_finished()

        # Warm up clock
        for _ in range(10): self.clock.tick(self.max_fps)

        self.__is_running = True

        while self.__is_running:
            if self.__stop_sig: self.__is_running = False

            self.lps = self._lps
            self._lps = 1

            dt = self.clock.tick(self.max_fps)
            self.deltatime = dt/1000
            self.fps = self.clock.get_fps()

            self.handle_events()

            self.get_current_stage().update()

            time_start = time.time()
            for gameobject in self.get_current_stage().gameobjects:
                self._lps += 1
                gameobject.update()

                if gameobject.collision_listener.gameobjects:
                    for gameobject2 in self.get_current_stage().gameobjects:
                        self._lps += 1
                        if gameobject == gameobject2: continue

                        if gameobject.hitarea.collide(gameobject2.hitarea):
                            gameobject.on_collide(gameobject2)

                gameobject.apply_velocity()

                if gameobject.collision_listener.triggers:
                    for trigger in self.get_current_stage().triggers:
                        self._lps += 1

                        if trigger.hitarea.collide(gameobject.hitarea):
                            gameobject.on_trigger_stay(trigger)

            for timer in self.timers: timer.update(); self._lps += 1

            for sound in self.sounds: sound.update(); self._lps += 1
            self.update_elapsed = (time.time() - time_start)*1000

            start_time = time.time()
            self.renderer.render()
            self.render_elapsed = (time.time() - start_time)*1000

        pygame.quit()
        self.renderer.ctx.release()
