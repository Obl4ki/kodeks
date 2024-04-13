# Polish dictionary downloaded from http://sjp.pl/slownik/odmiany/ as dict.txt


def _load_polish_dictionary(dict_filename: str) -> set[str]:
    dictionary = set()
    
    with open(dict_filename, "r", encoding="utf-8") as f:
        dictionary_lines = f.readlines()

    for line in dictionary_lines:
        for word in line.strip().lower().split(', '):
            dictionary.add(word)

    return dictionary


POLISH_DICT = _load_polish_dictionary('dict.txt')

def is_punctuation(word: str) -> bool:
    return word in [".", ",", "!", "?", ":", ";", "-", "§", '(', ')', '[', ']', '"']

def is_word_correct(word: str) -> bool:
    return word.lower() in POLISH_DICT or is_punctuation(word)