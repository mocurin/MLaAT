from typing import Dict, Callable


def to_ones(num: int) -> str:
    assert num >= 0, 'Number must be positive'
    return '1' * (num + 1)


def from_ones(num: str) -> int:
    return len(num) - 1


class Logger:
    _states: Dict[int, Callable]

    def __init__(self, states=None):
        if not states: states = {}
        self._states = states

    def __setitem__(self, key, value):
        self._states[key] = value

    def __call__(self, key, *args, **kwargs):
        self._states[key](*args, **kwargs)
