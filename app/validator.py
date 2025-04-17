class ValidationResult:
    """
    A simple class to collect validation errors and check if the result is valid.
    """

    def __init__(self):
        """Initialize with an empty list of errors."""
        self.errors = []

    def add_error(self, message):
        """
        Add a validation error message.

        :param message: The error message to add.
        """
        self.errors.append(message)

    def is_valid(self):
        """
        Check if there are no validation errors.

        :return: True if valid (no errors), False otherwise.
        """
        return len(self.errors) == 0
