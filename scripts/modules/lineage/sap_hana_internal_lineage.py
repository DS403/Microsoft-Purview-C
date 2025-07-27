##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules import *
from modules.lineage.shared_lineage_functions import *
from pyapacheatlas.core.util import GuidTracker


# Imports
# ---------------

import re
import json
import sys
from pathlib import Path


# Constants
# ---------------
 

# Global
# ---------------

prod_hana_view_qualified_names = []
prod_hana_table_qualified_names = []
prod_dsp_connection_qualified_names = []


# Functions
# ---------------

def parse_dsp_json_of_table(client, path_to_file, table_qualified_name_header_with_schema):
    '''
    Parses a JSON file representing a table in a Data Services Project (DSP) and creates corresponding Atlas entities.

    Parameters:
    - client: The Purview Atlas client for entity creation.
    - path_to_file (str): The file path to the DSP JSON file.
    - table_qualified_name_header_with_schema (str): The header part of the table's qualified name, including the schema.

    Returns:
    None
    '''
    with open(path_to_file, 'r') as json_file:
        json_dict = json.load(json_file)

    table_name =""
    for key in json_dict["definitions"]:
        table_name = key
        break

    #table_qualified_name = "sap_hana://86c39b57-6b4c-4172-a3ac-68fa3b408270.hana.prod-us10.hanacloud.ondemand.com/databases/H00/" + "tables/" + table_name
    table_qualified_name = table_qualified_name_header_with_schema + table_name
    guid_counter = -1002
    guid_tracker = GuidTracker(starting=guid_counter, direction='decrease')
    table_guid = guid_tracker.get_guid()
    table = AtlasEntity(table_name, "sap_hana_table", table_qualified_name, table_guid)

    elements = json_dict["definitions"][table_name]["elements"]
    columns_to_add = []
    for key in elements:
        column_name = key
        column_description = elements[column_name]["@EndUserText.label"]
        column_qualified_name = table_qualified_name + "#" + column_name
        column_guid = guid_tracker.get_guid()
        column = AtlasEntity(column_name, "sap_hana_table_column", column_qualified_name, column_guid, attributes={"type": "str", "userDescription": column_description})
        column.addRelationship(table = table)
        columns_to_add.append(column)

    entities_to_upload = [table] + columns_to_add
    assignments = client.upload_entities(entities_to_upload)
    global prod_hana_table_qualified_names
    prod_hana_table_qualified_names.append(table_qualified_name)
    print("Table Created for: " + table_name + "\n")
    print()



def parse_dsp_json_and_create_table(client, json_dict, table_name, table_qualified_name):
    '''
    Parses a JSON dictionary representing a table in a Data Services Project (DSP) and creates corresponding Atlas entities.

    Parameters:
    - client: The Purview Atlas client for entity creation.
    - json_dict (dict): The dictionary containing the DSP JSON information for the table.
    - table_name (str): The name of the table.
    - table_qualified_name (str): The qualified name of the table.

    Returns:
    None
    '''  
    guid_counter = -1002
    guid_tracker = GuidTracker(starting=guid_counter, direction='decrease')
    table_guid = guid_tracker.get_guid()
    table = AtlasEntity(table_name, "sap_hana_table", table_qualified_name, table_guid)

    elements = json_dict["elements"]
    columns_to_add = []
    for key in elements:
        try:
            column_name = key
            column_description = elements[column_name]["@EndUserText.label"]
            column_qualified_name = table_qualified_name + "#" + column_name
            column_guid = guid_tracker.get_guid()
            column = AtlasEntity(column_name, "sap_hana_table_column", column_qualified_name, column_guid, attributes={"type": "str", "userDescription": column_description})
            column.addRelationship(table = table)
            columns_to_add.append(column)
        except:
            print("Error with Table: " + table_name)

    try:
        entities_to_upload = [table] + columns_to_add
        assignments = client.upload_entities(entities_to_upload)
        print("Table created for: " + table_name + "\n")
        global prod_hana_table_qualified_names
        prod_hana_table_qualified_names.append(table_qualified_name)

    except:
        print("Error with Table: " + table_name)


