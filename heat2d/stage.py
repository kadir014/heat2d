class Stage:

    def __init__(self):
        self.gameobjects = list()

    def __repr__(self):
        return f"<heat2d.Stage({self.__class__.__name__})>"

    def add(self, gameobject):
        gobj = gameobject()
        self.gameobjects.append(gobj)
        setattr(self, gameobject.__name__, gobj)
        gobj.stage = self

    def update(self):
        pass
