##! /usr/bin/env python3

# Function Imports
# ---------------

from modules.entity import *
from modules.lineage.shared_lineage_functions import *
import requests
from pyapacheatlas.core.util import AtlasException
from typing import List
# Imports
# ---------------

import os
import pandas as pd
import xml.etree.ElementTree as ET

# Constants
# ---------------


# Functions
# ---------------

def get_sources_from_xml(file_path):
    """
    Parses an XML file to extract source and target details.

    This function processes an XML file, searches for elements with the tags 'SOURCE' or 'TARGET', and extracts 
    relevant attributes into a list of dictionaries.

    Parameters:
        file_path (str): The path to the XML file containing source and target details.

    Returns:
        list of dict: A list of dictionaries where each dictionary contains details about a source or target. 
                      Each dictionary has the following keys:
                      - "table": The name of the table.
                      - "server": The name of the database server.
                      - "schema": The name of the schema.
    """
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    sources = []
    
    for folder in root.findall('.//FOLDER'):
        for elem in folder:
            # Check if the element is a SOURCE
            if elem.tag == 'SOURCE' or elem.tag == 'TARGET':
                elem_dict = {
                    "table": elem.attrib.get('NAME'),
                    "server": elem.attrib.get('DBDNAME'),
                    "schema": elem.attrib.get('OWNERNAME')
                }
                #    <SOURCE BUSINESSNAME ="" DATABASETYPE ="Oracle" DBDNAME ="slbadw" DESCRIPTION ="" NAME ="SLBA_ITEM" OBJECTVERSION ="1" OWNERNAME ="STAGING" VERSIONNUMBER ="1">

                sources.append(elem_dict)

    return sources


def load_connection_name_details(excel_file_path):
    """
    Loads connection details from an Excel file into a dictionary.

    This function reads an Excel file and constructs a dictionary mapping each connection name to its server details. 

    Parameters:
        excel_file_path (str): The path to the Excel file containing connection details.

    Returns:
        dict: A dictionary where the keys are connection names and the values are dictionaries containing 
              server details. Each server details dictionary includes:
              - "Server name": The name of the server.
              - "Database name": The name of the database.
    """
    df = pd.read_excel(excel_file_path)
    # Create a dictionary with Connection Name as the key and server details as the value
    connection_map = df.set_index('Connection Name').to_dict(orient='index')
    return connection_map

def get_connection_names_from_xml(file_path):
    """
    Extracts CONNECTION NAME values from an XML file and associates them with session names.

    This function processes an XML file to find CONNECTION NAME attributes and maps them to their corresponding 
    session names (SINSTANCENAME). It prints each connection name as it is found.

    Parameters:
        file_path (str): The path to the XML file containing session and connection details.

    Returns:
        dict: A dictionary where the keys are CONNECTION NAME values and the values are lists of session names 
              (SINSTANCENAME) associated with each CONNECTION NAME.

    Note:
        This function prints each connection name as it is discovered in the XML file.
    """

    tree = ET.parse(file_path)
    root = tree.getroot()
    connection_names = {}

    for session in root.findall('.//SESSION'):
        for session_extension in session.findall('.//SESSIONEXTENSION'):
            session_name = session_extension.get('SINSTANCENAME')
            for connection_ref in session_extension.findall('.//CONNECTIONREFERENCE'):
                conn_name = connection_ref.get('CONNECTIONNAME')
                if conn_name:
                    #print(f"Connection name found: {conn_name}")  # Added print statement
                    if conn_name not in connection_names:
                        connection_names[conn_name] = []
                    connection_names[conn_name].append(session_name)
    
    return connection_names

