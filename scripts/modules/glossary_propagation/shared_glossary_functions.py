##! /usr/bin/env python3


# Function Imports
# ---------------

from utils import get_credentials, create_purview_client
from modules.entity import *

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

def change_key_names(dictionary: dict, key_mapping: dict) -> dict:
    """
    Changes the key names in a dictionary based on a given key mapping.

    Args:
        dictionary (dict): The input dictionary.
        key_mapping (dict): A dictionary containing the mapping of old key names to new key names.

    Returns:
        dict: The dictionary with updated key names.
    """
    new_dict = {}
    for old_key, new_key in key_mapping.items():
        if old_key in dictionary:
            new_dict[new_key] = dictionary[old_key]
        else:
            new_dict[new_key] = None
    return new_dict


def get_all_guids_of_entities_with_glossary_term(glossary_term_name: str, glossary_name: str):
    '''
    Retrieves the GUIDs of entities containing a specific glossary term within a given glossary.

    Parameters:
        glossary_term_name (str): The name of the glossary term.
        glossary_name (str): The name of the glossary.

    Returns:
        list: A list of dictionaries containing the GUIDs with the specified glossary term.
    '''
    json_str = '{"term": "'+ glossary_term_name +'", "glossary": "' + glossary_name + '"}'
    json_obj = json.loads(json_str)
    result = CLIENT.discovery.search_entities(query = glossary_term_name, search_filter=json_obj)

    all_guids_with_glossary_term = []
    mapping = {"id": "guid"}
    for r in result:
        # Change each entity's "id" to "guid" so assignTerms can find the guids of each entity
        updated_dict = change_key_names(r, mapping)
        all_guids_with_glossary_term.append(updated_dict)

    return all_guids_with_glossary_term


def get_all_entitities_with_glossary_term(glossary_term_name: str, glossary_name: str):
    '''
    Retrieves all entities containing a specific glossary term within a given glossary.

    Parameters:
        glossary_term_name (str): The name of the glossary term.
        glossary_name (str): The name of the glossary.

    Returns:
        list: A list of dictionaries representing the entities with the specified glossary term.
    '''
    # NOTE: This grabs the guids of the entities within which columns with glossary terms are,
    #    NOT the column guids
    all_guids = get_all_guids_of_entities_with_glossary_term(glossary_term_name, glossary_name)
    all_entities = []
    for guid_dict in all_guids:
        entities_from_guid = CLIENT.get_entity(guid_dict["guid"])["entities"]
        entity = entities_from_guid[0] # there should just be one entity per guid
        all_entities.append(entity)
    return all_entities


def output_column_names_with_specific_glossary_term(glossary_term_name, column_names_with_glossary_term):
    '''
    Outputs column names with a specific glossary term to a text file.

    Parameters:
        glossary_term_name (str): The name of the glossary term.
        column_names_with_glossary_term (list): List of column names with the specified glossary term.

    Returns:
        None
    '''
    file_path = glossary_term_name + " Column Names.txt"
    with open(file_path, 'w') as file:
        file.write("Glossary Term Name: " + glossary_term_name + "\n")
        file.write("Column Names with this Glossary Term Applied:" + "\n\n")
        for column_name in column_names_with_glossary_term:
            file.write(str(column_name) + '\n')
            print(column_name)


def get_column_names_with_specific_glossary_term(glossary_term_name, glossary_name):
    '''
    Retrieves column names with a specific glossary term within a given glossary.

    Parameters:
        glossary_term_name (str): The name of the glossary term.
        glossary_name (str): The name of the glossary.

    Returns:
        list: A list of column names with the specified glossary term.
    '''
    entities = get_all_entitities_with_glossary_term(glossary_term_name, glossary_name)
    # relationshipAttributes -> columns (list of dicts) -> guid
    guids_of_columns_within_entity = []
    for e in entities:
        relationshipAttributes = e.get("relationshipAttributes")
        columns = relationshipAttributes.get("columns")
        for c in columns:
            guids_of_columns_within_entity.append(c.get("guid"))
    
    column_names_with_glossary_term = []
    column_guids_already_found = []
    for column_guid in guids_of_columns_within_entity:
        column = CLIENT.get_entity(column_guid)
        entity = column.get("entities")[0]
        if entity.get("guid") not in column_guids_already_found:
            column_guids_already_found.append(entity.get("guid"))
            meanings = entity.get("relationshipAttributes").get("meanings") # just use the first entity returned
            for m in meanings:
                if m.get("typeName") == "AtlasGlossaryTerm" and m.get("displayText") == glossary_term_name:
                    column_name = entity.get("attributes").get("name")
                    column_names_with_glossary_term.append(column_name)

    output_column_names_with_specific_glossary_term(glossary_term_name, column_names_with_glossary_term)


