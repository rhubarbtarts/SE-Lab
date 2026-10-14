"""Pharmacy stock, billing, and dispensing management."""

import ast
import hashlib
import json
import math
import operator
import secrets
from datetime import date, datetime
from pathlib import Path

# Global pharmacy state
medicines = {}


def add_medicine(name, qty=0, price=0.0, expiry="2099-12-31", audit=None):
    """Add medicine stock and record the stock update."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Medicine name must be a non-empty string.")
    if not isinstance(qty, int) or isinstance(qty, bool):
        raise ValueError("Quantity must be an integer.")
    if qty < 0:
        raise ValueError("Quantity cannot be negative.")
    if not isinstance(price, (int, float)) or isinstance(price, bool):
        raise ValueError("Price must be a number.")
    if not math.isfinite(price) or price < 0:
        raise ValueError("Price must be finite and non-negative.")

    datetime.strptime(expiry, "%Y-%m-%d")
    name = name.strip()

    if name not in medicines:
        medicines[name] = {"qty": 0, "price": price, "expiry": expiry}

    medicines[name]["qty"] += qty
    if audit is not None:
        audit.append(
            f"{datetime.now()}: Stocked {qty} units of {name}"
        )
        return audit

    return [f"{datetime.now()}: Stocked {qty} units of {name}"]


def dispense_medicine(name, qty):
    """Dispense medicine only when sufficient stock is available."""
    if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
        raise ValueError("Dispensing quantity must be a positive integer.")
    if name not in medicines:
        raise ValueError(f"Medicine not found: {name}")
    if medicines[name]["qty"] < qty:
        raise ValueError("Insufficient stock.")

    medicines[name]["qty"] -= qty


def get_quantity(name):
    """Return the available quantity of a medicine."""
    if name not in medicines:
        raise ValueError(f"Medicine not found: {name}")
    return medicines[name]["qty"]


def is_expired(name):
    """Return whether a medicine has passed its expiry date."""
    if name not in medicines:
        raise ValueError(f"Medicine not found: {name}")

    expiry_date = datetime.strptime(
        medicines[name]["expiry"], "%Y-%m-%d"
    ).date()
    return expiry_date < date.today()


def bill_amount(prescription):
    """Calculate the total cost of a prescription."""
    total = 0.0

    for name, quantity in prescription:
        if name not in medicines:
            raise ValueError(f"Medicine not found: {name}")
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Prescription quantities must be integers.")
        if quantity <= 0:
            raise ValueError("Prescription quantities must be positive.")

        total += medicines[name]["price"] * quantity

    return total


def calculate_dosage(formula):
    """Evaluate basic arithmetic without executing arbitrary Python code."""
    if not isinstance(formula, str) or not formula.strip():
        raise ValueError("Dosage formula must be a non-empty string.")

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if (
            isinstance(node, ast.Constant)
            and type(node.value) in (int, float)
        ):
            return node.value

        if isinstance(node, ast.UnaryOp) and type(node.op) in (
            ast.UAdd, ast.USub
        ):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value

        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(
                node.op, (ast.Div, ast.FloorDiv, ast.Mod)
            ) and right == 0:
                raise ValueError("Division by zero is not allowed.")

            return allowed_operators[type(node.op)](left, right)

        raise ValueError("Invalid dosage formula.")

    try:
        tree = ast.parse(formula, mode="eval")
        result = evaluate(tree)

        if (
            not isinstance(result, (int, float))
            or not math.isfinite(result)
        ):
            raise ValueError("Dosage result must be a finite number.")

        return result
    except (SyntaxError, TypeError, OverflowError, ZeroDivisionError) as error:
        raise ValueError("Invalid dosage formula.") from error


def patient_id(name, phone):
    """Generate a deterministic patient identifier."""
    value = f"{name}{phone}".encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def generate_rx_number():
    """Generate an unpredictable prescription reference."""
    return f"RX-{secrets.randbelow(900000) + 100000}"


def save_stock(file="pharmacy.json"):
    """Save pharmacy stock in JSON format."""
    path = Path(file)
    with path.open("w", encoding="utf-8") as stock_file:
        json.dump(medicines, stock_file, indent=2)


def load_stock(file="pharmacy.json"):
    """Load and validate pharmacy stock from JSON."""

    path = Path(file)
    with path.open("r", encoding="utf-8") as stock_file:
        loaded_medicines = json.load(stock_file)

    if not isinstance(loaded_medicines, dict):
        raise ValueError("Stock data must be a JSON object.")

    for name, item in loaded_medicines.items():
        if not isinstance(name, str) or not isinstance(item, dict):
            raise ValueError("Invalid medicine record.")
        if not {"qty", "price", "expiry"}.issubset(item):
            raise ValueError(f"Incomplete medicine record: {name}")
        if (
            not isinstance(item["qty"], int)
            or isinstance(item["qty"], bool)
            or item["qty"] < 0
        ):
            raise ValueError(f"Invalid quantity for {name}")
        if (
            not isinstance(item["price"], (int, float))
            or isinstance(item["price"], bool)
            or not math.isfinite(item["price"])
            or item["price"] < 0
        ):
            raise ValueError(f"Invalid price for {name}")
        datetime.strptime(item["expiry"], "%Y-%m-%d")

    medicines.clear()
    medicines.update(loaded_medicines)


def print_label(name):
    """Print a dispensing label without invoking a shell."""
    print(f"Dispensing label: {name}")


def expiring_soon(days=30):
    """Return medicines expiring within the specified number of days."""
    if not isinstance(days, int) or isinstance(days, bool) or days < 0:
        raise ValueError("Days must be a non-negative integer.")

    result = []
    today = date.today()

    for name, medicine in medicines.items():
        expiry_date = datetime.strptime(
            medicine["expiry"], "%Y-%m-%d"
        ).date()
        days_remaining = (expiry_date - today).days

        if 0 <= days_remaining <= days:
            result.append(name)

    return result


def pharmacist_login(password):
    """Check a password against the configured demo credential."""
    configured_password = __import__("os").environ.get(
        "PHARMACIST_PASSWORD"
    )
    if not configured_password:
        return False
    return secrets.compare_digest(password, configured_password)


def print_stock():
    """Print a report of all available medicine stock."""
    print("===== Pharmacy Stock Report =====")

    for name, medicine in medicines.items():
        print(
            f"{name} -> {medicine['qty']} units, "
            f"Rs. {medicine['price']} exp {medicine['expiry']}"
        )


def main():
    """Run the pharmacy management demonstration."""
    medicines.clear()

    add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15")
    add_medicine("Cetirizine 10mg", 10, 2.0, "2027-03-31")

    dispense_medicine("Paracetamol 500mg", 30)

    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))
    print(
        "Bill:",
        bill_amount([
            ("Paracetamol 500mg", 10),
            ("Amoxicillin 250mg", 5),
        ]),
    )
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    print(
        "Login:",
        pharmacist_login(
            __import__("os").environ.get("PHARMACIST_PASSWORD", "")
        ),
    )
    print_label("Paracetamol 500mg")

    save_stock()
    load_stock()
    print_stock()


if __name__ == "__main__":
    main()