def get_targets_from_connection_names(excel_file_path, xml_file_path):
    """
    Maps connection names to target details by combining information from an Excel file and an XML file.

    This function uses connection details from an Excel file and connection names from an XML file to create 
    a list of targets with their respective server and schema details.

    Parameters:
        excel_file_path (str): The path to the Excel file containing connection details.
        xml_file_path (str): The path to the XML file containing connection names.

    Returns:
        list of dict: A list of dictionaries where each dictionary contains details about a target. Each dictionary 
                      has the following keys:
                      - "table": The list of session names associated with the connection.
                      - "server": The server name associated with the connection.
                      - "schema": The database schema associated with the connection.
    """
    # Load connection details from the Excel file
    connection_excel_details = load_connection_name_details(excel_file_path)
    
    # Extract CONNECTION NAME values from the XML file
    connection_names = get_connection_names_from_xml(xml_file_path)

    # Map connection names to server details
    targets = []
    for conn_name in connection_names:
        table_names = connection_names.get(conn_name)
        for table in table_names:
            if conn_name in connection_excel_details:
                #print("conn_name:", conn_name) #FIXME: failing here for FINCON
                # Pull the excel mapping details 
                server_details = connection_excel_details.get(conn_name)
                elem_dict = {
                        "table": table,
                        "server": server_details.get("Server name"),
                        "schema": server_details.get("Database name")
                    }
            elif conn_name.lower() == "slbadw" or conn_name.lower() == "slba" or conn_name.lower() == "slbadw_prd":
                # Hardcode the oakdwhp1 slba schema values
                elem_dict = {
                        "table": table,
                        "server":"oakdwhp1",
                        "schema": "SLBA"
                    }
            else:
                continue
            
            # Add each target to the list
            targets.append(elem_dict)

    return targets


def get_qualified_names_for_xml_elements(elements):
    """
    Constructs fully qualified names for XML elements based on server type.

    This function generates qualified names for sources and targets based on their server type. It builds URLs 
    with server-specific formats and removes any prefixes from table names as needed.

    Parameters:
        elements (list of dict): A list of dictionaries where each dictionary contains details about a source or 
                                 target. Each dictionary has the following keys:
                                 - "table": The name of the table.
                                 - "server": The name of the database server.
                                 - "schema": The name of the schema.

    Returns:
        list of str: A list of fully qualified names for each element, formatted according to the server type.
    """
    qualified_names = []
    for elem in elements:
        # Pull the server name
        server = elem.get("server")

        # Handle instances where no server was detected or server is not a string or it's a flat file
        if server is None or not isinstance(server, str) or server.lower() in ["flat_file", "flat file"]:
            continue

        # The XMLs for this server prepend LKP_ or SQ_ to the table name
        table_name = elem.get("table")
        prefixes = ["LKP_", "SQ_"] # looping instead of replace in case one of the prefixes is in the actual table name
        for prefix in prefixes:
            if table_name.startswith(prefix):
                table_name = table_name[len(prefix):]
        
        qual_name = None  # Initialize qual_name to None
        
        '''QA MAPPING'''
        # if server.lower() == "sqlpag19":
        #     qual_name = "mssql://10.1.70.20:1433/MSSQLSERVER/" + elem.get("schema") + "/" + table_name
        # elif server.lower() == "prod1":
        #     qual_name = "oracle://10.1.17.242/" + elem.get("schema") + "/" + table_name
        # elif server.lower() == "prod5":
        #     qual_name = "oracle://10.1.17.242/" + elem.get("schema") + "/" + table_name
        # elif server.lower() == "slbadw" or server.lower() == "slba" or server.lower() == "slbadw_prd":
        #     qual_name = "oracle://10.1.17.241/SLBA/" + table_name
        # elif server.lower() == "oakdwhp1":
        #     qual_name = "oracle://10.1.17.241/" + elem.get("schema") + "/" + table_name
        # else:
        #     print(f"NEW SERVER: {server}")

        """ PROD MAPPING"""
        if server.lower() == "sqlpag19":
            qual_name = "mssql://10.1.70.20:1433/MSSQLSERVER/" + elem.get("schema") + "/" + "dbo" + "/" + table_name #FIXME: dbo had to be hardcoded to build succesful connection asit is not present in the XML
        elif server.lower() == "wsbip3sqlv":
            qual_name = "mssql://wsbip3sqlv.res.hbi.net/MSSQLSERVER/" + "POS" + "/" + elem.get("schema") + "/" + table_name #FIXME: something needs to be hardcoded for it to work
        elif server.lower() == "bipaosql":
            qual_name = "mssql://bipaosql.res.hbi.net/MSSQLSERVER/" + elem.get("schema") + "/" + "dbo" + "/" + table_name ##FIXME: something needs to be hardcoded for it to work
        elif server.lower() == "prod1" or server.lower() == "tprod1":
            qual_name = "oracle://10.1.17.190/" + elem.get("schema") + "/" + table_name
        elif server.lower() == "prod5":
            qual_name = "oracle://10.1.17.28/" + elem.get("schema") + "/" + table_name
        elif server.lower() == "slbadw" or server.lower() == "slba" or server.lower() == "slbadw_prd":
            qual_name = "oracle://10.1.17.127/SLBA/" + table_name
        elif server.lower() == "oakdwhp1":
            qual_name = "oracle://10.1.17.127/" + elem.get("schema") + "/" + table_name
        elif server.lower() == "prod4d":
            qual_name = "oracle://10.1.17.106/" + elem.get("schema") + "/" + table_name
        elif server.lower() == "lawprod" or server.lower() == "lawp2":
            qual_name = "oracle://10.1.17.126/" + elem.get("schema") + "/" + table_name
        else:
            print(f"NEW SERVER: {server}\n")

        

        if qual_name is not None:
            qualified_names.append(qual_name)
    
    return qualified_names


