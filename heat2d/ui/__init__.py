import pygame
pygame.font.init()
from heat2d import DISPATCHER
from heat2d.ui.context import Context
from heat2d.timer import Timer

def init():
    engine = DISPATCHER["engine"]

    fps_display = Context((0, 0), (40, 18))
    fps_display.back_surface.fill((0, 0, 0))
    fps_display.back_surface.set_alpha(128)

    engine.add(fps_display)

    font_calibri = pygame.font.SysFont("Calibri", 14)

    timer = Timer(300)

    @timer.do
    def function():
        fps_display.front_surface.fill((255, 255, 255, 0))
        fps_display.front_surface.blit(font_calibri.render(str(int(engine.window.fps)), True, (0, 255, 0)), (2, 2))
