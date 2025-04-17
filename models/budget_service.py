import os
import json


class BudgetService:
    """
    Service class for managing monthly budget data stored in a JSON file.
    """

    def __init__(self, budget_file="data/budget.json"):
        """
        Initialize the BudgetService with the specified budget file.

        :param budget_file: Path to the JSON file where budgets are stored.
        """
        self.budget_file = budget_file
        self._initialize_budget_file()

    def _initialize_budget_file(self):
        """
        Create the budget file if it does not already exist.
        """
        if not os.path.exists(self.budget_file):
            with open(self.budget_file, 'w') as f:
                json.dump({}, f)

    def load_budgets(self):
        """
        Load all budgets from the JSON file.

        :return: Dictionary containing month-budget pairs.
        """
        with open(self.budget_file, 'r') as f:
            return json.load(f)

    def save_budgets(self, budgets):
        """
        Save the given budgets dictionary to the JSON file.

        :param budgets: Dictionary of month-budget pairs.
        """
        with open(self.budget_file, 'w') as f:
            json.dump(budgets, f, indent=4)

    def set_budget(self, month, amount):
        """
        Set the budget for a specific month.

        :param month: Month string in the format "YYYY-MM".
        :param amount: Budget amount as a number.
        """
        budgets = self.load_budgets()
        budgets[month] = amount
        self.save_budgets(budgets)

    def get_budget(self, month):
        """
        Retrieve the budget for a specific month.

        :param month: Month string in the format "YYYY-MM".
        :return: Budget amount or None if not found.
        """
        budgets = self.load_budgets()
        return budgets.get(month)
