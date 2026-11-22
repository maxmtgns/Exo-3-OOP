"""OOP problems — Part 1: Operator overloading.

In Python, operators are just method calls with special names ("dunder" =
double underscore methods). Writing `a + b` actually calls `a.__add__(b)`.
By defining these methods in our own classes, we decide what `+`, `>`, `*`...
mean for our objects.

    +   __add__      -   __sub__      *   __mul__
    <   __lt__       <=  __le__       ==  __eq__
    !=  __ne__       >   __gt__       >=  __ge__

When an operation makes no sense for the given type, the method returns
`NotImplemented`: Python then tries the other operand, and finally raises a
clean TypeError ("unsupported operand type(s)...").
"""

import math


# ---------------------------------------------------------------------------
# Problem 1 — Complex numbers: overload + and -
# ---------------------------------------------------------------------------
class Complex:
    """A complex number  real + imag·i."""

    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        # (a + bi) + (c + di) = (a + c) + (b + d)i
        if not isinstance(other, Complex):
            return NotImplemented
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        # (a + bi) - (c + di) = (a - c) + (b - d)i
        if not isinstance(other, Complex):
            return NotImplemented
        return Complex(self.real - other.real, self.imag - other.imag)

    def __eq__(self, other):
        # Not required, but makes testing results easy: Complex(1, 2) == Complex(1, 2)
        if not isinstance(other, Complex):
            return NotImplemented
        return self.real == other.real and self.imag == other.imag

    def __repr__(self):
        # Shown when printing the object, e.g.  3 + 4i  or  3 - 4i
        sign = "+" if self.imag >= 0 else "-"
        return f"{self.real} {sign} {abs(self.imag)}i"


# ---------------------------------------------------------------------------
# Problem 2 — Person: overload > to compare ages
# ---------------------------------------------------------------------------
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __gt__(self, other):
        # p1 > p2  is True only if p1 is strictly older than p2.
        if not isinstance(other, Person):
            return NotImplemented
        return self.age > other.age

    def __repr__(self):
        return f"Person({self.name!r}, {self.age}, {self.gender!r})"


# ---------------------------------------------------------------------------
# Problem 4 — Vector: overload * as the dot product
# ---------------------------------------------------------------------------
class Vector:
    """A vector in 3D space."""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        # Dot product: v1 · v2 = x1*x2 + y1*y2 + z1*z2  (the result is a number)
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"


# ---------------------------------------------------------------------------
# Problem 5 — Circle: overload ALL comparison operators (by radius)
# ---------------------------------------------------------------------------
class Circle:
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("radius cannot be negative")
        self.radius = radius

    # Each operator simply compares the radii.
    def __lt__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius < other.radius

    def __le__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius <= other.radius

    def __eq__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius == other.radius

    def __ne__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius != other.radius

    def __gt__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius > other.radius

    def __ge__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius >= other.radius

    # Defining __eq__ removes the default __hash__; give it back so circles can
    # still be put in sets / used as dict keys (equal circles -> equal hash).
    def __hash__(self):
        return hash(self.radius)

    def __repr__(self):
        return f"Circle(radius={self.radius})"


# ---------------------------------------------------------------------------
# Problem 6 — 2D Point: compare by distance from the origin
# ---------------------------------------------------------------------------
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_from_origin(self):
        # Euclidean distance = sqrt(x² + y²)
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # Helper so every operator below uses the same rule (and the same checks).
    def _distance_of(self, other):
        if not isinstance(other, Point):
            return None
        return other.distance_from_origin()

    def __lt__(self, other):
        d = self._distance_of(other)
        return NotImplemented if d is None else self.distance_from_origin() < d

    def __le__(self, other):
        d = self._distance_of(other)
        return NotImplemented if d is None else self.distance_from_origin() <= d

    def __eq__(self, other):
        # Note: with this rule, Point(3, 4) == Point(4, 3) == Point(0, 5)
        # because they are all at distance 5 from the origin.
        d = self._distance_of(other)
        return NotImplemented if d is None else self.distance_from_origin() == d

    def __ne__(self, other):
        d = self._distance_of(other)
        return NotImplemented if d is None else self.distance_from_origin() != d

    def __gt__(self, other):
        d = self._distance_of(other)
        return NotImplemented if d is None else self.distance_from_origin() > d

    def __ge__(self, other):
        d = self._distance_of(other)
        return NotImplemented if d is None else self.distance_from_origin() >= d

    def __hash__(self):
        return hash(self.distance_from_origin())

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


