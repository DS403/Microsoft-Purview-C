##! /usr/bin/env python3


# Function Imports
# ---------------

from modules.classification.shared_generator_functions import *
from utils import get_credentials, create_purview_client


# Package Imports
# ---------------

from pyapacheatlas.core import AtlasEntity, AtlasClassification
from pyapacheatlas.core.entity import AtlasEntity, AtlasUnInit
import csv
from pathlib import Path
import pandas as pd
import random
import string
import os


# Constants
# ---------------


# Functions
# ---------------

def generate_variations(keywords, mappings):
    """
    Generates variations of keywords based on mappings.

    Parameters:
        keywords (list): A list of keywords.
        mappings (list): A list of mappings containing word and abbreviation information.

    Returns:
        list: A list of generated variations.
    """
    variations = set(keywords)
    for keyword in keywords:
        for mapping in mappings:
            word = mapping['word']
            abbreviations = mapping['abbreviations']
            if word in keyword:
                mapping_variations = [keyword.replace(word, abbreviation) for abbreviation in abbreviations]
                variations.update(mapping_variations)
                variations.add(keyword)
                variations.update(generate_variations(mapping_variations, mappings))
    return list(variations)


def get_keyword_variations(classification: dict, mappings: list):
    """
    Generates keyword variations for a classification based on mappings.

    Parameters:
        classification (dict): A dictionary representing a classification.
        mappings (list): A list of mappings containing word and abbreviation information.

    Returns:
        list: A list of keyword variations.
    """
    keywords = classification["keywords"]
    variations = generate_variations(keywords, mappings)
    stripped_variations = strip_strings(variations)
    unique_variations = []
    for variation in stripped_variations:
        if not any(variation.startswith(abbreviation) for abbreviation in mappings[0]['abbreviations']):
            unique_variations.append(variation)
    
    unique_variations = list(set(unique_variations))
    return unique_variations


def get_excel_column_names(file_path):
    """
    Retrieves column names from an Excel file.

    Parameters:
        file_path (str): The file path to the Excel file.

    Returns:
        list: A list of column names.
    """
    df = pd.read_excel(file_path)
    column_names = df.columns.tolist()
    return column_names


def get_csv_column_names(file_name):
    """
    Retrieves column names from a CSV file.

    Parameters:
        file_name (str): The file name of the CSV file.

    Returns:
        list: A list of column names.
    """
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        column_names = next(reader)  # Read the first row
    return column_names


def to_snake_case(input_str: str):
    """
    Converts a string to snake case.

    Parameters:
        input_str (str): The input string.

    Returns:
        str: The string converted to snake case.
    """
    snake_case_string = input_str.replace(' ', '_')
    snake_case_string = snake_case_string.lower()
    return snake_case_string


def create_test_case_csv_file(directory: str, classification_name: str, to_pass_or_fail: str, column_names: list):
    """
    Creates a test case CSV file.

    Parameters:
        directory (str): The directory to store the CSV file.
        classification_name (str): The name of the classification.
        to_pass_or_fail (str): Indicates whether the test case is for "to_pass" or "to_fail".
        column_names (list): A list of column names.

    Returns:
        str: The file name of the created CSV file.
    """
    os.makedirs(directory, exist_ok=True) # Create the directory if it doesn't exist
    snake_case_classification_name = to_snake_case(classification_name)
    file_name_without_path = snake_case_classification_name + '_' + to_pass_or_fail + '_test_column_names.csv'
    file_name = os.path.join(directory, file_name_without_path)

    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
        writer.writerow(['0'] * len(column_names))

    print(f'CSV file "{file_name}" created successfully.')
    return file_name


def get_all_spacings_between(variations: list):
    """
    Generates variations by adding different spacings between the words.

    Parameters:
        variations (list): A list of variations.

    Returns:
        list: A list of variations with different spacings between the words.
    """
    all_spacings = []
    special_chars = ['!', '&', '*', '+', '.', '-', '/', ':', '_', '~', "|"]  # Add more special characters if desired
    
    for variation in variations:
        current_with_space = variation
        no_space = variation.replace(" ", "")
        with_underscores = variation.replace(" ", "_")
        with_one_special_char = variation.replace(" ", random.choice(special_chars))
        all_spacings.extend([current_with_space, no_space, with_underscores, with_one_special_char])
    return all_spacings


