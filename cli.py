import argparse
from app.tracker import ExpenseTracker
from app.storage import StorageService
from datetime import date

# Initialize storage and tracker
storage = StorageService("data/expenses.json")
tracker = ExpenseTracker(storage)


def add_expense(args):
    """Handle the 'add' command to add a new expense."""
    result = tracker.add_expense(args.description, args.amount, args.category)
    if result["success"]:
        print(f"✅ Expense added successfully (ID: {result['id']})")
    else:
        print("❌ Failed to add expense.")
        print("Errors:", result["errors"])


def list_expenses(args):
    """Handle the 'list' command to list expenses."""
    if args.category:
        tracker.list_expenses(args.category)
    else:
        tracker.list_expenses()


def delete_expense(args):
    """Handle the 'delete' command to remove an expense."""
    result = tracker.delete_expense(args.id)
    print(result["message"])


def summary(args):
    """Handle the 'summary' command to show total expenses."""
    if args.month:
        total = tracker.get_expenses_summary(month=int(args.month))
        print(f"📆 Total expenses for month {args.month}: ${total}")
    else:
        total = tracker.get_expenses_summary()
        print(f"💰 Total expenses: ${total}")


def set_budget(args):
    """Handle the 'budget' command to set a monthly budget."""
    result = tracker.set_monthly_budget(args.month, args.amount)
    if result[0]:
        print(result[1])
    else:
        print("❌", result[1])


def export_expenses(args):
    """Handle the 'export' command to export expenses to a CSV file."""
    tracker.export_to_csv(args.filename if args.filename else "data/expenses_export.csv")


# Set up CLI parser
parser = argparse.ArgumentParser(description="🧾 Expense Tracker CLI")
subparsers = parser.add_subparsers(help="Available commands")

# Add Expense
add_parser = subparsers.add_parser("add", help="Add a new expense")
add_parser.add_argument("--description", required=True, help="Description of the expense")
add_parser.add_argument("--amount", required=True, type=float, help="Amount spent")
add_parser.add_argument("--category", help="Category of the expense")
add_parser.set_defaults(func=add_expense)

# List Expenses
list_parser = subparsers.add_parser("list", help="List all expenses")
list_parser.add_argument("--category", help="Filter by category")
list_parser.set_defaults(func=list_expenses)

# Delete Expense
delete_parser = subparsers.add_parser("delete", help="Delete an expense")
delete_parser.add_argument("--id", required=True, type=int, help="Expense ID to delete")
delete_parser.set_defaults(func=delete_expense)

# Summary
summary_parser = subparsers.add_parser("summary", help="Show total expenses summary")
summary_parser.add_argument("--month", type=int, help="Optional month to filter")
summary_parser.set_defaults(func=summary)

# Set Budget
budget_parser = subparsers.add_parser("budget", help="Set monthly budget")
budget_parser.add_argument("--month", required=True, help="Month number (1-12)")
budget_parser.add_argument("--amount", required=True, type=float, help="Budget amount")
budget_parser.set_defaults(func=set_budget)

# Export as CSV
parser_export = subparsers.add_parser("export", help="Export expenses to CSV")
parser_export.add_argument("--filename", help="Filename to export to (default: data/expenses_export.csv)")
parser_export.set_defaults(func=export_expenses)

# Parse and run the appropriate command
args = parser.parse_args()
if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()