def parse_dsp_json_and_create_view(client, json_dict, view_name, view_qualified_name):
    '''
    Parses a JSON dictionary representing a view in a Data Services Project (DSP) and creates corresponding Atlas entities.

    Parameters:
    - client: The Purview Atlas client for entity creation.
    - json_dict (dict): The dictionary containing the DSP JSON information for the view.
    - view_name (str): The name of the view.
    - view_qualified_name (str): The qualified name of the view.

    Returns:
    None
    '''  
    guid_counter = -1002
    guid_tracker = GuidTracker(starting=guid_counter, direction='decrease')
    view_guid = guid_tracker.get_guid()
    view = AtlasEntity(view_name, "sap_hana_view", view_qualified_name, view_guid)

    elements = json_dict["elements"]
    columns_to_add = []
    for key in elements:
        try:
            column_name = key
            column_description = elements[column_name]["@EndUserText.label"]
            column_qualified_name = view_qualified_name + "#" + column_name
            column_guid = guid_tracker.get_guid()
            column = AtlasEntity(column_name, "sap_hana_view_column", column_qualified_name, column_guid, attributes={"type": "str", "userDescription": column_description})
            column.addRelationship(view = view)
            columns_to_add.append(column)
        except:
            print("Error with View: " + view_name)

    try:
        entities_to_upload = [view] + columns_to_add
        assignments = client.upload_entities(entities_to_upload)
        print("View Created for: " + view_name + "\n")
        global prod_hana_view_qualified_names
        prod_hana_view_qualified_names.append(view_qualified_name)

    except:
        print("Error with View: " + view_name)


def get_sap_hana_views_with_substring_of_qualified_name(client, entity_type, qualified_name_header):
    '''
    Retrieves SAP HANA views with a substring match in their qualified name.

    Parameters:
    - client: The Purview Atlas client for entity retrieval.
    - entity_type (str): The type of entity to retrieve, e.g., "sap_hana_view".
    - qualified_name_header (str): The substring to match against the qualified names of the entities.

    Returns:
    list: A list of dictionaries representing matching SAP HANA views.
    '''
    browse_result = client.discovery.browse(entityType=entity_type)
    total_search_count = browse_result.get("@search.count")
    if total_search_count == 0:
        return []
    count = 0
    matches = []
    while count < total_search_count:
        browse_result = client.discovery.browse(entityType = entity_type, offset = count)
        entities = browse_result.get("value")
        count += len(entities)
        
        for value_dict in entities:
            if qualified_name_header == value_dict.get("qualifiedName"):
                matches.append(value_dict)
    
    return matches


def find_ref_key(data):
    '''
    Recursively searches for a "ref" key in the provided JSON-like data structure.

    Parameters:
    - data (dict or list): The JSON-like data structure to search.

    Returns:
    str or None: The value of the "ref" key if found, otherwise None.
    '''
    if isinstance(data, dict):
        if "SELECT" in data and "from" in data["SELECT"]:
            from_data = data["SELECT"]["from"]
            if "ref" in from_data:
                return from_data["ref"]
        for key, value in data.items():
            result = find_ref_key(value)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_ref_key(item)
            if result is not None:
                return result
    return None


def extract_schema_from_qualified_name(qualified_name):
    '''
    Extracts the schema name from the given qualified name.

    Parameters:
    - qualified_name (str): The qualified name containing the schema information.

    Returns:
    str: The extracted schema name.
    '''
    result = ""
    if "views" in qualified_name:
        match = re.search(r'schemas/(.*?)/views', qualified_name)
        if match:
            result = match.group(1)
        else:
            print("Pattern not found in the string.")
    else:
        match = re.search(r'schemas/(.*?)/tables', qualified_name)
        if match:
            result = match.group(1)
        else:
            print("Pattern not found in the string.")
    return result


def extract_entity_name_from_qualified_name(qualified_name):
    '''
    Extracts the entity name from the given qualified name.

    Parameters:
    - qualified_name (str): The qualified name containing the entity information.

    Returns:
    str: The extracted entity name.
    '''
    result = ""
    if "views" in qualified_name:
        try:
            parts = qualified_name.split("views/")
            result = parts[1]
            return result
        except:
            print("Error extracting view name.")
    else:
        try:
            parts = qualified_name.split("tables/")
            result = parts[1]
            return result
        except:
            print("Error extracting table name.")