def remove_term_from_all_entities(entities_with_glossary_term: list, term_name: str, glossary_name: str):
    '''
    Removes a glossary term from all specified entities.

    Parameters:
        entities_with_glossary_term (list): List of entities with the specified glossary term.
        term_name (str): The name of the glossary term to be removed.
        glossary_name (str): The name of the glossary.

    Returns:
        dict: The result of the removal operation.
    '''
    result = CLIENT.glossary.delete_assignedTerm(entities=entities_with_glossary_term, termName = term_name, glossary_name = glossary_name)
    return result


def output_propagation_results(directory, glossary_term_name, elapsed_time_minutes, matched_strings):
    '''
    Outputs propagation results to a text file.

    Parameters:
        directory (str): The directory to save the results.
        glossary_term_name (str): The name of the glossary term.
        elapsed_time_minutes (float): Elapsed time for propagation in minutes.
        matched_strings (list): List of strings matched during propagation.

    Returns:
        None
    '''
    os.makedirs(directory, exist_ok=True) # Create the directory if it doesn't exist
    file_name = glossary_term_name + ".txt"
    file_path = os.path.join(directory, file_name)

    # Open the file in write mode
    with open(file_path, 'w') as file:
        end_timestamp = datetime.now().strftime("%m/%d/%Y %H:%M")
        file.write("Last propagated on: " + str(end_timestamp) + "\n")
        file.write("Elapsed time to propagate throughout SQL DW Tables: " + str(elapsed_time_minutes) + "\n")
        file.write("Number of columns this term was applied to: " + str(len(matched_strings)) + "\n\n")
        # Write each string from the list to the file, one string per line
        for item in matched_strings:
            file.write(item + '\n')
    print(f"The list has been exported to {file_path}.")


def propagate_glossary_term_by_specific_entity_type(entity_type, glossary_term_name, fields, directory):
    """
    Propagate a glossary term to columns of a specific entity type and the entities themselves based on a regular expression match in their names.

    Args:
        entity_type (str): The specific entity type (e.g., table) to target for glossary term propagation.
        glossary_term_name (str): The name of the glossary term to propagate.
        fields (list): List of field names to match for glossary term propagation.
        directory (str): The directory to output propagation results.

    Returns:
        None
    """
    start_time = time.time()
    regex = re.compile(regex, re.IGNORECASE) # this makes the regex case insensitive
    list_of_guids = get_guids_of_entities_with_specific_type(entity_type)
    matched_strings = []
    for guid in list_of_guids:
        # check the referred entities for a match with the glossary term
        pulled = CLIENT.get_entity(guid)
        referredEntities = pulled.get("referredEntities")
        if len(referredEntities) > 0:
            for key, value in referredEntities.items():
                # RIGHT NOW, JUST MATCHING WITH COLUMN NAMES
                # still need to match with column descriptions, and using table-fields listed in glossary file
                column_name = value.get("attributes").get("name")
                for field in fields:
                    # check with match with column name
                    if field == column_name:
                        # if a match, apply the glossary term to this asset 
                        # AND add the column name to a list of matches for this glossary term
                        print(f"Matched string: {column_name}")
                        matched_strings.append(column_name)

                        # this applies the glossary term to the columns themselves (with the guid:key) and the tables to which
                        #    the columns belong (guid:guid)
                        # IF NOT ATTACHED ALREADY - NEED TO IMPLEMENT TO OPTIMIZE
                        
                        entities = [{"guid": key}, {"guid": guid}]
                        applied_result = client.glossary.assignTerm(entities = entities, termName = glossary_term_name)
                        print(applied_result)

    end_time = time.time()
    elapsed_time_seconds = end_time - start_time
    elapsed_time_minutes = round(elapsed_time_seconds / 60)
    output_propagation_results(directory, glossary_term_name, elapsed_time_minutes, matched_strings)


