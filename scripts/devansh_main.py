##! /usr/bin/env python3
 
 
# Import Functions
# ---------------
 
from modules import entity
from modules.lineage.informatica_lineage import *
from modules.entity import *
from utils import get_credentials, create_purview_client
from pyapacheatlas.core.util import GuidTracker
from pyapacheatlas.readers import ExcelConfiguration, ExcelReader
 
 
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
import sys
 
 
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
   
 
 
# Functions
# ---------------
 
 
# Main Function
# ---------------
 
def main():
    # INFORMATICA DEV
    connection_names_excel = "testing_inputs\All_connections.xlsx"
    directories = ["D:\Git\Purview\scripts\data files\HIGHLEVEL_SALES_FORECAST"]
    build_mass_lineage_for_folders(prod_client, connection_names_excel, directories)
 
if __name__ == '__main__':
    main()