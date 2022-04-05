class Position:
    def __init__(self, *positionTuple) -> None:
        self.x = positionTuple[0]
        self.y = positionTuple[1]
        if len(positionTuple) == 3:
            self.z = positionTuple[2]
            self.dim = 3
        else:
            self.z = 0
            self.dim = 2

    def __str__(self) -> str:
        string = "Pos{0}[{1}, {2}".format(self.dim, self.x, self.y)
        if self.dim == 3:
            string += ", {0}".format(self.z)
        string += "]"
        return string

    def __len__(self) -> int:
        return self.dim

    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            if self.x != other.x or self.y != other.y or self.z != other.z:
                return False
            return True
        return False

    def __mul__(self, scalar):
        if isinstance(scalar, (float, int)):
            tmpProduct = self.copy()
            tmpProduct.x *= scalar
            tmpProduct.y *= scalar
            tmpProduct.z *= scalar
            return tmpProduct
        else:
            return NotImplemented

    def __rmul__(self, scalar):
        return self * scalar

    def __add__(self, other):
        if isinstance(other, Position):
            tmpSum = self.copy()
            tmpSum.x += other.x
            tmpSum.y += other.y
            tmpSum.z += other.z
            return tmpSum
        else:
            raise NotImplemented

    def __sub__(self, other):
        return self + -other

    def __neg__(self):
        return self * -1

    def __truediv__(self, scalar):
        if isinstance(scalar, (float, int)) and scalar != 0:
            tmpQuotient = self.copy()
            tmpQuotient.x /= scalar
            tmpQuotient.y /= scalar
            tmpQuotient.z /= scalar
            return tmpQuotient
        elif scalar == 0:
            raise ValueError("Cannot divide by 0.")
        else:
            raise NotImplemented

    def copy(self):
        return Position(self.x, self.y, self.z)

    @property
    def tuple(self):
        if self.dim == 2:
            return self.x, self.y
        return self.x, self.y, self.z

    @property
    def i(self):
        return int(self.x), int(self.y)


class Size(Position):
    def __init__(self, *positionTuple):
        super().__init__(*positionTuple)

    def __str__(self):
        string = "Size[{0}, {1}]".format(self.x, self.y)
        return string

    @property
    def w(self):
        return self.x

    @w.setter
    def w(self, value):
        self.x = value

    @property
    def h(self):
        return self.y

    @h.setter
    def h(self, value):
        self.y = value
