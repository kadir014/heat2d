import pygame
from heat2d import DISPATCHER


class Renderer:

    def __init__(self):
        self.window = DISPATCHER["engine"].window
        self.event_funcs = {"draw_last" : list(), "draw_first" : list()}

        self.ui_layers = list()

    def __repr__(self):
        return "<heat2d.Renderer>"

    def event(self, func):
        self.event_funcs[func.__name__].append(func)

    def draw(self):
        self.window.surface.fill(self.window.clear_color)

        gameobjects = DISPATCHER["engine"].stages[DISPATCHER["engine"].current_stage].gameobjects
        for gameobject in gameobjects:
            gameobject.update()
            self.window.surface.blit(gameobject.sprite.surface, (gameobject.x - gameobject.sprite.surface_width/2, gameobject.y - gameobject.sprite.surface_height/2))

        for layer in self.ui_layers:
            if layer.effect:
                layer.effect.process(self.window.surface, layer.back_surface.get_size(), (layer.x, layer.y))
            self.window.surface.blit(layer.back_surface, (layer.x, layer.y))
            self.window.surface.blit(layer.front_surface, (layer.x, layer.y))

        pygame.display.flip()