def propagate_glossary_term_by_specific_entity_type_and_return_string(all_entity_details, client, glossary_term_name, fields, column_type_name):
    '''
    Propagates a glossary term to entities of a specific type and returns relevant information.

    Parameters:
        all_entity_details (list): List of entity details.
        client (object): The Purview client object.
        glossary_term_name (str): The name of the glossary term.
        fields (list): List of fields related to the glossary term.
        column_type_name (str): The type of column.

    Returns:
        list: Elapsed time in seconds and a list of matched strings.
    '''
    start_time = time.time()
    matched_strings = []
    for entry in all_entity_details:
        entity_guid = entry.get("guid")

        # column_type_name = "columns" for azure_sql_dw_table and "view_columns" for sap_hana_view
        if column_type_name == "view_columns":
            columns = entry.get("entity").get("relationshipAttributes").get(column_type_name)
        else:
            columns = entry.get(column_type_name)
        if len(columns) > 0:
            for column in columns:
                column_guid = column.get("guid")
                column_name = column.get("displayText")

                for field in fields:
                    #print("Field: " + field)
                    if len(fields) == 2:
                        print((fields))
                        print()
                    """if field == column_name:
                        print(f"Matched string: {column_name}")
                        matched_strings.append(column_name)

                        #print("column guid: " + str(column_guid))
                        #print("entity guid: " + str(entity_guid))

                        # want to only apply IF NOT ATTACHED ALREADY - NEED TO IMPLEMENT TO OPTIMIZE
                        entities = [{"guid": column_guid}, {"guid": entity_guid}]
                        applied_result = client.glossary.assignTerm(entities = entities, termName = glossary_term_name)
                        print(applied_result)"""

    end_time = time.time()
    elapsed_time_seconds = round(end_time - start_time)
    return [elapsed_time_seconds, matched_strings]


def prod_glossary_propagation_non_sap():
    # This propagates the glossary terms contained in the input file throughout Purview Prod (when NO SAP instances in Prod.)
    # This does not handle SAP in Prod.

    # NOTE: some numbers are hard coded. Currently propagating terms 250-500, despite the file containing 1-500.

    # PROD ACCOUNT
    '''
    Propagates glossary terms in a non-SAP production environment.

    Parameters:
        None

    Returns:
        None
    '''
    REFERENCE_NAME_PURVIEW = "hbi-pd01-datamgmt-pview"
    CREDS = get_credentials(cred_type= 'default')
    client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)
    # pull_entities_from_purview("prod", "hbi-pd01-datamgmt-pview", client)

    input_filename = "prod_pulled_entities.json"
    prod_pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        prod_pulled_entities = json.load(json_file)

    # use the new regex sheet, extract the glossary term name and regex 
    file_path = "1_to_500_Glossary_with_Field_Duplicates_at_End_10.2.23.xlsx"
    glossary_terms_sheet = pd.read_excel(file_path)
    glossary_terms_dict = []
    for index, row in glossary_terms_sheet.iterrows():
        x = {
            "name": row["Nick Name"],
            #"fields": row["Field"].split(",")
            "fields": [field.strip() for field in row["Field"].split(",")]
        }
        glossary_terms_dict.append(x)

    directory = 'glossary propagation outputs'
    output_file_path = "250_to_500_prod_glossary_propagation_results"

    # NOTE: no columns in power bi datasets
    # power_bi_dataset_entities = prod_pulled_entities.get("data_sources").get("powerbi").get("powerbi_dataset").get("all_entity_details")
    sql_dw_table_entities = prod_pulled_entities.get("data_sources").get("azure_sql_dw").get("azure_sql_dw_table").get("all_entity_details")

    with open(output_file_path, 'w') as file:
        file.flush()
        count = 0
        for d in glossary_terms_dict: 
            count += 1

            # NOTE: This just applies terms 250-500 since 1-250 has already been run in non-SAP Prod
            if count >= 501:
                break
            elif count > 250 and count < 501:
                name = d.get("name")
                fields = d.get("fields")

                azure_sql_dw_table_result = propagate_glossary_term_by_specific_entity_type_and_return_string(sql_dw_table_entities, client, name, fields, "columns")
                
                elapsed_time = azure_sql_dw_table_result[0]
                matched_strings = azure_sql_dw_table_result[1]
                
                end_timestamp = datetime.now().strftime("%m/%d/%Y %H:%M")
                
                return_str = "Glossary term: " + name + "\nPropagated in PROD on: " + str(end_timestamp) + "\nElapsed Time (seconds): " + str(elapsed_time) + "\nNumber of matches, then applications: " + str(len(matched_strings)) + "\nGlossary Term Number: " + str(count) + "\n"
                print(return_str)

                file.write(str(return_str))

                for match in matched_strings:
                    file.write(str(match) + '\n') 
                file.write('\n\n')

        file.flush()
        file.close()


