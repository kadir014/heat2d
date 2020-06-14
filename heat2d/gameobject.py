class GameObject:

    def __init__(self, clone=False):
        self.x = 0
        self.y = 0
        self.sprite = None
        self.stage = None
        self.clone = clone

        self.display = True

    def update(self):
        pass

    def create_clone(self):
        clo = self.__class__()
        clo.clone = True
        clo.stage = self.stage
        clo.created_as_clone()
        self.stage.gameobjects.append(clo)

    def delete(self):
        if self.clone:
            self.stage.gameobjects.remove(self)
