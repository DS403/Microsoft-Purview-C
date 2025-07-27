##! /usr/bin/env python3

# Function Imports
# ---------------

from utils import get_credentials, create_purview_client
from pyapacheatlas.core import AtlasEntity
from pyapacheatlas.core.entity import AtlasEntity, AtlasProcess
from pyapacheatlas.core.typedef import EntityTypeDef, AtlasAttributeDef
from pyapacheatlas.readers import ExcelConfiguration,ExcelReader

# Imports
# ---------------

import pandas as pd
import json
from pathlib import Path
import os
import re

# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
qa_client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)

REFERENCE_NAME_PURVIEW = "hbi-pd01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
prod_client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)

def build_lineage_using_guids(client, source_guid, source_type, target_guid, target_type, process_type):
    '''
    Builds lineage between two assets using their GUIDs.

    Parameters:
        client (object): The client object for accessing the metadata service.
        source_guid (str): The GUID of the source asset.
        source_type (str): The type of the source asset.
        target_guid (str): The GUID of the target asset.
        target_type (str): The type of the target asset.
        process_type (str): The type of the process.

    Returns:
        None
    '''

    source_entity = client.get_entity(source_guid).get("entities")[0].get("attributes")
    target_entity = client.get_entity(target_guid).get("entities")[0].get("attributes")
    process_type_name = process_type

    s = AtlasEntity(
        name = source_entity.get("name"),
        typeName = source_type, 
        qualified_name = source_entity.get("qualifiedName"),
        guid = source_guid
    )
    source_naming_str = s.name.replace(" ", "_") + "/" 

    t = AtlasEntity(
        name = target_entity.get("name"),
        typeName = target_type,
        qualified_name = target_entity.get("qualifiedName"),
        guid = target_guid
    )
    target_naming_str = t.name.replace(" ", "_") + "/"

    process = AtlasProcess(
        name = process_type_name,
        typeName = process_type_name,
        qualified_name = "sources:" + source_naming_str + "targets:" + target_naming_str + "process_type:" + process_type_name,
        inputs = [s],
        outputs = [t]
    )

    result  = client.upload_entities(
        batch = [t] + [s] + [process]
    )

    print("Lineage built between " + source_entity["name"] + " and " + target_entity["name"])

def build_lineage_from_data_lake_stage_to_curated(client, stage_guid, curated_guid):
    '''
    Builds lineage from a data lake stage asset to a data lake curated asset.

    Parameters:
        client (object): The client object for accessing the metadata service.
        stage_guid (str): The GUID of the data lake stage asset.
        curated_guid (str): The GUID of the data lake curated asset.

    Returns:
        None
    Build lineage from a data lake stage asset to a data lake curated asset.
    '''
    stage_type = "azure_datalake_gen2_path"
    curated_type = "azure_datalake_gen2_path"
    process_type_name = "DL_Stage_to_DL_Curated"
    build_lineage_using_guids(client, stage_guid, stage_type, curated_guid, curated_type, process_type_name)


def get_guid_from_qualified_name(client,qualified_names):
    type_Name='azure_datalake_gen2_path'
    try:
        result=client.get_entity(qualifiedName=qualified_names,typeName=type_Name)
        # Extracting GUIDs
        guids = [entity['guid'] for entity in result['entities']]
    except Exception as e:
        #print(e)
        #print("Check the qualified name exists or not")
        guids=''

    return guids

def fetch_all_curated_guids(client,client_type,entityType):
    limit = 10000  # Maximum allowed limit per request
    all_results = []
    offset = 0
    data=client.discovery.browse(entityType=entityType)
    total_results = data.get('@search.count')
    while offset < total_results:
        response = client.discovery.browse(entityType=entityType, limit=limit, offset=offset)
        entities = response["value"]  # Adjust according to the structure of your response
        
        if not entities:
            break  # Exit loop if no more data is returned
        
        all_results.extend(entities)
        offset += limit
    if client_type.lower()=='prod':
        filtered_data = [
        item for item in all_results
        if item["qualifiedName"].startswith("https://hbipd01analyticsdls.dfs.core.windows.net/curated")
        ]
    elif client_type.lower()=='qa':
        filtered_data = [
        item for item in all_results
        if item["qualifiedName"].startswith("https://hbiqa01analyticsdls.dfs.core.windows.net/curated")
        ]
    filtered_result = [
    item for item in filtered_data
    if not any(exclusion in item["qualifiedName"] for exclusion in ["_delta_log", "Ingest", "Archive"])
    ]
    # Fetch all the ids
    curated_guids = [item['id'] for item in filtered_result]

    return curated_guids

def stage_qualified_name(client_type, paths):
    if client_type.lower()=='qa':
        base_url = 'https://hbiqa01analyticsdls.dfs.core.windows.net' 
    elif client_type.lower()=='prod':
        base_url = 'https://hbipd01analyticsdls.dfs.core.windows.net'
    # Replace '/mnt' with the base_url and ensure each path ends with '/'
    qualified_name = [path.replace("/mnt", base_url) + "/" if not path.endswith("/") else path.replace("/mnt", base_url) for path in paths]
    
    return qualified_name

