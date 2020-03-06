# Normal Markov algorithms
# '' is an empty symbol
# !!! RN there are no checks for alphabet intersections !!!

from builtins import str
from typing import List, Tuple


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

    def __call__(self,
                 string: str):
        backup = ''
        if self.verbose: print(f"Start: '{string}'")
        while backup != string and self._stop not in string:
            backup = string
            string = self._next_rule(string)
        if self.verbose: print(f"Stop: '{string}'")
        return string.replace(self._stop, '', 1)

    def _next_rule(self, string: str) -> str:
        for occ, rep in self._rules:
            if occ in string:
                string = string.replace(occ, rep, 1)
                if self.verbose:
                    print(f"Rule: '{occ}' -> '{rep}'")
                    print(f"Result: '{string}'")
                break
        return string
