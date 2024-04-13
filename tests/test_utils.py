from utils import tuple_windows


def test_utils():
    seq = [1, 2, 3, 4]
    assert list(tuple_windows(seq, n=2)) == [(1, 2), (2, 3), (3, 4)]
    assert list(tuple_windows(seq, n=3)) == [(1, 2, 3), (2, 3, 4)]
    assert list(tuple_windows(seq, n=4)) == [(1, 2, 3, 4)]

    assert list(tuple_windows(seq, n=10000)) == []
    assert list(tuple_windows(seq, n=0)) == []
    assert list(tuple_windows(seq, n=-3)) == []
