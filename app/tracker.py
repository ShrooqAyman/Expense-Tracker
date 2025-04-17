from datetime import date, datetime
from prettytable import PrettyTable
from app.validator import ValidationResult
from models.Expense import Expense
from models.budget_service import BudgetService
import csv
import os


class ExpenseTracker:
    """
    A class to track, manage, and export expenses with support for budget tracking.
    """

    def __init__(self, storage_service):
        """
        Initialize the ExpenseTracker with storage and budget services.

        :param storage_service: An object responsible for saving/loading expenses.
        """
        self.storage = storage_service
        self.budget_service = BudgetService()
        self.expenses = self.storage.load_expenses()

    def get_next_id(self):
        """
        Generate the next unique ID for a new expense.

        return: Integer representing the next ID.
        """
        if not self.expenses:
            return 1
        existing_ids = [int(expense["id"]) for expense in self.expenses]
        return max(existing_ids) + 1

    def validate_expense_id(self, expense_id, expenses):
        """
        Check whether a given expense ID exists.

        param expense_id: ID to validate.
        param expenses: List of existing expenses.
        return: ValidationResult object.
        """
        result = ValidationResult()
        if not any(str(exp["id"]) == str(expense_id) for exp in expenses):
            result.add_error(f"Expense with ID {expense_id} not found.")
        return result

    def validate_expense_data(self, description, amount, category=None):
        """
        Validate the input data for a new or updated expense.

        :param description: Expense description.
        :param amount: Expense amount.
        :param category: (Optional) Expense category.
        :return: ValidationResult object.
        """
        result = ValidationResult()

        if not description or not description.strip():
            result.add_error("Description is required.")

        if amount is None:
            result.add_error("Amount is required.")
        elif not isinstance(amount, (int, float)):
            result.add_error("Amount must be a number.")
        elif amount <= 0:
            result.add_error("Amount must be greater than 0.")

        return result

    def get_expense_by_id(self, expense_id):
        """
        Find and return an expense by its ID.

        :param expense_id: ID of the expense.
        :return: Expense dictionary or None.
        """
        for expense in self.expenses:
            if str(expense["id"]) == str(expense_id):
                return expense
        return None

    def get_expense_index_by_id(self, expense_id):
        """
        Get the index of an expense in the list by ID.

        :param expense_id: Expense ID.
        :return: Index or None if not found.
        """
        for i, expense in enumerate(self.expenses):
            if str(expense["id"]) == str(expense_id):
                return i
        return None

    def add_expense(self, description, amount, category=None):
        """
        Add a new expense to the tracker.

        :param description: Description of the expense.
        :param amount: Amount of the expense.
        :param category: (Optional) Category of the expense.
        :return: Dictionary with success status and new expense ID or errors.
        """
        validation = self.validate_expense_data(description, amount, category)
        if not validation.is_valid():
            return {"success": False, "errors": validation.errors}

        expense_id = self.get_next_id()
        today_obj = date.today()
        today = today_obj.isoformat()

        new_expense = Expense(
            id=expense_id,
            description=description.strip(),
            amount=amount,
            date=today,
            category=category
        )

        self.expenses.append(new_expense.__dict__)
        self.storage.save_expenses(self.expenses)

        total = self.get_expenses_summary(month=today_obj.month)
        month_str = f"{today_obj.year}-{today_obj.month:02}"
        budget = self.budget_service.get_budget(month_str)

        if budget and total > budget:
            print(f"⚠️ Warning: You have exceeded your budget for {month_str} (${budget})")

        return {"success": True, "id": expense_id}

    def update_expense(self, expense_id, description=None, amount=None, category=None):
        """
        Update an existing expense by ID.

        :param expense_id: ID of the expense to update.
        :param description: New description.
        :param amount: New amount.
        :param category: New category.
        :return: Dictionary with success status and message or errors.
        """
        id_validation = self.validate_expense_id(expense_id, self.expenses)
        if not id_validation.is_valid():
            return {"success": False, "errors": id_validation.errors}

        validation = self.validate_expense_data(description, amount, category)
        if not validation.is_valid():
            return {"success": False, "errors": validation.errors}

        expense = self.get_expense_by_id(expense_id)

        if description:
            expense["description"] = description
        if amount:
            expense["amount"] = amount
        if category:
            expense["category"] = category

        success = self.storage.update_expense_by_id(expense)
        if success:
            return {"success": True, "message": f"✅ Expense with ID {expense_id} updated."}
        else:
            return {"success": False, "message": "❌ Failed to update expense."}

    def delete_expense(self, expense_id):
        """
        Delete an expense by ID.

        :param expense_id: ID of the expense to delete.
        :return: Dictionary with success status and message or errors.
        """
        id_validation = self.validate_expense_id(expense_id, self.expenses)
        if not id_validation.is_valid():
            return {"success": False, "errors": id_validation.errors}

        index = self.get_expense_index_by_id(expense_id)
        if index is not None:
            del self.expenses[index]
            self.storage.save_expenses(self.expenses)
            return {"success": True, "message": f"Expense with ID {expense_id} deleted successfully."}

        return {"success": False, "message": f"Expense with ID {expense_id} not found."}

    def list_expenses(self, category=None):
        """
        Print a table of all expenses, optionally filtered by category.

        :param category: (Optional) Filter expenses by category.
        """
        if self.expenses:
            table = PrettyTable()
            table.field_names = ["ID", "Description", "Amount", "Category", "Date"]

            for expense in self.expenses:
                if category is None or expense["category"] == category:
                    table.add_row([
                        expense["id"],
                        expense["description"],
                        expense["amount"],
                        expense["category"],
                        expense["date"]
                    ])

            print(table)
        else:
            print("Not available any expense.")

    def get_expenses_summary(self, month=None):
        """
        Calculate the total expenses, optionally for a specific month.

        :param month: (Optional) Month number (1–12).
        :return: Total expenses as float.
        """
        expenses_summary = 0

        for expense in self.expenses:
            try:
                expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            except ValueError:
                continue  # Skip invalid dates

            if month:
                if expense_date.month == month:
                    expenses_summary += expense["amount"]
            else:
                expenses_summary += expense["amount"]

        return expenses_summary

    def set_monthly_budget(self, month, amount):
        """
        Set a budget for the specified month.

        :param month: Month number (1–12).
        :param amount: Budget amount.
        :return: Tuple of (success: bool, message: str)
        """
        try:
            month_int = int(month)
            amount = float(amount)
            if month_int < 1 or month_int > 12:
                return False, "❌ Invalid month. Please enter a value between 1 and 12."

            month_str = f"{date.today().year}-{month_int:02}"
            self.budget_service.set_budget(month_str, amount)
            return True, f"✅ Budget for {month_str} set to {amount}."

        except ValueError:
            return False, "❌ Please enter valid numbers for month and budget."

    def export_to_csv(self, filename="data/expenses_export.csv"):
        """
        Export all expenses to a CSV file.

        :param filename: File path for the exported CSV.
        """
        if not self.expenses:
            print("⚠️ No expenses to export.")
            return

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["id", "description", "amount", "category", "date"])
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow(expense)

        print(f"✅ Expenses exported successfully to {filename}")