# Function to clean table names (remove prefix like 'stage.')
def clean_table_name(table_name):
    # Remove any prefix and return the core table name
    return table_name.split('.')[-1]

def search_stage_sql_files(cleaned_table_names):
    stage_dir = r"C:\Users\Sravanthi.Dasam\Desktop\github\Purview\scripts\inputs\BIDW\Databricks\01\Workflows\Schema\Staging"

    # List all files in the specified directory
    files = os.listdir(stage_dir)

    Stage_Extracted_path = []

    for table_name in cleaned_table_names:
        found = False
        
        for sql_file in files:
            if sql_file.lower().endswith('.sql'):
                file_path = os.path.join(stage_dir, sql_file)

                # Read the file content
                with open(file_path, 'r') as file:
                    file_content = file.read()

                # Check if the table name is mentioned in the file content
                if table_name.lower() in file_content.lower():
                    found = True
                    # Regular expression to find the path after LOCATION
                    location_pattern = re.compile(r"LOCATION\s+'([^']+)'", re.IGNORECASE)

                    # Search for the pattern in the SQL content
                    location_match = location_pattern.search(file_content)

                    if location_match:
                        location_path = location_match.group(1)
                        Stage_Extracted_path.append(location_path)
                        break  # Stop checking once a match is found
                    else:
                        print(f"No LOCATION path found in file '{sql_file}'.")

        if not found:
            print(f"No match found for table '{table_name}' in any file.")

    return Stage_Extracted_path

def search_curated_sql_files(client,client_type,guid):
    #fetch_display_name_from_curated_guid
    result=client.get_entity(guid)
    display_name = result["entities"][0]["displayText"]
    #print(display_name)
    # Base directory
    curated_dir = r"C:\Users\Sravanthi.Dasam\Desktop\github\Purview\scripts\inputs\BIDW\Databricks\01\Workflows\Pipelines\Curated"

    # Construct the path to the target directory
    target_dir = os.path.join(curated_dir, display_name, "Dependencies")

    # Check if the target directory exists
    if os.path.exists(target_dir) and os.path.isdir(target_dir):
        # List all files in the Dependencies folder
        files = os.listdir(target_dir)
        
        # Filter for SQL files
        sql_files = [f for f in files if f.endswith(".sql")]
        
        # If SQL files are found, read them
        for sql_file in sql_files:
            sql_file_path = os.path.join(target_dir, sql_file)
            
            # Open and read the SQL file
            with open(sql_file_path, 'r') as file:
                sql_content = file.read()

                # Remove single-line comments that start with -- or -- MAGIC
                sql_content = re.sub(r'--.*', '', sql_content)

                # Remove multi-line comments (/* */)
                sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
                
                # Extract table name after FROM and JOIN clauses            
                table_pattern = re.compile(r'(FROM|JOIN)\s+(stage\.[^\s;)]+)', re.IGNORECASE)
                
                tables = table_pattern.findall(sql_content)
                
                # Extract and print the table names that match 'stage.'
                stage_tables = [match[1] for match in tables]
                
                unique_list = [clean_table_name(name) for name in stage_tables]
                cleaned_table_names = list(set(unique_list))
                if len(cleaned_table_names)==0:
                    #print("No Stage tables found")
                    Stage_guids='No Stage tables found'
                else:
                    #print("Stage tables found:",cleaned_table_names)
                    paths=search_stage_sql_files(cleaned_table_names)
                    #print("Stage location found:", paths)

                    qualified_names=stage_qualified_name(client_type,paths)
                    #print("Stage qualified_names found:", qualified_names) 

                    Stage_guids=get_guid_from_qualified_name(client,qualified_names)  
                    #print("Stage GUIDs:",Stage_guids)
    else:
        #print(f"The directory {target_dir} does not exist.")
        Stage_guids='Does not exist'
    
    return Stage_guids


def get_curated_stage_guid(client, client_type, entityType):
    # Fetch all guids
    data = fetch_all_curated_guids(client, client_type, entityType)
    
    # Initialize the result dictionary
    curated_stage_guid = {}
    
    # Iterate over each guid in the data
    for guid in data:
        # Generate the stage_guid list for each guid
        stage_guid = search_curated_sql_files(client, client_type, guid)
        
        # Assign the stage_guid list to the corresponding guid in the result dictionary
        curated_stage_guid[guid] = stage_guid
    
    # Define values to be removed
    values_to_remove = {"Does not exist", "No Stage tables found", ""}

    # Remove entries with specified values, handling lists separately
    filtered_data = {
        k: v for k, v in curated_stage_guid.items()
        if not (isinstance(v, str) and v in values_to_remove)
    }

    return filtered_data

def build_stage_curated_lineage(client,client_type):
    filtered_data=get_curated_stage_guid(client,client_type,entityType='azure_datalake_gen2_path')
    # Loop through each key-value pair in the dictionary
    for curated_guid, stage_guids in filtered_data.items():
        for stage_guid in stage_guids:
            build_lineage_from_data_lake_stage_to_curated(client, stage_guid, curated_guid)

result=get_curated_stage_guid(qa_client,'qa',entityType='azure_datalake_gen2_path')
  