def create_lineage_for_view(client, target_qualified_name, qualified_names_of_sources):
    '''
    Creates lineage connections between a target SAP HANA view and its source entities.

    Parameters:
    - client: The Purview Atlas client for entity retrieval and lineage creation.
    - target_qualified_name (str): The qualified name of the target SAP HANA view.
    - qualified_names_of_sources (list): List of qualified names of source entities.

    Returns:
    None
    '''
    target_schema = extract_schema_from_qualified_name(target_qualified_name)
    for source in qualified_names_of_sources:
        source_schema = extract_schema_from_qualified_name(source)
        source_name = extract_entity_name_from_qualified_name(source)
        target_name = extract_entity_name_from_qualified_name(target_qualified_name)

        source_naming_str = source_schema + "." + source_name + "/"
        target_naming_str = target_schema + "." + target_name + "/"
        process_type_name = "dsp_connection"
        connection_qualified_name = "sources:" + source_naming_str + "targets:" + target_naming_str + "process_type:" + process_type_name
        
        global prod_dsp_connection_qualified_names
        if connection_qualified_name not in prod_dsp_connection_qualified_names:
            if "views" in source:
                source_entity = get_entity_from_qualified_name_using_type(client, source, "sap_hana_view")
            elif "tables" in source:
                source_entity = get_entity_from_qualified_name_using_type(client, source, "sap_hana_table")
            if "views" in target_qualified_name:
                target_entity = get_entity_from_qualified_name_using_type(client, target_qualified_name, "sap_hana_view")
            elif "tables" in target_qualified_name:
                target_entity = get_entity_from_qualified_name_using_type(client, target_qualified_name, "sap_hana_table")
        
            if source_entity == None or target_entity == None:
                print("One of the entities could not be found with that qualified name. Cannot create lineage.")
            elif source_entity.get("qualifiedName") != target_entity.get("qualifiedName"):
                result = add_manual_dsp_lineage(client, source_entity, target_entity, "dsp_connection", source_schema, target_schema)
                print("Lineage built from " + source_name + " to " + target_name)
        else:
            print("Lineage already exists from " + source_name + " to " + target_name)
        

def parse_json_for_sap_hana_view(client, json_file, dsp_header_without_schema, schema):
    '''
    Parses a JSON file containing SAP HANA view information and creates entities accordingly.

    Parameters:
    - client: The Purview Atlas client for entity creation and retrieval.
    - json_file (str): The path to the JSON file containing SAP HANA view information.
    - dsp_header_without_schema (str): The DSP header without schema information.
    - schema (str): The schema to which the views belong.

    Returns:
    None
    '''
    with open(json_file, 'r') as file:
        print("FILE NAME: " + json_file + "\n")
        data = json.load(file)
        definitions = data.get("definitions")
        count = 0
        target_qualified_name = ""
        qualified_names_of_sources = []
        for key, value in definitions.items():
            count += 1
            print("File " + json_file + ", on entity " + str(count) + "\n")
            if "elements" in value:
                entity_name = key
                if "." in key: # means doesn't belong to the same schema
                    split_key = key.split(".")
                    schema = split_key[0]
                    entity_name = split_key[1]
                
                table_search_qual_name = dsp_header_without_schema + schema + "/tables/" + entity_name
                view_search_qual_name = dsp_header_without_schema + schema + "/views/" + entity_name

                global prod_hana_view_qualified_names
                global prod_hana_table_qualified_names
                if view_search_qual_name not in prod_hana_view_qualified_names and table_search_qual_name not in prod_hana_table_qualified_names:
                    if entity_name.startswith("ZV_") or entity_name.startswith("ZC_") or entity_name.startswith("TA_"): 
                        print("Need to create table")
                        parse_dsp_json_and_create_table(client, value, entity_name, table_search_qual_name)
                        if count == 1: # this is the target
                            target_qualified_name = table_search_qual_name
                        else: # these are the sources
                            qualified_names_of_sources.append(table_search_qual_name)

                    elif entity_name.startswith("HL_") or entity_name.startswith("RL_") or entity_name.startswith("IL_"):
                        print("Need to create view")
                        parse_dsp_json_and_create_view(client, value, entity_name, view_search_qual_name)
                        if count == 1: # this is the target
                            target_qualified_name = view_search_qual_name
                        else: # these are the sources
                            qualified_names_of_sources.append(view_search_qual_name)

                elif view_search_qual_name in prod_hana_view_qualified_names:
                    if count == 1: # this is the target
                        target_qualified_name = view_search_qual_name
                    else: # these are the sources
                        qualified_names_of_sources.append(view_search_qual_name)
                elif table_search_qual_name in prod_hana_table_qualified_names:
                    if count == 1: # this is the target
                        target_qualified_name = table_search_qual_name
                    else: # these are the sources
                        qualified_names_of_sources.append(table_search_qual_name)
            
        create_lineage_for_view(client, target_qualified_name, qualified_names_of_sources)
            
                    
