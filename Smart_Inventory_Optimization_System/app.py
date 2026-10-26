import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import init_db, get_db, seed_demo_data
from algorithms.searching import linear_search, binary_search
from algorithms.sorting import merge_sort, quick_sort
from algorithms.optimization import calculate_reorder, greedy_budget_selection

app = Flask(__name__)
app.secret_key = "change-this-secret-key-for-deployment"

init_db()
if not get_db().execute("SELECT COUNT(*) FROM products").fetchone()[0]:
    seed_demo_data()


def product_dict(row):
    return dict(row)


def all_products():
    return [product_dict(r) for r in get_db().execute(
        "SELECT * FROM products ORDER BY id DESC"
    ).fetchall()]


@app.route("/")
def dashboard():
    db = get_db()
    products = [dict(r) for r in db.execute("SELECT * FROM products ORDER BY name").fetchall()]
    total_products = len(products)
    inventory_value = sum(p["quantity"] * p["price"] for p in products)
    low_stock = [p for p in products if p["quantity"] <= p["reorder_level"]]
    total_units = sum(p["quantity"] for p in products)
    recent = [dict(r) for r in db.execute("SELECT * FROM products ORDER BY id DESC LIMIT 6").fetchall()]
    category_totals = {}
    for p in products:
        category_totals[p["category"]] = category_totals.get(p["category"], 0) + p["quantity"] * p["price"]
    return render_template("dashboard.html", total_products=total_products,
        inventory_value=inventory_value, low_stock_count=len(low_stock),
        total_units=total_units, low_stock=low_stock[:6], recent=recent,
        category_labels=json.dumps(list(category_totals.keys())),
        category_values=json.dumps([round(v, 2) for v in category_totals.values()]))


