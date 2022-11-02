# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_
from query_bed import extract_region
from bed import BedLine

def test_extract_region():
    """asserts that at least the examples are as expected :)"""
    #asserts that a very simple extraction works
    input1=[BedLine('chrom5', 983, 984, 'Feature-109')]
    assert extract_region(input1, 980, 985)==[BedLine('chrom5', 983, 984, 'Feature-109')]
    #asserts that a more complicated extraction works, also with 2 features
    input2 = [
        BedLine("chrom3",	774,	775,	"Feature-148"),
        BedLine("chrom3",	778,	779,	"Feature-125"),
        BedLine("chrom3",	780,	781,	"Feature-401"),
        BedLine("chrom3",	797,	798,	"Feature-515"),
        BedLine("chrom3",	797,	798,	"Feature-646"),
        BedLine("chrom3",	809,	810,	"Feature-335")
    ]
    assert extract_region(input2, 780, 985)==[
        BedLine(chrom='chrom3', chrom_start=780, chrom_end=781, name='Feature-401'),
        BedLine(chrom='chrom3', chrom_start=797, chrom_end=798, name='Feature-515'),
        BedLine(chrom='chrom3', chrom_start=797, chrom_end=798, name='Feature-646'),
        BedLine(chrom='chrom3', chrom_start=809, chrom_end=810, name='Feature-335')
        ]
    #asserts that an empty list is returned as an empty list
    input3=[]
    assert extract_region(input3, 780, 985)==[]
    #asserts that query outside of the range in the feature file is == []
    assert extract_region(input3, 1000, 7000)==[]

    



    
