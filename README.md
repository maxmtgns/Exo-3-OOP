# Exo 3 - OOP

Python solutions to the OOP practice problems: **operator overloading** and **inheritance**.

| File | Content |
|---|---|
| `operator_overloading.py` | Complex, Person, Vector, Circle, Point, Matrix |
| `inheritance.py` | Vehicle / Car / Bicycle, Person / Student / Employee, BankAccount / SavingsAccount |
| `test_oop.py` | 32 unit tests covering every problem |

Requires only Python 3 (no external libraries).

```bash
python3 operator_overloading.py   # demo of part 1
python3 inheritance.py            # demo of part 2
python3 -m unittest -v            # run all the tests
```

---

## Part 1 — Operator overloading

In Python, an operator is really a method call with a special name:
`a + b` runs `a.__add__(b)`. Defining these "dunder" methods in a class decides
what the operators do with its objects.

| Operator | Method | Operator | Method |
|---|---|---|---|
| `+` | `__add__` | `<`  | `__lt__` |
| `-` | `__sub__` | `<=` | `__le__` |
| `*` | `__mul__` | `==` | `__eq__` |
| `>` | `__gt__`  | `!=` | `__ne__` |
| `>=`| `__ge__`  | | |

If the other operand has the wrong type, the methods return `NotImplemented`,
so Python raises a clear `TypeError` instead of giving a wrong result.

| Problem | Class | What the operator does | Example |
|---|---|---|---|
| 1 | `Complex` | `+` and `-` work on real and imaginary parts separately | `(3+4i) + (1-2i) = 4+2i` |
| 2 | `Person` | `>` compares ages | `alice(30) > bob(25)` → `True` |
| 4 | `Vector` | `*` is the dot product `x1·x2 + y1·y2 + z1·z2` | `(1,2,3) * (4,5,6) = 32` |
| 5 | `Circle` | all 6 comparisons compare the radius | `Circle(2) < Circle(5)` → `True` |
| 6 | `Point` | all 6 comparisons compare `sqrt(x² + y²)` | `Point(3,4) > Point(1,1)` → `True` |
| 7 | `Matrix` | `*` is matrix multiplication (also `matrix * number`) | `[[1,2],[3,4]] * [[5,6],[7,8]] = [[19,22],[43,50]]` |

Notes:
- **Point:** two different points at the same distance are "equal" with this
  rule, e.g. `Point(3, 4) == Point(4, 3)` (both at distance 5).
- **Matrix:** an `n×m` matrix can only be multiplied by an `m×p` matrix;
  otherwise a `ValueError` explains why. Each cell of the result is
  `row i of A · column j of B`.
- (The original problem list has no Problem 3.)

## Part 2 — Inheritance

A subclass gets all of its parent's attributes and methods. It can **add** new
ones, **override** a method (same name, new behaviour), and call the parent's
version with `super()`.

**Problem 1 – Vehicles.** `Car` and `Bicycle` override `drive()`:

```text
Vehicle  -> Driving a vehicle
Car      -> Driving a car
Bicycle  -> Riding a bicycle
```

**Problem 2 – People.** `Student` and `Employee` call
`super().__init__(...)` to reuse the parent's setup, add their own attribute,
and extend `introduce()`:

```text
Hi, I'm Alice, I'm 40 years old and I live in Paris.
Hi, I'm Bob, I'm 21 years old and I live in Lyon. I study computer science.
Hi, I'm Chloe, I'm 33 years old and I live in Nantes. I work at Airbus.
```

**Problem 3 – Bank accounts.**

- `BankAccount(account_number, balance)` with `deposit`, `withdraw` and `transfer`.
  - `withdraw` returns `False` and changes nothing if the balance is too low.
  - `transfer(destination, amount)` returns `False` if the balance is insufficient, `True` otherwise. No money moves if it fails.
  - Negative or zero amounts raise a `ValueError`.
- `SavingsAccount` inherits from `BankAccount`, adds `interest_rate`
  (`0.05` = 5 %), `add_interest()` and `check_balance()`. It can still use
  `deposit`, `withdraw` and `transfer` from its parent, and can receive transfers.

```text
transfer 200  -> True    BankAccount balance 500 -> 300, SavingsAccount 1000 -> 1200
transfer 1000 -> False   (balance unchanged)
add_interest  -> +60.0   (5 % of 1200)
check_balance -> 1260.0
```
