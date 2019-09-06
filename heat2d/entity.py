from heat2d.sprite import Sprite

class Entity:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.sprite = Sprite(None, entity=self)
        #self.ignore_camera = False

    def __repr__(self):
        return f"<heat2d.entity.Entity({(self.x, self.y)})>"

    def __str__(self):
        return self.__repr__()

    def update(self):
        pass

    def init(self, stage):
        self.sprite.stage = stage
        self.sprite.init()
