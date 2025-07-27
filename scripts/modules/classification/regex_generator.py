##! /usr/bin/env python3


# Function Imports
# ---------------

from utils import get_credentials, create_purview_client
from modules.classification.shared_generator_functions import *


# Package Imports
# ---------------

from pyapacheatlas.core import AtlasEntity, AtlasClassification
from pyapacheatlas.core.entity import AtlasEntity, AtlasUnInit
from pathlib import Path
import pandas as pd


# Constants
# ---------------


# Functions
# ---------------

def incorporate_ignore_words():
    print()

def handle_word(word: str, mappings_dict: dict):
    """
    Handles a word by checking if it exists in the mappings dictionary and returns the corresponding word component.

    Parameters:
        word (str): The word to handle.
        mappings_dict (dict): A dictionary containing word mappings.

    Returns:
        str: The word component based on the mappings dictionary.
    """
    word_component = ""
    if word in mappings_dict:
        abbreviations = mappings_dict[word]
        word_component = f"({'|'.join([word] + abbreviations)})"
    else:
        word_component = "(" + word + ")"
    return word_component


def create_regex_string(keywords: list, mappings_dict: dict):
    """
    Creates a regex string by processing a list of keywords and a mappings dictionary.

    Parameters:
        keywords (list): A list of keywords.
        mappings_dict (dict): A dictionary containing word mappings.

    Returns:
        str: The resulting regex string.
    """
    regex_components = []
    for keyword in keywords:
        keyword_components = [handle_word(word, mappings_dict) for word in keyword.split()]
        regex_components.append("[^A-Za-z0-9]?".join(keyword_components) + ".*") 
    regex_string = ".*" + "|.*".join(regex_components)
    return regex_string


def get_regex_dict(classification: dict, mappings_dict: dict):
    """
    Generates a dictionary containing regex information for a given classification.

    Parameters:
        classification (dict): A dictionary representing a classification.
        mappings_dict (dict): A dictionary containing word mappings.

    Returns:
        dict: The dictionary containing regex information.
    """
    keywords = classification["keywords"]
    regex = create_regex_string(keywords, mappings_dict)
    regex_dict = {
        "classification_name": classification["classification_name"],
        "classification_description": classification["glossary_term"],
        "glossary_term": classification["glossary_term"],
        "keywords": keywords,
        "regex": regex
    }
    return regex_dict


def generate_all_regex(excel_file_path: str, classification_sheet_name: str, mappings_sheet_name: str, ignore_words_sheet_name: str):
    """
    Generates a list of dictionaries containing regex information for all classifications.

    Parameters:
        excel_file_path (str): The file path to the Excel file.
        classification_sheet_name (str): The name of the sheet containing classification information.
        mappings_sheet_name (str): The name of the sheet containing mappings information.

    Returns:
        list: A list of dictionaries containing regex information.
    """
    all_regex_dicts = []
    classifications = process_classifications_sheet(excel_file_path, classification_sheet_name)
    mappings = process_mappings_sheet(excel_file_path, mappings_sheet_name)
    ignore_words = process_ignore_words_sheet(excel_file_path, ignore_words_sheet_name)
    mappings_dict = {mapping['word']: mapping['abbreviations'] for mapping in mappings}

    for c in classifications:
        regex_dict = get_regex_dict(c, mappings_dict)
        all_regex_dicts.append(regex_dict)
        
    return all_regex_dicts


def export_to_excel(all_regex_dicts, file_path):
    """
    Exports a list of regex dictionaries to an Excel file.

    Parameters:
        all_regex_dicts (list): A list of dictionaries containing regex information.
        file_path: The file path where the Excel file will be saved.

    Returns:
        None
    """
    data = []
    for regex_dict in all_regex_dicts:
        classification_name = regex_dict["classification_name"]
        classification_description = regex_dict["classification_description"]
        glossary_term = regex_dict["glossary_term"]
        keywords = ", ".join(regex_dict["keywords"])
        regex = regex_dict["regex"]
        data.append([classification_name, classification_description, glossary_term, keywords, regex])
    
    df = pd.DataFrame(data, columns=["Classification_Name", "Classification_Description", "Glossary_Term", "Keywords", "REGEX"])
    df.to_excel(file_path, index=False)
    
