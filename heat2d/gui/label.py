import pygame
from .. import DISPATCHER

class Label:

    def __init__(self, position = (0, 0), text = "", sysfont = None, font = None, size = 10, fore_color = (0, 0, 0), back_color = None):
        if not sysfont and not font: raise Exception("One font has to be entered.")
        if sysfont and font: raise Exception("One font has to be entered.")

        if sysfont: self.font = pygame.font.SysFont(sysfont, size, bold = True)
        elif font: self.font = pygame.font.Font(font, size, bold = True)

        self.position = position
        self._text = text
        self.fore_color = fore_color
        self.back_color = back_color

        self.surface = None
        self.ignore_camera = False

        DISPATCHER["engine"].widgets.append(self)

        self.render()

    def __repr__(self):
        return f"<heat2d.gui.label({self.text}, {self.position})>"

    def __str__(self):
        return self.__repr__()

    def render(self):
        self.surface = self.font.render(self.text, True, self.fore_color, self.back_color)

    def update(self):
        pass

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.render()
