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

def apply_glossary_terms_and_write_output_of_sap_s4hana(client, file, updated_dict_for_string_matches, updated_dict_for_guids_of_a_glossary_term, start, end):
    '''
    Apply glossary terms to SAP S/4HANA views and tables, write output to a file, and log the results.

    Args:
        client: The Purview Atlas client for glossary term application.
        file: File object for writing the output log.
        updated_dict_for_string_matches (dict): Dictionary with glossary term names as keys and lists of matched string names.
        updated_dict_for_guids_of_a_glossary_term (dict): Dictionary with glossary term names as keys and lists of GUIDs.
        start (int): Start index for glossary term propagation.
        end (int): End index for glossary term propagation.

    Returns:
        file: Updated file object.
    '''
    count = 0
    for glossary_term_name, list_of_guids in updated_dict_for_guids_of_a_glossary_term.items():
        count += 1 
        if count > start - 1 and count < end + 1:  
            unique_guids = list(set(list_of_guids))
            count_str = "Glossary Term Number: " + str(count)
            if len(unique_guids) > 0:
                upload_formatted_list = []
                for guid in unique_guids:
                    if guid is not None:
                        upload_formatted_list.append({"guid": guid})
                
                print(count_str + "\nGoing to assign " + glossary_term_name + " to " + str(len(unique_guids)) + " entities")
                try:
                    applied_result = client.glossary.assignTerm(entities = upload_formatted_list, termName = glossary_term_name)
                    assignment_str = "Assigned glossary term, " + glossary_term_name + ", to " + str(len(unique_guids)) + " entities\n"
                    print(str(applied_result))
                    print(assignment_str)
                    file.write(count_str + "\n" + assignment_str)
                    file.write("Unique column names that the glossary term was applied to:\n")
                    unique_column_names = list(set(updated_dict_for_string_matches[glossary_term_name]))
                    for column_name in unique_column_names:
                        print("column name: " + column_name)
                        file.write("   " + column_name + "\n")
                    file.write("\n")
                    print()
                except:
                    file.write("Error with a guid for glossary term: " + glossary_term_name + "\n\n")
                    print("Error with a guid for glossary term: " + glossary_term_name + "\n")
            else:
                assignment_str = "No matches for glossary term, " + glossary_term_name + "\n\n"
                print(count_str + "\n" + assignment_str)
                file.write(count_str + "\n" + assignment_str)
            
    return file


def prepare_for_propagation_of_sap_s4hana(client, sap_s4hana_view_details, sap_s4hana_table_details, file, start, end, import_file_name):
    '''
    Prepare for glossary term propagation across SAP S/4HANA views and tables.

    Args:
        client: The Purview Atlas client for glossary term propagation.
        sap_s4hana_view_details (list): List of SAP S/4HANA view entities.
        sap_s4hana_table_details (list): List of SAP S/4HANA table entities.
        file: File object for writing the output log.
        start (int): Start index for glossary term propagation.
        end (int): End index for glossary term propagation.
        import_file_name (str): Name of the glossary term import file.

    Returns:
        list: A list containing the file object, merged_string_matches, and merged_guids.
    '''
    file.write("Glossary Terms Propagated Across SAP S4HANA Assets\n")
    file.write("Ran for Glossary Terms " + str(start) + " to " + str(end) + "\n")
    file.write("Ran on SAP S4HANA Tables and Views\n_____________________________________________________________\n\n")

    view_string_matches = {}
    view_guids = {}
    table_string_matches = {}
    table_guids = {}
    for glossary_term_dict in get_glossary_terms_dict(import_file_name):
        glossary_term_name = glossary_term_dict.get("name")
        view_string_matches[glossary_term_name] = []
        view_guids[glossary_term_name] = []
        table_string_matches[glossary_term_name] = []
        table_guids[glossary_term_name] = []

    glossary_dict_with_fields_as_keys = read_glossary_import_file(import_file_name)

    view_column_name = "view_columns"
    sap_s4hana_view_result = propagate_all_glossary_terms_across_specific_entity_type(client, sap_s4hana_view_details, view_column_name, glossary_dict_with_fields_as_keys, view_string_matches, view_guids)
    table_column_name = "primary_key_fields"
    sap_s4hana_table_result = propagate_all_glossary_terms_across_specific_entity_type(client, sap_s4hana_table_details, table_column_name, glossary_dict_with_fields_as_keys, table_string_matches, table_guids)

    updated_view_string_matches = sap_s4hana_view_result[1]
    updated_view_guids = sap_s4hana_view_result[2]
    updated_table_string_matches = sap_s4hana_table_result[1]
    updated_table_guids = sap_s4hana_table_result[2]

    merged_string_matches = {}
    for key in updated_view_string_matches:
        merged_string_matches[key] = updated_view_string_matches[key] + updated_table_string_matches[key]
    merged_guids = {}
    for key in updated_view_guids:
        merged_guids[key] = updated_view_guids[key] + updated_table_guids[key]

    return [file, merged_string_matches, merged_guids]


def glossary_propagation_of_sap_s4hana(client, purview_acct_short_name, import_file_name):
    '''
    Run glossary term propagation on SAP S/4HANA views and tables for a specified Purview account and import file.

    Args:
        client: The Purview Atlas client for glossary term propagation.
        purview_acct_short_name (str): Short name of the Purview account ("prod" or "qa").
        import_file_name (str): Name of the glossary term import file.
    '''
    # run this fresh on Prod if need to re-pull entities
    # pull_entities_from_purview("prod", "hbi-pd01-datamgmt-pview", CLIENT)

    short_name = purview_acct_short_name
    input_filename = short_name + "_pulled_entities.json"
    pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        pulled_entities = json.load(json_file)

    # NOTE: HARDCODING
    start = 651
    end = 716
    output_file_path = str(start) + "_to_" + str(end) + "_" + short_name + "_sap_s4hana_glossary_propagation_results.txt"
   
    directory = "glossary_propagation_outputs/sap_s4hana_outputs/" + short_name
    os.makedirs(directory, exist_ok=True) # Create the directory if it doesn't exist
    output_file_path = os.path.join(directory, output_file_path)

    sap_s4hana_view_details = pulled_entities.get("data_sources").get("sap_s4hana").get("sap_s4hana_view").get("all_entity_details")
    sap_s4hana_table_details = pulled_entities.get("data_sources").get("sap_s4hana").get("sap_s4hana_table").get("all_entity_details")

    with open(output_file_path, 'w') as file:
        file.flush()
        file_and_dicts = prepare_for_propagation_of_sap_s4hana(client, sap_s4hana_view_details, sap_s4hana_table_details, file, start, end, import_file_name)
        file = file_and_dicts[0]
        merged_string_matches = file_and_dicts[1]
        merged_guids = file_and_dicts[2]
        
        # hardcoded to only prop certain glossary term numbers
        # MODIFY HARDCODED NUMBERS
        file = apply_glossary_terms_and_write_output_of_sap_s4hana(client, file, merged_string_matches, merged_guids, start, end)
        file.flush()
        file.close()
        print("Propagation across SAP S4HANA tables and views in " + short_name + " is complete\n\n")
