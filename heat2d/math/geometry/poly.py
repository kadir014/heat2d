#  This file is a part of the Heat2D Project and  #
#  distributed under the LGPL 3 license           #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


from heat2d.math.vector import Vector2
from heat2d.math.geometry.aabb import AABB
from heat2d.math.geometry import tripy
from heat2d.math.geometry.collision import test_poly_poly, test_poly_circle, test_concave_poly_poly, \
                                           test_concave_poly_circle, test_concave_poly_concave_poly



class ConvexPolygon:
    def __init__(self, position, vertices, angle=0):
        self.position = position

        if tripy.is_clockwise(vertices): vertices = vertices[::-1]

        self.vertices = vertices

        self.rels    = [Vector2(0, 0) for _ in range(len(self.vertices))]
        self.edges   = [Vector2(0, 0) for _ in range(len(self.vertices))]
        self.normals = [Vector2(0, 0) for _ in range(len(self.vertices))]

        self.angle = angle

        self.__calc()

    def __repr__(self):
        return f"<heat2d.math.geometry.ConvexPolygon({len(self.vertices)} vertices)>"

    def get_center(self):
        return Vector2(0, 0)

    def __calc(self):
        for i in range(len(self.vertices)):
            self.rels[i] = self.vertices[i]
            self.rels[i].set_angle(self.angle)

        for i in range(len(self.vertices)):
            v1 = self.rels[i]
            v2 = self.rels[i+1] if i < len(self.rels)-1 else self.rels[0]

            e = self.edges[i] = v2-v1

            self.normals[i] = e.perp().normalize()

    def set_angle(self, angle):
        self.angle = angle
        self.__calc()

    def rotate(self, angle):
        self.angle += angle
        self.__calc()

    def get_vertices(self):
        return [self.position + vertex for vertex in self.rels]

    def get_aabb(self):
        vertices = self.get_vertices()

        x_min = vertices[0].x
        y_min = vertices[0].y
        x_max = vertices[0].x
        y_max = vertices[0].y

        for vertex in vertices:
            if vertex.x   < x_min: x_min = vertex.x
            elif vertex.x > x_max: x_max = vertex.x
            if vertex.y   < y_min: y_min = vertex.y
            elif vertex.y > y_max: y_max = vertex.y

        return AABB((x_min, y_min), (x_max, y_min), (x_min, y_max), (x_max, y_max))

    def get_centroid(self):
        cx = 0
        cy = 0
        ar = 0

        for i in range(len(self.rels)):
            v1 = self.rels[i]
            v2 = self.rels[0] if i == len(self.rels) - 1 else self.rels[i+1]
            a = v1.x * v2.y - v2.x * v1.y
            cx += (v1.x + v2.x) * a
            cy += (v1.x + v2.y) * a
            ar += a

        ar = ar * 3
        cx = cx / ar
        cy = cy / ar

        return Vector2(cx, cy)

    def collide(self, other):
        if other.__class__.__name__ == "ConvexPolygon" or other.__class__.__name__ == "Rectangle":
            return test_poly_poly(self, other)

        elif other.__class__.__name__ == "ConcavePolygon":
            return test_concave_poly_poly(other, self)

        elif other.__class__.__name__ == "Circle":
            return test_poly_circle(self, other)

        elif isinstance(other, Vector2):
            return point_in_poly(other, self, ConvexPolygon(Vector2(0, 0), (Vector2(0, 0), Vector2(0.000001, 0.000001))))

        return False


class ConcavePolygon:
    def __init__(self, position, vertices, area=0):
        self.position = position

        if tripy.is_clockwise(vertices): vertices = vertices[::-1]

        self.vertices = vertices

        self.rels    = [Vector2(0, 0) for _ in range(len(self.vertices))]
        self.edges   = [Vector2(0, 0) for _ in range(len(self.vertices))]
        self.normals = [Vector2(0, 0) for _ in range(len(self.vertices))]
        self.tris    = []

        self.angle = angle

        self.__calc_tris()
        self.__calc()

    def __repr__(self):
        return f"<heat2d.math.geometry.ConcavePolygon({len(self.vertices)} vertices)>"

    def __calc(self):
        for i in range(len(self.vertices)):
            self.rels[i] = self.vertices[i]
            self.rels[i] = self.rels[i].set_angle(self.angle)

        for i in range(len(self.vertices)):
            v1 = self.rels[i]
            v2 = self.rels[i+1] if i < len(self.rels)-1 else self.rels[0]

            e = self.edges[i] = v2-v1

            self.normals[i] = e.perp().normalize()

        for tri in self.tris:
            tri.angle = self.angle
            tri.position = self.position

    def __calc_tris(self):
        self.tris = [ConvexPolygon(self.position, vertices, self.angle) for vertices in tripy.earclip(self.vertices)]

    def rotate(self, angle):
        self.angle += angle
        self.__calc_tris()
        self.__calc()

    def get_vertices(self):
        return [self.position + vertex for vertex in self.rels]

    def get_aabb(self):
        vertices = self.get_vertices()
        x_min = vertices[0].x
        y_min = vertices[0].y
        x_max = vertices[0].x
        y_max = vertices[0].y

        for vertex in vertices:
            if vertex.x   < x_min: x_min = vertex.x
            elif vertex.x > x_max: x_max = vertex.x
            if vertex.y   < y_min: y_min = vertex.y
            elif vertex.y > y_max: y_max = vertex.y

        return AABB((x_min, y_min), (x_max, y_min), (x_min, y_max), (x_max, y_max))

    def get_centroid(self):
        cx = 0
        cy = 0
        ar = 0

        for i in range(len(self.rels)):
            v1 = self.rels[i]
            v2 = self.rels[0] if i == len(self.rels)-1 else self.rels[i+1]
            a = v1.x * v2.y - v2.x * v1.y
            cx += (v1.x + v2.x) * a
            cy += (v1.x + v2.y) * a
            ar += a

        ar = ar * 3
        cx = cx / ar
        cy = cy / ar

        return Vector2(cx, cy)

    def collide(self, other):
        if other.__class__.__name__ == "ConvexPolygon" or other.__class__.__name__ == "Rectangle":
            return test_concave_poly_poly(self, other)

        elif other.__class__.__name__ == "ConcavePolygon":
            return test_concave_poly_concave_poly(self, other)

        elif other.__class__.__name__ == "CirclePolygon":
            return test_concave_poly_circle(self, other)

        elif isinstance(other, Vector2):
            return point_in_concave_poly(other, self, ConvexPolygon(Vector2(0, 0), (Vector2(0, 0), Vector2(0.000001, 0.000001))))

        return False