def get_glossary_terms_dict(import_file_name):
    '''
    Reads an Excel file and extracts glossary term names and associated fields.

    Parameters:
        import_file_name (str): The name of the Excel file.

    Returns:
        list: A list of dictionaries representing glossary terms and associated fields.
    '''
    # use the new regex sheet, extract the glossary term name and regex 
    #file_path = "1_to_500_Glossary_with_Field_Duplicates_at_End_10.2.23.xlsx"

    glossary_terms_sheet = pd.read_excel(import_file_name)
    glossary_terms_dict = []
    for index, row in glossary_terms_sheet.iterrows():
        if type(row["[Attribute][Business Glossary]System-Table-Field"]) != float:
            x = {
                "name": row["Nick Name"],
                "system-table-field": [field.strip() for field in row["[Attribute][Business Glossary]System-Table-Field"].split(",")]
            }
            glossary_terms_dict.append(x)
                
    return glossary_terms_dict


def read_glossary_import_file(file_name):
    '''
    Reads an Excel file containing glossary terms and their associated fields.

    Parameters:
        file_name (str): The name of the Excel file.

    Returns:
        dict: A dictionary with field names as keys and glossary term names as values.
    '''
    glossary_terms_sheet = pd.read_excel(file_name)
    glossary_dict_with_fields_as_keys = {}
    for index, row in glossary_terms_sheet.iterrows():
        glossary_term_name = row["Nick Name"]
        fields = [field.strip() for field in row["[Attribute][Business Glossary]System-Table-Field"].split(",")]
        for field in fields:
            glossary_dict_with_fields_as_keys[field] = glossary_term_name
    return glossary_dict_with_fields_as_keys


