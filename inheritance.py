"""OOP problems — Part 2: Inheritance.

A subclass ("child") inherits all attributes and methods of its parent class,
and can:
  * add new attributes / methods,
  * override (re-define) a parent method to change its behaviour,
  * call the parent's version with  super().method(...)
"""


# ---------------------------------------------------------------------------
# Problem 1 — Vehicle / Car / Bicycle: method overriding
# ---------------------------------------------------------------------------
class Vehicle:
    def drive(self):
        return "Driving a vehicle"


class Car(Vehicle):
    # Same method name as the parent -> this version replaces it for cars.
    def drive(self):
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self):
        return "Riding a bicycle"


# ---------------------------------------------------------------------------
# Problem 2 — Person / Student / Employee
# ---------------------------------------------------------------------------
class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def introduce(self):
        return f"Hi, I'm {self.name}, I'm {self.age} years old and I live in {self.address}."


class Student(Person):
    def __init__(self, name, age, address, field_of_study):
        # super().__init__ lets the parent set name/age/address,
        # so we don't repeat that code here.
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self):
        # Reuse the parent's sentence, then add the student-specific part.
        return f"{super().introduce()} I study {self.field_of_study}."


class Employee(Person):
    def __init__(self, name, age, address, company):
        super().__init__(name, age, address)
        self.company = company

    def introduce(self):
        return f"{super().introduce()} I work at {self.company}."


# ---------------------------------------------------------------------------
# Problem 3 — BankAccount / SavingsAccount
# ---------------------------------------------------------------------------
class BankAccount:
    def __init__(self, account_number, balance=0):
        if balance < 0:
            raise ValueError("initial balance cannot be negative")
        self.account_number = account_number
        self.balance = balance

    @staticmethod
    def _check_amount(amount):
        # Refuse 0 or negative amounts: depositing -50 would really be a withdrawal.
        if amount <= 0:
            raise ValueError("amount must be positive")

    def deposit(self, amount):
        self._check_amount(amount)
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """Remove money. Returns False (and changes nothing) if the balance is too low."""
        self._check_amount(amount)
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def transfer(self, destination, amount):
        """Move money to another account.

        Returns False if the balance is insufficient, True otherwise.
        Works with any BankAccount, including a SavingsAccount (a subclass).
        """
        if not isinstance(destination, BankAccount):
            raise TypeError("destination must be a BankAccount")
        if destination is self:
            raise ValueError("cannot transfer to the same account")
        # Withdraw first: if it fails, nothing has moved.
        if not self.withdraw(amount):
            return False
        destination.deposit(amount)
        return True

    def __repr__(self):
        return f"{type(self).__name__}({self.account_number!r}, balance={self.balance})"


class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0, interest_rate=0.02):
        super().__init__(account_number, balance)
        if interest_rate < 0:
            raise ValueError("interest rate cannot be negative")
        # Rate as a fraction: 0.02 means 2 %.
        self.interest_rate = interest_rate

    def add_interest(self):
        """Add the interest to the balance and return the amount added."""
        interest = self.balance * self.interest_rate
        self.balance += interest
        return interest

    def check_balance(self):
        return self.balance


# ---------------------------------------------------------------------------
# Demo — run:  python3 inheritance.py
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- Problem 1: Vehicles ---")
    for vehicle in (Vehicle(), Car(), Bicycle()):
        # Same call, different result depending on the class: polymorphism.
        print(f"{type(vehicle).__name__:<8} -> {vehicle.drive()}")

    print("\n--- Problem 2: People ---")
    people = [
        Person("Alice", 40, "Paris"),
        Student("Bob", 21, "Lyon", "computer science"),
        Employee("Chloe", 33, "Nantes", "Airbus"),
    ]
    for person in people:
        print(person.introduce())

    print("\n--- Problem 3: Bank accounts ---")
    checking = BankAccount("FR-001", 500)
    savings = SavingsAccount("FR-002", 1000, interest_rate=0.05)
    print(f"Start:                 {checking}, {savings}")
    print(f"transfer 200 -> {checking.transfer(savings, 200)}:   {checking}, {savings}")
    print(f"transfer 1000 -> {checking.transfer(savings, 1000)}: {checking} (unchanged)")
    print(f"add_interest -> +{savings.add_interest()}")
    print(f"check_balance -> {savings.check_balance()}")
