import json
from pathlib import Path

# ============================
# DATA PERSISTENCE FUNCTIONS
# ============================

# Define paths
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

inventory_file = data_dir / "inventory.json"
customers_file = data_dir / "customers.json"
orders_file = data_dir / "orders.json"
order_items_file = data_dir / "order_items.json"

# Save helper
def save_data(data, file_path):
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved to {file_path}")
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")

# Load helper
def load_data(file_path, default):
    try:
        if file_path.exists():
            with open(file_path, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading from {file_path}: {e}")
    return default

# Save all data
def save_all(inventory_movements, customers, orders, order_items):
    save_data(inventory_movements, inventory_file)
    save_data(customers, customers_file)
    save_data(orders, orders_file)
    save_data(order_items, order_items_file)

# Load all data
def load_all():
    inventory_movements = load_data(inventory_file, [])
    customers = load_data(customers_file, {})
    orders = load_data(orders_file, [])
    order_items = load_data(order_items_file, [])
    return inventory_movements, customers, orders, order_items

def export_summary(customers, orders, inventory_movements, filename="summary_report.json"):
    try:
        summary = {
            "inventory_count": len(inventory_movements),
            "customer_ids": list(customers.keys()),
            "order_count": len(orders),
            "total_revenue_cents": sum(o["total_cents"] for o in orders)
        }
        with open(data_dir / filename, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"Exported summary to {filename}")
    except Exception as e:
        print(f"Error exporting report: {e}")
