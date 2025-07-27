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

def propagate_glossary_terms_across_data_lake_resource_sets(datalake_resource_set_entities, client, glossary_term_name, fields):
    '''
    Propagate a glossary term across data lake resource sets by matching fields and applying the glossary term.

    Args:
        datalake_resource_set_entities (list): List of data lake resource set entities.
        client: The Purview Atlas client for entity upload.
        glossary_term_name (str): Name of the glossary term to be propagated.
        fields (list): List of field names to match for glossary term propagation.

    Returns:
        list: A list containing elapsed time in seconds and matched field names.
    '''
    start_time = time.time()
    matched_strings = []

    for resource_set in datalake_resource_set_entities:
        columns = resource_set.get("columns")
        
        if columns != None:
            for column in columns:  
                column_guid = column.get("guid")
                column_name = column.get("displayText")

                if column_name in fields:
                    print(f"Matched string: {column_name}")
                    matched_strings.append(column_name)

                    print("column guid: " + str(column_guid))
                    print("entity guid: " + str(resource_set.get("guid")))

                    # want to only apply IF NOT ATTACHED ALREADY - NEED TO IMPLEMENT TO OPTIMIZE
                    entities = [{"guid": column_guid}, {"guid": resource_set.get("guid")}]
                    applied_result = client.glossary.assignTerm(entities = entities, termName = glossary_term_name)
                    print(applied_result)

    end_time = time.time()
    elapsed_time_seconds = round(end_time - start_time)

    return [elapsed_time_seconds, matched_strings]


def glossary_propagation_of_datalake(client, purview_acct_short_name):
    '''
    Run glossary term propagation for data lake entities.
    Args:
        purview_acct_short_name : The name of purview account short name.
        client: The Purview Atlas client for entity upload.

    Note: The function reads entities from a pre-pulled JSON file, applies glossary terms, and logs the results.
    '''
    # Note: purview_acct_short_name = "qa" or "prod"
    # RUN BELOW FOR REFRESHED PULL OF PROD INSTANCES
    #pull_prod_entities_from_purview("prod", "hbi-pd01-datamgmt-pview", client)

    input_filename = purview_acct_short_name + "_pulled_entities.json"
    pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        pulled_entities = json.load(json_file)

    glossary_terms_dict = get_glossary_terms_dict()
    directory = 'outputs/glossary_propagation_outputs/datalake_outputs/' + purview_acct_short_name
    output_file_path = purview_acct_short_name + "_datalake_glossary_propagation_results"
    os.makedirs(directory, exist_ok=True) # Create the directory if it doesn't exist
    output_file_path = os.path.join(directory, output_file_path)

    datalake_resource_set_entities = pulled_entities.get("data_sources").get("azure_datalake_gen2").get("azure_datalake_gen2_resource_set").get("all_entity_details")

    with open(output_file_path, 'w') as file:
        file.flush()
        count = 0
        for d in glossary_terms_dict: 
            count += 1
            name = d.get("name")
            fields = d.get("fields")
            datalake_result = propagate_glossary_terms_across_data_lake_resource_sets(datalake_resource_set_entities, client, name, fields)
            
            elapsed_time = datalake_result[0]
            matched_strings = datalake_result[1]
            end_timestamp = datetime.now().strftime("%m/%d/%Y %H:%M")
            
            return_str = "Glossary term: " + name + "\nPropagated in " + purview_acct_short_name + " on: " + str(end_timestamp) + "\nElapsed Time (seconds): " + str(elapsed_time) + "\nNumber of matches, then applications: " + str(len(matched_strings)) + "\nGlossary Term Number: " + str(count) + "\n"
            print(return_str)

            file.write(str(return_str))

            for match in matched_strings:
                file.write(str(match) + '\n') 
            file.write('\n\n')

        file.flush()
        file.close()
        
