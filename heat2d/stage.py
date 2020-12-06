from heat2d import DISPATCHER
from heat2d.game_object import GameObject


class Stage:
    def __init__(self):
        self.game_objects: list[GameObject, ...] = list()

    def __repr__(self):
        return f"<heat2d.Stage({self.__class__.__name__})>"

    def created(self):
        pass

    def update(self):
        pass

    def add(self, gameobject):
        gobj = gameobject(self)
        self.game_objects.append(gobj)
        gobj.stage = self
        gobj.created()
        return gobj

    def get(self, game_object):
        for gobj in self.game_objects:
            if gobj.__class__.__name__ == game_object: return gobj

    def get_all_with_tag(self, tag: str) -> tuple:
        game_objects_with_tag: list = []

        for game_object in self.game_objects:
            if tag == game_object.tag:
                game_objects_with_tag.append(game_object)

        return tuple(game_objects_with_tag)