def propagate_all_glossary_terms_across_specific_entity_type(client, all_entity_details, column_type_name, 
                                                             glossary_dict_with_fields_as_keys, dict_for_string_matches, dict_for_guids_of_a_glossary_term):
    '''
    Propagates glossary terms across entities of a specific type and returns relevant information.

    Parameters:
        client (object): The Purview client object.
        all_entity_details (list): List of entity details.
        column_type_name (str): The type of column.
        glossary_dict_with_fields_as_keys (dict): Dictionary with field names as keys and glossary term names as values.
        dict_for_string_matches (dict): Dictionary for storing string matches during propagation.
        dict_for_guids_of_a_glossary_term (dict): Dictionary for storing GUIDs associated with glossary terms.

    Returns:
        list: Elapsed time in seconds, a dictionary of string matches, and a dictionary of GUIDs.
    '''
    start_time = time.time()
    for entity in all_entity_details:
        entity_guid = entity.get("guid")
        entity_name = entity.get("entity").get("attributes").get("name").strip()

        # column_type_name = "columns" for azure_sql_dw_table, "view_columns" for sap_hana_view, and "primary_key_fields" for sap_s4hana_table
        if column_type_name == "view_columns":
            columns = entity.get("entity").get("relationshipAttributes").get(column_type_name)
        elif column_type_name == "primary_key_fields":
            key_fields_columns = entity.get("entity").get("relationshipAttributes").get("primary_key_fields")
            fields_columns = entity.get("entity").get("relationshipAttributes").get("fields") 
            columns = key_fields_columns + fields_columns
        else:
            columns = entity.get(column_type_name)

        if len(columns) > 0:
            for column in columns:
                column_guid = column.get("guid")
                column_name = column.get("displayText")
                system_table_field = "MDG-" + entity_name + "-" + column_name

                #if column_name in glossary_dict_with_fields_as_keys: # changed to now utilize system-table-field
                if system_table_field in glossary_dict_with_fields_as_keys: # changed to now utilize system-table-field
                    # ONLY works with terms 1-500 where no duplicates
                    #glossary_term_name = glossary_dict_with_fields_as_keys[column_name]
                    glossary_term_name = glossary_dict_with_fields_as_keys[system_table_field]
                    #guids = [{"guid": column_guid}, {"guid": entity_guid}]
                    guids = [column_guid, entity_guid]
                    dict_for_guids_of_a_glossary_term[glossary_term_name].extend(guids)
                    dict_for_string_matches[glossary_term_name].append(column_name)

                    #applied_result = client.glossary.assignTerm(entities = entities, termName = glossary_term_name)
                    #print(applied_result)

    end_time = time.time()
    elapsed_time_seconds = round(end_time - start_time)

    return [elapsed_time_seconds, dict_for_string_matches, dict_for_guids_of_a_glossary_term]
 

def delete_term_from_entity_and_columns(view_guid):
    '''
    Deletes a glossary term from a specified view entity and its columns.

    Parameters:
        view_guid (str): The GUID of the view entity.

    Returns:
        None
    '''
    entity_details = CLIENT.get_entity(view_guid).get("entities")[0]
    view_columns = entity_details.get("relationshipAttributes").get("view_columns")
    for c in view_columns:
        column_details = CLIENT.get_entity(c.get("guid")).get("entities")[0]
        if "meanings" in column_details.get("relationshipAttributes"):
            meanings = column_details.get("relationshipAttributes").get("meanings")
            for m in meanings:
                if m.get("typeName") == "AtlasGlossaryTerm":
                    relationshipGuid = m.get("relationshipGuid")
                    delete_result = CLIENT.delete_relationship(relationshipGuid)
                    print(delete_result)
                    print()

    # then delete from main asset too
    meanings = entity_details.get("relationshipAttributes").get("meanings")
    for m in meanings:
        if m.get("typeName") == "AtlasGlossaryTerm":
            relationshipGuid = m.get("relationshipGuid")
            delete_result = CLIENT.delete_relationship(relationshipGuid)
            print(delete_result)
            print()


def pull_sap_s4hana_table_columns_without_glossary_terms(purview_acct_short_name, table_name):
    # ie.  purview_acct_short_name = "prod", table_name = "MARA"
    '''
    Pulls SAP S/4HANA table columns without associated glossary terms.

    Parameters:
        purview_acct_short_name (str): The short name of the Purview account.
        table_name (str): The name of the SAP S/4HANA table.

    Returns:
        None
    '''
    input_filename = purview_acct_short_name + "_pulled_entities.json"
    pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        pulled_entities = json.load(json_file)

    sap_s4hana_table_details = pulled_entities.get("data_sources").get("sap_s4hana").get("sap_s4hana_table").get("all_entity_details")

    for table in sap_s4hana_table_details:
        if table.get("entity").get("attributes").get("name") == table_name:
            table_match = table.get("entity")
            primary_fields = table_match.get("relationshipAttributes").get("primary_key_fields")
            fields = table_match.get("relationshipAttributes").get("fields")

            fields_from_table = []
            for p in primary_fields:
                fields_from_table.append(p.get("displayText"))
            for f in fields:
                fields_from_table.append(f.get("displayText"))
            fields_from_table = list(set(fields_from_table))
            print(len(fields_from_table))


            glossary_dict = get_glossary_terms_dict()
            fields_where_there_are_glossary_terms = []
            for g in glossary_dict:
                for f in g.get("fields"):
                    fields_where_there_are_glossary_terms.append(f)
            fields_where_there_are_glossary_terms = list(set(fields_where_there_are_glossary_terms))
            print(len(fields_where_there_are_glossary_terms))

            fields_without_glossary_terms = []
            for f in fields_from_table:
                if f not in fields_where_there_are_glossary_terms:
                    fields_without_glossary_terms.append(f)

            print(len(fields_without_glossary_terms))
            data = []
            file_path = table_name + "_Fields_Without_Glossary_Terms.xlsx"
            for field_name in fields_without_glossary_terms:
                data.append([field_name])
            
            df = pd.DataFrame(data, columns=["Field"])
            result = df.to_excel(file_path, index=False)
            print(df)


