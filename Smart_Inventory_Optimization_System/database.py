import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("inventory.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'General',
            quantity INTEGER NOT NULL CHECK(quantity >= 0),
            price REAL NOT NULL CHECK(price >= 0),
            daily_demand REAL NOT NULL DEFAULT 0 CHECK(daily_demand >= 0),
            lead_time INTEGER NOT NULL DEFAULT 1 CHECK(lead_time >= 0),
            reorder_level INTEGER NOT NULL DEFAULT 0 CHECK(reorder_level >= 0)
        )""")
        db.commit()


def seed_demo_data():
    """Load Burger Mania menu items as starter inventory records.

    Stock, price, demand, and lead time are placeholders and should be edited
    in the website to match the outlet's actual inventory and purchase costs.
    """
    menu = [
        # Burgers
        ("BUR-001", "Aloo Tikki Burger", "Burgers"),
        ("BUR-002", "Peri Peri Burger", "Burgers"),
        ("BUR-003", "Schezwan Burger", "Burgers"),
        ("BUR-004", "Chilli Garlic Burger", "Burgers"),
        ("BUR-005", "Chipotle Burger", "Burgers"),
        ("BUR-006", "Cheese Jalapeno Burger", "Burgers"),
        ("BUR-007", "Indian Masala Burger", "Burgers"),
        ("BUR-008", "Italian Burger", "Burgers"),
        ("BUR-009", "BBQ Burger", "Burgers"),
        ("BUR-010", "Mexican Burger", "Burgers"),
        ("BUR-011", "Tandoori Burger", "Burgers"),
        ("BUR-012", "Onion Splash Burger", "Burgers"),
        ("BUR-013", "Tomato Splash Burger", "Burgers"),
        ("BUR-014", "Hot n Spicy Burger", "Burgers"),
        ("BUR-015", "Mumbaiya Burger", "Burgers"),
        ("BUR-016", "Makhani Burger", "Burgers"),
        # Sandwiches
        ("SAN-001", "Mumbai Masala Sandwich", "Sandwiches"),
        ("SAN-002", "Veg Cheese Mayo Sandwich", "Sandwiches"),
        ("SAN-003", "Cheese Schezwan Sandwich", "Sandwiches"),
        ("SAN-004", "Ahmedabadi Touch Sandwich", "Sandwiches"),
        ("SAN-005", "Ghughra Sandwich", "Sandwiches"),
        ("SAN-006", "Mexican Sandwich", "Sandwiches"),
        ("SAN-007", "Jungli Sandwich", "Sandwiches"),
        ("SAN-008", "Cheese Grilled Sandwich", "Sandwiches"),
        ("SAN-009", "Cheese Chutney Sandwich", "Sandwiches"),
        ("SAN-010", "Cheese Chocolate Sandwich", "Sandwiches"),
        ("SAN-011", "Cheese Pineapple Jam Sandwich", "Sandwiches"),
        ("SAN-012", "Cheese Mix Fruit Jam Sandwich", "Sandwiches"),
        ("SAN-013", "Cheese Chilly Corn Sandwich", "Sandwiches"),
        # Fries
        ("FRI-001", "Classic Fries", "French Fries"),
        ("FRI-002", "Masala Fries", "French Fries"),
        ("FRI-003", "Mayo Fries", "French Fries"),
        ("FRI-004", "Peri Peri Fries", "French Fries"),
        # Mocktails
        ("MOC-001", "Mint Mocktail", "Mocktails"),
        ("MOC-002", "Green Apple Mocktail", "Mocktails"),
        ("MOC-003", "Blue Berry Mocktail", "Mocktails"),
        ("MOC-004", "Strawberry Mocktail", "Mocktails"),
        ("MOC-005", "Passion Fruit Mocktail", "Mocktails"),
        ("MOC-006", "Blue Ocean Mocktail", "Mocktails"),
        ("MOC-007", "Bubble Gum Mocktail", "Mocktails"),
        ("MOC-008", "Kiwi Mocktail", "Mocktails"),
        ("MOC-009", "Watermelon Mocktail", "Mocktails"),
        # Coffee and other drinks
        ("COF-001", "Classic Cold Coffee", "Cold Coffee"),
        ("COF-002", "Hazelnut Cold Coffee", "Cold Coffee"),
        ("COF-003", "Caramel Cold Coffee", "Cold Coffee"),
        ("COC-001", "Cold Coco", "Cold Coco"),
        # Other menu categories
        ("WRP-001", "Chilli Garlic Wrap", "Wraps"),
        ("WRP-002", "Veg Delight Wrap", "Wraps"),
        ("WRP-003", "Spicy Schezwan Wrap", "Wraps"),
        ("NAC-001", "Masala Nachos", "Masala Nachos"),
        ("CGP-001", "Chilly Garlic Pockets (12 pc)", "Chilly Garlic Pockets"),
    ]
    # DEMO VALUES: estimated sample figures for the student project, not actual
    # Burger Mania business records. Replace them with the outlet's real values.
    # Unit price is treated as estimated unit inventory cost by reorder reports.
    category_defaults = {
        "Burgers": (35, 12.0, 18.0, 2),
        "Sandwiches": (24, 10.0, 14.0, 2),
        "French Fries": (30, 8.0, 12.0, 2),
        "Mocktails": (28, 9.0, 12.0, 2),
        "Cold Coffee": (22, 11.0, 10.0, 2),
        "Cold Coco": (20, 8.0, 8.0, 2),
        "Wraps": (18, 9.0, 10.0, 2),
        "Masala Nachos": (15, 5.0, 6.0, 2),
        "Chilly Garlic Pockets": (16, 4.0, 6.0, 2),
    }
    rows = []
    for sku, name, category in menu:
        stock, demand, unit_cost, lead_days = category_defaults.get(category, (15, 5.0, 10.0, 2))
        # Small deterministic variations make the demo dashboard more realistic.
        offset = sum(ord(ch) for ch in sku) % 9
        quantity = max(0, stock + offset - 4)
        daily_demand = max(1.0, demand + ((offset % 5) - 2))
        reorder_level = int(daily_demand * lead_days + 5)  # includes sample safety stock
        price = round(unit_cost + (offset % 4) * 1.5, 2)
        rows.append((sku, name, category, quantity, price, daily_demand, lead_days, reorder_level))
    with get_db() as db:
        db.executemany("""INSERT OR IGNORE INTO products
            (sku, name, category, quantity, price, daily_demand, lead_time, reorder_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", rows)
        db.commit()
