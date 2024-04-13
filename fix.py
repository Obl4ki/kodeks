from utils import tuple_windows

from polish_dictionary import is_word_correct
from copy import deepcopy


def fix_text(text: str) -> str:
    splits = split_by_whitespace_and_symbols(text)
    fixed_article = remove_newline_dash(splits)
    fixed_article = remove_unnecessary_splits(fixed_article)
    joined_fixed = fix_whitespace_puctuation(" ".join(fixed_article))

    return joined_fixed


def split_by_whitespace_and_symbols(text: str) -> list[str]:
    for punctuation in [
        ".",
        ",",
        "!",
        "?",
        ":",
        ";",
        "-",
        "§",
        "(",
        ")",
        "[",
        "]",
        '"',
    ]:
        text = text.replace(punctuation, f" {punctuation} ")

    return text.split()


def remove_newline_dash(splits: list[str]) -> list[str]:
    new_splits = deepcopy(splits)

    for window_begin_idx, (first_word, _maybe_dash, second_word) in enumerate(
        tuple_windows(splits, n=3)
    ):
        if not _maybe_dash in ["-", "-\n"]:
            continue

        if is_word_correct(first_word + second_word):
            new_splits[window_begin_idx] = first_word + second_word
            new_splits[window_begin_idx + 1] = ""
            new_splits[window_begin_idx + 2] = ""

    return [split for split in new_splits if not split == ""]


def remove_unnecessary_splits(splits: list[str]) -> list[str]:
    new_splits = deepcopy(splits)

    # Remove spaces that were inserted into words by mistake of the pdf parser.
    # The method is aggresive - for example "więc ej" will become "więcej" because "więcej" is a valid word,
    # even though "więc" & "ej" are also valid.
    for window_begin_idx, (first_word, second_word) in enumerate(
        tuple_windows(splits, n=2)
    ):
        # if not first_word.isalpha() or not second_word.isalpha():
        #     return splits

        if is_word_correct(first_word + second_word):
            new_splits[window_begin_idx] = first_word + second_word
            new_splits[window_begin_idx + 1] = ""

    return [split for split in new_splits if not split == ""]


def fix_whitespace_puctuation(text: str) -> str:
    toggle = ' "'
    while ' " ' in text:
        text = text.replace(' " ', toggle, 1)
        if toggle == '" ':
            toggle = ' "'
        else:
            toggle = '" '

    right_sided_punctuation = ["(", "["]

    left_sided_punctuation = [".", ",", "!", "?", ":", ";", "]", ")"]

    for p in right_sided_punctuation:
        text = text.replace(f"{p} ", p)

    for p in left_sided_punctuation:
        text = text.replace(f" {p}", p)

    return text
