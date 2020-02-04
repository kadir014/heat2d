import pygame
pygame.font.init()
from heat2d import DISPATCHER
from heat2d.ui.layer import UILayer

def init():
    engine = DISPATCHER["engine"]

    fps_display = UILayer((0, 0), (40, 18))
    fps_display.back_surface.fill((0, 0, 0))
    fps_display.back_surface.set_alpha(128)

    engine.add(fps_display)

    font_calibri = pygame.font.SysFont("Calibri", 14)

    @engine.event(300)
    def every_time():
        fps_display.front_surface.fill((255, 255, 255, 0))
        fps_display.front_surface.blit(font_calibri.render(str(int(engine.window.fps)), True, (0, 255, 0)), (2, 2))
        fps_display.render()
