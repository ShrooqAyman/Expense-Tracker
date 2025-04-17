import json
import os

class FileNotFoundError(Exception):
    """Custom exception raised when a file is not found."""
    pass

class FileWriteError(Exception):
    """Custom exception raised when writing to a file fails."""
    pass

class InvalidJsonError(Exception):
    """Custom exception raised when JSON data is invalid or corrupted."""
    pass

def create_new_json_file(file_path):
    """
    Creates a new JSON file if it doesn't already exist. Initializes it with an empty list.

    Args:
        file_path (str): The path of the file to create.

    Raises:
        FileWriteError: If the file cannot be created or written to.
    """
    try:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)  # Initialize with an empty list
    except IOError as e:
        print( FileWriteError(f"Failed to create or write to the file at {file_path}: {str(e)}"))

def read_json_file(file_path):
    """
    Reads the contents of a JSON file and returns the data as a Python object.

    Args:
        file_path (str): The path of the file to read.

    Returns:
        list: The data read from the JSON file (expected to be a list of tasks).

    Raises:
        FileNotFoundError: If the file is not found.
        InvalidJsonError: If the file contents are not valid JSON.
    """
    try:
        if not os.path.exists(file_path):
            print(FileNotFoundError(f"The file at {file_path} does not exist."))
            return
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        print( InvalidJsonError(f"Error parsing the JSON file at {file_path}: {str(e)}"))
    except IOError as e:
        print( FileNotFoundError(f"Error reading the file at {file_path}: {str(e)}"))

def update_json_file(file_path, data):
    """
    Writes the given data to the specified JSON file.

    Args:
        file_path (str): The path of the file to update.
        data (list): The data to write to the file.

    Raises:
        FileWriteError: If the file cannot be written to.
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(FileWriteError(f"Failed to write to the file at {file_path}: {str(e)}"))

def update_item_in_json_by_id(file_path, updated_item, key="id"):
    """
    Updates one item in the JSON file using the unique key (e.g., 'id').

    Args:
        file_path (str): Path to the JSON file.
        updated_item (dict): The updated dictionary to replace the existing one.
        key (str): The key used to match the item (default: 'id').

    Returns:
        bool: True if item was updated, False if not found.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} does not exist.")

        with open(file_path, 'r') as f:
            data = json.load(f)

        for index, item in enumerate(data):
            if str(item.get(key)) == str(updated_item.get(key)):
                data[index] = updated_item
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                return True

        return False  # Item not found

    except (IOError, json.JSONDecodeError) as e:
        print(FileWriteError(f"Failed to update item in file: {str(e)}"))
        return False
