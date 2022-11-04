"""Testing bounds."""

from bounds import lower_bound, upper_bound
from random import randint


def test_bounds() -> None:
    """
    Test lower_bound and upper_bound.

    Test that if we extract the range from lower to upper bound,
    we get the block we are searching for.
    """
    x = [randint(0, 100) for _ in range(500)]
    x.sort()
    for i in range(500):
        query = x[lower_bound(x, i):upper_bound(x, i)]
        for q in query:
            assert i == q

def test_lower_bound() -> None:
    x = [0, 1, 2, 2, 3, 4, 4, 6]
    assert lower_bound(x, 0) == 0
    assert lower_bound(x, 1) == 1
    assert lower_bound(x, 2) == 2
    assert lower_bound(x, 3) == 4
    assert lower_bound(x, 4) == 5
    assert lower_bound(x, 5) == 7
    assert lower_bound(x, 6) == 7
    assert lower_bound(x, 7) == 8

def test_upper_bound() -> None:
    x = x = [0, 1, 2, 2, 3, 4, 4, 6]
    assert upper_bound(x, 0) == 1
    assert upper_bound(x, 1) == 2
    assert upper_bound(x, 2) == 4
    assert upper_bound(x, 3) == 5
    assert upper_bound(x, 4) == 7
    assert upper_bound(x, 5) == 7
    assert upper_bound(x, 6) == 7
    assert upper_bound(x, 7) == 8
