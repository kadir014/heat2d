#  This file is a part of the Heat2D Project and  #
#  distributed under the GPL 3 license            #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


import pygame
from heat2d.math.vector import Vector2
from heat2d.errors import UnknownControllerButton
from heat2d.libs.keys import controller_dictionary



class ControllerStick:
    def __init__(self):
        self.axis = Vector2(0)

    def __repr__(self):
        return "<heat2d.ControllerStick()>"



class Controller:
    def __init__(self, id):
        self._joystick_obj = pygame.joystick.Joystick(id)
        self._joystick_obj.init()

        self.left_stick  = ControllerStick()
        self.right_stick = ControllerStick()

        self.button_states = {b: [0, 0, 0] for b in controller_dictionary}

    def __repr__(self):
        return f"<heat2d.Controller({self.name})>"

    def button_pressed(self, button):
        button = button.lower().strip()
        if not button in controller_dictionary:
            raise UnknownControllerButton(f"'{button}' is not a controller button")

        if self.button_states[button][1]: return True
        return False

    def button_released(self, button):
        button = button.lower().strip()
        if not button in controller_dictionary:
            raise UnknownControllerButton(f"'{button}' is not a controller button")

        if self.button_states[button][2]: return True
        return False

    def button_held(self, button):
        button = button.lower().strip()
        if not button in controller_dictionary:
            raise UnknownControllerButton(f"'{button}' is not a controller button")

        if self.button_states[button][0]: return True
        return False

    @property
    def name(self):
        return self._joystick_obj.get_name()

    @property
    def power_level(self):
        return self._joystick_obj.get_power_level()

    @property
    def id(self):
        return self._joystick_obj.get_instance_id()

    @property
    def guid(self):
        return self._joystick_obj.get_guid()
