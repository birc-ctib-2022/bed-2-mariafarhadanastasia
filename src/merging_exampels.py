def merge_2(x: list[int], y: list[int]) -> list[int]:
    """
    Merges 2 sorted lists of integers
    >>> merge_2([1,2,4], [3, 4, 5, 6])
    [1, 2, 3, 4, 4, 5, 6]
    """
    result = []
    i, j = 0, 0
    while i<len(x) and j<len(y):
        if x[i] < y[j]:
            result.append(x[i])
            i += 1
        else:
            result.append(y[j])
            j += 1
    result.extend(x[i:])
    result.extend(y[j:])
    return result

def merge_3_onebyone(x: list[int], y:list[int], z:list[int]) -> list[int]:
    """
    Merges 3 sorted lists of integers. It does so by merging x and y, and then merge z in afterward 
    >>> merge_3_onebyone([1, 2, 3, 6], [3, 4, 5], [1, 7])
    [1, 1, 2, 3, 3, 4, 5, 6, 7]
    """
    merged = merge_2(x,y)
    return merge_2(merged, z)

def merge_3_atonce(x: list[int], y:list[int], z:list[int]) -> list[int]:
    """
    Merges 3 sorted list of integers all at a time.
    >>> merge_3_onebyone([1, 2, 3, 6], [3, 4, 5], [1, 7])
    [1, 1, 2, 3, 3, 4, 5, 6, 7]
    """
    result = []
    i, j, k = 0, 0, 0
    while i<len(x) and j<len(y) and k<len(z):
        if x[i] < y[j] and x[i] < z[k]:
            result.append(x[i])
            i += 1
        elif y[j] < x[i] and y[j] < z[k]:
            result.append(y[j])
            j += 1
        else: 
            result.append(z[k])
            k += 1
    if i < len(x):
        result.append(merge_2(y[j:], z[k:]))
    elif j < len(y):
        result.append(merge_2(x[i:], z[k:]))
    else:
        result.append(merge_2(x[i:], y[j:]))
    return result
    return
