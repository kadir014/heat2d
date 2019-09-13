import pygame
from math import ceil
from heat2d import DISPATCHER
from heat2d.libs.keys import key_dictionary

class Engine:

    class Window:

        def __init__(self, size, title, icon = None, color = (0, 0, 0)):
            self._width = size[0]
            self._height = size[1]
            self._size = size
            self._title = title
            self._icon = icon
            self.color = color

            self.size = size
            self.title = "Heat2D Game"
            if icon: self.icon = icon

            self.surface = pygame.Surface(self.size)

            self.center_x = self.width / 2
            self.center_y = self.height / 2
            self.center = (self.center_x, self.center_y)

            self.clock = pygame.time.Clock()
            self.max_fps = 60
            self.fps = self.max_fps
            self.active = True

        def __repr__(self):
            return f"<heat2d.engine.Engine.Window({self.size}, {self.title})>"

        @property
        def width(self): return self._width

        @width.setter
        def width(self, val):
            self._width = val
            self.surface = pygame.display.set_mode((self._width, self._height))

        @property
        def height(self): return self._height

        @height.setter
        def height(self, val):
            self._height = val
            self.surface = pygame.display.set_mode((self._width, self._height))

        @property
        def size(self): return self._size

        @size.setter
        def size(self, val):
            self._size = val
            self.surface = pygame.display.set_mode(self._size)

        @property
        def title(self): return self._title

        @title.setter
        def title(self, val):
            self._title = val
            pygame.display.set_caption(self._title)

        @property
        def icon(self): return self._icon

        @icon.setter
        def icon(self, val):
            self._icon = val
            pygame.display.set_icon(pygame.image.load(self._icon))


    class Camera:
        def __init__(self):
            self.x = 0
            self.y = 0
            self.focus_entity = None
            self.focus_type = None
            self.offset = (0, 0)
            self.center = (0, 0)

            self.dx = 0
            self.dy = 0
            self.speed = 3

        def __repr__(self):
            return f"<heat2d.engine.Engine.Camera({self.x}, {self.y})>"

        def focus(self, focus_entity, offset = (0, 0), center = (0, 0), glide = False):
            self.focus_entity = focus_entity
            self.offset = offset
            self.center = center

            if glide:
                self.focus_type = "glide"
                self.dx = 0
                self.dy = 0

            if not glide: self.focus_type = "solid"

            if not focus_entity: self.focus_type = None


    def __init__(self):
        pygame.init()

        #Default window
        self.window = self.Window((800, 600), "Heat2D Game")
        self.camera = self.Camera()

        self.events = None
        self.inp_funcs = {"key_held" : list(), "key_pressed" : list(), "key_released" : list(), "mouse_held" : list(), "mouse_pressed" : list(), "mouse_released" : list()}
        self.key_used = list()

        self.current_stage = None
        self.stages = dict()

        self.sprites = dict()

        self.widgets = list()

        DISPATCHER["engine"] = self

    def __repr__(self):
        return f"<heat2d.engine.Engine({self.window})>"

    #   @engine.input decorator function to store inputs
    def input(self, func):
        self.inp_funcs[func.__name__].append(func)

    def add_stage(self, stage):
        self.stages[stage.__class__.__name__] = stage
        if len(self.stages) == 1: self.current_stage = stage.__class__.__name__

    def add_stages(self, *stages):
        for stage in stages:
            self.add_stage(stage)

    def change_stage(self, stage):
        self.current_stage = stage

    def handle_events(self):
        for key in self.key_used:
            for func in self.inp_funcs["key_held"]:
                func(list(key_dictionary.keys())[list(key_dictionary.values()).index(key)])

        for func in self.inp_funcs["mouse_held"]:
            m = pygame.mouse.get_pressed()
            b = None
            if m[0]: b = "left"
            elif m[1]: b = "middle"
            elif m[2]: b = "right"
            for func in self.inp_funcs["mouse_held"]: func(b)

        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT: self.window.active = False

            elif event.type == pygame.KEYDOWN:
                self.key_used.append(event.key)
                for func in self.inp_funcs["key_pressed"]:
                    func(list(key_dictionary.keys())[list(key_dictionary.values()).index(event.key)])

            elif event.type == pygame.KEYUP:
                self.key_used.remove(event.key)
                for func in self.inp_funcs["key_released"]:
                    func(list(key_dictionary.keys())[list(key_dictionary.values()).index(event.key)])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                b = None
                if event.button == 1: b = "left"
                elif event.button == 2 : b = "middle"
                elif event.button == 3 : b = "right"
                for func in self.inp_funcs["mouse_pressed"]: func(b)

            elif event.type == pygame.MOUSEBUTTONUP:
                b = None
                if event.button == 1: b = "left"
                elif event.button == 2 : b = "middle"
                elif event.button == 3 : b = "right"
                for func in self.inp_funcs["mouse_released"]: func(b)


        self.inp_funcs = {"key_held" : list(), "key_pressed" : list(), "key_released" : list(), "mouse_held" : list(), "mouse_pressed" : list(), "mouse_released" : list()}

    def draw(self):
        if self.camera.focus_type == "solid":
            self.camera.x = self.camera.focus_entity.x - self.camera.offset[0] + self.camera.focus_entity.sprite.center[0] * self.camera.center
            self.camera.y = self.camera.focus_entity.y - self.camera.offset[1] + self.camera.focus_entity.sprite.center[1] * self.camera.center

        if self.camera.focus_type == "glide":
            self.camera.dx = (self.camera.focus_entity.x - self.camera.offset[0] + self.camera.focus_entity.sprite.center[0] * self.camera.center - self.camera.x) / self.camera.speed
            self.camera.dy = (self.camera.focus_entity.y - self.camera.offset[1] + self.camera.focus_entity.sprite.center[1] * self.camera.center - self.camera.y) / self.camera.speed
            self.camera.x += self.camera.dx
            self.camera.y += self.camera.dy

        self.window.surface.fill(self.window.color)

        cstage = list()
        for i in self.sprites:
            if i.startswith(self.current_stage): cstage.append(self.sprites[i])

        for sprite in cstage:
            if sprite["sprite"].has_animation:
                if sprite["sprite"].animation_state == "playing" or sprite["sprite"].animation_state == "stopped": sprite["sprite"].next_frame()

            if sprite["background"]:
                bgw = sprite["sprite"].surface.get_rect().width
                bgh = sprite["sprite"].surface.get_rect().height
                dx = self.window.width / bgw
                dy = self.window.height / bgh

                #if sprite["sprite"].scroll == "x": dy = 0

                for y in range(ceil(dy)+1):
                    for x in range(ceil(dx)+1):
                        self.window.surface.blit(sprite["sprite"].surface, (x * bgw + (-self.camera.x % bgw) - bgw, y * bgh + (-self.camera.y % bgh) - bgh))

        for sprite in cstage:
            if sprite["entity"]:
                if sprite["entity"] == self.camera.focus_entity and self.camera.focus_type == "solid": self.window.surface.blit(sprite["sprite"].surface, (self.camera.offset[0] - self.camera.focus_entity.sprite.center[0] * self.camera.center, self.camera.offset[1] - self.camera.focus_entity.sprite.center[1] * self.camera.center))
                else: self.window.surface.blit(sprite["sprite"].surface, (sprite["entity"].x - self.camera.x, sprite["entity"].y - self.camera.y))

        for widget in self.widgets: self.window.surface.blit(widget.surface, widget.position)

        pygame.display.flip()

    #   Main loop
    def run(self):
        stage_warn = False
        if not self.current_stage:
            print("Warning: No stage has been declared.")
            stage_warn = True

        while self.window.active:
            self.window.clock.tick(self.window.max_fps)
            self.window.fps = self.window.clock.get_fps()

            self.handle_events()
            if not stage_warn: self.stages[self.current_stage].update()

            self.draw()

        pygame.quit()