# ---------------------------------------------------------------------------
# Problem 7 — Matrix: overload * as matrix multiplication
# ---------------------------------------------------------------------------
class Matrix:
    """A matrix stored as a list of rows, e.g. Matrix([[1, 2], [3, 4]])."""

    def __init__(self, rows):
        if not rows or not rows[0]:
            raise ValueError("a matrix needs at least one row and one column")
        if any(len(row) != len(rows[0]) for row in rows):
            raise ValueError("all rows must have the same length")
        # Copy the rows so changing the original list doesn't change the matrix.
        self.rows = [list(row) for row in rows]

    @property
    def shape(self):
        return len(self.rows), len(self.rows[0])

    def __mul__(self, other):
        # Matrix × number: multiply every element (bonus).
        if isinstance(other, (int, float)):
            return Matrix([[value * other for value in row] for row in self.rows])

        if not isinstance(other, Matrix):
            return NotImplemented

        # (n × m) × (m × p) -> (n × p): columns of A must equal rows of B.
        n, m = self.shape
        m2, p = other.shape
        if m != m2:
            raise ValueError(
                f"cannot multiply a {n}x{m} matrix by a {m2}x{p} matrix "
                f"({m} columns != {m2} rows)"
            )

        # result[i][j] = sum over k of A[i][k] * B[k][j]
        #               (row i of A "dot" column j of B)
        result = [
            [sum(self.rows[i][k] * other.rows[k][j] for k in range(m)) for j in range(p)]
            for i in range(n)
        ]
        return Matrix(result)

    def __rmul__(self, other):
        # Makes  2 * matrix  work, not only  matrix * 2.
        if isinstance(other, (int, float)):
            return self * other
        return NotImplemented

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.rows == other.rows

    def __repr__(self):
        return f"Matrix({self.rows})"

    def __str__(self):
        # Pretty display, one row per line.
        return "\n".join("  ".join(f"{v:>4}" for v in row) for row in self.rows)


# ---------------------------------------------------------------------------
# Demo — run:  python3 operator_overloading.py
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- Problem 1: Complex ---")
    c1, c2 = Complex(3, 4), Complex(1, -2)
    print(f"({c1}) + ({c2}) = {c1 + c2}")
    print(f"({c1}) - ({c2}) = {c1 - c2}")

    print("\n--- Problem 2: Person ---")
    alice, bob = Person("Alice", 30, "F"), Person("Bob", 25, "M")
    print(f"alice > bob -> {alice > bob}")
    print(f"bob > alice -> {bob > alice}")

    print("\n--- Problem 4: Vector ---")
    v1, v2 = Vector(1, 2, 3), Vector(4, 5, 6)
    print(f"{v1} * {v2} = {v1 * v2}")

    print("\n--- Problem 5: Circle ---")
    small, big = Circle(2), Circle(5)
    for symbol, result in [
        ("<", small < big), ("<=", small <= big), ("==", small == big),
        ("!=", small != big), (">", small > big), (">=", small >= big),
    ]:
        print(f"{small} {symbol:>2} {big} -> {result}")

    print("\n--- Problem 6: Point ---")
    p1, p2 = Point(3, 4), Point(1, 1)
    print(f"{p1} is at distance {p1.distance_from_origin()}")
    print(f"{p2} is at distance {p2.distance_from_origin():.3f}")
    print(f"p1 > p2 -> {p1 > p2},  p1 == Point(4, 3) -> {p1 == Point(4, 3)}")

    print("\n--- Problem 7: Matrix ---")
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    print(f"A =\n{a}\nB =\n{b}\nA * B =\n{a * b}\n2 * A =\n{2 * a}")
