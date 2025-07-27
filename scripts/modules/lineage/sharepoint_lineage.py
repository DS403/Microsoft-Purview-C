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


# Functions
# ---------------

def build_sharepoint_to_pbi_lineage(client, sharepoint_source, sharepoint_short_name, pbi_target, pbi_short_name, process_type_name):
    '''
    Build lineage between a SharePoint entity and a Power BI dataset by creating AtlasEntities for source and target entities,
    and an AtlasProcess connecting them.

    Args:
        client: The Purview Atlas client for entity upload.
        sharepoint_source (dict): Details of the SharePoint entity (source).
        sharepoint_short_name (str): Short name of the SharePoint entity.
        pbi_target (dict): Details of the Power BI dataset (target).
        pbi_short_name (str): Short name of the Power BI dataset.
        process_type_name (str): Name of the process type.

    Returns:
        dict: Result of the entity upload operation.
    '''
    qualified_name = "sources:" + sharepoint_short_name + "/targets:" + pbi_short_name + "/process_type:" + process_type_name

    sources = []
    targets = []
    s = AtlasEntity(
        name = sharepoint_source["name"],
        typeName = sharepoint_source["entityType"],
        qualified_name = sharepoint_source["qualifiedName"],
        guid = sharepoint_source["id"]
    )
    sources.append(s)

    t = AtlasEntity(
        name = pbi_target["name"],
        typeName = pbi_target["entityType"],
        qualified_name = pbi_target["qualifiedName"],
        guid = pbi_target["id"]
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

    return result


def create_sharepoint_entity(client, entity_name, entity_qualified_name, actual_sharepoint_link):
    '''
    Create a SharePoint entity in the Purview Atlas with the specified details and link to an actual SharePoint resource.

    Args:
        client: The Purview Atlas client for entity upload.
        entity_name (str): Name of the SharePoint entity.
        entity_qualified_name (str): Qualified name of the SharePoint entity.
        actual_sharepoint_link (str): Link to the actual SharePoint resource.

    Returns:
        dict: Dictionary containing details of the created SharePoint entity.
    '''
    guid_counter = -1002
    guid_tracker = GuidTracker(starting=guid_counter, direction='decrease')
    entity_guid = guid_tracker.get_guid()
    entity = AtlasEntity(entity_name, "SharePoint Entity", entity_qualified_name, entity_guid, attributes = {"description": "Link to entity in Sharepoint:\n" + actual_sharepoint_link})

    try:
        assignments = client.upload_entities(entity)
        print("Sharepoint entity created for: " + entity_name + "\n")
        sharepoint_entity_dict = {
            "name": entity_name,
            "entityType": "SharePoint Entity",
            "qualifiedName": entity_qualified_name,
            "id": entity_guid
        }
        return sharepoint_entity_dict

    except:
        print("Error with Sharepoint entity: " + entity_name)


def create_sharepoint_entity_and_build_lineage_to_pbi(client, entity_name, actual_sharepoint_link, pbi_dataset_qualified_name, pbi_short_name):
    '''
    Create a SharePoint entity and build lineage to a Power BI dataset in the Purview Atlas.

    Args:
        client: The Purview Atlas client for entity upload.
        entity_name (str): Name of the SharePoint entity.
        actual_sharepoint_link (str): Link to the actual SharePoint resource.
        pbi_dataset_qualified_name (str): Qualified name of the Power BI dataset.
        pbi_short_name (str): Short name of the Power BI dataset.
    '''
    sharepoint_short_name = entity_name.replace(" ", "_")
    entity_qualified_name = "sharepoint://hanes.sharepoint.com/" + sharepoint_short_name
    sharepoint_dict = create_sharepoint_entity(client, entity_name, entity_qualified_name, actual_sharepoint_link)
    
    pbi_dataset_dict = get_entity_from_qualified_name_using_type(client, pbi_dataset_qualified_name, "powerbi_dataset")
    build_sharepoint_to_pbi_lineage(client, sharepoint_dict, sharepoint_short_name, pbi_dataset_dict, pbi_short_name, "sharepoint_to_pbi")
    print("Lineage built between " + entity_name + " and " + pbi_short_name)

