from typing import NamedTuple, List, Tuple, Dict, Iterable
from enum import IntEnum
from builtins import str


class Move(IntEnum):
    Left = -1
    Stay = 0
    Right = 1


Condition = NamedTuple('Condition', [('state', int),
                                     ('letter', str)])
Replacement = NamedTuple('Replacement', [('state', int),
                                         ('letter', str),
                                         ('move', Move)])
Rule = Tuple[Condition, Replacement]


class Tape:
    _data: Dict[int, str]

    def __init__(self, string: str):
        self._data = {i: e for i, e in enumerate(string)}

    def __getitem__(self, item: int) -> str:
        if item not in self._data.keys():
            return ''
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __str__(self):
        return ''.join(self._data[i] for i in sorted(self._data.keys()))


class Turing:
    _program: List[Rule]
    _state: int

    def __init__(self, program: Iterable, state=0):
        # TODO(Mocurin) add string support
        self._program = Turing._parse_iterable(program)
        self._state = state

    def __call__(self, tape: str):
        tape = Tape(tape)
        st = self._state
        pos = 0

        while True:
            rep = self._by_state(st, tape[pos])
            if rep is None: return str(tape)
            st = rep.state
            tape[pos] = rep.letter
            pos += rep.move

    def _by_state(self, state: int, letter: str):
        for cond, rep in self._program:
            if cond.state == state and cond.letter == letter:
                return rep
        return None

    @staticmethod
    def _parse_iterable(program: Iterable) -> List[Rule]:
        return [(Condition(*cond), Replacement(*rep)) for cond, rep in program]
