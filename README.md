# Python Oddities

Some oddities of the Python language and recommendations for dealing with them.

- WeakSet equality behaves strangely: `WeakSet() != set()`. See `weak_set_equality.py` (Python 3.8.5)
- Liskov substitution principle is ignored for implicit setters and getters. See `liskov_implicit_setters.py` (Python 3.8.5, mypy 0.782)