def parse_all_views_for_schema(client, directory, dsp_qa_header_without_schema, schema_this_view_belongs_to):
    '''
    Parses all JSON files in a directory containing SAP HANA view information for a specific schema.

    Parameters:
    - client: The Purview Atlas client for entity creation and retrieval.
    - directory (str): The path to the directory containing JSON files.
    - dsp_qa_header_without_schema (str): The DSP QA header without schema information.
    - schema_this_view_belongs_to (str): The schema to which the views belong.

    Returns:
    None
    '''
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            # Process each JSON file
            file_path = os.path.join(directory, filename)
            
            # Pass the file name to your code
            parse_json_for_sap_hana_view(client, file_path, dsp_qa_header_without_schema, schema_this_view_belongs_to)


def create_all_tables_for_schema(client, directory, dsp_header_with_schema):
    '''
    Creates tables for SAP HANA schema based on JSON files in a directory.

    Parameters:
    - client: The Purview Atlas client for entity creation.
    - directory (str): The path to the directory containing JSON files.
    - dsp_header_with_schema (str): The DSP header with schema information.

    Returns:
    None
    '''
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            # Process each JSON file
            file_path = os.path.join(directory, filename)
            
            # Pass the file name to your code
            parse_dsp_json_of_table(client, file_path, dsp_header_with_schema)


def add_manual_dsp_lineage(client, source_entity, target_entity, process_type_name: str, source_schema, target_schema):
    '''
    Adds manual DSP lineage connection between source and target entities.

    Parameters:
    - client: The Purview Atlas client for lineage creation.
    - source_entity (dict): Dictionary representing the source entity.
    - target_entity (dict): Dictionary representing the target entity.
    - process_type_name (str): The name of the DSP process type.
    - source_schema (str): The schema of the source entity.
    - target_schema (str): The schema of the target entity.

    Returns:
    None
    '''
    try:
        sources = []
        targets = []

        source_naming_str = source_schema + "." + source_entity["name"] + "/"
        target_naming_str = target_schema + "." + target_entity["name"] + "/"
        qualified_name = "sources:" + source_naming_str + "targets:" + target_naming_str + "process_type:" + process_type_name

        s = AtlasEntity(
            name = source_entity["name"],
            typeName = source_entity["entityType"],
            qualified_name = source_entity["qualifiedName"],
            guid = source_entity["id"]
        )
        sources.append(s)

        t = AtlasEntity(
            name = target_entity["name"],
            typeName = target_entity["entityType"],
            qualified_name = target_entity["qualifiedName"],
            guid = target_entity["id"]
        )
        targets.append(t)
    
        process = AtlasProcess(
            name = process_type_name,
            typeName = process_type_name,
            qualified_name = qualified_name,
            inputs = sources,
            outputs = targets
        )

        result  = client.upload_entities(
            batch = targets + sources + [process]
        )

        prod_dsp_connection_qualified_names.append(qualified_name)
        return result

    except (KeyError, TypeError) as e:
        raise ValueError("Invalid input. Expected a list of source_entities and target_entities, and a string process_type_name.") from e


