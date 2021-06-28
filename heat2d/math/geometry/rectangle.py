#  This file is a part of the Heat2D Project and  #
#  distributed under the GPL 3 license            #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


from heat2d.math.geometry.poly import ConvexPolygon
from heat2d.math.vector import Vector2



class Rectangle(ConvexPolygon):
    def __init__(self, position, size, angle=0):
        w, h = (Vector2(size)/4).to_tuple()
        vertices = (Vector2(-w, h), Vector2(w, h), Vector2(w, -h), Vector2(-w, -h))

        super().__init__(position, vertices, angle)

    def __repr__(self):
        return f"<heat2d.math.geometry.Rectangle({self.get_aabb().width}x{self.get_aabb().height})>"

    def get_center(self):
        return self.get_centroid()
