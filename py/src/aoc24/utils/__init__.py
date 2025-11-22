from pathlib import Path
from typing import NamedTuple, Self, override

BASE_DATA_PATH = Path(__file__, "..", "../../../../data").resolve()


def get_data_file(day: int, *, check_if_exists: bool = True):
    pth = BASE_DATA_PATH.joinpath(f"day{day}")

    if check_if_exists and not pth.exists():
        msg = f"Nothing found at '{pth}'"
        raise ValueError(msg)

    return pth


def read_contents(day: int) -> str:
    return get_data_file(day, check_if_exists=True).read_text()


def read_lines(day: int) -> list[str]:
    return read_contents(day).splitlines()


class Pair(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_str(
        cls, s: str, *, line_offset: int = 0, part_offset: int = 0, separator: str = ","
    ) -> "Pair":
        parts = s.strip()[line_offset:].strip().split(separator)
        parts = (x.strip() for x in parts)
        if part_offset:
            parts = (x[part_offset:] for x in parts)

        xy = list(map(int, parts))

        assert len(xy) > 1, "need atleast 2 nums"

        return cls(xy[0], xy[1])

    def determinant(self, other: "Pair") -> int:
        return (self.x * other.y) - (other.x * self.y)

    @override
    def __mul__(self, other: "Pair | int", /) -> "Pair":
        if isinstance(other, int):
            return Pair(self.x * other, self.y * other)

        else:
            return Pair(self.x * other.x, self.y * other.y)

    @override
    def __rmul__(self, other: "Pair | int", /) -> "Pair":
        return self.__mul__(other)

    @override
    def __add__(self, other: "Pair", /) -> "Pair":
        return Pair(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Pair", /) -> "Pair":
        return Pair(self.x - other.x, self.y - other.y)


if __name__ == "__main__":
    a = Pair(94, 34)
    b = Pair(22, 67)

    print(a.determinant(b))