def get_informatica_entities_by_qualified_names(client, qualified_names_list):
    entities = []
    for qualified_name in qualified_names_list:
        if "oracle" in qualified_name:
            # Search for the first entity of type "oracle_view"
            view_entities = get_entity_from_qualified_name_using_type(client, qualified_name, "oracle_view")
            if view_entities is not None:
                entity = next(view_entities, None)
            else:
                entity = None
            
            # If no entity found in "oracle_view", search for "oracle_table"
            if entity is None:
                table_entities = get_entity_from_qualified_name_using_type(client, qualified_name, "oracle_table")
                if table_entities is not None:
                    entity = next(table_entities, None)
                else:
                    entity = None
        else:
            # Search for the first entity from get_entity_from_qualified_name
            entities_gen = get_entity_from_qualified_name(client, qualified_name)
            if entities_gen is not None:
                entity = next(entities_gen, None)
            else:
                entity = None
        
        if entity is not None:
            entities.append(entity)


    return entities


def parse_informatica_xml_export(client, excel_file_path, xml_file_path):
    """
    Parses an XML export from Informatica and builds lineage between sources and targets.

    This function reads an XML file to get source and target information, constructs fully qualified names for each, 
    retrieves entity details using those names, and then builds lineage relationships between sources and targets.

    Parameters:
        client: An instance of the client used to interact with the lineage or metadata repository.
        excel_file_path (str): The path to the Excel file containing connection details.
        xml_file_path (str): The path to the XML file containing source and target information.

    Returns:
        None: This function does not return a value but prints the results of the lineage addition operations.
    """
    # Separate the XML export into sources and targets
    sources = get_sources_from_xml(xml_file_path)
    print("sources:", sources, "\n")
    targets = get_targets_from_connection_names(excel_file_path, xml_file_path)
    print("targets:", targets, "\n")

    # Based on the server details, craft a qualified name for each of the sources and targets
    source_qualified_names = get_qualified_names_for_xml_elements(sources) #FIXME: failing here
    target_qualified_names = get_qualified_names_for_xml_elements(targets)

    # Check if source_qualified_names is empty
    if not source_qualified_names:
        print("Source_qualified_names not fetched, server None or falt file!\n")
        return "Source_qualified_names not fetched, server None or falt file!\n"
    # Using the qualified names, pull the Purview details for each entity
    source_entities = []
    target_entities = []
    #source_entities = get_informatica_entities_by_qualified_names(client, source_qualified_names)
    #target_entities = get_informatica_entities_by_qualified_names(client, target_qualified_names)
    """for source_qual_name in source_qualified_names:
        entity = get_entity_from_qualified_name(client, source_qual_name)
        if entity is not None:
            if entity["entityType"] == "oracle_synonym":
                entity["entityType"] = "oracle_table"
            source_entities.append(entity)"""
    
    for source_qual_name in source_qualified_names:
        
        entity = get_entity_from_qualified_name(client, source_qual_name)
        if entity is not None:
            source_entities.append(entity)
            print("Source Found! source_qual_name: " + source_qual_name)
        else:
            print("Source not found!", source_qual_name)
