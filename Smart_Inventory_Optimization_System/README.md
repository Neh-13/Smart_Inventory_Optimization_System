# Smart Inventory Optimization System

A 5th-semester Design and Analysis of Algorithms (DAA) mini project. This is an educational Flask web app with SQLite persistence, custom searching/sorting implementations, inventory reorder estimates, a greedy budget heuristic, and benchmark measurements.

## Features
- Dashboard with inventory value, low-stock counts, and category chart
- Product create, read, update, delete, and filtering
- Linear Search vs Binary Search comparison by SKU
- Merge Sort vs Quick Sort comparison
- Simplified reorder recommendations
- Greedy heuristic for choosing whole reorder orders within a budget
- Benchmark page for custom algorithm implementations with CSV export
- SQLite database and demo records on first run

## Requirements
- Python 3.10 or newer
- Flask (installed from `requirements.txt`)
- A modern browser

## Run locally
1. Extract the ZIP file.
2. Open a terminal in the project folder.
3. Create and activate a virtual environment (recommended).
   - macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate`
   - Windows: `py -m venv .venv` then `.venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the app: `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.

The SQLite file `inventory.db` is created automatically. Demo products are inserted only when the database is empty.

## DAA algorithm notes
- Linear Search: scans records sequentially; best O(1), average/worst O(n), O(1) auxiliary space.
- Binary Search: requires records sorted by SKU; best O(1), average/worst O(log n), O(1) auxiliary space for iterative implementation. The comparison endpoint sorts a copy before searching and explicitly excludes that preprocessing time from the search-operation timing.
- Merge Sort: divide-and-conquer; O(n log n) time in best/average/worst cases and O(n) auxiliary space.
- Quick Sort: median-of-three pivot and three-way partition. Expected/average O(n log n); theoretical worst O(n²). This implementation builds partition lists, so auxiliary space can reach O(n) per level and recursion depth depends on partition balance.
- Greedy budget selection: ranks needed reorder purchases by estimated daily-demand value per rupee, then takes a whole order if it fits the remaining budget. This is a heuristic and does not guarantee an optimal 0/1 knapsack result.
- Reorder policy: a product is considered for reorder when `quantity <= reorder_level`. Target stock is `max(reorder_level, round(2 * daily_demand * lead_time))`; reorder quantity is `max(0, target_stock - quantity)`. This is a simplified educational rule, not professional inventory advice.

## Benchmark methodology
The benchmark uses deterministic synthetic SKU and numeric data for reproducibility, but measured times depend on hardware, Python version, background processes, and dataset sizes. Linear search targets the last SKU to demonstrate a worst-case position. Binary-search preprocessing is reported separately. The web interface focuses on Dashboard, Products, Algorithm Studio, and Optimization. Search can compare product names or SKU codes; sorting can use product name, SKU, stock, daily demand, or price.

## Suggested report chapters
1. Abstract
2. Problem statement, objectives, inputs/outputs/constraints
3. Background study and algorithm selection
4. System design and architecture
5. Algorithm pseudocode and complexity analysis
6. Implementation details
7. Test cases and sample outputs
8. Benchmark setup, measured results, and discussion
9. Limitations and future scope
10. References

## Security / production note
This is a local educational prototype. Before deployment, configure a strong secret key, turn off Flask debug mode, add authentication/authorization and CSRF protection, validate inputs more strictly, and use a production WSGI server.


## Burger Mania menu starter data

The starter inventory list now uses Burger Mania menu names found on its public menu. The linked myBillBook store page did not expose its full product/price list to the browser retrieval used for this update, so please verify the list against your store. Prices, stock quantities, and daily demand are intentionally initialized to zero rather than inventing business figures. Edit these values in the Products page.

**To replace the old demo inventory:** stop the Flask server, delete `inventory.db` from this project folder, and start `python app.py` again. The app will create a fresh database and seed the menu items. This permanently removes the old local inventory database, so back it up first if you need its data.
