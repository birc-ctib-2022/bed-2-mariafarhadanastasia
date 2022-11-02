# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_

from sort_bed import merge, merge_sort
from bed import BedLine

def test_merge():
    assert merge([5], [4]) == [4, 5]
    assert merge([2, 9], [0, 5]) == [0, 2, 5, 9]
    assert merge([0, 1, 4, 5, 5, 7], [0, 2, 3, 5, 5, 7, 9]) == [0, 0, 1, 2, 3, 4, 5, 5, 5, 5, 7, 7, 9]
    assert merge([9, 6, 8, 7], [5, 4, 3, 2, 1]) == [5, 4, 3, 2, 1, 9, 6, 8, 7]

def test_merge_sort():
    assert merge_sort([0, 5, 4, 7, 5, 1, 7, 5, 3, 2, 9, 0, 5]) == [0, 0, 1, 2, 3, 4, 5, 5, 5, 5, 7, 7, 9]
    assert merge_sort(
        [("chr1", 2, 3), ("chr1", 3, 4), ("chr1", 0, 1), ("chr1", 7, 8), ("chr1", 5, 6)]
    ) == [('chr1', 0, 1), ('chr1', 2, 3), ('chr1', 3, 4), ('chr1', 5, 6), ('chr1', 7, 8)]
    assert merge_sort(
        [(2, 5), (7, 3), (0, 2), (9, 6), (0, 1), (4, 8)]
    ) == [(0, 1), (0, 2), (2, 5), (4, 8), (7, 3), (9, 6)]
    assert merge_sort(
        [
            BedLine("chrom1", 4, 5, "04"), 
            BedLine("chrom1", 17, 18, "08"),
            BedLine("chrom1", 12, 13, "07"),
            BedLine("chrom1", 6, 7, "05"),
            BedLine("chrom1", 10, 11, "06")
        ]
    ) == [
            BedLine("chrom1", 4, 5, "04"), 
            BedLine("chrom1", 6, 7, "05"),
            BedLine("chrom1", 10, 11, "06"),
            BedLine("chrom1", 12, 13, "07"),
            BedLine("chrom1", 17, 18, "08"),
    ]
    assert merge_sort(
        [
            BedLine("chrom1", 4, 5, "04"), 
            BedLine("chrom1", 17, 18, "08"),
            BedLine("chrom2", 12, 13, "07"),
            BedLine("chrom2", 6, 7, "05"),
            BedLine("chrom1", 10, 11, "06")
        ]
    ) == [
            BedLine("chrom1", 4, 5, "04"), 
            BedLine("chrom1", 10, 11, "06"),
            BedLine("chrom1", 17, 18, "08"),
            BedLine("chrom2", 6, 7, "05"),
            BedLine("chrom2", 12, 13, "07")
    ]
