def calculate_reorder(quantity, daily_demand, lead_time, reorder_level):
    """
    Educational reorder policy:
    target stock = max(reorder level, estimated demand during lead time + one lead-time buffer)
    If stock is at/below reorder level, recommend enough to reach target stock.
    This is a simplified policy, not a forecast or guaranteed optimal business decision.
    """
    demand_during_lead_time = daily_demand * lead_time
    target_stock = max(int(reorder_level), int(round(demand_during_lead_time + daily_demand * lead_time)))
    reorder_quantity = max(0, target_stock - quantity) if quantity <= reorder_level else 0
    days_of_stock = round(quantity / daily_demand, 1) if daily_demand > 0 else None
    return {
        "target_stock": target_stock,
        "reorder_quantity": int(reorder_quantity),
        "days_of_stock": days_of_stock,
        "demand_during_lead_time": round(demand_during_lead_time, 2),
    }


def greedy_budget_selection(candidates, budget):
    """
    Greedy heuristic: rank needed products by daily-demand value per rupee,
    then take each whole reorder if it fits the remaining budget.
    It is a heuristic and does not guarantee a globally optimal knapsack solution.
    """
    ranked = sorted(
        candidates,
        key=lambda p: (
            -((p["daily_demand"] * p["price"]) / p["estimated_cost"])
            if p["estimated_cost"] > 0 else float("-inf"),
            p["estimated_cost"],
            p["name"].casefold()
        )
    )
    selected = []
    remaining = float(budget)
    for product in ranked:
        cost = float(product["estimated_cost"])
        if cost > 0 and cost <= remaining:
            selected.append(product)
            remaining -= cost
    return selected
