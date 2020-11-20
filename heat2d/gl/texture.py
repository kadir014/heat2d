import moderngl
import pygame

from heat2d import DISPATCHER


filters = {
           "nearest" : moderngl.NEAREST,
           "linear"  : moderngl.LINEAR
          }


class Texture:
    def __init__(self, surface, format="RGBA", ctx=None):
        if ctx: self.ctx = ctx
        else: self.ctx = DISPATCHER.engine.renderer.ctx

        self.surface = surface
        self.format = format
        self.location = 0

        self.texobj = self.ctx.texture(
            self.surface.get_size(),
            len(self.format),
            pygame.image.tostring(self.surface, self.format, True)
        )

        self.texobj.repeat_x = False
        self.texobj.repeat_y = False
        self.filter_min = filters["nearest"]
        self.filter_mag = filters["nearest"]
        self.texobj.filter = (self.filter_min, self.filter_mag)

        self.update()

    def __repr__(self):
        return f"<heat2d.gl.Texture()>"

    def update(self, surface=None, format=None):
        if format == None: format = self.format
        if surface == None: surface = self.surface

        texture_data = pygame.image.tostring(surface, format, True)
        self.texobj.write(texture_data)

    def use(self, location=0):
        self.location = location
        self.texobj.use(self.location)

    def set_repeat(self, x=None, y=None):
        if x != None:
            self.texobj.repeat_x = x

        if y != None:
            self.texobj.repeat_y = y

    def set_filter(self, filter, min=False, mag=False):
        if min and mag:
            self.filter_min = filters[filter]
            self.filter_mag = filters[filter]
            self.texobj.filter = (self.filter_min, self.filter_mag)

        elif min:
            self.filter_min = filters[filter]
            self.texobj.filter = (self.filter_min, self.filter_mag)

        elif mag:
            self.filter_mag = filters[filter]
            self.texobj.filter = (self.filter_min, self.filter_mag)
