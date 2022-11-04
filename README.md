[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9078496&assignment_repo_type=AssignmentRepo)
# Processing BED files (Part 2)

If our BED files are sorted, we should be able to extract regions in logarithmic time instead of linear time, if we use binary search instead of linear search.

We won't *quite* get there in this project, because it will take us linear time to load a BED file into memory, but once there we will be able to do such queries. Doing it from file is possible, but involves some technical issues that we don't care to look at here. If you were to look a little deeper into files, and how to make random access queries in files, we could get the rest of the way.

If you are interested in a fully fledged tool that does what we are attempting here, you can check out [Tabix](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3042176/).

## Sorting BED files

In the file `src/sort_bed.py` there is a function

```python
def sort_file(table: Table) -> None
```

that almost sorts a BED file. I is just lacking the sorting part. The function runs through all the chromosomes in the input, and you get them as a list for each chromosome. Sort that list according to the start position. Then the rest of the program should work.

## Merging sorted BED files

If you have two sorted BED files and you want a single sorted BED file with the features from them, it is more efficient to merge them than to concatenate them and then sort them. Merging them can be done in time O(n + m), where *n* and *m* are their length, but sorting the concatenated file alone would take O((n+m)log(n+m)) with a comparison-based sorting algorithm.

The tool `src/merge_bed.py` is almost done, except for the merging. Write the code to merge the features from two BED files. When you merge, you need to consider both the chromosome and the chromosomal position. Because of the simplifying assumptions we have made about features, that they only span one nucelotide, you don't have to worry about their end position; just merge according to chromosomes and start positions.


## Querying BED files with binary search

Now, if we have a sorted BED file and we want to get the region `chrom start end` we can use the hash table I already wrote to get all features on chromosome `chrom` and from there we just need to filter these to only get those with start postion in range `start <= pos < end`.

