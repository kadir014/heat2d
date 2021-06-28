#  This file is a part of the Heat2D Project and  #
#  distributed under the GPL 3 license            #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


from heat2d import DISPATCHER
from heat2d.math import Vector2
from heat2d.math.geometry import Rectangle
from heat2d.trigger import Trigger
from heat2d.physics.collisionlistener import CollisionListener



class GameObject:
    def __init__(self, stage):
        self.__position = Vector2(0, 0)
        self.__sprite = None

        self.__position._x_setter = self._x_setter
        self.__position._y_setter = self._y_setter

        self.velocity = Vector2(0, 0)
        self.friction = 0.15

        self.stage = stage

        self.visible = True

        self.collision_listener = CollisionListener()
        self.collision_listener.triggers = True

    def __repr__(self):
        return f"<heat2d.GameObject({self.position})>"

    def created(self):
        pass

    def update(self):
        pass

    def engine_init_finished(self):
        pass

    def on_collide(self, object):
        pass

    def on_trigger_enter(self, trigger):
        pass

    def on_trigger_stay(self, trigger):
        pass

    def on_trigger_leave(self, trigger):
        pass

    def apply_velocity(self):
        self.position += self.velocity
        self.velocity *= 1 - self.friction

    def _x_setter(self):
        self.hitarea.position.x = self.__position.x - (self.__position.x / 2)

    def _y_setter(self):
        self.hitarea.position.y = self.__position.y - (self.__position.y / 2)

    @property
    def sprite(self): return self.__sprite

    @sprite.setter
    def sprite(self, val):
        val.gameobject = self
        self.__sprite = val
        self.hitarea = Rectangle(self.__position - (self.__position / 2), self.__sprite.size)

    @property
    def position(self): return self.__position

    @position.setter
    def position(self, val):
        self.__position = val
        self.__position._x_setter = self._x_setter
        self.__position._y_setter = self._y_setter
