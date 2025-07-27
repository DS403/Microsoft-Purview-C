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

def delete_glossary_terms_from_all_sap_hana_tables(client):
    '''
    Delete glossary terms from all SAP HANA tables by iterating through the pulled entities.

    Note: This function reads entities from a pre-pulled JSON file and deletes glossary terms from SAP HANA tables.
    '''
    input_filename = "qa_pulled_entities.json"
    qa_pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        qa_pulled_entities = json.load(json_file)

    # use the new regex sheet, extract the glossary term name and regex 
    sap_hana_views = qa_pulled_entities.get("data_sources").get("sap_hana").get("sap_hana_view").get("all_entity_details")
    
    count = 0
    print("Views to iterate through: " + str(len(sap_hana_views)))
    for view in sap_hana_views:
        count += 1
        print("View: " + str(count) + "\n")
        view_guid = view.get("guid")
        delete_term_from_entity_and_columns(view_guid)


def apply_glossary_terms_and_write_output_of_sap_hana(client, file, updated_dict_for_string_matches, updated_dict_for_guids_of_a_glossary_term, start, end):
    '''
    Apply glossary terms to SAP HANA views, write output to a file, and log the results.

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
            if len(unique_guids) > 0 and glossary_term_name == "Denominator for Conversion to Base Units of Measure": # REMOVE EHRE HARDCODING
                upload_formatted_list = []
                for guid in unique_guids:
                    if guid is not None:
                        upload_formatted_list.append({"guid": guid})

                print(upload_formatted_list)
                
                print(count_str + "\nGoing to assign " + glossary_term_name + " to " + str(len(unique_guids)) + " entities")
                try:
                    try:
                        applied_result = client.glossary.assignTerm(entities = upload_formatted_list, termName = glossary_term_name)
                        print(applied_result)
                    except Exception as x:
                        print(f"{x}")
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
                except Exception as e:
                    file.write(f"{e}\n\n")
                    file.write("Error with a guid for glossary term: " + glossary_term_name + "\n\n")
                    print(f"{e}")
                    print("Error with a guid for glossary term: " + glossary_term_name + "\n")
            else:
                assignment_str = "No matches for glossary term, " + glossary_term_name + "\n"
                print(count_str + "\n" + assignment_str)
                file.write(count_str + "\n" + assignment_str)
            
    return file


def prepare_for_propagation_of_sap_hana(client, sap_hana_view_details, file, start, end, import_file_name):
    '''
    Prepare for glossary term propagation across SAP HANA views.

    Args:
        client: The Purview Atlas client for glossary term propagation.
        sap_hana_view_details (list): List of SAP HANA view entities.
        file: File object for writing the output log.
        start (int): Start index for glossary term propagation.
        end (int): End index for glossary term propagation.
        import_file_name (str): Name of the glossary term import file.

    Returns:
        list: A list containing the file object, updated_dict_for_string_matches, and updated_dict_for_guids_of_a_glossary_term.
    '''
    file.write("Glossary Terms Propagated Across SAP HANA Assets\n")
    file.write("Ran for Glossary Terms " + str(start) + " to " + str(end) + "\n")
    file.write("Ran on SAP HANA Views and Tables\n_____________________________________________________________\n\n")

    dict_for_string_matches = {}
    dict_for_guids_of_a_glossary_term = {}
    for glossary_term_dict in get_glossary_terms_dict(import_file_name):
        glossary_term_name = glossary_term_dict.get("name")
        dict_for_string_matches[glossary_term_name] = []
        dict_for_guids_of_a_glossary_term[glossary_term_name] = []

    glossary_dict_with_fields_as_keys = read_glossary_import_file(import_file_name)

    column_type_name = "view_columns"
    sap_hana_view_result = propagate_all_glossary_terms_across_specific_entity_type(client, sap_hana_view_details, column_type_name, glossary_dict_with_fields_as_keys, dict_for_string_matches, dict_for_guids_of_a_glossary_term)

    elapsed_time = sap_hana_view_result[0]
    updated_dict_for_string_matches = sap_hana_view_result[1]
    updated_dict_for_guids_of_a_glossary_term = sap_hana_view_result[2]

    return [file, updated_dict_for_string_matches, updated_dict_for_guids_of_a_glossary_term]


def glossary_propagation_of_sap_hana(client, purview_acct_short_name, import_file_name):
    '''
    Run glossary term propagation on SAP HANA views for a specified Purview account and import file.

    Args:
        client: The Purview Atlas client for glossary term propagation.
        purview_acct_short_name (str): Short name of the Purview account.
        import_file_name (str): Name of the glossary term import file.
    '''
    # run this fresh on prod if need to re-pull entities
    # pull_entities_from_purview("prod", "hbi-pd01-datamgmt-pview", prod_client)

    short_name = purview_acct_short_name
    input_filename = short_name + "_pulled_entities.json"
    pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        pulled_entities = json.load(json_file)

    # NOTE: HARDCODING
    start = 0 
    end = 716
    output_file_path = str(start) + "_to_" + str(end) + "_" + short_name + "_sap_hana_glossary_propagation_results.txt"
    # NOTE: HARDCODING
    #output_file_path = "451_to_500_qa_sap_hana_glossary_propagation_results.txt"
   
    directory = "glossary_propagation_outputs/sap_hana_outputs/" + short_name
    os.makedirs(directory, exist_ok=True) # Create the directory if it doesn't exist
    output_file_path = os.path.join(directory, output_file_path)

    sap_hana_view_details = pulled_entities.get("data_sources").get("sap_hana").get("sap_hana_view").get("all_entity_details")
    with open(output_file_path, 'w') as file:
        file.flush()
        file_and_dicts = prepare_for_propagation_of_sap_hana(client, sap_hana_view_details, file, start, end, import_file_name)
        file = file_and_dicts[0]
        updated_dict_for_string_matches = file_and_dicts[1]
        updated_dict_for_guids_of_a_glossary_term = file_and_dicts[2]
        
        # hardcoded to only prop certain glossary term numbers
        # MODIFY HARDCODED NUMBERS
        file = apply_glossary_terms_and_write_output_of_sap_hana(client, file, updated_dict_for_string_matches,updated_dict_for_guids_of_a_glossary_term, start, end)
        file.flush()
        file.close()
        print("Propagation across SAP HANA in " + short_name + " is complete\n\n")