def pull_sap_s4hana_columns_of_table(purview_acct_short_name, table_name):
    # ie.  purview_acct_short_name = "prod", table_name = "MARA"
    '''
    Pulls SAP S/4HANA table columns and writes them to an Excel file.

    Parameters:
        purview_acct_short_name (str): The short name of the Purview account.
        table_name (str): The name of the SAP S/4HANA table.

    Returns:
        None
    '''
    input_filename = purview_acct_short_name + "_pulled_entities.json"
    pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        pulled_entities = json.load(json_file)

    sap_s4hana_table_details = pulled_entities.get("data_sources").get("sap_s4hana").get("sap_s4hana_table").get("all_entity_details")

    for table in sap_s4hana_table_details:
        if table.get("entity").get("attributes").get("name") == table_name:
            table_match = table.get("entity")
            primary_fields = table_match.get("relationshipAttributes").get("primary_key_fields")
            fields = table_match.get("relationshipAttributes").get("fields")

            fields_from_table = []
            for p in primary_fields:
                fields_from_table.append(p.get("displayText"))
            for f in fields:
                fields_from_table.append(f.get("displayText"))
            fields_from_table = list(set(fields_from_table))
            print("There are " + str(len(fields_from_table)) + " columns in the " + table_name + "table")

            data = []
            file_path = table_name + "_Fields.xlsx"
            for field_name in fields_from_table:
                data.append([field_name])
            
            df = pd.DataFrame(data, columns=["Field"])
            result = df.to_excel(file_path, index=False)
            print(df)



def pull_s4_table_columns():
    '''
    Pulls SAP S/4HANA table columns without associated glossary terms for a specified table.

    Parameters:
        None

    Returns:
        None
    '''
    print()
    
    client = CLIENT
    input_filename = "qa_pulled_entities.json"
    qa_pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        qa_pulled_entities = json.load(json_file)

    sap_s4hana_table_details = qa_pulled_entities.get("data_sources").get("sap_s4hana").get("sap_s4hana_table").get("all_entity_details")
    sought_table = "KNVV"

    for table in sap_s4hana_table_details:
        if table.get("entity").get("attributes").get("name") == sought_table:
            grabbed_table = table.get("entity")
            primary_fields = grabbed_table.get("relationshipAttributes").get("primary_key_fields")
            fields = grabbed_table.get("relationshipAttributes").get("fields")

            fields_from_table = []
            for p in primary_fields:
                fields_from_table.append(p.get("displayText"))
            for f in fields:
                fields_from_table.append(f.get("displayText"))
            fields_from_table = list(set(fields_from_table))
            print(len(fields_from_table))


            glossary_dict = get_glossary_terms_dict()
            fields_where_there_are_glossary_terms = []
            for g in glossary_dict:
                for f in g.get("fields"):
                    fields_where_there_are_glossary_terms.append(f)
            fields_where_there_are_glossary_terms = list(set(fields_where_there_are_glossary_terms))
            print(len(fields_where_there_are_glossary_terms))

            fields_without_glossary_terms = []
            for f in fields_from_table:
                if f not in fields_where_there_are_glossary_terms:
                    fields_without_glossary_terms.append(f)

            data = []
            file_path = sought_table + "_fields_without_glossary_terms.xlsx"
            for field_name in fields_without_glossary_terms:
                data.append([field_name])
            
            df = pd.DataFrame(data, columns=["Field"])
            df.to_excel(file_path, index=False)


