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


# Dict is too muсh for such a simple structure. Also tried
# collections.deque as _data, but it does not have __setitem__()
class Tape:
    _data: Dict[int, str]
    sep: str

    def __init__(self, data: Iterable, sep=''):
        self._data = {i: e for i, e in enumerate(data)}
        self.sep = sep

    def __getitem__(self, item: int) -> str:
        if item not in self._data.keys():
            # Empty cells can be used as spaces (can they?)
            self._data[item] = ' '
            return ''
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __str__(self):
        return self.sep.join(self._data[i] for i in sorted(self._data.keys())).strip()

    def as_list(self):
        return list(self._data[i] for i in sorted(self._data.keys()))


class Logger:
    _states: Dict[int, Callable]

    def __init__(self, states=None):
        if not states: states = {}
        self._states = states

    def __setitem__(self, key, value):
        self._states[key] = value

    def __call__(self, key, *args, **kwargs):
        self._states[key](*args, **kwargs)
