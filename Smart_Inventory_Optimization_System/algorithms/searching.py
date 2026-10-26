from time import perf_counter


def linear_search(items, target, key="sku"):
    """Return (matching item or None, elapsed seconds, comparisons)."""
    checks = 0
    start = perf_counter()
    result = None
    for item in items:
        checks += 1
        if str(item[key]).casefold() == str(target).casefold():
            result = item
            break
    elapsed = perf_counter() - start
    return result, elapsed, checks


def binary_search(items, target, key="sku"):
    """Binary search on items already sorted by key. Returns result, seconds, comparisons."""
    lo, hi = 0, len(items) - 1
    checks = 0
    target_value = str(target).casefold()
    start = perf_counter()
    result = None
    while lo <= hi:
        mid = (lo + hi) // 2
        checks += 1
        value = str(items[mid][key]).casefold()
        if value == target_value:
            result = items[mid]
            break
        if value < target_value:
            lo = mid + 1
        else:
            hi = mid - 1
    elapsed = perf_counter() - start
    return result, elapsed, checks
