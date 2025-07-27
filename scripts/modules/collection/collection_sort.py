##! /usr/bin/env python3

# Function Imports
# ---------------

from pyapacheatlas.core import AtlasEntity ,AtlasClassification
from pyapacheatlas.core.entity import AtlasEntity, AtlasProcess
from pyapacheatlas.core.typedef import EntityTypeDef, AtlasAttributeDef
from pyapacheatlas.readers import ExcelConfiguration,ExcelReader
from utils import get_credentials,create_purview_client
from collection_shared_functions import *

# Imports
# ---------------

import pandas as pd
import json
from pathlib import Path
import random
import string


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


def get_existing_collection_friendly_names(client):
    """
    Retrieves a list of existing collection friendly names.
    Returns:
        List[str]: A list of existing collection friendly names.
    """
    collections = get_flattened_collections(client)
    collection_friendly_name = []
    for c in collections:
        collection_friendly_name.append(c["friendly_name"])
    return collection_friendly_name

def create_subcollections_from_json(client):
    collection_friendly_name = get_existing_collection_friendly_names(client)
    for friendly_name in collection_friendly_name:
        try:
            with open(r"collections_structure.json", 'r') as file:
                data = json.load(file)
                json_string = json.dumps(data)
            generate_subcollections_from_json(client,friendly_name, json_string)
        except Exception as e:
            print("Skip Collection friendly names:"+friendly_name)

def sort_collection_into_subcollections(client, parent_collection_name: str,archive_subcollection_name:str,delta_log_subcollection_name: str,ingest_subcollection_name:str):
    """
    Retrieves all entities in the specified collection.
    Args:
        collection_name (str): The name of the collection to retrieve entities from.
    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the entities in the collection.
            Each dictionary contains the entity properties.
    """
    json_str = '{"collectionId": "' + parent_collection_name + '"}'
    json_obj = json.loads(json_str)
    result = client.discovery.search_entities(query = parent_collection_name, search_filter=json_obj)
    all_entities_in_collection = []
    mapping = {"id": "guid","displayText": "AssetName"}
    for r in result:
        # Change each entity's "id" to "guid" so assignTerms can find the guids of each entity
        updated_dict = change_key_names(r, mapping)
        all_entities_in_collection.append(updated_dict)
    #return all_entities_in_collection

    # Initialize empty lists for each category
    delta_log_guids = []
    archive_guids = []
    ingest_guids = []

    # Iterate through the list and categorize GUIDs
    for item in all_entities_in_collection:
        if item["AssetName"] == "Log" or "_delta_log" in item["AssetName"]:
            delta_log_guids.append(item["guid"])
        elif item["AssetName"] == "Archive":
            archive_guids.append(item["guid"])
        elif item["AssetName"] == "Ingest":
            ingest_guids.append(item["guid"])

    #print("Log GUIDs:", delta_log_guids)
    #print("Archive GUIDs:", archive_guids)
    #print("Ingest GUIDs:", ingest_guids)
    if len(archive_guids)>20:
        #move assets to Archive subcollection
        client.collections.move_entities(guids=archive_guids, collection=archive_subcollection_name)

    if len(delta_log_guids)>20:
        #move assets to delta log subcollection
        client.collections.move_entities(guids=delta_log_guids, collection=delta_log_subcollection_name)

    if len(ingest_guids)>20:
        #move assets to Ingest subcollection
        client.collections.move_entities(guids=ingest_guids, collection=ingest_subcollection_name)

    return None

#create_subcollections_from_json(prod_client) 
#sort_collection_into_subcollections(prod_client,'a72ccq','tspr1x','fii3o3','j7jz84')