#  This file is a part of the Heat2D Project and  #
#  distributed under the GPL 3 license            #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


from heat2d.math.vector import Vector2
import math

LEFT_VORONOI_REGION = -1
MIDDLE_VORONOI_REGION = 0
RIGHT_VORONOI_REGION = 1


def voronoi_region(line, point):
    dp = point.dot(line)

    if dp < 0:
        return LEFT_VORONOI_REGION
    elif dp > line.ln2():
        return RIGHT_VORONOI_REGION
    return MIDDLE_VORONOI_REGION

def flatten_points_on(points, normal, result):
    minpoint = math.inf
    maxpoint = -math.inf

    for i in range(len(points)):
        dot = points[i].dot(normal)
        if dot < minpoint:
            minpoint = dot
        if dot > maxpoint:
            maxpoint = dot

    result[0] = minpoint
    result[1] = maxpoint


def is_separating_axis(a_pos, b_pos, a_points, b_points, axis, response=None):
    range_a = [0, 0]
    range_b = [0, 0]

    offset_v = b_pos-a_pos

    projected_offset = offset_v.dot(axis)

    flatten_points_on(a_points, axis, range_a)
    flatten_points_on(b_points, axis, range_b)

    range_b[0] += projected_offset
    range_b[1] += projected_offset

    if range_a[0] > range_b[1] or range_b[0] > range_a[1]:
        return True
    return False


def test_aabb(b1,b2):
    return b1[0][0] <= b2[1][0] and b2[0][0] <= b1[1][0] and b1[0][1] <= b2[2][1] and b2[0][1] <= b1[2][1]

def point_in_circle(p, c):
    difference_v = p - c.position

    radius_sq = c.radius * c.radius

    distance_sq = difference_v.ln2()

    return distance_sq <= radius_sq

def point_in_poly(p, poly, test):
    test.position = p

    result = test_poly_poly(test, poly)

    return result

def test_circle_circle(a, b, response = None):

    difference_v = b.position - a.position
    total_radius = a.radius + b.radius
    total_radius_sq = total_radius * total_radius
    distance_sq = difference_v.ln2()

    if distance_sq > total_radius_sq:
        return False

    return True

def test_poly_circle(polygon, circle, response = None):
    circle_pos = circle.position - polygon.position
    radius = circle.radius
    radius2 = radius * radius
    points = polygon.rels
    ln = len(points)

    for i in range(ln):
        nextn = 0 if i == ln - 1 else i + 1
        prevn = ln - 1 if i == 0 else i - 1

        overlap = 0
        overlap_n = None

        edge = polygon.edges[i].copy()
        point = circle_pos - points[i]

        region = voronoi_region(edge,point)

        if region == LEFT_VORONOI_REGION:
            edge = polygon.edges[prevn]

            point2 = circle_pos - points[prevn]

            region = voronoi_region(edge, point2)

            if region == RIGHT_VORONOI_REGION:

                dist = point.ln()

                if dist > radius:
                    return False

        elif region == RIGHT_VORONOI_REGION:
            edge = polygon.edges[nextn]
            point = circle_pos - points[nextn]
            region = voronoi_region(edge,point)

            if region == LEFT_VORONOI_REGION:
                dist = point.ln()

                if dist > radius:
                    return False

        else:
            normal = edge.perp().normalize()

            dist = point.dot(normal)

            dist_abs = abs(dist)

            if dist > 0 and dist_abs > radius:
                return False

            elif response:
                overlap_n = normal
                overlap = radius - dist

    return True

def test_poly_poly(a, b):
    a_points = a.rels
    b_points = b.rels
    a_pos = a.position
    b_pos = b.position

    for n in a.normals:
        if is_separating_axis(a.position, b.position, a.rels, b.rels, n):
            return False

    for n in b.normals:
        if is_separating_axis(a_pos, b_pos, a_points, b_points, n):
            return False

    return True

def point_in_concave_poly(p, poly, test):
    test.position = p

    for tri in poly.tris:
        result = test_poly_poly(test, tri)
        if result:
            return result

    return result

def test_concave_poly_concave_poly(a, b):
    a_pos = a.position
    b_pos = b.position

    for a_tri in a.tris:
        for b_tri in b.tris:
            test = True
            for n in a_tri.normals:
                if is_separating_axis(a_pos, b_pos, a_tri.rels, b_tri.rels, n):
                    test = False

            for n in b_tri.normals:
                if is_separating_axis(a_pos, b_pos, a_tri.rels, b_tri.res, n):
                    test = False

            if test:
                return True

    return False

def test_concave_poly_poly(a, b):
    b_points = b.rels
    a_pos = a.position
    b_pos = b.position

    for a_tri in a.tris:
        test = True
        for n in a_tri.normals:
            if is_separating_axis(a_pos, b_pos, a_tri.rels, b_points, n):
                test = False

        for n in b.normals:
            if is_separating_axis(a_pos, b_pos, a_tri.rels, b_points, n):
                test = False

        if test:
            return True

    return False

def test_concave_poly_circle(concave_poly, circle):
    for polygon in concave_poly.tris:
        test = True
        circle_pos = circle.position - polygon.position
        radius = circle.radius
        radius2 = radius * radius
        points = polygon.rels
        ln = len(points)

        for i in range(ln):
            next = 0 if i == ln - 1 else i + 1
            prev = ln - 1 if i == 0 else i - 1
            overlap = 0
            overlap_n = None
            edge = polygon.edges[i].copy()
            point = circle_pos - points[i]
            region = voronoi_region(edge,point)

            if region == LEFT_VORONOI_REGION:
                edge = polygon.edges[prev]
                point2 = circle_pos - points[prev]
                region = voronoi_region(edge, point2)

                if region == RIGHT_VORONOI_REGION:
                    dist = point.ln()

                    if dist > radius:
                        test = False

            elif region == RIGHT_VORONOI_REGION:
                edge = polygon.edges[next]
                point = circle_pos - points[next]
                region = voronoi_region(edge,point)

                if region == LEFT_VORONOI_REGION:
                    dist = point.ln()
                    if dist > radius:
                        test = False

            else:
                normal = edge.perp().normalize()
                dist = point.dot(normal)
                dist_abs = abs(dist)

                if dist > 0 and dist_abs > radius:
                    test = False

        if test:
            return True

    return False
