from utils.helper import (
    create_new_json_file,
    read_json_file,
    update_json_file,
    update_item_in_json_by_id
)


class StorageService:
    """
    Service class to handle expense storage operations using a JSON file.
    """

    def __init__(self, file_path):
        """
        Initialize the StorageService with the given JSON file path.
        Creates a new JSON file if it doesn't exist.

        :param file_path: Path to the JSON file for storing expenses.
        """
        self.file_path = file_path
        create_new_json_file(self.file_path)

    def load_expenses(self):
        """
        Load expenses from the JSON file.

        :return: A list of expenses, or an empty list if none exist.
        """
        expenses = read_json_file(self.file_path)
        return expenses if expenses else []

    def save_expenses(self, expenses):
        """
        Save the list of expenses to the JSON file.

        :param expenses: A list of expenses to be saved.
        """
        update_json_file(self.file_path, expenses)

    def update_expense_by_id(self, updated_expense):
        """
        Update an existing expense by its ID in the JSON file.

        :param updated_expense: A dictionary containing the updated expense data.
        :return: True if the expense was updated, False otherwise.
        """
        return update_item_in_json_by_id(self.file_path, updated_expense)
