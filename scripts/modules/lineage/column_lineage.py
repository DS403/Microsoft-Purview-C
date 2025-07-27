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

def get_all_column_from_guid(client,asset_name,source_type_name,source_guid,source_qualified_name,target_type_name,target_guid,target_qualified_name):
    """
    Fetches column details from source and target entities using their GUIDs,
    then creates an Excel file with 'UpdateLineage' and 'ColumnMapping' sheets.

    Args:
    - client: The client object for accessing entity details.
    - asset_name (str): Name of the asset or dataset.
    - source_type_name (str): Type name of the source entity.
    - source_guid (str): GUID of the source entity.
    - source_qualified_name (str): Qualified name of the source entity.
    - target_type_name (str): Type name of the target entity.
    - target_guid (str): GUID of the target entity.
    - target_qualified_name (str): Qualified name of the target entity.
    """

    # Define the file path dynamically
    file_path = f"./ColumnMapping/{asset_name}_ColumnMapping.xlsx"
    # Define column data

    source_details = client.get_entity(guid=source_guid)
    source_col = [entity['displayText'] for entity in source_details['referredEntities'].values()]
    source_columns = sorted(source_col)

    target_details = client.get_entity(guid=target_guid)
    target_col = [entity['displayText'] for entity in target_details['referredEntities'].values()]  
    target_columns = sorted(target_col) 

    process_qualified_name="sources:" + asset_name + "/targets:" + asset_name + "/process_type:Column_Connection"
    process_type_name='Column_Connection'
    process_name='Column Lineage'

    # Find matched columns and extra columns
    matched_columns = [(col, col) for col in source_columns if col in target_columns]
    extra_source_columns = [(col, '') for col in source_columns if col not in target_columns]
    extra_target_columns = [('',col) for col in target_columns if col not in source_columns]

    # Not adding the unmatched columns as of now building lineage for mapped columns
    sorted_columns = matched_columns # + extra_source_columns + extra_target_columns 

    # Separate into source and target lists
    source_columns_sorted, target_columns_sorted = zip(*sorted_columns)

    # Create data for UpdateLineage sheet
    UpdateLineage = {
        "Target typeName": [target_type_name],
        "Target qualifiedName": [target_qualified_name],
        "Source typeName": [source_type_name],
        "Source qualifiedName": [source_qualified_name],
        "Process name": [process_name],
        "Process qualifiedName": [process_qualified_name],
        "Process typeName": [process_type_name]        
    }

    # Create data for ColumnMapping sheet
    ColumnMapping = {
        "Source qualifiedName": [source_qualified_name] * len(source_columns_sorted),
        "Source column": source_columns_sorted,
        "Target qualifiedName": [target_qualified_name] * len(target_columns_sorted),
        "Target column": target_columns_sorted,
        "Process qualifiedName": [process_qualified_name] * len(source_columns_sorted),
        "Process typeName": [process_type_name] * len(source_columns_sorted),
        "Process name": [process_name] * len(source_columns_sorted)
    }

    # Create DataFrames for the sheets
    df_update_lineage = pd.DataFrame(UpdateLineage) 
    df_column_mapping = pd.DataFrame(ColumnMapping)
    
    # Write DataFrames to an Excel file with multiple sheets
    with pd.ExcelWriter(file_path) as writer:
        df_update_lineage.to_excel(writer, sheet_name='UpdateLineage', index=False)
        df_column_mapping.to_excel(writer, sheet_name='ColumnMapping', index=False)

    print("Excel file with UpdateLineage and ColumnMapping sheets created successfully.")


def create_column_lineage(client,file_path):
    """
    Creates column lineage data and uploads it to a client (e.g., Purview) using mappings from an Excel file.

    Args:
    - client: The client object used to upload entities.
    - file_path (str): The path to the Excel file containing mappings.

    Returns:
    - dict: Upload results in JSON format.
    """
    ec =ExcelConfiguration()
    reader = ExcelReader(ec)

    #Update the lineage with given mappings
    processes = reader.parse_update_lineage_with_mappings(file_path)
    
    #upload the lineage to purview
    results = client.upload_entities(processes)
    print(json.dumps(results, indent=2))

asset_name='AFS_KNVV' 
file_path = f"./ColumnMapping/{asset_name}_ColumnMapping.xlsx"

#get_all_column_from_guid(qa_client,'MARA','sap_s4hana_table','3a6db04d-998c-4317-accc-e9f6f6f60000','sap_s4hana://vhhbrmd1ci_MD1_00_220/MARA','azure_datalake_gen2_resource_set','8f4e90b7-d276-406a-b727-2497366fc0b9','https://hbiqa01analyticsdls.dfs.core.windows.net/curated/Business/US/DimProject/Ingest/{ProjectYear}/{SparkPartitions}')
create_column_lineage(prod_client,file_path)
