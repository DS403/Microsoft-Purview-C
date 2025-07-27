##! /usr/bin/env python3


# Function Imports
# ---------------

from utils import get_credentials, create_purview_client
from modules.entity import *
from modules.glossary_propagation.shared_glossary_functions import *


# Package Imports
# ---------------

import json
import os
import re
import time
from datetime import datetime
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
from pyapacheatlas.core.glossary import PurviewGlossaryTerm
from pathlib import Path
import pandas as pd



# Constants
# ---------------


# Functions
# ---------------

def glossary_propagation_azure_dw(client, purview_acct_short_name):
    """
    Perform glossary term propagation in Azure SQL Data Warehouse entities.

    Parameters:
    - client: Purview client for making API requests.
    - purview_acct_short_name (str): Short name of the Purview account.

    Returns:
    - None: Outputs results to files, detailing the glossary term propagation.
    """
    input_filename = purview_acct_short_name + "_pulled_entities.json"
    pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        pulled_entities = json.load(json_file)

    # use the new regex sheet, extract the glossary term name and regex 
    file_path = "1_to_500_Glossary_with_Field_Duplicates_at_End_10.2.23.xlsx"
    glossary_terms_sheet = pd.read_excel(file_path)
    glossary_terms_dict = []
    for index, row in glossary_terms_sheet.iterrows():
        x = {
            "name": row["Nick Name"],
            "fields": row["Field"].split(",")
        }
        glossary_terms_dict.append(x)

    directory = 'outputs/glossary_propagation_outputs/sql_dw/' + purview_acct_short_name
    output_file_path = purview_acct_short_name + "_sql_dw_glossary_propagation_results"
    os.makedirs(directory, exist_ok=True) # Create the directory if it doesn't exist
    output_file_path = os.path.join(directory, output_file_path)

    sql_dw_table_entities = pulled_entities.get("data_sources").get("azure_sql_dw").get("azure_sql_dw_table").get("all_entity_details")

    with open(output_file_path, 'w') as file:
        file.flush()
        count = 0
        for d in glossary_terms_dict: 
            count += 1
            name = d.get("name")
            fields = d.get("fields")
            azure_sql_dw_table_result = propagate_glossary_term_by_specific_entity_type_and_return_string(sql_dw_table_entities, client, name, fields, "columns")
            
            elapsed_time = azure_sql_dw_table_result[0]
            matched_strings = azure_sql_dw_table_result[1]
            end_timestamp = datetime.now().strftime("%m/%d/%Y %H:%M")
            
            return_str = "Glossary term: " + name + "\nPropagated in " + purview_acct_short_name + " on: " + str(end_timestamp) + "\nElapsed Time (seconds): " + str(elapsed_time) + "\nNumber of matches, then applications: " + str(len(matched_strings)) + "\nGlossary Term Number: " + str(count) + "\n"
            print(return_str)

            file.write(str(return_str))

            for match in matched_strings:
                file.write(str(match) + '\n') 
            file.write('\n\n')

        file.flush()
        file.close()
                   