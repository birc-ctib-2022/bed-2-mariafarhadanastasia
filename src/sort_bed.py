"""Tool for cleaning up a BED file."""

import argparse  # we use this module for option parsing. See main for details.

import sys
from typing import TextIO, TypeVar
from bed import (
    BedLine, read_bed_file, print_line, Table
)


T = TypeVar('T')


def sort_file(table: Table) -> None:
    """Sort each chromosome and update the table."""
    for chrom, features in table.items():
        # Here we iterate through all the chromosomes in the file.
        # You need to sort `features` with respect to chrom_start
        # and then update the table
        # FIXME: sort `features`
        table[chrom] = sort_feature(features)  # features should be sorted here


def merge(left: list[T], right: list[T]) -> list[T]:
    """
    This function will merge two lists.

    >>> merge([3], [2])
    [2, 3]
    >>> merge([9, 8, 7], [5, 4, 3, 2, 1])
    [5, 4, 3, 2, 1, 9, 8, 7]
    """
    i, j = 0, 0
    out = []

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1

    out += left[i:]
    out += right[j:]

    return out


def merge_sort(features: list[T]) -> list[T]:
    """
    This function will sort a list utilizing merge function.

    >>> merge_sort([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> merge_sort([9, 8])
    [8, 9]
    >>> merge_sort([5, 4, 10, 2, 1, 9, 6, 8, 3, 7])
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    if len(features) < 2:
        return features

    mid = len(features) // 2

    return merge(
        left = merge_sort(features[:mid]),
        right = merge_sort(features[mid:])
    )


def sort_feature(features: list[T]) -> list[T]:
    """
    This function only calls merge_sort function.
    It will sort the features based on the first column.
    If the first column is the same, it will sort based on the next column.
    """
    return merge_sort(features)


def print_file(table: Table, outfile: TextIO) -> None:
    """Write the content of table to outfile."""
    for chrom in sorted(table.tbl):
        for feature in table.get_chrom(chrom):
            print_line(feature, outfile)


def main() -> None:
    """Run the program."""
    # Setting up the option parsing using the argparse module
    argparser = argparse.ArgumentParser(description="Sorts a BED file")
    # 'infile' is either provided as an input file name or stdin
    argparser.add_argument('infile',
                           nargs='?',                    # 0 or 1 arguments
                           type=argparse.FileType('r'),  # file for reading
                           default=sys.stdin)
    # 'outfile' is either provided as a file name or we use stdout
    argparser.add_argument('outfile',
                           nargs='?',                    # 0 or 1 arguments
                           type=argparse.FileType('w'),  # file for writing
                           default=sys.stdout)

    # Parse options and put them in the table args
    args = argparser.parse_args()

    # With all the options handled, we just need to do the real work
    table = read_bed_file(args.infile)
    sort_file(table)
    print_file(table, args.outfile)


if __name__ == '__main__':
    main()
