from typing import Dict, Callable, Iterable


def to_ones(num: int) -> str:
    assert not num < 0, 'Number must be positive'
    return '1' * (num + 1)


def from_ones(num: str) -> int:
    return len(num) - 1


def load_file(path: str):
    with open(path, 'r') as file:
        return file.read()


def on_condition(iterable: Iterable, condition):
    res = []
    for elem in iterable:
        if condition(elem): res.append(elem)
    return res


class Logger:
    _states: Dict[int, Callable]

    def __init__(self, states=None):
        if not states: states = {}
        self._states = states

    def __setitem__(self, key, value):
        self._states[key] = value

    def __call__(self, key, *args, **kwargs):
        self._states[key](*args, **kwargs)
