from builtins import str
from typing import List, NamedTuple, TypeVar, Dict, Tuple, Callable

from ram_commands import _commands, Mode
from tools import load_file, on_condition, Logger, Tape


# Logging utils
_ram_logger = Logger()
_ram_logger['start'] = lambda state: print(f"Initial tape: '{state['in_tape'][0].as_list()}'")
_ram_logger['stop'] = lambda state: print(f"Result tape: '{state['out_tape'][0].as_list()}'")
_ram_logger['process'] = lambda state, command: print(
    f"{state['line']}: {command}, res memory: {state['memory']}, res tape: {state['out_tape'][0].as_list()}"
)


OpType = TypeVar('OpType', int, str)
Operand = NamedTuple('Operand', [('value', OpType),
                                 ('mode', Mode)])


class RAM:
    _program: List[Tuple[str, Operand]]
    _commands: Dict[str, Callable]
    _flags: Dict[str, int]
    verbose: bool

    def __init__(self,
                 string=None, *,
                 path=None,
                 verbose=False,
                 commands=None):
        assert bool(string) != bool(path), 'Code must be either string or path'
        if commands is None:
            self._commands = _commands
        else:
            self._commands = commands
        if type(path) is str:
            string = load_file(path)
        self._program, self._flags = RAM._parse_code(string)
        self._flags[''] = -1 # Halt case
        self.verbose = verbose

    def __call__(self, tape: List[str], *, sep=''):
        state = dict()
        state['in_tape'] = (Tape(tape, sep=sep), 0)
        state['out_tape'] = (Tape([], sep=sep), 0)
        state['memory'] = dict()
        state['line'] = 0
        self._log('start', state)
        while state['line'] != -1 and state['line'] < len(self._program):
            comm, op = self._program[state['line']]
            res = self._commands[comm](op, state)
            self._log('process', state, (comm, op))
            if not res: state['line'] += 1
            else: state['line'] = self._flags[op.value]
        self._log('stop', state)
        if sep:
            return str(state['out_tape'][0])
        return state['out_tape'][0].as_list()

    def _log(self, *args, **kwargs):
        if self.verbose: _ram_logger(*args, **kwargs)

    # TODO(Mocurin): use RE
    @staticmethod
    def _parse_code(string):
        code = string.splitlines()
        code = on_condition(code, lambda x: x.strip())
        lines = list()
        flags = dict()
        valid = True
        for i, line in enumerate(code):
            line = line.strip()
            try:
                flag, line = RAM._split_flag(line)
                flags[flag] = i
                comm, op = RAM._split_command(line)
                lines.append((RAM._parse_command(comm),
                             Operand(*RAM._parse_operand(op))))
            except SyntaxError as err:
                valid = False
                print(f"Line {i + 1}, SyntaxError: {err}")
        assert valid, "Code is parsed with errors. Terminating execution"
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
            return line, ''
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
            return '', Mode.Flag
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
