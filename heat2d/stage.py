class Stage:

    def __init__(self):
        self.gameobjects = list()

    def __repr__(self):
        return f"<heat2d.Stage({self.__class__.__name__})>"

    def add(self, gameobject):
        self.gameobjects.append(gameobject())

    def update(self):
        pass
