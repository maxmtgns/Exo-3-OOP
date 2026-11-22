"""Tests for every problem. Run with:  python3 -m unittest -v"""

import math
import unittest

from operator_overloading import Circle, Complex, Matrix, Point, Vector
from operator_overloading import Person as AgedPerson
from inheritance import (
    BankAccount, Bicycle, Car, Employee, Person, SavingsAccount, Student, Vehicle,
)


# ----------------------------- Operator overloading -----------------------------
class TestComplex(unittest.TestCase):
    def test_add(self):
        self.assertEqual(Complex(3, 4) + Complex(1, -2), Complex(4, 2))

    def test_sub(self):
        self.assertEqual(Complex(3, 4) - Complex(1, -2), Complex(2, 6))

    def test_repr(self):
        self.assertEqual(repr(Complex(3, -4)), "3 - 4i")

    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            Complex(1, 1) + "hello"


class TestPersonAge(unittest.TestCase):
    def test_greater(self):
        p1, p2 = AgedPerson("A", 30, "F"), AgedPerson("B", 25, "M")
        self.assertTrue(p1 > p2)
        self.assertFalse(p2 > p1)

    def test_same_age_is_not_greater(self):
        self.assertFalse(AgedPerson("A", 30, "F") > AgedPerson("B", 30, "M"))


class TestVector(unittest.TestCase):
    def test_dot_product(self):
        self.assertEqual(Vector(1, 2, 3) * Vector(4, 5, 6), 32)

    def test_perpendicular(self):
        self.assertEqual(Vector(1, 0, 0) * Vector(0, 1, 0), 0)


class TestCircle(unittest.TestCase):
    def test_all_operators(self):
        small, big, same = Circle(2), Circle(5), Circle(2)
        self.assertTrue(small < big)
        self.assertTrue(small <= big and small <= same)
        self.assertTrue(small == same)
        self.assertTrue(small != big)
        self.assertTrue(big > small)
        self.assertTrue(big >= small and small >= same)
        self.assertFalse(small > big)

    def test_negative_radius(self):
        with self.assertRaises(ValueError):
            Circle(-1)


class TestPoint(unittest.TestCase):
    def test_distance(self):
        self.assertEqual(Point(3, 4).distance_from_origin(), 5)

    def test_comparisons(self):
        far, near = Point(3, 4), Point(1, 1)
        self.assertTrue(far > near and far >= near)
        self.assertTrue(near < far and near <= far)
        self.assertTrue(far != near)
        # Same distance from the origin -> considered equal.
        self.assertTrue(Point(3, 4) == Point(-4, 3))

    def test_sorting(self):
        points = [Point(3, 4), Point(0, 1), Point(1, 1)]
        self.assertEqual([p.distance_from_origin() for p in sorted(points)],
                         [1, math.sqrt(2), 5])


class TestMatrix(unittest.TestCase):
    def test_square(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[5, 6], [7, 8]])
        self.assertEqual(a * b, Matrix([[19, 22], [43, 50]]))

    def test_rectangular(self):
        a = Matrix([[1, 2, 3], [4, 5, 6]])       # 2x3
        b = Matrix([[7, 8], [9, 10], [11, 12]])  # 3x2
        self.assertEqual(a * b, Matrix([[58, 64], [139, 154]]))  # 2x2

    def test_identity(self):
        a = Matrix([[1, 2], [3, 4]])
        self.assertEqual(a * Matrix([[1, 0], [0, 1]]), a)

    def test_scalar(self):
        a = Matrix([[1, 2], [3, 4]])
        self.assertEqual(a * 2, Matrix([[2, 4], [6, 8]]))
        self.assertEqual(2 * a, Matrix([[2, 4], [6, 8]]))

    def test_incompatible_sizes(self):
        with self.assertRaises(ValueError):
            Matrix([[1, 2]]) * Matrix([[1, 2]])  # 1x2 * 1x2

    def test_ragged_rows(self):
        with self.assertRaises(ValueError):
            Matrix([[1, 2], [3]])


# --------------------------------- Inheritance ---------------------------------
class TestVehicles(unittest.TestCase):
    def test_drive(self):
        self.assertEqual(Vehicle().drive(), "Driving a vehicle")
        self.assertEqual(Car().drive(), "Driving a car")
        self.assertEqual(Bicycle().drive(), "Riding a bicycle")

    def test_is_a_vehicle(self):
        self.assertIsInstance(Car(), Vehicle)
        self.assertIsInstance(Bicycle(), Vehicle)


class TestPeople(unittest.TestCase):
    def test_person(self):
        self.assertEqual(Person("Alice", 40, "Paris").introduce(),
                         "Hi, I'm Alice, I'm 40 years old and I live in Paris.")

    def test_student(self):
        s = Student("Bob", 21, "Lyon", "maths")
        self.assertIsInstance(s, Person)
        self.assertEqual(s.field_of_study, "maths")
        self.assertTrue(s.introduce().endswith("I study maths."))
        self.assertIn("Bob", s.introduce())

    def test_employee(self):
        e = Employee("Chloe", 33, "Nantes", "Airbus")
        self.assertIsInstance(e, Person)
        self.assertTrue(e.introduce().endswith("I work at Airbus."))


class TestBank(unittest.TestCase):
    def test_deposit_withdraw(self):
        acc = BankAccount("A", 100)
        acc.deposit(50)
        self.assertEqual(acc.balance, 150)
        self.assertTrue(acc.withdraw(30))
        self.assertEqual(acc.balance, 120)

    def test_withdraw_too_much(self):
        acc = BankAccount("A", 100)
        self.assertFalse(acc.withdraw(500))
        self.assertEqual(acc.balance, 100)

    def test_invalid_amounts(self):
        acc = BankAccount("A", 100)
        with self.assertRaises(ValueError):
            acc.deposit(-10)
        with self.assertRaises(ValueError):
            acc.withdraw(0)

    def test_transfer_ok(self):
        a, b = BankAccount("A", 100), BankAccount("B", 0)
        self.assertTrue(a.transfer(b, 60))
        self.assertEqual((a.balance, b.balance), (40, 60))

    def test_transfer_insufficient(self):
        a, b = BankAccount("A", 100), BankAccount("B", 0)
        self.assertFalse(a.transfer(b, 1000))
        self.assertEqual((a.balance, b.balance), (100, 0))

    def test_savings_inherits(self):
        s = SavingsAccount("S", 1000, interest_rate=0.05)
        self.assertIsInstance(s, BankAccount)
        s.deposit(100)                      # inherited method
        self.assertEqual(s.check_balance(), 1100)

    def test_add_interest(self):
        s = SavingsAccount("S", 1000, interest_rate=0.05)
        self.assertAlmostEqual(s.add_interest(), 50)
        self.assertAlmostEqual(s.check_balance(), 1050)

    def test_transfer_to_savings(self):
        a, s = BankAccount("A", 300), SavingsAccount("S", 0)
        self.assertTrue(a.transfer(s, 300))
        self.assertEqual(s.check_balance(), 300)
        self.assertEqual(a.balance, 0)


if __name__ == "__main__":
    unittest.main()
