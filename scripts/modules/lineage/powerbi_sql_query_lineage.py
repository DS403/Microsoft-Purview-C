##! /usr/bin/env python3


# Import Functions
# ---------------
from modules import entity
from modules.classification.test_case_generator import *
from modules.classification.regex_generator import *
from modules.classification.shared_generator_functions import *
from modules.classification.classification import *
from modules.lineage.json_payload_lineage import *
from modules.lineage.shared_lineage_functions import *
from modules.collection.collection_shared_functions import *
from modules.glossary_propagation.shared_glossary_functions import *
from modules.entity import *
from utils import get_credentials, create_purview_client
from pyapacheatlas.core.util import GuidTracker


# Import Packages
# ---------------
from pathlib import Path
from pyapacheatlas.core.typedef import AtlasAttributeDef, AtlasStructDef, TypeCategory, AtlasRelationshipAttributeDef
from pyapacheatlas.core import AtlasEntity, AtlasProcess
from azure.core.exceptions import HttpResponseError
import json
from datetime import datetime
import re
import time
import pandas as pd
from pyapacheatlas.readers import ExcelConfiguration, ExcelReader


# Constants
# ---------------  

TABLE_NAME_PATTERN = r'\bFROM\s+([a-zA-Z0-9._]+)|\bJOIN\s+([a-zA-Z0-9._]+)'


# Functions
# ---------------
def extract_table_names(sql_query):
    if len(str(sql_query))!=0:
        sql_query=sql_query.replace('[','').replace(']','')
        matches = re.findall(TABLE_NAME_PATTERN, sql_query, re.IGNORECASE)
        table_names = [name for match in matches for name in match if name]
        return (str(list(set(table_names)))[1:-1]).replace("'",'')
 
def extract_qualified_path(tbl_names):
    if len(str(tbl_names))!=0:
        tbl_names=tbl_names.split(',')
        tbl_names = [ele.replace('.', '/') for ele in tbl_names]
        url = "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/"
        l = [url+ele for ele in tbl_names]
        return (str(l)[1:-1]).replace("'",'')

def extract_source_entities_qualified_paths(file_path):
    df=pd.read_excel(file_path)
    df['Query'].fillna('',inplace=True)
    df['Table Names']=df['Query'].apply(extract_table_names)
    df['Table Names'].fillna('',inplace=True)
    df['Fully Qualified Path']=df['Table Names'].apply(extract_qualified_path)
    df['Fully Qualified Path'].fillna('',inplace=True)
    df.to_excel(file_path,index=False)
    val=[ele.split(', ') for ele in df['Fully Qualified Path']]
    source_qualified_paths = list(set([item for sublist in val for item in sublist]))
    source_qualified_paths.remove('')
    return source_qualified_paths


def build_powerbi_lineage_from_sql_query(client, source_entities_qualified_paths, target_entity_qualified_path, target_name_without_special_char):
    '''
    Builds lineage information between Azure SQL Database (SQL) sources and a PowerBI target.

    Parameters:
    - client: The client object for interacting with the metadata repository.
    - source_entities_qualified_paths (list): List of qualified paths for Azure SQL Database (SQL) entities.
    - target_entity_qualified_path (str): Qualified path for the PowerBI target entity.
    - target_name_without_special_char (str): Name of the PowerBI target without special characters.

    Returns:
    None
    '''
    # ie. target_name_without_special_char = "5114AmazonKPIReporting"
    """result = upload_custom_type_def_with_specific_client(client, SQL_DATABASE_EXTRACT_TYPEDEF)
    print(result)"""

    #source_entities_qualified_paths=extract_source_entities_qualified_paths(r"Lineage inputs\51.15 Stackline Industry Visibility - Weekly Level - ACTIVEWEAR.xlsx")

    
    # for i in here, run get_entity_from_qualified_name, add to list of entities, then pass that to add_manual_lineage
    process_type_name = "sql_database_source"
    source_type_name = "AzureSQLDB"
    target_type_name = "PowerBI"

    source_entities_get = []
    for s in source_entities_qualified_paths:
        ent = get_entity_from_qualified_name(client, s)
        source_entities_get.append(ent)
    
    target_entity = get_entity_from_qualified_name(client, target_entity_qualified_path)
    result = add_manual_lineage_with_specific_client(client, source_entities_get, [target_entity], process_type_name, source_type_name, target_type_name, target_name_without_special_char)
    print(result)


def build_lineage_from_azure_sql_to_pbi(client, azure_sql_asset_qualified_name, pbi_dataset_qualified_name):
    '''
    Build lineage from an Azure Dedicated SQL Pool Table's asset to a Power BI dataset.
    '''

    source_entity = get_entity_from_qualified_name(client, azure_sql_asset_qualified_name)
    target_entity = get_entity_from_qualified_name(client, pbi_dataset_qualified_name)
    process_type_name = "sql_database_source"
    result = add_manual_lineage(client, [source_entity], [target_entity], process_type_name)
    print("Lineage built between " + source_entity["name"] + " and " + target_entity["name"])

