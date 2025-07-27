##! /usr/bin/env python3


# Function Imports
# ---------------

from .admin import *


# Package Imports
# ---------------

from pathlib import Path
from pyapacheatlas import *
from pyapacheatlas.core.typedef import AtlasAttributeDef, AtlasStructDef, TypeCategory
from pyapacheatlas.core import PurviewClient, AtlasEntity
from utils import get_credentials, create_purview_client
import json


# Constants
# ---------------


# Functions
# ---------------

def create_attribute(client, attribute_group_name: str, attribute_names: list):
    """
    Creates an attribute group with multiple attribute definitions.

    Args:
        attribute_group_name (str): The name of the attribute group.
        attribute_names (list): The names of the attributes to create.

    Returns:
        dict: The response of the upload operation.
    """
    attr_list = []
    for n in attribute_names: 
        attr_list.append(AtlasAttributeDef(name=n, options={"maxStrLength": "50", "applicableEntityTypes": "[\"DataSet\"]"}))

    bizdef = AtlasStructDef(
        name=attribute_group_name,
        category=TypeCategory.BUSINESSMETADATA,
        attributeDefs=attr_list
    )

    response = client.upload_typedefs(businessMetadataDefs=[bizdef], force_update=True)
    return response


def add_attributes_to_entity(client, entity: AtlasEntity, attribute_group_name: str, attribute_name: str, attribute_value: str):
    """
    Adds attributes to a business metadata group associated with an entity.

    Args:
        entity (AtlasEntity): The entity to which the attributes will be added.
        attribute_group_name (str): The name of the attribute group.
        attribute_name (str): The name of the attribute to add.
        attribute_value (str): The value of the attribute to add.

    Returns:
        dict: The response of the update operation.
    """
    response_update = client.update_businessMetadata(
        guid=entity.guid,
        businessMetadata={
            attribute_group_name: {attribute_name: attribute_value}
        }
    )
    return response_update
    

def delete_attribute(client, guid: str, attribute_group_name: str, attribute_name: str):
    """
    Deletes a specific attribute from a business metadata group associated with an entity.

    Args:
        guid (str): The unique identifier of the entity.
        attribute_group_name (str): The name of the attribute group.
        attribute_name (str): The name of the attribute to delete.

    Returns:
        dict: The response of the deletion operation.
    """
    response_deleted = client.delete_businessMetadata(
        guid=guid,
        businessMetadata={attribute_group_name: {attribute_name: ""}}
    )
    return response_deleted
 

# Main Processing
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()