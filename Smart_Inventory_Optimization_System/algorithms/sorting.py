from time import perf_counter


def merge_sort(items, key=lambda x: x, measure=False):
    """Stable merge sort. Returns a sorted copy; optionally returns elapsed seconds too."""
    start = perf_counter()
    values = list(items)

    def sort(seq):
        if len(seq) <= 1:
            return seq
        middle = len(seq) // 2
        left = sort(seq[:middle])
        right = sort(seq[middle:])
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    result = sort(values)
    elapsed = perf_counter() - start
    return (result, elapsed) if measure else result


def quick_sort(items, key=lambda x: x, measure=False):
    """Quick sort using a median-of-three pivot and three-way partition."""
    start = perf_counter()
    values = list(items)

    def sort(seq):
        if len(seq) <= 1:
            return seq
        first, middle, last = seq[0], seq[len(seq) // 2], seq[-1]
        pivot = sorted((key(first), key(middle), key(last)))[1]
        lower, equal, upper = [], [], []
        for item in seq:
            value = key(item)
            if value < pivot:
                lower.append(item)
            elif value > pivot:
                upper.append(item)
            else:
                equal.append(item)
        return sort(lower) + equal + sort(upper)

    result = sort(values)
    elapsed = perf_counter() - start
    return (result, elapsed) if measure else result