# TODO: to check if target_qualifiendname is empty. Result: Not empty
    for target_qual_name in target_qualified_names:
        
        entity = get_entity_from_qualified_name(client, target_qual_name) #FIXME: entity is empty for QA
        if entity is not None:
            target_entities.append(entity)
            print("Target Found! target_qual_name: " + target_qual_name)
        else:
            print("Target not found!", target_qual_name)
    
    # Check for a list of empty targets
    if target_entities == []:
        print("Empty targets!")
        return "Empty targets!"

    # Iterate through each of the sources and build lineage to each of the targets
    for source_entity in source_entities:
        for target_entity in target_entities:
            # Scenario 1: Skip if source and target are the same entity
            if source_entity["id"] == target_entity["id"]:
                print("Skipping Scenario 1: Source and Target are the same.")
                continue

            # Scenario 2: Source is not oracle_synonym, Target is oracle_synonym
            if source_entity["entityType"] != "oracle_synonym" and target_entity["entityType"] == "oracle_synonym":
                print("Scenario 2: Target is oracle_synonym.")
                upload_relationships(client, source_entity["id"], target_entity["id"])

            # Scenario 3: Source and Target are anything other than oracle_synonym
            elif source_entity["entityType"] != "oracle_synonym" and target_entity["entityType"] != "oracle_synonym":
                try:
                    result = add_manual_lineage(client, [source_entity], [target_entity], "Informatica_Connection")
                    if result is not None:
                        print("Scenario 3: Connections successfully built: \n\n", result)
                    else:
                        print("Scenario 3: Lineage not added!")
                except Exception as e:
                    print(f"Error adding lineage from {source_entity['qualifiedName']} to {target_entity['qualifiedName']}: {e}")
                print("\n\n")

            # Scenario 4: Both source and target are different and are oracle_synonym
            elif (source_entity["entityType"] == "oracle_synonym" and target_entity["entityType"] == "oracle_synonym" and source_entity["id"] != target_entity["id"]):
                print("Scenario 4: Both source and target are different and are oracle_synonym.")
                upload_relationships(client, source_entity["id"], target_entity["id"])

            # Scenario 5: Source is oracle_synonym, Target is anything other than oracle_synonym
            elif source_entity["entityType"] == "oracle_synonym" and target_entity["entityType"] != "oracle_synonym":
                print(f"Scenario 5: Uploading relationship between {source_entity['qualifiedName']} and {target_entity['qualifiedName']}")
                upload_relationships(client, source_entity["id"], target_entity["id"])

            else:
                print("\nScenario 6: Skipping unknown scenario\n\n")


def build_mass_lineage_for_folders(client, connection_names_excel, directories):
    """
    Builds lineage for XML export files located in specified directories.

    This function iterates through each file in the given directories, parses each XML file to extract and build 
    lineage information, and then processes the files using the `parse_informatica_xml_export` function.

    Parameters:
        client: An instance of the client used to interact with the lineage or metadata repository.
        connection_names_excel (str): The path to the Excel file containing connection details.
        directories (list of str): A list of directory paths containing XML export files.

    Returns:
        None: This function does not return a value but processes each XML file to build lineage.
    """
    # Iterate through each directory and each file in the directory
    for directory_path in directories:
        for filename in os.listdir(directory_path):
            # Construct the full file path
            file_path = os.path.join(directory_path, filename)
            
            # Check if it's a file (and not a directory)
            if os.path.isfile(file_path):
                print(file_path + "\n")
                parse_informatica_xml_export(client, connection_names_excel, file_path)

def upload_relationships(client, entity_a_guid: str, entity_c_guid: str):
    rel_type = "oracle_synonym_source_synonym"
    # Create the relationship as a dictionary with the correct structure
    relationship = {
            "typeName": rel_type,
            "attributes": {},  # You can add any relevant attributes here if needed
            #"guid": -1,  # Set to -1 or remove it if not needed
            "end1": {
                "guid": entity_a_guid
            },
            "end2": {
                "guid": entity_c_guid
            }
        }
    try:
        response = client.upload_relationship(relationship)
        print(f"Successfully added relationship '{rel_type}' between {entity_a_guid} and {entity_c_guid}.")
        print(f"Response: {response}")
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 409:
            # Handle the conflict when the relationship already exists
            print(f"Relationship '{rel_type}' already exists between {entity_a_guid} and {entity_c_guid}.")
        else:
            # Re-raise the exception for other HTTP errors
            raise
    except AtlasException as atlas_err:
        print(f"AtlasException occurred: {str(atlas_err)}")