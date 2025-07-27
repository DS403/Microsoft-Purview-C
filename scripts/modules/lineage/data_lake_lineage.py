##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules import *
from modules.lineage.shared_lineage_functions import *
from pyapacheatlas.core.util import GuidTracker


# Imports
# ---------------
from pathlib import Path
import os


# Constants
# ---------------


# Functions
# ---------------

def build_lineage_from_data_lake_curated_to_data_warehouse_stage(client, dl_curated_guid, dw_stage_guid):
    '''
    Builds lineage from a data lake curated asset to a data warehouse stage asset.

    Parameters:
        client (object): The client object for accessing the metadata service.
        dl_curated_guid (str): The GUID of the data lake curated asset.
        dw_stage_guid (str): The GUID of the data warehouse stage asset.

    Returns:
        None
    '''
    dl_type = "azure_datalake_gen2_path"
    dw_type = "azure_sql_dw_table"
    process_type_name = "DL_Curated_to_DW_Stage"
    build_lineage_using_guids(client, dl_curated_guid, dl_type, dw_stage_guid, dw_type, process_type_name)


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


def build_lineage_from_data_lake_manual_file_to_data_lake_stage(client, manual_file_guid, dl_stage_guid):
    '''
    Builds lineage from a manually added asset to a data lake stage asset.

    Parameters:
        client (object): The client object for accessing the metadata service.
        manual_file_guid (str): The GUID of the manually added file asset.
        dl_stage_guid (str): The GUID of the data lake stage asset.

    Returns:
        None
    '''
    manual_file_type = "azure_datalake_gen2_path"
    dl_type = "azure_datalake_gen2_path"
    process_type_name = "DL_Manual_File_to_DL_Stage"
    build_lineage_using_guids(client, manual_file_guid, manual_file_type, dl_stage_guid, dl_type, process_type_name)


def build_lineage_from_data_lake_curated_to_data_lake_curated(client, source_curated_guid, target_curated_guid):
    '''
    Builds lineage from one data lake curated asset to another data lake curated asset.

    Parameters:
        client (object): The client object for accessing the metadata service.
        source_curated_guid (str): The GUID of the source data lake curated asset.
        target_curated_guid (str): The GUID of the target data lake curated asset.

    Returns:
        None
    '''
    source_curated_type = "azure_datalake_gen2_path"
    target_curated_type = "azure_datalake_gen2_path"
    process_type_name = "DL_Curated_to_DL_Curated"
    build_lineage_using_guids(client, source_curated_guid, source_curated_type, target_curated_guid, target_curated_type, process_type_name)




def datalake_get_curated_asset(input_file):
    '''
    Extracts the target location from a SQL query that creates or inserts into a data lake asset.

    Parameters:
        input_file (str): Path to the input SQL file.

    Returns:
        str: The target location in the data lake.
    '''
    with open(input_file, 'r') as file:
        sql_query = file.read()
        split_sql_query = sql_query.split()
        for i in range(len(split_sql_query)):
            sql_str = split_sql_query[i]
            list_of_keywords = ["into", "create"]
            if sql_str.lower() in list_of_keywords and i != len(split_sql_query) - 1:
                # replace the periods with slashes for searching them as qualified paths
                target = split_sql_query[i + 1].replace(".", "/").replace("_", "/").replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(";", "")
                return target

        print("No targets for this view.")
        sys.exit(0)


def datalake_get_stage_asset(input_file):
    '''
    Extracts the source locations from a SQL query used in staging data into a data lake.

    Parameters:
        input_file (str): Path to the input SQL file.

    Returns:
        list: List of source locations in the data lake.
    '''
    with open(input_file, 'r') as file:
        sources = []
        sql_query = file.read()
        split_sql_query = sql_query.split()
        for i in range(len(split_sql_query)):
            sql_str = split_sql_query[i]
            list_of_keywords = ["using", "from", "join"]
            if sql_str.lower() in list_of_keywords and i != len(split_sql_query) - 1:
                # replace the periods with slashes for searching them as qualified paths
                source = split_sql_query[i + 1].replace(".", "/").replace("_", "/").replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(";", "")
                if i != len(split_sql_query):
                    if split_sql_query[i + 2] == "SRC":
                        sources.append(source)

        sources = list(set(sources)) # remove duplicates
        sources = [s for s in sources if '/' in s] # removes empty strings and only allows paths
        if len(sources) == 0:
            print("No sources for this view.")
            sys.exit(0)

        return sources
    

