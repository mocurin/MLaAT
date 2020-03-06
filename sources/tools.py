def to_ones(num: int) -> str:
    assert num >= 0, 'Number must be positive'
    return '1' * (num + 1)


def from_ones(num: str) -> int:
    return len(num) - 1