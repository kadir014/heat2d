#  This file is a part of the Heat2D Project and  #
#  distributed under the LGPL 3 license           #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


from heat2d.math.vector import Vector2



class AABB:
    def __init__(self, topleft, topright, bottomleft, bottomright):
        self.topleft = topleft
        self.topright = topright
        self.bottomleft = bottomleft
        self.bottomright = bottomright

    def __repr__(self):
        return f"<heat2d.math.geometry.AABB({self.width}x{self.height})>"

    def get_center(self):
        return Vector2((self.bottomright[1] + self.topleft[1])/2,
                       (self.bottomright[0] + self.topleft[0])/2)

    @property
    def size(self):
        return (self.bottomright[0]-self.topleft[0], self.bottomright[1]-self.topleft[1])

    @property
    def width(self):
        return self.bottomright[0]-self.topleft[0]

    @property
    def height(self):
        return self.bottomright[1]-self.topleft[1]