def get_inventory_datalake_stage_qualified_name(partial_source_names):
    '''
    Constructs the qualified names for inventory data lake staging sources.

    Parameters:
        partial_source_names (list of str): List of partial source names.

    Raises:
        Exception: If all details of stage Ingest source are not provided.

    Returns:
        None
    '''
    for name in partial_source_names:
        split_name = name.split("/")
        if len(split_name) != 3:
            print("Not provided all details of stage Ingest source. Verify stage asset name in the stage_Ingest_to_curated_Ingest.sql file.")
        
        source_qualified_name = "https://hbipd01analyticsdls.dfs.core.windows.net/" + split_name[0] + "/Inventory/US/Manual/" + split_name[1] + "/" + split_name[2] + "/{SparkPartitions}"
        print(source_qualified_name)
        print()
        raise Exception
    

def get_target_partial_qual_name(asset_name):
    '''
    Retrieves the partial qualified name of the target asset.

    Parameters:
        asset_name (str): Name of the target asset.

    Raises:
        Exception: If the asset file is not found or if there's an issue loading its JSON data.

    Returns:
        None
    '''
    process_payloads_directory = "BIDW/ProcessPayloads/Curated/"
    if os.path.exists(process_payloads_directory):
        items = os.listdir(process_payloads_directory)
        
        # Filter out only the directories
        folders = [item for item in items if os.path.isdir(os.path.join(process_payloads_directory, item))]
        folder_name = ""
        prod_header = "https://hbipd01analyticsdls.dfs.core.windows.net"

        for folder in folders:
            print("Folder name:", folder)
            folder_path = os.path.join(process_payloads_directory, folder)  # Full path to the subfolder
            files = os.listdir(folder_path)


            # Iterate through the files and capture their names
            seeking = asset_name + ".json"
            for file in files:
                if seeking == file:
                    file_path = os.path.join(folder_path, file)  # Full path to the subfolder

                    folder_name = folder
                    with open(file_path, "r") as json_file:
                        data = json.load(json_file)
                        path_to_ingest = data["configurationPayload"]["dataPayload"][0]["dataConfig"]["path"]
                        qual_name_for_ingest = prod_header + path_to_ingest.replace("/mnt", "")
                        print(qual_name_for_ingest)
                        print("\n\n")
                        raise Exception


        raise Exception




def datalake_inventory_stage_ingest_to_curated_ingest():
    '''
    Constructs lineage and retrieves target partial qualified name for the inventory data lake staging process.

    Raises:
        Exception: If there's an error with the process.

    Returns:
        None
    '''
    path_to_file_with_this_source = ""
    what_we_have_source = "stage.WinningPortfolioSKUList_ingest"
    what_we_need_source = "https://hbipd01analyticsdls.dfs.core.windows.net/stage/Inventory/US/Manual/WinningPortfolioSKUList/Ingest/{SparkPartitions}"


    # iterate through every file in curated and fill in this path
    # pull the source (stage) and target (curated)
    stage_to_curated_directory = "BIDW/Databricks/01/Workflows/Pipelines/Curated/"
    if os.path.exists(stage_to_curated_directory):
        items = os.listdir(stage_to_curated_directory)
        
        # Filter out only the directories
        folders = [item for item in items if os.path.isdir(os.path.join(stage_to_curated_directory, item))]
        for folder in folders:
            if folder == "DimFlatBOM": # HARDCODING
                print("Folder name:", folder)
                file_path = stage_to_curated_directory + folder + "/dependencies/stage_Ingest_to_curated_Ingest.sql"
                
                try:
                    partial_source_names = datalake_get_stage_asset(file_path)
                    partial_target_name = datalake_get_curated_asset(file_path)
                    asset_name = partial_target_name.split("/")[1]
                    print(asset_name)

                    target_partial_qual_name = get_target_partial_qual_name(asset_name)
                    #source_qualified_name = get_inventory_datalake_stage_qualified_name(partial_source_names)

                except:
                    print("Error with " + file_path)

                raise Exception
    else:
        print("The specified path does not exist.")
    
    #input_file = "BIDW/Databricks/01/Workflows/Pipelines/Curated/DimWinningPortfolioSkuList/dependencies/stage_Ingest_to_curated_Ingest.sql"
    # will give back something like ["stage/WinningPortfolioSKUList/Ingest"]
    #partial_source_names = datalake_get_stage_asset(input_file)
    #source_qualified_name = get_inventory_datalake_stage_qualified_name(partial_source_names)

    # iterate through the process payloads until file name found
    # save that sub-directory
    # need to then pull the curated process payload
    # load the process payload json into a dict to extract
    "/mnt/curated/Inventory/US/Manual/DimWinningPortfolioSkuList/Ingest/"
    # remove /mnt, and use this to search, but add header of htt.... first
    
    # then pull entities for both qual names and create lineage
    # then use process payload code to pull this asset again

    what_we_have_target = "curated.DimWinningPortfolioSkuList_Ingest"
    what_we_need_target = "https://hbipd01analyticsdls.dfs.core.windows.net/curated/Inventory/US/Manual/DimWinningPortfolioSkuList/Ingest/{Division}/{SparkPartitions}"

