##! /usr/bin/env python3


# Function Imports
# ---------------


#from modules.classification.classification import change_key_names
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

def change_key_names(dictionary: dict, key_mapping: dict) -> dict:
    """
    Changes the key names in a dictionary based on a given key mapping.

    Args:
        dictionary (dict): The input dictionary.
        key_mapping (dict): A dictionary containing the mapping of old key names to new key names.

    Returns:
        dict: The dictionary with updated key names.
    """
    new_dict = {}
    for old_key, new_key in key_mapping.items():
        if old_key in dictionary:
            new_dict[new_key] = dictionary[old_key]
        else:
            new_dict[new_key] = None
    return new_dict

def nest_collections(data):
    """
    Nest the collections data into a hierarchical structure.

    Args:
        data (generator): A generator yielding collection data.

    Returns:
        list: A list of dictionaries representing the nested collections.
              Each dictionary contains the following keys:
              - 'name': The name of the collection.
              - 'friendly_name': The friendly name of the collection.
              - 'description': The description of the collection.
              - 'parent_collection': The name of the parent collection (if any).
              - 'subcollections': A list of nested subcollections (if any),
                                  each represented as a dictionary with the same structure.
    """
    collections = {}
    for item in data:
        name = item.get('name')
        friendly_name = item.get('friendlyName')
        description = item.get('description')
        parent_collection = item.get('parentCollection', {}).get('referenceName')
        if name not in collections:
            collections[name] = {
                'name': name,
                'friendly_name': friendly_name,
                'description': description,
                'parent_collection': parent_collection,
                'subcollections': []
            }
        else:
            collections[name]['friendly_name'] = friendly_name
            collections[name]['description'] = description
            collections[name]['parent_collection'] = parent_collection

        if parent_collection:
            if parent_collection not in collections:
                collections[parent_collection] = {
                    'name': parent_collection,
                    'friendly_name': None,
                    'description': None,
                    'parent_collection': None,
                    'subcollections': []
                }
            collections[parent_collection]['subcollections'].append(collections[name])

    return [collection for collection in collections.values() if not collection['parent_collection']]


def flatten_collections(data):
    """
    Flattens the nested collections data into a flat list of dictionaries.

    Args:
        data (generator): A generator yielding collection data.

    Returns:
        list: A flat list of dictionaries representing the collections.
              Each dictionary contains the following keys:
              - 'name': The name of the collection.
              - 'friendly_name': The friendly name of the collection.
              - 'description': The description of the collection.
              - 'parent_collection': The name of the parent collection (if any).
              - 'subcollections': A list of names of subcollections (if any).
    """
    collections = {}
    data = list(data)  # Convert generator to list
    for item in data:
        name = item.get('name')
        friendly_name = item.get('friendlyName')
        description = item.get('description')
        parent_collection = item.get('parentCollection', {}).get('referenceName')

        if name not in collections:
            collections[name] = {
                'name': name,
                'friendly_name': friendly_name,
                'description': description,
                'parent_collection': parent_collection,
                'subcollections': []
            }

        if parent_collection:
            if parent_collection not in collections:
                collections[parent_collection] = {
                    'name': parent_collection,
                    'friendly_name': '',
                    'description': '',
                    'parent_collection': None,
                    'subcollections': []
                }

            collections[parent_collection]['subcollections'].append(name)

    return list(collections.values())


def get_nested_collections(client):
    """
    Retrieves a list of collections that are nested.

    Returns:
        list: A list of dictionaries representing the collections.
    """
    generator = client.collections.list_collections()
    collections = nest_collections(generator)
    return collections


def get_flattened_collections(client):
    """
    Retrieves a list of collections that is a flattened hierarchy.

    Returns:
        list: A list of dictionaries representing the collections.
    """
    generator = client.collections.list_collections()
    collections = flatten_collections(generator)
    return collections


def get_existing_collection_names(client):
    """
    Retrieves a list of existing collection names.

    Returns:
        List[str]: A list of existing collection names.

    """
    collections = get_flattened_collections(client)
    collection_names = []
    for c in collections:
        collection_names.append(c["name"])
    return collection_names


def create_unique_collection_name(client):
    """
    Generates a unique collection name.

    Returns:
        str: A unique collection name.

    """
    existing_names = get_existing_collection_names(client)
    while True:
        # Generate a 6-character random name
        new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        # Check if the generated name is unique
        if new_name not in existing_names:
            return new_name


def create_collection(client, friendly_name: str, parent_collection_name: str, description: str):
    """
    Creates or updates a collection with the specified details.

    Args:
        friendly_name (str): The friendly name of the collection.
        parent_collection_name (str): The name of the parent collection.
        description (str): The description of the collection.

    Returns:
        dict: The result of creating or updating the collection.
    """
    name = create_unique_collection_name(client)
    result = client.collections.create_or_update_collection(name, friendly_name, parent_collection_name, description)
    return result




