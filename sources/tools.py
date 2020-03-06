from typing import Dict, Callable


class Logger:
    _states: Dict[int, Callable]

    def __init__(self, states=None):
        if not states: states = {}
        self._states = states

    def __setitem__(self, key, value):
        self._states[key] = value

    def __call__(self, key, *args, **kwargs):
        self._states[key](*args, **kwargs)