@app.route("/products", methods=["GET", "POST"])
def products_page():
    db = get_db()
    if request.method == "POST":
        try:
            sku = request.form["sku"].strip()
            name = request.form["name"].strip()
            category = request.form.get("category", "General").strip() or "General"
            quantity = int(request.form["quantity"])
            price = float(request.form["price"])
            daily_demand = float(request.form["daily_demand"])
            lead_time = int(request.form["lead_time"])
            reorder_level = int(request.form["reorder_level"])
            if not sku or not name or min(quantity, price, daily_demand, lead_time, reorder_level) < 0:
                raise ValueError("Please provide valid non-negative values.")
            db.execute("""INSERT INTO products
                (sku, name, category, quantity, price, daily_demand, lead_time, reorder_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (sku, name, category, quantity, price, daily_demand, lead_time, reorder_level))
            db.commit()
            flash("Product added successfully.", "success")
        except Exception as e:
            db.rollback()
            flash("Could not add product. Check the values and ensure the SKU is unique. " + str(e), "error")
        return redirect(url_for("products_page"))

    search = request.args.get("q", "").strip()
    if search:
        rows = db.execute("""SELECT * FROM products WHERE name LIKE ? OR sku LIKE ? OR category LIKE ?
            ORDER BY name""", (f"%{search}%", f"%{search}%", f"%{search}%")).fetchall()
    else:
        rows = db.execute("SELECT * FROM products ORDER BY name").fetchall()
    return render_template("products.html", products=[dict(r) for r in rows], query=search)


@app.route("/products/<int:product_id>/edit", methods=["POST"])
def edit_product(product_id):
    db = get_db()
    try:
        db.execute("""UPDATE products SET sku=?, name=?, category=?, quantity=?, price=?,
            daily_demand=?, lead_time=?, reorder_level=? WHERE id=?""",
            (request.form["sku"].strip(), request.form["name"].strip(),
             request.form.get("category", "General").strip() or "General",
             int(request.form["quantity"]), float(request.form["price"]),
             float(request.form["daily_demand"]), int(request.form["lead_time"]),
             int(request.form["reorder_level"]), product_id))
        db.commit()
        flash("Product updated.", "success")
    except Exception as e:
        db.rollback()
        flash("Update failed. Check the fields and ensure the SKU is unique. " + str(e), "error")
    return redirect(url_for("products_page"))


@app.route("/products/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    db = get_db()
    db.execute("DELETE FROM products WHERE id=?", (product_id,))
    db.commit()
    flash("Product deleted.", "success")
    return redirect(url_for("products_page"))


@app.route("/algorithms")
def algorithms_page():
    return render_template("algorithms.html")


@app.route("/api/search-compare", methods=["POST"])
def search_compare():
    payload = request.get_json(force=True)
    target = payload.get("target", "").strip()
    search_field = payload.get("field", "sku")
    if search_field not in {"sku", "name"}:
        search_field = "sku"
    products = [dict(r) for r in get_db().execute("SELECT * FROM products").fetchall()]
    # Binary search receives a copy sorted by the exact selected field.
    linear_result, linear_time, linear_checks = linear_search(products, target, key=search_field)
    sorted_products = merge_sort(products, key=lambda p: str(p[search_field]).casefold())
    binary_result, binary_time, binary_checks = binary_search(sorted_products, target, key=search_field)
    return jsonify({
        "target": target,
        "field": search_field,
        "linear": {"found": linear_result, "time_ms": round(linear_time * 1000, 6),
                   "comparisons": linear_checks, "complexity": "Best O(1), average/worst O(n)"},
        "binary": {"found": binary_result, "time_ms": round(binary_time * 1000, 6),
                   "comparisons": binary_checks, "complexity": "Best O(1), average/worst O(log n)"},
        "note": "Binary search uses a sorted copy. The displayed search time excludes sorting/preprocessing time; this keeps search-operation times separate."
    })


@app.route("/api/sort-compare", methods=["POST"])
def sort_compare():
    payload = request.get_json(force=True)
    field = payload.get("field", "quantity")
    allowed = {"quantity", "daily_demand", "price", "name", "sku"}
    if field not in allowed:
        field = "quantity"
    products = [dict(r) for r in get_db().execute("SELECT * FROM products").fetchall()]
    key = (lambda p: str(p[field]).lower()) if field == "name" else (lambda p: p[field])
    merge_result, merge_time = merge_sort(products, key=key, measure=True)
    quick_result, quick_time = quick_sort(products, key=key, measure=True)
    return jsonify({
        "field": field,
        "merge": {"time_ms": round(merge_time * 1000, 6), "complexity": "O(n log n)", "items": merge_result},
        "quick": {"time_ms": round(quick_time * 1000, 6), "complexity": "Average O(n log n), worst O(n²)", "items": quick_result},
        "count": len(products)
    })


@app.route("/optimization", methods=["GET", "POST"])
def optimization_page():
    products = [dict(r) for r in get_db().execute("SELECT * FROM products ORDER BY name").fetchall()]
    budget = None
    selected = []
    total_cost = 0.0
    if request.method == "POST":
        try:
            budget = float(request.form["budget"])
            if budget < 0:
                raise ValueError()
            candidates = []
            for p in products:
                reorder = calculate_reorder(p["quantity"], p["daily_demand"], p["lead_time"], p["reorder_level"])
                p["reorder_quantity"] = reorder["reorder_quantity"]
                p["target_stock"] = reorder["target_stock"]
                p["estimated_cost"] = round(reorder["reorder_quantity"] * p["price"], 2)
                p["days_of_stock"] = reorder["days_of_stock"]
                if reorder["reorder_quantity"] > 0:
                    candidates.append(p)
            selected = greedy_budget_selection(candidates, budget)
            total_cost = round(sum(p["estimated_cost"] for p in selected), 2)
            products = sorted(products, key=lambda p: (p["quantity"] > p["reorder_level"], p["name"]))
            for p in products:
                if "reorder_quantity" not in p:
                    r = calculate_reorder(p["quantity"], p["daily_demand"], p["lead_time"], p["reorder_level"])
                    p.update(r)
                    p["estimated_cost"] = round(r["reorder_quantity"] * p["price"], 2)
        except (ValueError, TypeError):
            flash("Enter a valid non-negative budget.", "error")
    else:
        for p in products:
            r = calculate_reorder(p["quantity"], p["daily_demand"], p["lead_time"], p["reorder_level"])
            p.update(r)
            p["estimated_cost"] = round(r["reorder_quantity"] * p["price"], 2)
    return render_template("optimization.html", products=products, budget=budget,
                           selected_ids={p["id"] for p in selected}, selected=selected, total_cost=total_cost)


@app.route("/api/products")
def products_api():
    return jsonify(all_products())


if __name__ == "__main__":
    app.run(debug=True)