We can break this down into two parts. First, find the first position in the interval (let's call it `pos_i`)

```
   chrom pos_{i-3} ...
   chrom pos_{i-2} ...
   chrom pos_{i-1} ...
=> chrom pos_i ...
   chrom pos_{i+1} ...
   chrom pos_{i+2} ...
```

This `pos_i` is the smallest position greater or equal to `start`. This kind of value is know as the *lower bound* of `start` in the range; it is admittedly a weird name for something that can be greater than `start`, but the idea is that if you have a block of features with position `start`, then the lower bound is the first (lowest) of them. There is a similar position, the *upper bound* that is the smallest number greater than `start`. For any sorted sequence `x`, if `lb(a)` is the lower bound of a value `a` and `ub(a)` is the upper bound, then `x[lb(a):ub(a)]` contains all the positions with the value `a` (and it will be empty if `a` is not in `x`).

Lower and upper bounds are useful when you need to not only determine whether a value is in a set, but also identify where it is or with which associated features. You can compute both with binary search, so you can think of them as slightly more powerful generalisations of binary search.

We don't necessarily need the upper bound in this project, but in the file `src/bounds.py` I have put some code you can use to experiment with computing lower and upper bounds, and in `src/test_bounds.py` there are a few tests. You can use this to figure out how to adapt a binary search to a lower bound search, and once you have that, you can write code to find `pos_i` in a BED file using lower bound.

From `pos_i` we can scan forward, emitting every feature we see, until we reach a `pos_j >= end`. At that point we have left the region, and we can stop emitting. This isn't the only way to identify the region of features to emit, but it is a simple one, and it is as efficient as we can hope to make it (since we spend time O(z) to emit z features). You can also use an upper bound to figure out where to stop emitting (but it is not the upper bound of `start`); you can even use a lower bound. I'll leave it up to you to figure out how, but if everything else faisl, the strategy described above will work.

In the previous project, where the features weren't sorted, we would have to scan through the entire chromosome to get all the positions that fell within a desired region. If they are sorted, however, we can obviously stop emitting as soon as we reach a position that falls later than (or equal to) `end`, so we only need O(z) time to emit z features in a region.

Furthemore, to find `pos_i`, we can make use of binary search (in the form of a lower bound). If we scan the entire chromosome, as you would in the previous project, it takes time O(m) to find `pos_i` (where m is the number of features in the chromosome). With a binary search, instead, you would only need O(log m).

Once you have implemented a lower bound search for the start of the range, implement the query functionality in `src/query_bed.py`.


## Report

*Answer the questions below and then push this file to GitHub.*

*How do you use binary search to find the lower bound of a number? How did you have to modify the binary search algorithm?*

This code below is a basic binary search:

      def binary_search(arr, x, first, last):
      
         # Check base case
         if last >= first:
      
            mid = (last + first) // 2
      
            # If element is present at the middle itself
            if arr[mid] == x:
                  return mid
      
            # If element is smaller than mid, then it can only
            # be present in left subarray
            elif arr[mid] > x:
                  return binary_search(arr, x, first, mid - 1)
      
            # Else the element can only be present in right subarray
            else:
                  return binary_search(arr, x, mid + 1, last)
It will return the index where we first find the number we are looking for, even if we have several same numbers.

In our lower_bound binary search, we try to find the index of the number we are looking for which located in the very left, where we assume that the array is already sorted.

      def lower_bound(x, v):
         def search(arr, v, first, last):
            if v > arr[last]: # 1
                  return len(arr)

            if last >= first: # 2
                  mid = (last + first) // 2
                  
                  if mid == 0: # 3
                     if arr[mid] >= v:
                        return mid
                     else:
                        return mid + 1      

                  if arr[mid] >= v: # 4
                     # 5
                     if arr[mid - 1] < v: # 6
                        return mid
                     else: # 7
                        return search(arr, v, first, mid - 1) 
                  else: # 8
                     return search(arr, v, mid + 1, last)

         first = 0
         last = len(x) - 1
         return search(x, v, first, last)

We will go through the code one by one. I put the number so it can be easier to read.

1. Base case: if the largest number in the array is smaller than integer we are looking for.
2. We will run the code below if the last index is equal or larger than the first index. 
3. We end up in this condition if we already reach the very left of array, where last = first = 0. If the value in that index is equal or larger than the number we are looking for, we return 0, otherwise we return 1.
4. Otherwise, we do the binary search. We check if value in the mid index, is the same or larger than the number we search.
5. If yes, then we check if the value in the index before the mid is smaller than the number we search. `This part is where it differs from the normal binary search.`
6. If it also yes, this mid index is indeed the lower bound of the number we are looking for.
7. Otherwise, we will continue doing a binary search in the  left part of mid index
8. If the value in mid index we found is smaller than what we are looking for, so it must be in the right side of our mid index.

*Would anything be more difficult if the features covered ranges instead of single nucleotides (like real BED files)? What could go wrong, if anything?*
We are looking at the chrom_start for the features. This would ot change if the features wasn't SNPs. 
All features with start within a certain region was extracted, and this would still be possible even if the features wasn't SNPs. 
If we want the entire feature to be within the range given by the query file we would have to change the extract_features to include the end-position. 

If the features wasn't SNPs we would also have to account for how we wanted them sorted if several features has the same start but different lengths. 
The obvius would be to sort them with the shortest/them with the lowest chrom_end first. But we would have to include this in the code. 
And the same thing for merging. 

*We wrote a tool for merging two BED files, but what if we had a bunch of them? What would the complexity be if we merged them in, one at a time? What would the complexity be if we merged all of the files at the same time?*

The complexity of the merge we have made is O(n+m), where n and m are the lenghts of the two files we need to merge. This is because we need to go through each feature individually and copy it to a new merged list. 
If we were to merge more than two files one by one, it would just be O(n+m+o+p....) where the letters are the lenghts of the files for however many files we want to merge. 
If we merge lists with lengths n, m and o would the complexity be O(n+m) for the merge of the two first list and O(n+m+o), which boils down to O(n+m+o) (linear time)
If we merged three lists at one it would still happen in linear time O(n+m+o). 
Even tough the complexity is the same for both methods every element of the first two lists will be copied twice with the first method and only once for the second method. 
The number of comparisons on the other hand will be higher for the second method.
