# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_

import pytest
import sys
from io import StringIO

from bed import(parse_line, Table)
from query_bed import (BedLine, extract_region, read_bed_file, print_line, upper_bound, lower_bound)

def test_works_with_different_bedlines():
    """
    The function should work with different string representations of int in base 10
    And it should work with different white spaces

    Uses parse_line which is defined in bed.py
    Parse_line is not used directly in query_bed.py but it is used in the function for read_bed_file
    """
    expected = BedLine('chr1', 20100, 20101, 'foo')
    assert parse_line('chr1 20_100 20_101 foo') == expected
    assert parse_line('chr1 20100     20101         foo') == expected
    assert parse_line('chr1 20100\t20101\nfoo') == expected



def test_error_if_wrong_line():
    """
    And ValueError should be raised with a line with to many or to few columns is parsed
    And AssertionError should be raised if the interval is not a single nucleotide

    Uses parse_line which is defined in bed.py
    Parse_line is not used directly in query_bed.py but it is used in the function for read_bed_file
    """
    line_with_less_columns = 'chr1 20100 20101'
    line_with_more_columns = 'chr1 20100 20101 foo 10'
    line_with_interval_not_SNP = 'chr1 20100 20201 foo'
    with pytest.raises(ValueError):
        parse_line(line_with_less_columns)
    with pytest.raises(ValueError):
        parse_line(line_with_more_columns)
    with pytest.raises(AssertionError):
        parse_line(line_with_interval_not_SNP)


def test_extracted_regions():
    """
    Should handle a list of bedlines (as the one provided by Table.get_chrom()) 
    and return a list of BedLines containing all the features between a given start and end 
    """

    bed = [BedLine("chrom1", 2, 3, "01"),
    BedLine("chrom1", 4, 5, "03"), 
    BedLine("chrom1", 4, 5, "04"), 
    BedLine("chrom1", 6, 7, "05"),
    BedLine("chrom1", 10, 11, "06"),
    BedLine("chrom1", 12, 13, "07"),
    BedLine("chrom1", 17, 18, "08"),
    BedLine("chrom1", 19, 20, "09"),
    BedLine("chrom1", 200, 201, "10")]

    assert extract_region(bed, 1, 201) == [BedLine("chrom1", 2, 3, "01"),
    BedLine("chrom1", 4, 5, "03"), 
    BedLine("chrom1", 4, 5, "04"), 
    BedLine("chrom1", 6, 7, "05"),
    BedLine("chrom1", 10, 11, "06"),
    BedLine("chrom1", 12, 13, "07"),
    BedLine("chrom1", 17, 18, "08"),
    BedLine("chrom1", 19, 20, "09"),
    BedLine("chrom1", 200, 201, "10")]

    assert extract_region(bed, 4, 5) == [BedLine("chrom1", 4, 5, "03"), 
    BedLine("chrom1", 4, 5, "04")]

    assert extract_region(bed, 1, 4) == [BedLine("chrom1", 2, 3, "01")]

    assert extract_region(bed, 201, 1000) == []

    assert extract_region(bed, 5, 20) == [BedLine("chrom1", 6, 7, "05"),
    BedLine("chrom1", 10, 11, "06"),
    BedLine("chrom1", 12, 13, "07"),
    BedLine("chrom1", 17, 18, "08"),
    BedLine("chrom1", 19, 20, "09")]

def test_extracting_features_from_BEDtable():
    bed = StringIO("chrom1 201 202 foo\nchrom1 304 305 bar\nchrom1 20100 20101 bas\nchrom7 207 208 qux\nchrom20 506 507 qax")
    bedtable = Table()
    for line in bed:
        bedtable.add_line(parse_line(line))
    
    assert extract_region(bedtable.get_chrom("chrom1"), 200, 20101) == [BedLine("chrom1", 201, 202, "foo"), 
    BedLine("chrom1", 304, 305, "bar"), 
    BedLine("chrom1", 20100, 20101, "bas")]

    assert extract_region(bedtable.get_chrom("chrom7"), 200, 250) == [BedLine("chrom7", 207, 208, "qux")]

    assert extract_region(bedtable.get_chrom("chrom20"), 500, 510) == [BedLine("chrom20", 506, 507, "qax")]

def test_print_lines_correctly(capsys):
    """
    Tests that the lines that are printed to the output file (og stdout) in the end is printed in the correct format
    """
    print_line(BedLine("chrom1", 1, 2, "Feature01"), sys.stdout)
    out, err = capsys.readouterr()
    assert out == "chrom1\t1\t2\tFeature01\n"
    assert err == "" 

    print_line(BedLine("chrom20", 204, 205, "Feature1000"), sys.stdout)
    out, err = capsys.readouterr()
    assert out == "chrom20\t204\t205\tFeature1000\n"
    assert err == "" 
