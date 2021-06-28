#  This file is a part of the Heat2D Project and  #
#  distributed under the LGPL 3 license           #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


from math import sqrt, sin, cos, atan2, radians, degrees



class Vector2:
    def __init__(self, a, b=None):
        if isinstance(a, Vector2):
            self.__x = a.x
            self.__y = a.y

        elif isinstance(a, (tuple, list)):
            self.__x = a[0]
            self.__y = a[1]

        elif isinstance(a, (int, float)):
            if b:
                if isinstance(b, (int, float)):
                    self.__x = a
                    self.__y = b
                else:
                    raise TypeError(f"expected arguments\nVector2(x, y)\nVector2((x, y))\nVector2(length)\nVector2(Vector2)\nbut got unexpected type '{type(b).__name__}'")
            else:
                self.__x = a
                self.__y = 0

        else:
            raise TypeError(f"expected arguments\nVector2(x, y)\nVector2((x, y))\nVector2(length)\nVector2(Vector2)\nbut got unexpected type '{type(a).__name__}'")

        self._x_setter = None
        self._y_setter = None

    def __repr__(self):
        return f"<heat2d.math.Vector2({self.x}, {self.y})>"

    @property
    def x(self): return self.__x

    @property
    def y(self): return self.__y

    @x.setter
    def x(self, val):
        self.__x = val
        if self._x_setter: self._x_setter()

    @y.setter
    def y(self, val):
        self.__y = val
        if self._y_setter: self._y_setter()

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x + other, self.y + other)

        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Vector2' and '{type(other).__name__}'")

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x - other, self.y - other)

        else:
            raise TypeError(f"unsupported operand type(s) for -: 'Vector2' and '{type(other).__name__}'")

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)

        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Vector2' and '{type(other).__name__}'")

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x / other, self.y / other)

        else:
            raise TypeError(f"unsupported operand type(s) for /: 'Vector2' and '{type(other).__name__}'")

    def __floordiv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x // other, self.y // other)

        else:
            raise TypeError(f"unsupported operand type(s) for //: 'Vector2' and '{type(other).__name__}'")

    def __iadd__(self, other):
        if isinstance(other, Vector2):
            self = Vector2(self.x + other.x, self.y + other.y)

        elif isinstance(other, (int, float)):
            self = Vector2(self.x + other, self.y + other)

        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Vector2' and '{type(other).__name__}'")

        return self

    def __isub__(self, other):
        if isinstance(other, Vector2):
            self = Vector2(self.x - other.x, self.y - other.y)

        elif isinstance(other, (int, float)):
            self = Vector2(self.x - other, self.y - other)

        else:
            raise TypeError(f"unsupported operand type(s) for -: 'Vector2' and '{type(other).__name__}'")

        return self

    def __imul__(self, other):
        if isinstance(other, Vector2):
            self = Vector2(self.x * other.x, self.y * other.y)

        elif isinstance(other, (int, float)):
            self = Vector2(self.x * other, self.y * other)

        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Vector2' and '{type(other).__name__}'")

        return self

    def __itruediv__(self, other):
        if isinstance(other, Vector2):
            self = Vector2(self.x / other.x, self.y / other.y)

        elif isinstance(other, (int, float)):
            self = Vector2(self.x / other, self.y / other)

        else:
            raise TypeError(f"unsupported operand type(s) for /: 'Vector2' and '{type(other).__name__}'")

        return self

    def __ifloordiv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x // other, self.y // other)

        else:
            raise TypeError(f"unsupported operand type(s) for //: 'Vector2' and '{type(other).__name__}'")

        return self

    def __neg__(self):
        return self * -1

    def to_tuple(self):
        return (self.x, self.y)

    def length(self):
        return sqrt(self.x**2 + self.y**2)

    def distance_to(self, vector):
        return sqrt((vector.x-self.x)**2 + (vector.y-self.y)**2)

    def angle_to(self, vector):
        return atan2((vector.y-self.y), (vector.x-self.x))

    def set_angle(self, angle):
        r = radians(-angle)
        c = cos(r)
        s = sin(r)
        x = self.x * c - self.y * s
        y = self.x * s + self.y * c
        self.x, self.y = x, y

    def get_angle(self):
        return degrees(atan2(self.y, self.x))

    def rotate(self, angle):
        self.set_angle(self.get_angle() + angle)

    def rotate_around(self, vector, angle):
        angle = radians(-angle)
        s = sin(angle)
        c = cos(angle)

        self.x -= vector.x
        self.y -= vector.y

        xn = self.x * c - self.y * s
        yn = self.x * s + self.y * c

        self.x = xn + vector.x
        self.y = yn + vector.y

    def dot(self, vector):
        return self.x * vector.x + self.y * vector.y

    def inverse(self):
        return Vector2(1 / self.x, 1 / self.y)

    def normalize(self):
        l = self.length()
        if l == 0: return self
        else: return self / l

    def perp(self):
        return Vector2(self.y, -self.x)
