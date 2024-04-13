from typing import Iterator


def tuple_windows(seq: list, n: int) -> Iterator:
    if n < 1 or n > n > len(seq):
        return []

    for i in range(len(seq) - n + 1):
        yield tuple(seq[i : i + n])


def write_to_file_utf8(filename: str, text: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
