"""
As of Python 3.8.5, mypy 0.782, mypy will miss the violation of Liskov substitution principle for implicit setters,
although it catches it for explicit ones.

Recommendation: When subclassing mutable types, do not change the type of any mutable attributes,
even though mypy will not complain.

"""

from dataclasses import dataclass


class Explicit:
    _x: float

    def __init__(self, x: float):
        self._x = x

    def set_x(self, value: float) -> None: ...

    def get_x(self) -> float: ...


class Explicit2(Explicit):
    """
    Mypy catches the violation of Liskov substitution principle

    """
    _x: int

    def set_x(self, value: int) -> None: ...

    def get_x(self) -> int: ...


@dataclass
class Implicit:
    x: float


@dataclass
class Implicit2(Implicit):
    """
    Mypy ignores the violation of Liskov substitution principle
    """
    x: int


explicit: Explicit = Explicit2(1)
explicit.set_x(1.0)  # witness the violation that mypy noted

implicit: Implicit = Implicit2(1)
implicit.x = 1.0  # witness the violation that mypy ignored
