from enum import Enum


class Mode(Enum):
    Value = 0      # =i
    Index = 1      # i
    Reference = 2  # *i
    Flag = 3       # flag:


def to_value(op, memory, mode):
    if mode == Mode.Reference:
        op = memory[memory[op]]
    if mode == Mode.Index:
        op = memory[op]
    return op


def to_index(op, memory, mode):
    if mode == mode.Reference:
        op = memory[op]
    return op


def load(op, state):
    op, mode = op
    assert mode in [Mode.Value, Mode.Index, Mode.Reference], f"'{mode}' is not available for this command"
    op = to_value(op, state['memory'], mode)
    state['memory'][0] = op


def store(op, state):
    op, mode = op
    assert mode in [Mode.Index, Mode.Reference], f"'{mode}' is not available for this command"
    op = to_index(op, state['memory'], mode)
    state['memory'][op] = state['memory'][0]


def add(op, state):
    op, mode = op
    assert mode in [Mode.Value, Mode.Index, Mode.Reference], f"'{mode}' is not available for this command"
    op = to_value(op, state['memory'], mode)
    state['memory'][0] += op


def sub(op, state):
    op, mode = op
    assert mode in [Mode.Value, Mode.Index, Mode.Reference], f"'{mode}' is not available for this command"
    op = to_value(op, state['memory'], mode)
    state['memory'][0] -= op


def mult(op, state):
    op, mode = op
    assert mode in [Mode.Value, Mode.Index, Mode.Reference], f"'{mode}' is not available for this command"
    op = to_value(op, state['memory'], mode)
    state['memory'][0] *= op


def div(op, state):
    op, mode = op
    assert mode in [Mode.Value, Mode.Index, Mode.Reference], f"'{mode}' is not available for this command"
    op = to_value(op, state['memory'], mode)
    state['memory'][0] /= op


def read(op, state):
    op, mode = op
    assert mode in [Mode.Index, Mode.Reference], f"'{mode}' is not available for this command"
    op = to_index(op, state['memory'], mode)
    tape, i = state['in_tape']
    elem = tape[i]
    if tape[i].isalpha():
        state['memory'][op] = tape[i]
    else:
        state['memory'][op] = int(tape[i])
    state['in_tape'] = (tape, i + 1)


def write(op, state):
    op, mode = op
    assert mode in [Mode.Value, Mode.Index, Mode.Reference], f"'{mode}' is not available for this command"
    op = to_value(op, state['memory'], mode)
    tape, i = state['out_tape']
    tape[i] = op
    state['out_tape'] = (tape, i + 1)


def jgtz(op, state):
    op, mode = op
    assert mode in [Mode.Flag], f"'{mode}' is not available for this command"
    return state['memory'][0] > 0


def jzero(op, state):
    op, mode = op
    assert mode in [Mode.Flag], f"'{mode}' is not available for this command"
    return state['memory'][0] == 0


def jump(op, state):
    op, mode = op
    assert mode in [Mode.Flag], f"'{mode}' is not available for this command"
    return True


def halt(op, state):
    op, mode = op
    assert mode in [Mode.Flag], f"'{mode}' is not available for this command"
    assert op == '', "Halt requires no operand"
    return True


_commands = {
    'load' : load,
    'store': store,
    'read' : read,
    'write': write,
    'add'  : add,
    'sub'  : sub,
    'div'  : div,
    'mult' : mult,
    'jump' : jump,
    'jgtz' : jgtz,
    'jzero': jzero,
    'halt' : halt
}