def get_existing_prod_sap_hana_view_and_tables_qualified_names():
    '''
    Retrieves the qualified names of existing SAP HANA views and tables from a production data file.

    Returns:
    None
    '''
    input_filename = "prod_pulled_entities.json"
    prod_pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        prod_pulled_entities = json.load(json_file)
    sap_hana_view_details = prod_pulled_entities.get("data_sources").get("sap_hana").get("sap_hana_view").get("all_entity_details")
    sap_hana_table_details = prod_pulled_entities.get("data_sources").get("sap_hana").get("sap_hana_table").get("all_entity_details")

    global prod_hana_view_qualified_names
    prod_hana_view_qualified_names = []
    for view in sap_hana_view_details:
        prod_hana_view_qualified_names.append(view.get("entity").get("attributes").get("qualifiedName"))

    global prod_hana_table_qualified_names
    prod_hana_table_qualified_names = []
    for table in sap_hana_table_details:
        prod_hana_table_qualified_names.append(table.get("entity").get("attributes").get("qualifiedName"))


def get_existing_prod_dsp_connection_qualified_names():
    '''
    Retrieves the qualified names of existing DSP connections from a production data file.

    Returns:
    None
    '''
    input_filename = "prod_pulled_lineage_connections.json"
    prod_pulled_lineage_connections = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        prod_pulled_lineage_connections = json.load(json_file)
    
    dsp_connection_lineage_connections = prod_pulled_lineage_connections.get("lineage_connections").get("dsp_connection").get("all_entity_details")
    global prod_dsp_connection_qualified_names
    prod_dsp_connection_qualified_names = []
    for connection in dsp_connection_lineage_connections:
        connection_qualified_name = prod_dsp_connection_qualified_names.append(connection.get("entity").get("attributes").get("qualifiedName"))
        prod_dsp_connection_qualified_names.append(connection_qualified_name)

    prod_dsp_connection_qualified_names = list(set(prod_dsp_connection_qualified_names))


def parse_sap_hana_internal_lineage():
    '''
    Main function to parse SAP HANA internal lineage, create entities, and build lineage connections.

    Returns:
    None
    '''
    get_existing_prod_sap_hana_view_and_tables_qualified_names()
    get_existing_prod_dsp_connection_qualified_names()

    schema_this_view_belongs_to = "TD_STG"
    dsp_qa_header = "sap_hana://6d3e383d-90d7-45f3-a678-0a9a4dc5d562.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/" + schema_this_view_belongs_to + "/tables/" 
    
    #create_all_tables_for_schema(directory, dsp_qa_header)
    
    dsp_qa_header_without_schema = "sap_hana://6d3e383d-90d7-45f3-a678-0a9a4dc5d562.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/"
    views_path = "dsp_sap_hana_lineage_input_files/FIN_REP/FIN_REP_Views/"
    file_name = views_path + "RL_FIN_FIGL.json"
    schema_this_view_belongs_to = "FIN_REP"
    file_path = ""
    #parse_json_for_sap_hana_view(client, file_name, dsp_qa_header_without_schema, schema_this_view_belongs_to)

    # RUN BELOW FOR VIEW CREATION
    # BELOW IS QA!!
    #schema_this_view_belongs_to = "TD_STG"
    #directory = "dsp_sap_hana_lineage_input_files/TD_STG/TD_STG_Views/"
    dsp_prod_header_with_schema = "sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/"  + schema_this_view_belongs_to + "/views/" 

    dsp_qa_header_without_schema = "sap_hana://6d3e383d-90d7-45f3-a678-0a9a4dc5d562.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/"
    #parse_all_views_for_schema(client, directory, dsp_qa_header_without_schema, schema_this_view_belongs_to)
    
    schema_this_view_belongs_to = "FIN_REP"  # did FIN_REP 10/30  # running OTC_REP, TD_STG
    directory = "dsp_sap_hana_lineage_input_files/" + schema_this_view_belongs_to + "/" + schema_this_view_belongs_to + "_Views/"
    dsp_prod_header_without_schema = "sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/" 

    parse_all_views_for_schema(prod_client, directory, dsp_prod_header_without_schema, schema_this_view_belongs_to)

    # RUN BELOW FOR TABLE CREATION
    # BELOW IS PROD!!!
    """ 
    schema_this_view_belongs_to = "FIN_REP"
    dsp_prod_header_with_schema = "sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/"  + schema_this_view_belongs_to + "/tables/" 
    directory = "dsp_sap_hana_lineage_input_files/" + schema_this_view_belongs_to + "/" + schema_this_view_belongs_to + "_Tables/"
    
    create_all_tables_for_schema(prod_client, directory, dsp_prod_header_with_schema)
    """
