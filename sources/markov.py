# Normal Markov algorithms
# '' is an empty symbol
# !!! RN there are no checks for alphabet intersections !!!

from builtins import str
from typing import List, Tuple
from tools import Logger


# Logging utils
_markov_logger = Logger()
_markov_logger['start'] = lambda string: print(f"Start: '{string}'")
_markov_logger['stop'] = lambda string: print(f"Stop: '{string}'")
_markov_logger['process'] = lambda occ, rep, string: print(f"Rule: '{occ}'->'{rep}'; Result: '{string}'")


Rule = Tuple[str, str]


class Markov:
    _rules: List[Rule]
    _stop: str

    def __init__(self,
                 rules: List[Rule], *,
                 stop='.',
                 verbose=False):
        self._rules = rules
        self._stop = stop
        self.verbose = verbose

    def __call__(self, string: str):
        backup = ''
        self._log('start', string)
        while backup != string and self._stop not in string:
            backup = string
            string = self._next_rule(string)
        self._log('stop', string)
        return string.replace(self._stop, '', 1)

    def _next_rule(self, string: str) -> str:
        for occ, rep in self._rules:
            if occ in string:
                string = string.replace(occ, rep, 1)
                self._log('process', occ, rep, string)
                break
        return string

    def _log(self, *args, **kwargs):
        if self.verbose: _markov_logger(*args, **kwargs)