def get_all_letter_cases(variations: list):
    """
    Generates variations by changing the letter cases.

    Parameters:
        variations (list): A list of variations.

    Returns:
        list: A list of variations with different letter cases.
    """
    all_cases = []
    for variation in variations:
        current = variation
        all_upper = variation.upper()
        all_lower = variation.lower()
        mixed_case = ''.join([char.upper() if random.choice([True, False]) else char.lower() for char in variation])
        title_case = variation.title()
        all_cases.extend([current, all_upper, all_lower, mixed_case, title_case])

    return all_cases


def get_all_paddings(variations: list):
    """
    Generates variations by adding different paddings.

    Parameters:
        variations (list): A list of variations.

    Returns:
        list: A list of variations with different paddings.
    """
    all_paddings = []
    special_chars = ['!', '&', '*', '.', '/', ':', '_', '~', "|"]  # DO NOT USE '+' or '-'
    chars_to_use = list(string.ascii_letters) + special_chars

    for variation in variations:
        current = variation
        pad_with_spaces = ' ' + variation + ' '
        pad_with_underscores = '_' + variation + '_'
        pad_with_special_chars_or_random_letters = random.choice(chars_to_use) + variation + random.choice(chars_to_use)
        all_paddings.extend([current, pad_with_spaces, pad_with_underscores, pad_with_special_chars_or_random_letters])
    
    return all_paddings


def generate_pass_column_names(variations: list):
    """
    Generates column names for passing test cases.

    Parameters:
        variations (list): A list of variations.

    Returns:
        list: A list of column names for passing test cases.
    """
    # Get all cases for each variation
    all_letter_cases = get_all_letter_cases(variations)
    unique_all_letter_cases = list(set(all_letter_cases))

    # Get all spacings between the words
    all_spacings_between = get_all_spacings_between(unique_all_letter_cases)
    unique_all_spacings_between = list(set(all_spacings_between))

    # Pad the variations
    padded_and_complete_variations = get_all_paddings(unique_all_spacings_between)
    unique_padded_and_complete_variations = list(set(padded_and_complete_variations))

    return unique_padded_and_complete_variations


def strip_strings(strings):
    """
    Strips leading and trailing spaces from a list of strings.

    Parameters:
        strings (list): A list of strings.

    Returns:
        list: A list of stripped strings.
    """
    return [string.strip() for string in strings]


def generate_pass_test_file(classification: dict, mappings: list):
    """
    Generates a CSV test file for passing test cases.

    Parameters:
        classification (dict): A dictionary representing a classification.
        mappings (list): A list of mappings containing word and abbreviation information.

    Returns:
        str: The file name of the created CSV test file.
    """
    # Get variations of the keywords
    variations = get_keyword_variations(classification, mappings)

    # Create test cases from the variations
    pass_column_names = generate_pass_column_names(variations)

    # Purview only works with 1000 column names or less in a csv file, so cap it a 1000
    capped_pass_column_names = random.sample(pass_column_names, k=min(1000, len(pass_column_names)))

    # Populate the CSV test file
    directory = 'test_CSVs/to_pass'
    pass_file_name = create_test_case_csv_file(directory, classification["classification_name"], "to_pass", capped_pass_column_names)

    # Return the file name
    return pass_file_name


def generate_all_pass_test_files(excel_file_path: str, classifications_sheet_name: str, mappings_sheet_name: str):
    """
    Generates CSV test files for all passing test cases.

    Parameters:
        excel_file_path (str): The file path to the Excel file.
        classifications_sheet_name (str): The name of the sheet containing classification information.
        mappings_sheet_name (str): The name of the sheet containing mappings information.

    Returns:
        list: A list of file names for the created CSV test files.
    """
    pass_test_file_names = []
    classifications = process_classifications_sheet(excel_file_path, classifications_sheet_name)
    mappings = process_mappings_sheet(excel_file_path, mappings_sheet_name)
    for c in classifications:
        test_file_name = generate_pass_test_file(c, mappings)
        pass_test_file_names.append(test_file_name)
        
    return pass_test_file_names


