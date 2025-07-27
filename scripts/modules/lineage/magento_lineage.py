#!/usr/bin/env python3

# Function Imports
from utils import get_credentials, create_purview_client
from modules import *
from pyapacheatlas.core import AtlasEntity
from pathlib import Path
import pandas as pd
from pyapacheatlas.core.util import GuidTracker


def parse_excel_file(file):
    """
    Parse the given Excel file to extract entity names and their columns.
    """
    df = pd.read_excel(file)
    entity_dict = {}

    for _, row in df.iterrows():
        table_name = row['TABLE_NAME']
        column_name = row['COLUMN_NAME']

        if table_name not in entity_dict:
            entity_dict[table_name] = []
        entity_dict[table_name].append(column_name)

    return entity_dict

def upload_entities_to_purview(client, entity_dict, table_name):
    """
    Upload entities and their relationships to Purview.
    """
    table_qualified_name = "magento://" + table_name 
    guid_tracker = GuidTracker(starting=-1002, direction='decrease')
    table_guid = guid_tracker.get_guid()
    table = AtlasEntity(table_name, "DataSet", table_qualified_name, table_guid)

    columns_to_add = []
    dimensions = entity_dict.get(table_name)
    
    for column_name in dimensions:
        dimension_qualified_name = table_qualified_name + "/column/" + column_name
        dimension_guid = guid_tracker.get_guid()
        dimension = AtlasEntity(column_name, "column", dimension_qualified_name, dimension_guid, attributes={"type": "Dimension"})
        dimension.addRelationship(table = table)
        columns_to_add.append(dimension)


    tabular_schema = AtlasEntity(table_name + " Tabular Schema", "tabular_schema", table_qualified_name + "/tabular_schema", guid_tracker.get_guid())
    tab_assgn = client.upload_entities([tabular_schema])
    tab_key, tab_guid = next(iter(tab_assgn.get('guidAssignments').items()))
    tabular_schema = AtlasEntity(table_name + " Tabular Schema", "tabular_schema", table_qualified_name + "/tabular_schema", tab_guid)

    table_assignment = client.upload_entities([table] + [tabular_schema])
    table_key, table_guid = next(iter(table_assignment.get('guidAssignments').items()))
    column_assignment = client.upload_entities(columns_to_add)

    tab_dataset_relationship = {
            "typeName": "tabular_schema_datasets",
            "attributes": {},
            "guid": -100,
            "end1": {
                "guid": table_guid
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

    print("Cube created for: " + table_name + "\n\n\n")



def main():
    # Define file path
    path_to_file = r'C:\path\to\your\file.xlsx'

    # Get credentials and create Purview client
    CREDS = get_credentials(cred_type='default')
    client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account="your_account")

    # Parse the Excel file
    entity_dict = parse_excel_file(path_to_file)

    # Upload entities to Purview
    upload_entities_to_purview(client, entity_dict)

if __name__ == '__main__':
    main()
