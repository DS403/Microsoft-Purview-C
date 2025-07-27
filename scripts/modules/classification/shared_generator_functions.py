##! /usr/bin/env python3


# Function Imports
# ---------------

from utils import get_credentials, create_purview_client


# Package Imports
# ---------------

from pathlib import Path
import pandas as pd


# Constants
# ---------------


# Functions
# ---------------

def process_classifications_sheet(excel_file_path: str, sheet_name: str):
    """
    Processes the classification sheet from an Excel file and returns a list of dictionaries representing classifications.

    Parameters:
        excel_file_path (str): The file path to the Excel file.
        sheet_name (str): The name of the sheet containing classification information.

    Returns:
        list: A list of dictionaries representing classifications.
    """
    classification_sheet = extract_sheet_from_excel(excel_file_path, sheet_name)
    classifications_dict = []
    for index, row in classification_sheet.iterrows():
        x = {
            "classification_name": row["Classification_Name"],
            "glossary_term": row["Associated_Glossary_Terms"],
            "keywords": row['Keywords'].split(",")
        }
        classifications_dict.append(x)
    return classifications_dict


def process_mappings_sheet(excel_file_path: str, sheet_name: str):
    """
    Processes the mappings sheet from an Excel file and returns a list of dictionaries representing mappings.

    Parameters:
        excel_file_path (str): The file path to the Excel file.
        sheet_name (str): The name of the sheet containing mappings information.

    Returns:
        list: A list of dictionaries representing mappings.
    """
    mappings_sheet = extract_sheet_from_excel(excel_file_path, sheet_name)
    mappings = []
    for index, row in mappings_sheet.iterrows():
        abbreviations_str = row['Abbreviations']
        abbreviations = [word.strip() for word in abbreviations_str.split(",")]
        x = {
            "word": row['Word'],
            "abbreviations": abbreviations
        }
        mappings.append(x)
    return mappings


def process_ignore_words_sheet(excel_file_path: str, sheet_name: str):
    ignore_words_sheet = extract_sheet_from_excel(excel_file_path, sheet_name)
    ignore_words = []
    for index, row in ignore_words_sheet.iterrows():
        ignore_words_str = row['Words_to_Ignore']
        ignore_words_split = [word.strip() for word in ignore_words_str.split(",")]
        x = {
            "classification_name": row['Classification_Name'],
            "ignore_words": ignore_words_split
        }
        ignore_words.append(x)
    return ignore_words


def extract_sheet_from_excel(file_path, sheet_name):
    """
    Extracts a specific sheet from an Excel file and returns it as a pandas DataFrame.

    Parameters:
        file_path: The file path to the Excel file.
        sheet_name: The name of the sheet to extract.

    Returns:
        pd.DataFrame: The extracted sheet as a pandas DataFrame.
    """
    excel_sheet = pd.read_excel(file_path, sheet_name=sheet_name)
    return excel_sheet

