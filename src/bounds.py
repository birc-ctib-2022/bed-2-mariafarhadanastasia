"""
Module for experimenting with lower and upper bounds.

Unlike in the BED functionality, where we need to search for a lower bound in
a list of features, here we only concern ourselves with lists of integers.
"""


def lower_bound(x: list[int], v: int) -> int:
    """Get the index of the lower bound of v in x.

    If all values in x are smaller than v, return len(x).

    >>> lower_bound([0, 1, 2, 2, 3, 4, 4, 6], 0)
    0
    >>> lower_bound([0, 1, 2, 2, 3, 4, 4, 6], 1)
    1
    >>> lower_bound([0, 1, 2, 2, 3, 4, 4, 6], 2)
    2
    >>> lower_bound([0, 1, 2, 2, 3, 4, 4, 6], 3)
    4
    >>> lower_bound([0, 1, 2, 2, 3, 4, 4, 6], 4)
    5
    >>> lower_bound([0, 1, 2, 2, 3, 4, 4, 6], 5)
    7
    >>> lower_bound([0, 1, 2, 2, 3, 4, 4, 6], 6)
    7
    >>> lower_bound([0, 1, 2, 2, 3, 4, 4, 6], 7)
    8
    >>> lower_bound([1, 11, 17, 21, 22], 3)
    1
    """
    def search(arr, v, first, last):
        if v > arr[last]:
            return len(arr)

        if last >= first:
            mid = (last + first) // 2

            if mid == 0:
                if arr[mid] >= v:
                    return mid
                else:
                    return mid+1

            if arr[mid] >= v:
                if arr[mid - 1] < v: 
                    return mid # We find the lower bound!
                else: # arr[mid - 1] >= v
                    return search(arr, v, first, mid - 1) 
            else: # arr[mid] < v
                return search(arr, v, mid + 1, last)

    first = 0
    last = len(x) - 1
    return search(x, v, first, last)


def upper_bound(x: list[int], v: int) -> int:
    """Get the index of the upper bound of v in x.

    If all values in x are smaller than v, return len(x).

    >>> upper_bound([0, 1, 2, 2, 3, 4, 4, 6], 0)
    1
    >>> upper_bound([0, 1, 2, 2, 3, 4, 4, 6], 1)
    2
    >>> upper_bound([0, 1, 2, 2, 3, 4, 4, 6], 2)
    4
    >>> upper_bound([0, 1, 2, 2, 3, 4, 4, 6], 3)
    5
    >>> upper_bound([0, 1, 2, 2, 3, 4, 4, 6], 4)
    7
    >>> upper_bound([0, 1, 2, 2, 3, 4, 4, 6], 5)
    7
    >>> upper_bound([0, 1, 2, 2, 3, 4, 4, 6], 6)
    7
    >>> upper_bound([0, 1, 2, 2, 3, 4, 4, 6], 7)
    8
    """
    def search(arr, v, first, last):
        if v > arr[last]:
            return len(arr)

        if last >= first:
            mid = (last + first) // 2

            if mid == last:
                return mid

            if arr[mid] > v:
                if arr[mid - 1] <= v:
                    return mid # We find the upper bound!
                else: # arr[mid - 1] > v
                    return search(arr, v, first, mid - 1)
            else: # arr[mid] <= v
                return search(arr, v, mid + 1, last)

    first = 0
    last = len(x) - 1
    return search(x, v, first, last)
    