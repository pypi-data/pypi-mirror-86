# ParAlg

## Requirements

Python 3.7+

## Install

```bash
$ pip install paralg
```

## Examples

### Sorting algorithms

```py
from random import random
from paralg.sorting import MergeSorting

array = [random() for _ in range(1000)]

assert MergeSorting(ascending=True).sort(array, cpu_count=2) == sorted(array)
assert MergeSorting(ascending=False).sort(array, cpu_count=2) == sorted(array, reverse=True)
```
