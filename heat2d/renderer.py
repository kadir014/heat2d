import moderngl
import pygame
from math import radians

from heat2d import DISPATCHER
from heat2d.version import OPENGL_VERSION, SDL_VERSION
from heat2d.gl import Texture, Shader


class Renderer:
    def __init__(self):
        self.engine = DISPATCHER.engine

        self.viewport = [0, 0, self.engine.window.width, self.engine.window.height]

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)

        self.texture = Texture(self.engine.window.surface, ctx=self.ctx)

        self.postprocess = Shader(ctx=self.ctx)

        self.gamefbo = self.ctx.framebuffer((self.texture.texobj,))

    def __repr__(self):
        return f"<heat2d.Renderer(OpenGL {OPENGL_VERSION}, SDL {SDL_VERSION})>"

    def render(self):
        self.gamefbo.use()
        self.gamefbo.clear(*self.engine.window.clear_color.normalise().to_tuple())

        for i, gameobject in enumerate(self.engine.stages[self.engine.current_stage].game_objects):

            if gameobject.visible:

                gameobject.sprite.texture.use()

                gameobject.sprite.shader.set_uniform("rotation", radians(gameobject.sprite.angle))
                gameobject.sprite.shader.set_uniform("position", gameobject.position.x / self.engine.window.width, gameobject.position.y / self.engine.window.height)
                #game_object.sprite.shader.set_uniform("size", (game_object.sprite.source_width-game_object.sprite.width) / self.engine.window.width, (game_object.sprite.source_height-game_object.sprite.height) / self.engine.window.height)
                gameobject.sprite.shader.set_uniform("size",
                        gameobject.sprite.width / self.engine.window.width,
                        gameobject.sprite.height / self.engine.window.height)

                if gameobject.sprite.palette:
                    gameobject.sprite.shader.set_uniform("has_palette", True)
                    gameobject.sprite.shader.set_uniform("palette_length", len(gameobject.sprite.palette))
                    gameobject.sprite.shader.set_uniform("palette", gameobject.sprite._palette_buffer)
                else:
                    gameobject.sprite.shader.set_uniform("has_palette", False)

                gameobject.draw()
                gameobject.sprite.shader.render()

        self.ctx.screen.use()
        self.gamefbo.color_attachments[0].use()
        self.postprocess.render()

        pygame.display.flip()
