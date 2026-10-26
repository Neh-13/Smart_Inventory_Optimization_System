import unittest
from algorithms.searching import linear_search, binary_search
from algorithms.sorting import merge_sort, quick_sort
from algorithms.optimization import calculate_reorder, greedy_budget_selection


class AlgorithmTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            {"sku": "SKU-03", "quantity": 5},
            {"sku": "SKU-01", "quantity": 9},
            {"sku": "SKU-02", "quantity": 1},
        ]

    def test_linear_search_found_and_missing(self):
        self.assertEqual(linear_search(self.items, "SKU-01")[0]["quantity"], 9)
        self.assertIsNone(linear_search(self.items, "missing")[0])

    def test_binary_search_sorted(self):
        sorted_items = merge_sort(self.items, key=lambda p: p["sku"].casefold())
        self.assertEqual(binary_search(sorted_items, "SKU-02")[0]["quantity"], 1)
        self.assertIsNone(binary_search(sorted_items, "missing")[0])

    def test_sorting(self):
        self.assertEqual([x["sku"] for x in merge_sort(self.items, key=lambda p: p["sku"])],
                         ["SKU-01", "SKU-02", "SKU-03"])
        self.assertEqual([x["quantity"] for x in quick_sort(self.items, key=lambda p: p["quantity"])],
                         [1, 5, 9])

    def test_reorder(self):
        result = calculate_reorder(3, 2, 5, 5)
        self.assertEqual(result["reorder_quantity"], 17)

    def test_greedy_budget(self):
        candidates = [
            {"name": "A", "daily_demand": 10, "price": 5, "estimated_cost": 20},
            {"name": "B", "daily_demand": 3, "price": 4, "estimated_cost": 12},
        ]
        selected = greedy_budget_selection(candidates, 20)
        self.assertEqual(sum(p["estimated_cost"] for p in selected), 20)


if __name__ == "__main__":
    unittest.main()
