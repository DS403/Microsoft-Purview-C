##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules import *
from modules.lineage.shared_lineage_functions import *


# Imports
# ---------------

from pathlib import Path


# Constants
# ---------------


# Functions
# ---------------

def build_lineage_from_oracle_server_to_pbi(client, oracle_asset_qualified_name, pbi_dataset_qualified_name):
    '''
    Builds lineage from an Oracle Server's asset to a Power BI dataset.

    Parameters:
        client (object): The client object for accessing the metadata service.
        oracle_asset_qualified_name (str): The qualified name of the Oracle Server asset.
        pbi_dataset_qualified_name (str): The qualified name of the Power BI dataset.

    Returns:
        None
    '''

    source_entity = get_entity_from_qualified_name(client, oracle_asset_qualified_name)
    target_entity = get_entity_from_qualified_name(client, pbi_dataset_qualified_name)
    process_type_name = "Oracle_Server_to_PBI"
    result = add_manual_lineage(client, [source_entity], [target_entity], process_type_name)
    print("Lineage built between " + source_entity["name"] + " and " + target_entity["name"])


def build_lineage_from_oracle_to_data_lake_stage(client, oracle_guid, dl_stage_guid):
    '''
    Builds lineage from an Oracle asset to a data lake stage asset.

    Parameters:
        client (object): The client object for accessing the metadata service.
        oracle_guid (str): The GUID of the Oracle asset.
        dl_stage_guid (str): The GUID of the data lake stage asset.

    Returns:
        None
    '''
    oracle_type = "oracle_table"
    dl_type = "azure_datalake_gen2_path"
    process_type_name = "Oracle_to_DL_Stage"
    build_lineage_using_guids(client, oracle_guid, oracle_type, dl_stage_guid, dl_type, process_type_name)

