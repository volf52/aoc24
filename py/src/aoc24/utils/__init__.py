from pathlib import Path

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
