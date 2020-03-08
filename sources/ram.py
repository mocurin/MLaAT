from builtins import str
from enum import Enum
from typing import List, NamedTuple, TypeVar, Dict, Tuple

from tools import load_file, on_condition


class Mode(Enum):
    Value = 0      # =i
    Index = 1      # i
    Reference = 2  # *i
    Flag = 3       # flag:


OpType = TypeVar[int, str]
Operand = NamedTuple('Operand', [('value', OpType),
                                 ('mode', Mode)])

_commands = {}


class RAM:
    _program: List[Tuple[str, Operand]]
    _flags: Dict[str, int]

    def __init__(self, string=None, path=None):
        assert bool(string) != bool(path), 'Code must be either string or path'
        if type(path) is str: string = load_file(path)
        self._program, self._flags = RAM._parse_code(string)

    # TODO(Mocurin): use RE
    @staticmethod
    def _parse_code(string):
        code = string.splitlines()
        code = on_condition(code, lambda x: x)
        lines = list()
        flags = dict()
        for i, line in enumerate(code):
            line = line.strip()
            try:
                flag, line = RAM._split_flag(line)
                flags[flag] = i
                comm, op = RAM._split_command(line)
                lines.append((RAM._parse_command(comm),
                              RAM._parse_operand(op)))
            except SyntaxError as err:
                print(f"Line {i}, SyntaxError: {err}")
        return lines, flags

    @staticmethod
    def _split_flag(line: str):
        if ':' not in line:
            return None, line
        tmp = line.split(':', 1)
        if not tmp[0].isalpha():
            raise SyntaxError(f"Non-alpha flag: {tmp[0]}")
        if not tmp[1]:
            raise SyntaxError(f"Incomplete line: {line}")
        tmp[1] = tmp[1].lstrip()
        return tmp

    @staticmethod
    def _split_command(line: str):
        if line.isalpha():
            return line, None
        l, r = line.find('('), line.rfind(')')
        if l == -1 or r == -1:
            raise SyntaxError(f"Invalid operand part: {line}")
        return line[0: l], line[l + 1: r]

    @staticmethod
    def _parse_command(comm: str):
        comm = comm.lower()
        if comm not in _commands.keys():
            raise SyntaxError(f"Unknown command: {comm}")
        return comm

    @staticmethod
    def _parse_operand(op: str):
        if not op:
            return None
        if op.isalpha():
            return op, Mode.Flag
        mode = Mode.Index
        if op[0] == '=':
            mode = Mode.Value
            op = op[1:]
        elif op[0] == '*':
            mode = Mode.Reference
            op = op[1:]
        try:
            op = int(op)
        except ValueError:
            raise SyntaxError(f"Invalid value operand: {op}")
        if mode != Mode.Value and op < 0:
            raise SyntaxError(f"Negative indexer value: {op}")
        return op, mode