def get_allowed_standalone_keywords(keywords: list):
    """
    Retrieves allowed standalone keywords from a list of keywords.

    Parameters:
        keywords (list): A list of keywords.

    Returns:
        list: A list of allowed standalone keywords.
    """
    allowed_standalone_keywords = []
    for keyword in keywords:
        words = keyword.split()
        if len(words) == 1:
            allowed_standalone_keywords.append(words[0])
    return allowed_standalone_keywords


def get_base_fail_column_names(keywords: list, allowed_standalone_keywords: list, mappings: list):
    """
    Retrieves base fail column names based on keywords, allowed standalone keywords, and mappings.

    Parameters:
        keywords (list): A list of keywords.
        allowed_standalone_keywords (list): A list of allowed standalone keywords.
        mappings (list): A list of mappings containing word and abbreviation information.

    Returns:
        list: A list of base fail column names.
    """
    base_fail_column_names = []
    for keyword in keywords:
        words = keyword.split()
        for word in words:
            if word.lower() not in [kw.lower() for kw in allowed_standalone_keywords]:
                base_fail_column_names.append(word)

    for mapping in mappings:
        if mapping["word"] in base_fail_column_names:
            base_fail_column_names.extend(mapping["abbreviations"])

    unique_base_fail_column_names = list(set(base_fail_column_names))
    return unique_base_fail_column_names


def get_all_fail_column_names(base_fail_column_names: list):
    """
    Generates all fail column names based on base fail column names.

    Parameters:
        base_fail_column_names (list): A list of base fail column names.

    Returns:
        list: A list of all fail column names.
    """
    all_fail_column_names = []
    special_chars = ['!', '&', '*', '.', '/', ':', '_', '~', "|"]  # DO NOT USE '+' or '-'

    for item in base_fail_column_names:
        current = item
        pad_with_spaces = ' ' + item + ' '
        pad_with_underscores = '_' + item + '_'
        pad_with_special_chars_or_random_letters = random.choice(special_chars) + item + random.choice(special_chars)
        all_fail_column_names.extend([current, pad_with_spaces, pad_with_underscores, pad_with_special_chars_or_random_letters])

        all_upper = item.upper()
        all_lower = item.lower()
        mixed_case = ''.join([char.upper() if random.choice([True, False]) else char.lower() for char in item])
        title_case = item.title()
        all_fail_column_names.extend([all_upper, all_lower, mixed_case, title_case])
    
    unique_all_fail_column_names = list(set(all_fail_column_names))
    return unique_all_fail_column_names


def generate_fail_test_file(classification: dict, mappings: list):
    """
    Generates a CSV test file for failing test cases.

    Parameters:
        classification (dict): A dictionary representing a classification.
        mappings (list): A list of mappings containing word and abbreviation information.

    Returns:
        str: The file name of the created CSV test file.
    """
    # Get keywords and mappings to use 
    keywords = classification["keywords"]
    allowed_standalone_keywords = get_allowed_standalone_keywords(keywords)
    base_fail_column_names = get_base_fail_column_names(keywords, allowed_standalone_keywords, mappings)
    all_fail_column_names = get_all_fail_column_names(base_fail_column_names)

    # Purview only works with 1000 column names or less in a csv file, so cap it a 1000
    capped_fail_column_names = random.sample(all_fail_column_names, k=min(1000, len(all_fail_column_names)))

    # Populate the CSV test file
    directory = 'test_CSVs/to_fail'
    fail_file_name = create_test_case_csv_file(directory, classification["classification_name"], "to_fail", capped_fail_column_names)

    # Return the file name
    return fail_file_name


def generate_all_fail_test_files(excel_file_path: str, classifications_sheet_name: str, mappings_sheet_name: str):
    """
    Generates CSV test files for all failing test cases.

    Parameters:
        excel_file_path (str): The file path to the Excel file.
        classifications_sheet_name (str): The name of the sheet containing classification information.
        mappings_sheet_name (str): The name of the sheet containing mappings information.

    Returns:
        list: A list of file names for the created CSV test files.
    """
    fail_test_file_names = []
    classifications = process_classifications_sheet(excel_file_path, classifications_sheet_name)
    mappings = process_mappings_sheet(excel_file_path, mappings_sheet_name)
    for c in classifications:
        test_file_name = generate_fail_test_file(c, mappings)
        fail_test_file_names.append(test_file_name)
        
    return fail_test_file_names

