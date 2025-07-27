##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from pyapacheatlas.core.util import GuidTracker
from pyapacheatlas.readers import ExcelConfiguration, ExcelReader
from pyapacheatlas.core import AtlasEntity


# Imports
# ---------------

import re
import json
import sys
from pathlib import Path
import pandas as pd

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


# Global
# ---------------


# Functions
# ---------------

def parse_pkms_tables_from_excel(client, file_name):
    """
    Parses tables from an Excel file and uploads them to Apache Atlas in a predefined structure.

    Parameters:
    - client: Purview client for making Atlas API requests.
    - file_name (str): The name of the Excel file containing tables to be parsed.

    Returns:
    - None
    """
    xls = pd.ExcelFile(file_name)
    tables = {}

    for sheet_name in xls.sheet_names:
        already_built = ["STSTYL00", "IDCASE00", "PHPICK00", "PDPICK00", "PIPICK00"]
        # REMOVE THIS already_built LOGIC - temporarily added from timeout exception
        if sheet_name not in already_built:

            df = pd.read_excel(file_name, sheet_name=sheet_name)
            tables[sheet_name] = df
            record_name = df.iloc[1, 1]
            record_qualified_name = "pkms://file/" + sheet_name + "/record/" + record_name 

            guid_counter = -1002
            guid_tracker = GuidTracker(starting=guid_counter, direction='decrease')
            record_guid = guid_tracker.get_guid()
            record = AtlasEntity(record_name, "DataSet", record_qualified_name, record_guid)


            columns_to_add = []

            for index, row in df.iterrows():
                column_name = row["Field"]
                column_description = row["Field text description"]
                column_type=" "
                '''
                is_numeric = row["Number of digits"]
                column_type = "NUM"
                if is_numeric == 0:
                    column_type = "CHAR"
                '''
                column_qualified_name = record_qualified_name + "#" + column_name
                column_guid = guid_tracker.get_guid()
                column = AtlasEntity(column_name, "column", column_qualified_name, column_guid, attributes={"type": column_type, "userDescription": column_description})
                column.addRelationship(table = record)
                columns_to_add.append(column)
                
            tabular_schema = AtlasEntity(record_name + " Tabular Schema", "tabular_schema", record_qualified_name + "/tabular_schema", guid_tracker.get_guid())
            tab_assgn = client.upload_entities([tabular_schema])
            tab_key, tab_guid = next(iter(tab_assgn.get('guidAssignments').items()))
            tabular_schema = AtlasEntity(record_name + " Tabular Schema", "tabular_schema", record_qualified_name + "/tabular_schema", tab_guid)

            record_assignment = client.upload_entities([record] + [tabular_schema])
            record_key, record_guid = next(iter(record_assignment.get('guidAssignments').items()))
            column_assignment = client.upload_entities(columns_to_add)

            tab_dataset_relationship = {
                    "typeName": "tabular_schema_datasets",
                    "attributes": {},
                    "guid": -100,
                    "end1": {
                        "guid": record_guid
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

            print("Table created for: " + record_name + "\n\n\n")

parse_pkms_tables_from_excel(prod_client, 'CQSTYL00.xlsx')
