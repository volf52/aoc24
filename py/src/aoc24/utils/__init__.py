from pathlib import Path

BASE_DATA_PATH = Path(__file__, "..", "../../../../data").resolve()


def get_data_file(day: int, check_if_exists: bool = True):
    pth = BASE_DATA_PATH.joinpath(f"day{day}")

    if check_if_exists and not pth.exists():
        raise ValueError(f"Nothing found at '{pth}'")

    return pth
