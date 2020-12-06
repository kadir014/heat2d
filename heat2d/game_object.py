from heat2d import DISPATCHER
from heat2d.math import Vector2


class GameObject:
    def __init__(self, stage, tag: str = "Untagged"):
        self.position = Vector2(0, 0)
        self._sprite = None
        self.stage = stage
        self.tag: str = tag

        self.visible = True

    def __repr__(self):
        return f"<heat2d.GameObject()>"

    def created(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    @property
    def sprite(self): return self._sprite

    @sprite.setter
    def sprite(self, val):
        val.gameobject = self
        self._sprite = val
