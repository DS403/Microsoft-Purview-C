##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules import *
from modules.lineage.shared_lineage_functions import *


# Imports
# ---------------

import re
from pathlib import Path


# Constants
# ---------------


# Functions
# ---------------

def remove_newlines(text: str) -> str:
    """
    Removes newline characters from the given text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with newline characters removed.
    """
    try:
        return text.replace('\n', '')
    except AttributeError:
        raise ValueError("Invalid input. Expected a string.")  


def extract_string_with_regex(before: str, after: str, sql_string: str):
    """
    Extracts a substring from the given `sql_string` using a regular expression pattern.

    Args:
        before (str): The string that precedes the desired substring in the `sql_string`.
        after (str): The string that follows the desired substring in the `sql_string`.
        sql_string (str): The input string from which the substring is extracted.

    Returns:
        str: The extracted substring that occurs between `before` and `after` in the `sql_string`, with any single quotes removed.
    """

    regex_pattern = re.escape(before) + r"(.*?)" + re.escape(after)
    match = re.search(regex_pattern, sql_string)
    if match:
        result = match.group(1)
        result = result.replace("'", "")
        return result
    else:
        raise ValueError("Pattern not found in the input string.")


def extract_source_and_target_from_external_table(sql_file_path: str):
    """
    Extracts the source location and target table name from an SQL file.

    Args:
        sql_file_path (str): The path to the SQL file.

    Returns:
        tuple: A tuple containing the extracted source location and target table name.
    """
    try:
        with open(sql_file_path, 'r') as file:
            sql_string = file.read()

        # Remove the BEGIN statement and newlines if they are present
        sql_string = remove_begin_statement(sql_string)
        sql_string = remove_newlines(sql_string)

        # Extract source and target
        source_location = extract_string_with_regex("LOCATION = N", ",", sql_string)
        target_table = extract_string_with_regex("CREATE EXTERNAL TABLE ", "(", sql_string)

        return [source_location], [target_table]
    
    except FileNotFoundError:
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")
    
    except Exception as e:
        raise ValueError("Failed to extract source location or target table name from the SQL file.") from e

