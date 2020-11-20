import pygame
pygame.font.init()
from heat2d import DISPATCHER, HEAT2D_VERSION, PYGAME_VERSION, SDL_VERSION
from heat2d.ui.context import Context
from heat2d.timer import Timer

fps_display = None
fps_graph = None
font16 = pygame.font.SysFont("Calibri", 16)
font14 = pygame.font.SysFont("Calibri", 14)

def toggle_fps_display():
    global fps_display
    if fps_display.visible:
        fps_display.visible = False
    else:
        fps_display.visible = True

def toggle_debug_display():
    global fps_graph
    if fps_graph.visible:
        fps_graph.visible = False
    else:
        fps_graph.visible = True

def init():
    return
    global fps_display, fps_graph
    engine = DISPATCHER["engine"]

    fps_display = Context((0, 0), (40, 18))
    fps_display.new_layer()
    fps_display.layers[0].clear((0, 0, 0, 255))
    fps_display.layers[0].opacity = 180

    fps_graph = Context((0, engine.window.height-150), (410, 150))
    fps_graph.visible = False
    fps_graph.new_layer(2)
    fps_graph.perf = list()
    fps_graph.layers[0].clear((0, 0, 0, 255))
    fps_graph.layers[0].opacity = 180
    fps_graph.effect = GaussianBlur(radius=4)
    fps_graph.layers[2].surface.blit(font16.render(str(engine.window.max_fps), True, (255, 255, 255)), (257, 5))
    fps_graph.layers[2].surface.blit(font16.render(str(engine.window.max_fps//2), True, (255, 255, 255)), (257, 70))
    fps_graph.layers[2].surface.blit(font16.render("0", True, (255, 255, 255)), (257, 132))
    pygame.draw.line(fps_graph.layers[0].surface, (60, 60, 60), (0, 10), (253, 10))
    pygame.draw.line(fps_graph.layers[0].surface, (60, 60, 60), (0, 75), (253, 75))
    pygame.draw.line(fps_graph.layers[0].surface, (60, 60, 60), (0, 138), (253, 138))
    pygame.draw.line(fps_graph.layers[0].surface, (60, 60, 60), (290, 0), (290, 150))
    fps_graph.layers[2].surface.blit(font16.render("Versions", True, (255, 255, 255)), (295, 5))
    fps_graph.layers[2].surface.blit(font14.render(f"Heat2D  : {HEAT2D_VERSION}", True, (255, 255, 255)), (295, 35))
    fps_graph.layers[2].surface.blit(font14.render(f"SDL         : {SDL_VERSION[0]}.{SDL_VERSION[1]}.{SDL_VERSION[2]}", True, (255, 255, 255)), (295, 55))
    fps_graph.layers[2].surface.blit(font14.render(f"Pygame : {PYGAME_VERSION}", True, (255, 255, 255)), (295, 75))

    engine.add(fps_display)
    engine.add(fps_graph)

    timer = Timer()

    @timer.every_millisec(300)
    def callback():
        fps_display.layers[1].clear()
        fps_display.layers[1].surface.blit(font14.render(str(int(engine.window.fps)), True, (0, 255, 0)), (2, 2))

    @timer.every_millisec(30)
    def callback():
        fps = engine.window.fps
        if fps > engine.window.max_fps: fps = engine.window.max_fps
        fps_graph.perf.append(fps)
        if len(fps_graph.perf)>250: fps_graph.perf.pop(0)

        fps_graph.layers[1].clear()

        for i, p in enumerate(fps_graph.perf):
            p *= (60 / engine.window.max_fps)
            a = int((130 - (p * (130/60))) + 460)

            f = int(510-(p*(510/60)))
            if f == 0: color = (0, 255, 0)
            elif f < 255: color = (255-(255-f), 255, 0)
            else:       color = (255, 255-(f-255), 0)

            pygame.draw.line(fps_graph.layers[1].surface, (color[0], color[1], color[2], 100.0), (i, a-450), (i, 600), 2)
            pygame.draw.line(fps_graph.layers[1].surface, (color[0], color[1], color[2], 255.0), (i, a-450), (i, a-447), 2)
