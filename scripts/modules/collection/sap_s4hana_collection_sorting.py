##! /usr/bin/env python3


# Function Imports
# ---------------

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

def pull_and_move_s4hana_application_component_and_nested_entities_to_collection(client, application_component_guid, collection_id):
    """
    Collects and moves S4 HANA application component and its nested entities to a specified collection.

    Parameters:
        client (object): The Purview client object.
        application_component_guid (str): The GUID of the S4 HANA application component.
        collection_id (str): The ID of the collection to which the entities will be moved.

    Returns:
        dict: A dictionary containing the result of the move operation.
    """
    application_component_details = client.get_entity(application_component_guid).get("entities")[0]
    guids_to_move_for_this_app_comp = [application_component_guid]
    packages_in_application_component = application_component_details.get("relationshipAttributes").get("packages")

    for package in packages_in_application_component:
        guids_to_move = collect_nested_packages_and_entities(client, package.get("guid"))
        guids_to_move_for_this_app_comp.extend(guids_to_move)

    print("Collected all guids to be moved")
    result = client.collections.move_entities(guids = guids_to_move_for_this_app_comp, collection = collection_id)
    print("Moved " + str(len(guids_to_move_for_this_app_comp)) + " assets within this application component")
    print("Moved to the collection with the ID of: " + collection_id)
    print()
    return result


def move_sap_s4hana_to_collection(client):
    """
    Moves S4 HANA MDG application components to a specified collection.

    Returns:
        dict: A dictionary containing the result of the move operation.
    """
    application_component_guid = "9c47efce-5e78-45c9-aa0b-43b9a8a9273e"
    collection_id = "mpaqu7"
    result = pull_and_move_s4hana_application_component_and_nested_entities_to_collection(client, application_component_guid, collection_id)
    print(result)

