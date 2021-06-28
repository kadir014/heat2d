#  This file is a part of the Heat2D Project and  #
#  distributed under the GPL 3 license            #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


from heat2d.math.vector import Vector2



class Camera:
    def __init__(self):
        self.position = Vector2(0, 0)

        self.focus_object = None
        self.focus_offset = Vector2(0, 0)

    def focus(self, object):
        self.focus_object = object
