"""
WeakSet equality behaves strangely as of Python `3.8.5`. For example, `set() != WeakSet()`.
"""

from dataclasses import dataclass
from typing import AbstractSet
from weakref import WeakSet
import pytest


@dataclass(frozen=True)
class X:
    """A type that can be placed in a WeakSet"""
    a: int


x = X(1)


def test_equality():
    """
    Set equality appears to be undefined behavior when used on sets and WeakSets.
    Note that the documentation [^1] does not explicitly define the behavior of equality in general, only
    for set and frozenset.
    [^1]: https://docs.python.org/3.8/library/stdtypes.html#set-types-set-frozenset
    """

    assert {x} == {x}
    assert {x} == frozenset([x])
    assert {x} != WeakSet([x])  # Unintuitive!!
    assert set() != WeakSet()

    """
    Solution Attempt 1: Symmetric Difference
    
    Instead of `a == b`, one can use `not a ^ b`.
    However, the symmetric difference is not symmetrically defined. The
    problem is that set.__xor__ should return NotImplemented instead of raising
    a TypeError so that WeakSet.__rxor__ is called.

    """

    assert not WeakSet([x]) ^ {x}
    with pytest.raises(TypeError):
        assert not {x} ^ WeakSet([x])  # Bad surprise!!

    class MySet(set):
        """Patch the bad behavior"""
        def __xor__(self, other):
            try:
                super().__xor__(other)
            except TypeError:
                return NotImplemented

    assert not MySet([x]) ^ WeakSet([x])
    assert not MySet() ^ WeakSet()

    """
    Solution Attempt 2: Set Containment
    
    Use `a <= b <= a`, which is symmetric. This is nicer when you don't want to create a workaround subclass.
    """

    def eq(a: AbstractSet, b: AbstractSet) -> bool:
        return a <= b <= a

    assert eq({x}, WeakSet([x]))
    assert eq(WeakSet([x]), {x})

    """Alternatively, subclass WeakSet and override __eq__"""

    class MyWeakSet(WeakSet):
        __eq__ = eq

    assert MyWeakSet([x]) == {x}
    assert {x} == MyWeakSet([x])
    assert set() == MyWeakSet()


if __name__ == '__main__':
    test_equality()
