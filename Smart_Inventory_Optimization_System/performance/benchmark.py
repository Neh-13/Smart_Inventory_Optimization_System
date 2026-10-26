import random
from time import perf_counter
from algorithms.searching import linear_search, binary_search
from algorithms.sorting import merge_sort, quick_sort


def run_benchmarks(sizes):
    rng = random.Random(20261025)  # reproducible dataset values
    results = []
    for n in sizes:
        data = [{"sku": f"SKU-{i:07d}", "quantity": rng.randint(0, 100000),
                 "daily_demand": rng.randint(0, 1000)} for i in range(n)]
        target = f"SKU-{n - 1:07d}"

        _, linear_time, linear_checks = linear_search(data, target)
        sorted_data, prep_time = merge_sort(data, key=lambda p: p["sku"].casefold(), measure=True)
        _, binary_time, binary_checks = binary_search(sorted_data, target)

        quantities = [p["quantity"] for p in data]
        _, merge_time = merge_sort(quantities, measure=True)
        _, quick_time = quick_sort(quantities, measure=True)
        results.append({
            "size": n,
            "linear_ms": round(linear_time * 1000, 4),
            "linear_checks": linear_checks,
            "binary_ms": round(binary_time * 1000, 4),
            "binary_checks": binary_checks,
            "sort_prep_ms": round(prep_time * 1000, 4),
            "merge_ms": round(merge_time * 1000, 4),
            "quick_ms": round(quick_time * 1000, 4),
        })
    return results
