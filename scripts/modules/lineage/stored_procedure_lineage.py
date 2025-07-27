##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules import *
from modules.lineage.shared_lineage_functions import *


# Imports
# ---------------

from pyapacheatlas.core import PurviewClient
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import AtlasEntity
from pyapacheatlas.core import AtlasEntity
from pyapacheatlas.core.entity import AtlasEntity, AtlasProcess
from getpass import getpass
from pathlib import Path
from sqllineage.runner import LineageRunner


# Constants
# ---------------


# Functions
# ---------------

def confirm_source_not_target(source_tables: list, target_tables: list):
    """
    Confirm that the tables in the source_tables list are not present in the target_tables list.

    Args:
        source_tables (list): List of source table names.
        target_tables (list): List of target table names.

    Returns:
        list: Filtered list of source tables that are not present in the target tables.
    """
    try:
        filtered_tables = []
        for table in source_tables:
            if table not in target_tables:
                filtered_tables.append(table)
        return filtered_tables
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None


def extract_source_and_target_from_stored_procedure(sql_file_path: str):
    """
    Extract the source and target tables from a stored procedure SQL file.

    Args:
        sql_file_path (str): The file path to the SQL file.

    Returns:
        tuple: A tuple containing the source tables and target tables.
    """
    try:
        with open(sql_file_path, 'r') as file:
            sql_string = file.read()
        
        sql_string = remove_begin_statement(sql_string)
        lineage = LineageRunner(sql_string)
        source_tables = lineage.source_tables
        target_tables = lineage.target_tables

        # Confirm that no source tables are the same entity as the target table
        source_tables = confirm_source_not_target(source_tables, target_tables)
        return source_tables, target_tables
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None, None