def get_all_entities_in_collection(client, collection_name: str):
    """
    Retrieves all entities in the specified collection.

    Args:
        collection_name (str): The name of the collection to retrieve entities from.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the entities in the collection.
            Each dictionary contains the entity properties.

    """
    json_str = '{"collectionId": "' + collection_name + '"}'
    json_obj = json.loads(json_str)
    result = client.discovery.search_entities(query = collection_name, search_filter=json_obj)

    all_entities_in_collection = []
    mapping = {"id": "guid"}
    for r in result:
        # Change each entity's "id" to "guid" so assignTerms can find the guids of each entity
        updated_dict = change_key_names(r, mapping)
        all_entities_in_collection.append(updated_dict)

    return all_entities_in_collection


def delete_collection(client, collection_name: str):
    """
    Deletes a collection with the specified name.

    Args:
        collection_name (str): The name of the collection to delete.

    Returns:
        Any: The result of the delete operation.

    """
    result = client.collections.delete_collection(collection_name)
    return result


def find_collection_in_json(collection_name, json_str):
    """
    Finds the collection with the given name in the JSON structure.

    Args:
        collection_name (str): The friendly name of the collection to find.
        json_str (str): The JSON string representing the structure to search.

    Returns:
        dict or None: The collection if found, None otherwise.
    """
    json_obj = json.loads(json_str)
    for collection in json_obj:
        if collection.get('friendly_name') == collection_name:
            return collection
        if collection.get('subcollections'):
            found_collection = find_collection_in_json(collection_name, json.dumps(collection['subcollections']))
            if found_collection:
                return found_collection
    return None


def create_collections_recursive(client, collections: list, parent_collection_name: str):
    """
    Recursively creates collections and their subcollections.

    Args:
        collections (list): A list of collections to create.
        parent_collection_name (str): The name of the parent collection.

    Returns:
        None
    """
    for collection in collections:
        friendly_name = collection['friendly_name']
        description = collection['description']
        create_collection(client, friendly_name, parent_collection_name, description)

        subcollections = collection['subcollections']
        if subcollections:
            # Recursively create subcollections
            create_collections_recursive(subcollections, friendly_name)


def get_collection_name_from_friendly_name(friendly_name: str, collections: list):
    """
    Retrieves the collection name corresponding to the given friendly name.

    Args:
        friendly_name (str): The friendly name of the collection to find.
        collections (list): The list of collections to search.

    Returns:
        str or None: The collection name if found, None otherwise.
    """
    for collection in collections:
        if collection['friendly_name'] == friendly_name:
            return collection['name']
        if collection['subcollections']:
            found_collection = get_collection_name_from_friendly_name(friendly_name, collection['subcollections'])
            if found_collection:
                return found_collection
    return None


def generate_subcollections_from_json(client,friendly_name: str, json_str: str):
    """
    Generates subcollections based on a JSON structure.

    Args:
        friendly_name (str): The friendly name of the collection to generate subcollections for.
        json_str (str): The JSON structure containing the collection hierarchy.

    Returns:
        None
    """
    collection = find_collection_in_json(friendly_name, json_str)
    existing_collections = get_nested_collections(client)
    collection_name = get_collection_name_from_friendly_name(friendly_name, existing_collections)
    if collection:
        create_collections_recursive(client,collection['subcollections'], collection_name)
    else:
        print(f"Collection '{friendly_name}' not found in the output structure.")


def collect_nested_packages_and_entities(client, package_guid, collected_guids=None):
    """
    Recursively collects GUIDs of a package and its nested entities.

    Parameters:
        client (object): The Purview client object.
        package_guid (str): The GUID of the package to collect.
        collected_guids (set): A set to store the collected GUIDs. Default is None.

    Returns:
        set: A set containing the collected GUIDs.
    """
    if collected_guids is None:
        collected_guids = set()

    package_details = client.get_entity(package_guid).get("entities")[0]
    print("Identified package: " + package_details.get("displayText") + "\n")
    guids_to_move_for_this_package = [package_guid]

    for table in package_details.get("relationshipAttributes").get("tables"):
        print("Identified table: " + table.get("displayText") + "\n")
        guids_to_move_for_this_package.append(table.get("guid"))

    collected_guids.update(guids_to_move_for_this_package)

    subpackages = package_details.get("relationshipAttributes").get("packages")

    for subpackage in subpackages:
        subpackage_guid = subpackage.get("guid")
        if subpackage_guid not in collected_guids:
            collect_nested_packages_and_entities(client, subpackage_guid, collected_guids)

    return collected_guids


# added client
def move_assets_to_ignore_Collection(client, base_asset_guid,collection_name):
    '''
    Move all the related entities of the specified guid to the provided collection.

    Args:
        base_asset_guid : The list of guid's to move to destination collection.
        collection_name : The Collection name of destination collection.
    Returns:
        Dict of an entity mutation response.
    '''
    result_search=client.get_entity(base_asset_guid)
    list_of_Guid=[]
    for i in result_search:
        if i=="entities":
            nl=result_search[i]
            inner_dict=nl[0]
            for x in inner_dict:
                if x=="guid":
                    list_of_Guid.append(inner_dict[x])
                elif x=="relationshipAttributes":
                    i_inner_dict=inner_dict[x]
                    for y in i_inner_dict:
                        lst_i_inner_dict=i_inner_dict[y]
                        for itr_dicts in lst_i_inner_dict:
                            for key in itr_dicts:
                                if key=="guid":
                                    list_of_Guid.append(itr_dicts[key])
    result=client.collections.move_entities(guids=list_of_Guid, collection=collection_name)
    return result  

