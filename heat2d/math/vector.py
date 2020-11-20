from math import sqrt, sin, cos, atan2, radians


class Vector2:
    def __init__(self, a, b=None):
        if isinstance(a, (tuple, list)):
            self.x = a[0]
            self.y = a[1]

        elif isinstance(a, (int, float)):
            if b:
                if isinstance(b, (int, float)):
                    self.x = a
                    self.y = b
                else: raise ValueError("Invalid vector argument")
            else:
                self.x = a
                self.y = 0

        else: raise ValueError("Invalid vector argument")

    def __repr__(self):
        return f"<heat2d.Vector2({self.x}, {self.y})>"

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x + other, self.y + other)

        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Vector2' and '{other.__class__.__name__}'")

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x - other, self.y - other)

        else:
            raise TypeError(f"unsupported operand type(s) for -: 'Vector2' and '{other.__class__.__name__}'")

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)

        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Vector2' and '{other.__class__.__name__}'")

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x / other, self.y / other)

        else:
            raise TypeError(f"unsupported operand type(s) for /: 'Vector2' and '{other.__class__.__name__}'")

    def __floordiv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x // other, self.y // other)

        else:
            raise TypeError(f"unsupported operand type(s) for //: 'Vector2' and '{other.__class__.__name__}'")

    def __iadd__(self, other):
        if isinstance(other, Vector2):
            self = Vector2(self.x + other.x, self.y + other.y)

        elif isinstance(other, (int, float)):
            self = Vector2(self.x + other, self.y + other)

        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Vector2' and '{other.__class__.__name__}'")

        return self

    def __isub__(self, other):
        if isinstance(other, Vector2):
            self = Vector2(self.x - other.x, self.y - other.y)

        elif isinstance(other, (int, float)):
            self = Vector2(self.x - other, self.y - other)

        else:
            raise TypeError(f"unsupported operand type(s) for -: 'Vector2' and '{other.__class__.__name__}'")

        return self

    def __imul__(self, other):
        if isinstance(other, Vector2):
            self = Vector2(self.x * other.x, self.y * other.y)

        elif isinstance(other, (int, float)):
            self = Vector2(self.x * other, self.y * other)

        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Vector2' and '{other.__class__.__name__}'")

        return self

    def __itruediv__(self, other):
        if isinstance(other, Vector2):
            self = Vector2(self.x / other.x, self.y / other.y)

        elif isinstance(other, (int, float)):
            self = Vector2(self.x / other, self.y / other)

        else:
            raise TypeError(f"unsupported operand type(s) for /: 'Vector2' and '{other.__class__.__name__}'")

        return self

    def __ifloordiv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x // other, self.y // other)

        else:
            raise TypeError(f"unsupported operand type(s) for //: 'Vector2' and '{other.__class__.__name__}'")

        return self

    def __lt__(self, other):
        return self.length() < other.length()

    def __gt__(self, other):
        return self.length() > other.length()

    def __le__(self, other):
        return self.length() <= other.length()

    def __ge__(self, other):
        return self.length() >= other.length()

    def __eq__(self, other):
        return self.length() == other.length()

    def __ne__(self, other):
        return self.length() != other.length()

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
        self.x *= cos(radians(angle))
        self.y *= sin(radians(angle))

    def get_angle(self):
        return atan2(self.y, self.x)

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

    def normalise(self):
        l = self.length()
        if l == 0: return self
        else: return self / l
