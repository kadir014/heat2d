import pygame
pygame.font.init()
from heat2d import DISPATCHER
from heat2d.ui.layer import UILayer

fps_display_surface = pygame.Surface((40, 18))
fps_display_surface.set_alpha(200)
font_calibri = pygame.font.SysFont("Calibri", 14)

__fps_display_id = None
__fps_display_enabled = False

def enable_fps_display():
    global __fps_display_id, __fps_display_enabled
    if not __fps_display_enabled:
        __fps_display_enabled = True
        renderer = DISPATCHER["engine"].renderer

        def draw_last(display):
            fps_display_surface.fill((0, 0, 0))
            fps = str(int(DISPATCHER["engine"].window.fps))
            fps_display_surface.blit(font_calibri.render(fps, True, (0, 255, 0)), (2, 2))
            display.blit(fps_display_surface, (0, 0))

        __fps_display_id = id(draw_last)
        renderer.event(draw_last)

def disable_fps_display():
    global __fps_display_enabled
    if __fps_display_enabled:
        __fps_display_enabled = False
        renderer = DISPATCHER["engine"].renderer
        for i, func in enumerate(renderer.event_funcs["draw_last"]):
            if id(func) == __fps_display_id:
                renderer.event_funcs["draw_last"].pop(i)
                return

def toggle_fps_display():
    global __fps_display_enabled
    if __fps_display_enabled: disable_fps_display()
    else: enable_fps_display()
