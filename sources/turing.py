from builtins import str
from enum import IntEnum
from typing import NamedTuple, List, Tuple, Dict, Iterable

from tools import Logger

# Logging utils
_turing_logger = Logger()
_turing_logger['start'] = lambda tape: print(f"Initial tape: '{tape}'")
_turing_logger['stop'] = lambda tape: print(f"Result tape: '{tape}'")
_turing_logger['process'] = lambda pos, cond, rep, tape: print(
    f"I:{pos}, St:{cond.state}; Rule: (q{cond.state},{cond.letter})->(q{rep.state},"
    f"{rep.letter if rep.letter else 'Empty'},{rep.move.name}); Tape: '{tape}';"
)


class Move(IntEnum):
    L = -1
    St = 0
    R = 1


# Named tuples are especially good there, as they provide sort of
# readable access to tuple members. Though, now i have to convert tuples
# to named tuples
Condition = NamedTuple('Condition', [('state', int),
                                     ('letter', str)])
Replacement = NamedTuple('Replacement', [('state', int),
                                         ('letter', str),
                                         ('move', Move)])
Rule = Tuple[Condition, Replacement]


# Dict is too muсh for such a simple structure. Also tried
# collections.deque as _data, but it does not have __setitem__()
class Tape:
    _data: Dict[int, str]

    def __init__(self, string: str):
        self._data = {i: e for i, e in enumerate(string)}

    def __getitem__(self, item: int) -> str:
        if item not in self._data.keys():
            # Empty cells can be used as spaces (can they?)
            self._data[item] = ' '
            return ''
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __str__(self):
        return ''.join(self._data[i] for i in sorted(self._data.keys())).strip()


class Turing:
    _program: List[Rule]
    _state: int

    def __init__(self,
                 program: Iterable,
                 state=0, *,
                 verbose=False):
        # TODO(Mocurin) add string support
        self._program = Turing._parse_iterable(program)
        self._state = state
        self.verbose = verbose

    def __call__(self, tape: str):
        tape = Tape(tape)
        st = self._state
        pos = 0

        self._log('start', tape)
        while True:
            cond, rep = self._by_state(st, tape[pos])
            if rep is None: break
            self._log('process', pos, cond, rep, tape)
            st = rep.state
            tape[pos] = rep.letter
            pos += rep.move
        self._log('stop', tape)
        return str(tape)

    def _by_state(self, state: int, letter: str):
        for cond, rep in self._program:
            if cond.state == state and cond.letter == letter:
                return cond, rep
        return None, None

    def _log(self, *args, **kwargs):
        if self.verbose: _turing_logger(*args, **kwargs)

    @staticmethod
    def _parse_iterable(program: Iterable) -> List[Rule]:
        return [(Condition(*cond), Replacement(*rep)) for cond, rep in program]
