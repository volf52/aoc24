from collections.abc import Generator, Sequence

from aoc24 import utils

SEQ = "XMAS"
SEQ_REV = SEQ[::-1]
SUB_SEQ = "MAS"
SUB_SEQ_REV = SUB_SEQ[::-1]
SEQ_LEN = len(SEQ)


def line_count(line: str) -> int:
    return line.count(SEQ) + line.count(SEQ_REV)


def candidate_generator(lines: Sequence[str]) -> Generator[str]:
    yield from lines
    # yield line[::-1]

    total_rows = len(lines)
    total_cols = len(lines[0])

    # cols
    for i in range(total_cols):
        col = "".join([row[i] for row in lines])
        yield col

    # diag - rows
    for d in range(-(total_rows - SEQ_LEN), total_cols - SEQ_LEN + 1):
        diag = "".join(
            lines[r][c] for r in range(total_rows) for c in range(total_cols) if r - c == d
        )
        if len(diag) >= SEQ_LEN:
            yield diag

    for d in range(SEQ_LEN - 1, total_rows + total_cols - SEQ_LEN):
        diag = "".join(
            lines[r][c] for r in range(total_rows) for c in range(total_cols) if r + c == d
        )
        if len(diag) >= SEQ_LEN:
            yield diag


def count_em(lines: Sequence[str]) -> int:
    return sum(line_count(line) for line in candidate_generator(lines))


def count_mas_x(grid: Sequence[str]) -> int:
    n_rows = len(grid)
    n_cols = len(grid[0])

    def show_x_shape(center_row: int, center_col: int) -> None:
        print(
            f"{grid[center_row-1][center_col-1]}-{grid[center_row-1][center_col+1]}\n-{grid[center_row][center_col]}-\n{grid[center_row+1][center_col-1]}-{grid[center_row+1][center_col+1]}",
        )

    def is_x_shape(center_row: int, center_col: int) -> bool:
        try:
            # show_x_shape(center_row, center_col)
            if grid[center_row][center_col] != SUB_SEQ[1]:
                return False

            tl = grid[center_row - 1][center_col - 1]
            tr = grid[center_row - 1][center_col + 1]
            bl = grid[center_row + 1][center_col - 1]
            br = grid[center_row + 1][center_col + 1]

            main_diag_ok = (tl == SUB_SEQ[0] and br == SUB_SEQ[2]) or (
                tl == SUB_SEQ_REV[0] and br == SUB_SEQ_REV[2]
            )
            if not main_diag_ok:
                return False

            return (bl == SUB_SEQ[0] and tr == SUB_SEQ[2]) or (
                bl == SUB_SEQ_REV[0] and tr == SUB_SEQ_REV[2]
            )
        except IndexError:
            return False

    count = 0
    for row in range(1, n_rows - 1):
        for col in range(1, n_cols - 1):
            # show_x_shape(row, col)
            res = is_x_shape(row, col)
            # print(f"Result: {res}")
            if res:
                count += 1

    return count


def part1():
    lines = utils.read_lines(4)

    res = count_em(lines)

    print(f"Day 4 part 1: {res}")


def part2():
    lines = utils.read_lines(4)

    res = count_mas_x(lines)

    print(f"Day 4 part 2: {res}")


test = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".splitlines()

test2 = """.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........""".splitlines()

print("Count:", count_mas_x(test2))
