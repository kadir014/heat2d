#  This file is a part of the Heat2D Project and  #
#  distributed under the LGPL 3 license           #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


import moderngl
import pygame
import os
from math import radians

from heat2d import DISPATCHER
from heat2d.version import OPENGL_VERSION, SDL_VERSION
from heat2d.gl import Texture, Shader
from heat2d.libs.utils import source_path



class Renderer:
    def __init__(self):
        self.engine = DISPATCHER.engine

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

        if self.engine.camera.focus_object: self.engine.camera.position = self.engine.camera.focus_object.position

        for i, gameobject in enumerate(self.engine.get_current_stage().gameobjects):
            self.engine._lps += 1

            if gameobject.visible:
                gameobject.sprite.update()

                screen = pygame.Rect(self.engine.camera.position.x - (self.engine.window.width/2),
                                     self.engine.camera.position.y - (self.engine.window.height/2),
                                     self.engine.window.width*2,
                                     self.engine.window.height*2)

                gbo    = pygame.Rect(gameobject.position.x - gameobject.sprite.width/2 + self.engine.camera.position.x - (self.engine.window.width / 2),
                                     gameobject.position.y - gameobject.sprite.height/2 + self.engine.camera.position.y - (self.engine.window.height / 2),
                                     gameobject.sprite.width*2,
                                     gameobject.sprite.height*2)

                #if not screen.colliderect(gbo): continue

                if gameobject.sprite.has_animation:
                    gameobject.sprite.sheets[gameobject.sprite.current_animation].sources[int(gameobject.sprite.current_frame)]["texture"].use()

                    # gameobject.sprite.shader.set_uniform("size",
                    #         gameobject.sprite.sheets[gameobject.sprite.current_animation].sources[int(gameobject.sprite.anim_frame)]["size"][0] / self.engine.window.width,
                    #         gameobject.sprite.sheets[gameobject.sprite.current_animation].sources[int(gameobject.sprite.anim_frame)]["size"][1] / self.engine.window.height)

                    gameobject.sprite.shader.set_uniform("size",
                            gameobject.sprite.width / self.engine.window.width,
                            gameobject.sprite.height / self.engine.window.height)

                else:
                    gameobject.sprite.texture.use()

                    gameobject.sprite.shader.set_uniform("size",
                            gameobject.sprite.width / self.engine.window.width,
                            gameobject.sprite.height / self.engine.window.height)

                gameobject.sprite.shader.set_uniform("rotation", radians(gameobject.sprite.angle))
                gameobject.sprite.shader.set_uniform("position", (gameobject.position.x - self.engine.camera.position.x + (self.engine.window.width / 2)) / self.engine.window.width, (gameobject.position.y - self.engine.camera.position.y + (self.engine.window.height / 2)) / self.engine.window.height)

                if gameobject.sprite.palette:
                    gameobject.sprite.shader.set_uniform("has_palette", True)
                    gameobject.sprite.shader.set_uniform("palette_length", len(gameobject.sprite.palette))
                    gameobject.sprite.shader.set_uniform("palette", gameobject.sprite._palette_buffer)
                else:
                    gameobject.sprite.shader.set_uniform("has_palette", False)

                gameobject.sprite.shader.render()

        self.ctx.screen.use()
        self.gamefbo.color_attachments[0].use()
        self.postprocess.set_uniform("SCREEN", float(self.engine.window.width), float(self.engine.window.height), ignore=True)
        self.postprocess.render()

        pygame.display.flip()

    def load_postprocess(self, shadername):
        self.postprocess = Shader(fragment=source_path(f"shaders/post_{shadername}.fsh"))
