#  This file is a part of the Heat2D Project and  #
#  distributed under the LGPL 3 license           #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


from heat2d.math.vector import Vector2
from heat2d.math.geometry.aabb import AABB



class Circle:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def __repr__(self):
        return f"<heat2d.math.geometry.Circle({self.radius} radius)>"

    def get_aabb(self):
        return AABB((self.position.x - self.radius, self.position.y - self.radius),
                    (self.position.x + self.radius, self.position.y - self.radius),
                    (self.position.x - self.radius, self.position.y + self.radius),
                    (self.position.x + self.radius, self.position.y + self.radius))

    def collide(self, other):
        if other.__class__.__name__ == "ConvexPolygon" or other.__class__.__name__ == "Rectangle":
            return test_poly_circle(other, self)

        elif other.__class__.__name__ == "ConcavePolygon":
            return test_concave_poly_circle(other, self)

        elif other.__class__.__name__ == "Circle":
            return test_circle_circle(self, other)

        elif isinstance(other, Vector2):
            return point_in_circle(other, self)