def extract_fields_for_which_there_are_not_glossary_terms(client):
    '''
    Extracts fields for which there are no associated glossary terms and writes them to an Excel file.

    Parameters:
        client (object): The Purview client object.

    Returns:
        None
    '''
    input_filename = "All_Fields_from_Paola.xlsx"
    # load terms

    fields_sheet = pd.read_excel(input_filename)
    fields_dict = []
    for index, row in fields_sheet.iterrows():
        x = {
            "master_data_category": row["MASTER DATA CATEGORY"],
            "table_name": row["TABLE NAME"],
            "table_description": row["TABLE DESCRIPTION"],
            "column_name": row["COLUMN NAME"],
            "column_id": row["COLUMN ID"],
            "pk": row["PK"],
            "data_type": row["DATA TYPE"],
            "num_distinct": row["NUM DISTINCT"],
            "column_description": row["COLUMN DESCRIPTION"],
            "reptext": row["REPTEXT"],
            "scrtext_s": row["SCRTEXT S"],
            "scrtext_m": row["SCRTEXT M"],
            "scrtext_l": row["SCRTEXT L"]
        }
        fields_dict.append(x)

    glossary_dict = get_glossary_terms_dict()
    fields_where_there_are_glossary_terms = []
    for g in glossary_dict:
        for f in g.get("fields"):
            fields_where_there_are_glossary_terms.append(f)
    fields_where_there_are_glossary_terms = list(set(fields_where_there_are_glossary_terms))
    print(len(fields_where_there_are_glossary_terms))

    fields_without_glossary_terms = []
    for row in fields_dict:
        if row.get("column_name") not in fields_where_there_are_glossary_terms:
            fields_without_glossary_terms.append(row)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(fields_without_glossary_terms)

    # Specify the Excel file path
    excel_file = 'all_fields_without_glossary_terms.xlsx'

    # Write the DataFrame to the Excel file
    df.to_excel(excel_file, index=False)


def unassign_then_delete_glossary_terms(client):
    glossary  = client.glossary.get_glossaries(limit = 1)
    #print(glossary)
    terms = glossary[0].get("terms")
    count = 0
    for term in terms:
        if term.get("displayText") != "Material Number" and term.get("displayText") != "Plant" and term.get("displayText") != "Profit Center":
            count += 1
            print("Term: " + term.get("displayText") + ", Count: " + str(count))
            pulled = client.glossary.get_termAssignedEntities(term.get("termGuid"))
            num_to_unassign = len(pulled)
            if num_to_unassign > 0:
                unassign_result = client.glossary.delete_assignedTerm(entities = pulled, termGuid = term.get("termGuid"))
                print(unassign_result)
                print("Unassigned " + term.get("displayText") + " from " + str(num_to_unassign) + " entities")
         
            else:
                print("Unassigned " + term.get("displayText") + " from 0 entities")
            
            delete_term_result = client.glossary.delete_term(term.get("termGuid"))
            print(delete_term_result)
            print("Deleted term " + term.get("displayText"))
            print("\n\n")


def extract_fields_of_table(client):
    '''
    Extracts fields of a specified table for which there are no associated glossary terms and writes them to an Excel file.

    Parameters:
        client (object): The Purview client object.

    Returns:
        None
    '''
    # pull table from dict
    # pull column names
    # write column names 
    fields_without_glossary_terms = []
    for row in fields_dict:
        if row.get("column_name") not in fields_where_there_are_glossary_terms:
            fields_without_glossary_terms.append(row)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(fields_without_glossary_terms)

    # Specify the Excel file path
    excel_file = 'all_fields_without_glossary_terms.xlsx'

    # Write the DataFrame to the Excel file
    df.to_excel(excel_file, index=False)

