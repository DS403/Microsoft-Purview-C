##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules import *
from modules.lineage.shared_lineage_functions import *
import xml.etree.ElementTree as ET
from pyapacheatlas.core.util import GuidTracker


# Imports
# ---------------

import re
import sys
from pathlib import Path


# Constants
# ---------------


# Functions
# ---------------

def ensure_unique_sets(dimensions):
    '''
    Ensures uniqueness of attribute IDs within each dimension.

    Parameters:
        dimensions (dict): A dictionary mapping dimension IDs to lists of attribute IDs.

    Returns:
        dict: A dictionary with the same structure as the input 'dimensions' dictionary,
              where each list of attribute IDs is made unique.

    '''
    for dimension_id, attribute_ids in dimensions.items():
        unique_attribute_ids = list(set(attribute_ids))
        dimensions[dimension_id] = unique_attribute_ids
    return dimensions


def parse_cube_xmla(xmla_file):
    '''
    Parses an XMLA file containing cube metadata to extract dimension and attribute information.

    Parameters:
        xmla_file (str): The path to the XMLA file.

    Returns:
        dict: A dictionary representing dimensions and their associated attribute IDs.
              Structure: {dimension_ID: [list of unique attribute IDs]}.

    '''
    tree = ET.parse(xmla_file)
    root = tree.getroot()
    dimensions = {} # structured as {dimension_ID: [list of attribute IDs]}

    # Find all Dimension elements
    for dimension_elem in root.findall('.//{http://schemas.microsoft.com/analysisservices/2003/engine}Dimension'):
        dimension_id_elem = dimension_elem.find('{http://schemas.microsoft.com/analysisservices/2003/engine}ID')
        if dimension_id_elem is None:
            dimension_id_elem = dimension_elem.find('{http://schemas.microsoft.com/analysisservices/2003/engine}DimensionID')
        if dimension_id_elem is not None:
            dimension_id = dimension_id_elem.text
            attributes = []

            # Find all Attribute elements within the dimension
            for attribute_elem in dimension_elem.findall('.//{http://schemas.microsoft.com/analysisservices/2003/engine}Attribute'):
                attribute_id_elem = attribute_elem.find('{http://schemas.microsoft.com/analysisservices/2003/engine}ID')
                if attribute_id_elem is None:
                    attribute_id_elem = attribute_elem.find('{http://schemas.microsoft.com/analysisservices/2003/engine}AttributeID')
                if attribute_id_elem is not None:
                    attribute_id = attribute_id_elem.text
                    attributes.append(attribute_id)

            # Check if dimension already exists in dimensions dictionary
            if dimension_id in dimensions:
                # Append attributes to existing list
                dimensions[dimension_id].extend(attributes)
            else:
                # Add dimension and its attributes to dimensions dictionary
                dimensions[dimension_id] = attributes

    return ensure_unique_sets(dimensions)


def create_cubes_from_xmla_file(client, xmla_file_name, cube_name):
    """
    Parses cubes from a XMLA file and uploads them to Purview in a predefined structure.

    Parameters:
    - client: Purview client for making Atlas API requests.
    - xmla_file_name (str): The name of the XMLA file containing the cube to be parsed.
    - cube_name (str): The name of the cube.

    Returns:
    - None
    """

    cube_qualified_name = "wsbissasqryp2v.res.hbi.net://" + cube_name 
    guid_counter = -1002
    guid_tracker = GuidTracker(starting=guid_counter, direction='decrease')
    cube_guid = guid_tracker.get_guid()
    cube = AtlasEntity(cube_name, "DataSet", cube_qualified_name, cube_guid)

    columns_to_add = []
    cube_dimensions = parse_cube_xmla(xmla_file_name)

    for key, value in cube_dimensions.items():
        dimension_ID = key
        attributes_list = value
        dimension_qualified_name = cube_qualified_name + "/dimension/" + dimension_ID
        dimension_guid = guid_tracker.get_guid()
        dimension = AtlasEntity(dimension_ID, "column", dimension_qualified_name, dimension_guid, attributes={"type": "Dimension"})
        dimension.addRelationship(table = cube)
        columns_to_add.append(dimension)

        for a in attributes_list:
            attribute_ID = a
            attribute_qualified_name = dimension_qualified_name + "/attribute/" + attribute_ID
            attribute_guid = guid_tracker.get_guid()
            attribute = AtlasEntity(attribute_ID, "column", attribute_qualified_name, attribute_guid, attributes={"type": "Attribute"})
            attribute.addRelationship(table = cube)
            columns_to_add.append(attribute)
                
    tabular_schema = AtlasEntity(cube_name + " Tabular Schema", "tabular_schema", cube_qualified_name + "/tabular_schema", guid_tracker.get_guid())
    tab_assgn = client.upload_entities([tabular_schema])
    tab_key, tab_guid = next(iter(tab_assgn.get('guidAssignments').items()))
    tabular_schema = AtlasEntity(cube_name + " Tabular Schema", "tabular_schema", cube_qualified_name + "/tabular_schema", tab_guid)

    cube_assignment = client.upload_entities([cube] + [tabular_schema])
    cube_key, cube_guid = next(iter(cube_assignment.get('guidAssignments').items()))
    column_assignment = client.upload_entities(columns_to_add)

    tab_dataset_relationship = {
            "typeName": "tabular_schema_datasets",
            "attributes": {},
            "guid": -100,
            "end1": {
                "guid": cube_guid
            },
            "end2": {
                "guid": tab_guid
            }
        }
    relationship_assignment = client.upload_relationship(tab_dataset_relationship)  

    for key, value in column_assignment.get('guidAssignments').items():
        column_guid = value

        tab_column_relationship = {
            "typeName": "tabular_schema_columns",
            "attributes": {},
            "guid": -100,
            "end1": {
                "guid": tab_guid
            },
            "end2": {
                "guid": column_guid
            }
        } 
        relationship_assignment = client.upload_relationship(tab_column_relationship) 
        print("Column added for column guid " + str(column_guid))

    print("Cube created for: " + cube_name + "\n\n\n")


def build_lineage_from_cube_to_pbi(client, cube_guid, pbi_dataset_guid):
    '''
    Builds lineage from a cube to a Power BI dataset.

    Parameters:
        client (object): The client object for accessing the metadata service.
        cube_guid (str): The GUID of the cube.
        pbi_dataset_guid (str): The GUID of the Power BI dataset.

    Returns:
        None
    Build lineage from a cube to a Power BI dataset.
    '''
    cube_type = "DataSet"
    pbi_dataset_type = "powerbi_dataset"
    process_type_name = "Cube_to_PBI"
    build_lineage_using_guids(client, cube_guid, cube_type, pbi_dataset_guid, pbi_dataset_type, process_type_name)

