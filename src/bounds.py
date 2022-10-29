"""
Module for experimenting with lower and upper bounds.

Unlike in the BED functionality, where we need to search for a lower bound in
a list of features, here we only concern ourselves with lists of integers.
"""


def lower_bound(x: list[int], v: int) -> int:
    """Get the index of the lower bound of v in x.

    If all values in x are smaller than v, return len(x).
    """
    low, high=0, len(x)
    while low<high:
        mid=(low+high)//2
        if x[mid]==v:
            while x[mid-1]==x[mid]:
                mid-=1
            else:
                return mid
        elif x[mid]<v:
            low=mid+1
        else:
            high=mid
    if low==len(x):
        return len(x)
    else:
        return 0


x=[1,2,3,3,3,4,4,4,4,4,5]
v=4
print(lower_bound(x,v))

def upper_bound(x: list[int], v: int) -> int:
    """Get the index of the upper bound of v in x.

    If all values in x are smaller than v, return len(x).
    """
    low, high=0, len(x)
    while low<high:
        mid=(low+high)//2
        if x[mid]==v:
            while x[mid]==x[mid+1]:
                mid+=1
            else:
                return mid
        elif x[mid]<v:
            low=mid+1
        else:
            high=mid
    if low==len(x):
        return len(x)
    else:
        return 0


x=[1,2,3,4,4,4,4,4,5]
v=4
print(upper_bound(x,v))


