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


def build_lineage_from_databricks_to_pbi(client, databricks_qualified_name, pbi_dataset_qualified_name):
    '''
    Build lineage from a Databricks table to a Power BI dataset.

    Args:
        client: The Purview Atlas client for entity upload.
        entity_name (str): Name of the SharePoint entity.
        actual_sharepoint_link (str): Link to the actual SharePoint resource.
        pbi_dataset_qualified_name (str): Qualified name of the Power BI dataset.
        pbi_short_name (str): Short name of the Power BI dataset.
    '''

    source_entity = get_entity_from_qualified_name(client, databricks_qualified_name)
    target_entity = get_entity_from_qualified_name(client, pbi_dataset_qualified_name)
    process_type_name = "Databricks_to_PBI"
    result = add_manual_lineage(client, [source_entity], [target_entity], process_type_name)
    print("Lineage built between " + source_entity["name"] + " and " + target_entity["name"])

