from heat2d import DISPATCHER
from heat2d.gameobject import GameObject


class Stage:
    def __init__(self):
        self.gameobjects = list()

    def __repr__(self):
        return f"<heat2d.Stage({self.__class__.__name__})>"

    def created(self):
        pass

    def update(self):
        pass

    def add(self, gameobject):
        gobj = gameobject(self)
        self.gameobjects.append(gobj)
        gobj.stage = self
        gobj.created()
        return gobj

    def get(self, gameobject):
        for gobj in self.gameobjects:
            if gobj.__class__.__name__ == gameobject: return gobj
