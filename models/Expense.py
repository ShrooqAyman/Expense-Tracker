class Expense:
    """
    Represents an individual expense entry.
    """

    def __init__(self, id, description, amount, date, category=None):
        """
        Initialize a new Expense object.

        :param id: Unique identifier for the expense.
        :param description: Description of the expense.
        :param amount: Amount of the expense.
        :param date: Date of the expense (in YYYY-MM-DD format).
        :param category: Optional category for the expense.
        """
        self.id = id
        self.description = description
        self.amount = amount
        self.date = date
        self.category = category
