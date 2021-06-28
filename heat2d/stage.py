#  This file is a part of the Heat2D Project and  #
#  distributed under the LGPL 3 license           #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


from heat2d import DISPATCHER
from heat2d.gameobject import GameObject
from heat2d.trigger import Trigger



class Stage:
    def __init__(self):
        self.gameobjects = list()
        self.triggers = list()

    def __repr__(self):
        return f"<heat2d.Stage({self.__class__.__name__})>"

    def created(self):
        pass

    def update(self):
        pass

    def engine_init_finished(self):
        pass

    def add(self, component):
        # Component is Trigger
        if isinstance(component, Trigger):
            self.triggers.append(component)

        # Component is GameObject
        elif component.__base__ == GameObject:
            gameobject = component(self)
            self.gameobjects.append(gameobject)
            gameobject.stage = self
            gameobject.created()

    def get(self, gameobject):
        for gobj in self.gameobjects:
            if gobj.__class__.__name__ == gameobject: return gobj
