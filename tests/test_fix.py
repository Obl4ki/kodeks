from fix import (
    fix_text,
    remove_newline_dash,
    remove_unnecessary_splits,
    split_by_whitespace_and_symbols,
)


TEST_ARTICLE = """Art. 53. § 1. Sąd wymierza karę według swojego uznania, w gran-
icach przewidziany ch w ustawie, uwzględniając stopień społecznej szkodliwości czynu, 
okoliczności obciążające i okoliczności łagodzące, cele kary w zakresie społecznego oddziaływania, a także cele zapobiegawcze, które ma ona osiągnąć w stosunku do 
skazanego. Dolegliwość kar y nie może przekraczać stopnia winy.  
§ 2. Wymierzając karę, sąd uwzględnia w  szczególności motywację i  sposób 
zachowania się sprawcy, zwłaszcza w  razie  popełnienia przestępstwa na szkodę osoby 
nieporadnej ze względu na wiek lub stan zdrowia, popełnienie pr zestępstwa wspólnie 
z nieletnim, rodzaj i  stopień naruszenia ciążących na sprawcy obowiązków, rodzaj 
i rozmiar ujemnych następstw przestępstwa, właściwości i  warunki osobiste sprawcy, 
sposób życia przed popełnieniem przestępstwa i  zachowanie się po jego po pełnieniu, 
a zwłaszcza staranie o  naprawienie szkody lub zadośćuczynienie w  innej formie 
społecznemu poczuciu sprawiedliwości, a  także zachowanie się pokrzywdzonego.  """


def test_split():
    expected_start = [
        "Art",
        ".",
        "53",
        ".",
        "§",
        "1",
        ".",
        "Sąd",
        "wymierza",
        "karę",
        "według",
        "swojego",
        "uznania",
        ",",
        "w",
        "gran",
        "-",
        "icach",
    ]

    result = split_by_whitespace_and_symbols(TEST_ARTICLE)
    for expected_word, result_word in zip(expected_start, result):
        assert expected_word == result_word

    result = split_by_whitespace_and_symbols("!-?studnia bez\ndna§")
    assert result == ["!", "-", "?", "studnia", "bez", "dna", "§"]


SPLITTED_WORDS = splitted_words = [
    "Art",
    ".",
    "53",
    ".",
    "§",
    "1",
    ".",
    "Sąd",
    "wymierza",
    "karę",
    "według",
    "swojego",
    "uznania",
    ",",
    "w",
    "gran",
    "-",
    "icach",
    "przewidziany",
    "ch",
    "w",
    "ustawie",
]


def test_remove_newline_dash():

    expected_start = [
        "Art",
        ".",
        "53",
        ".",
        "§",
        "1",
        ".",
        "Sąd",
        "wymierza",
        "karę",
        "według",
        "swojego",
        "uznania",
        ",",
        "w",
        "granicach",
    ]

    result = remove_newline_dash(SPLITTED_WORDS)
    for expected_word, result_word in zip(expected_start, result):
        assert expected_word == result_word


def test_remove_unnecessary_splits():
    result = " ".join(remove_unnecessary_splits(SPLITTED_WORDS))
    assert "przewidziany ch" not in result
    assert "przewidzianych w ustawie" in result


def test_fix_whitespace_puctuation():
    DIACRITIC_MESS = 'To jest tekst testowy[1],który jest próbą ( choć nie wiadomo ,czy udaną )- wprowadzić system poprawy tekstu w "zakłopotanie ".'

    result = fix_text(DIACRITIC_MESS)

    assert (
        result
        == 'To jest tekst testowy [1], który jest próbą (choć nie wiadomo, czy udaną) - wprowadzić system poprawy tekstu w "zakłopotanie".'
    )


def test_fix():
    result = fix_text(TEST_ARTICLE)

    assert result.startswith(
        "Art. 53. § 1. Sąd wymierza karę według swojego uznania, w granicach przewidzianych w ustawie, uwzględniając stopień"
    )
