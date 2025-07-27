##! /usr/bin/env python3


# Function Imports
# ---------------

from modules import entity
from modules.collection.collection_shared_functions import *
from utils import get_credentials, create_purview_client


# Package Imports
# ---------------

from pyapacheatlas.core import AtlasEntity, AtlasClassification
from pyapacheatlas.core.entity import AtlasEntity, AtlasUnInit
import json
from pathlib import Path
import random
import string


# Constants
# ---------------


# Functions
# ---------------

def pull_and_move_azure_dw_schema_and_nested_entities_to_collections(client, schema_guid, collection_id):
    """
    Pulls Azure SQL Data Warehouse (SQL DW) schema details and its nested entities and moves them to a Purview collection.

    Parameters:
        client (object): The Purview client object.
        schema_guid (str): The GUID of the SQL DW schema to be moved.
        collection_id (str): The ID of the Purview collection to which the schema and nested entities will be moved.

    Returns:
        dict: The result of the move operation.
    """
    schema_details = client.get_entity(schema_guid).get("entities")[0]
    guids_to_move_for_this_schema = [schema_guid]

    for table in schema_details.get("relationshipAttributes").get("tables"):
        print("Identified table: " + table.get("displayText") + "\n")
        guids_to_move_for_this_schema.append(table.get("guid"))

    for view in schema_details.get("relationshipAttributes").get("views"):
        print("Identified view: " + view.get("displayText") + "\n")
        guids_to_move_for_this_schema.append(view.get("guid"))

    print("Collected all guids to be moved")
    result = client.collections.move_entities(guids = guids_to_move_for_this_schema, collection = collection_id)
    print("Moved " + str(len(guids_to_move_for_this_schema)) + " assets within this schema")
    print("Moved to the collection with the ID of: " + collection_id)
    print()
    return result


def move_azure_dw_to_collection():
    """
    Moves Azure SQL Data Warehouse (SQL DW) schema and its nested entities to a Purview collection.

    Returns:
        None
    """
    REFERENCE_NAME_PURVIEW = "hbi-pd01-datamgmt-pview"
    CREDS = get_credentials(cred_type= 'default')
    client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)
    
    schema_guid = "0f6c798e-0b32-4d5d-867d-916e8b015071" # inventory in Prod
    collection_id = "mn8dqe" # inventory
    result = pull_and_move_azure_dw_schema_and_nested_entities_to_collections(client, schema_guid, collection_id)
    print()
    print(result)

