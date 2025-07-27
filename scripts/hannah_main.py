##! /usr/bin/env python3


# Import Functions
# ---------------

from modules import entity
from modules.lineage.cube_lineage import *
from modules.lineage.magento_lineage import *
from modules.lineage.databricks_lineage import *
from modules.lineage.data_lake_lineage import *
from modules.lineage.data_warehouse_internal_lineage import *
from modules.lineage.json_payload_lineage import *
from modules.lineage.informatica_lineage import *
from modules.lineage.oracle_server_lineage import *
#from modules.lineage.pkms_lineage import *
from modules.lineage.powerbi_sql_query_lineage import *
from modules.lineage.analysis_services_tabular_model_lineage import *
from modules.lineage.sap_hana_internal_lineage import *
from modules.lineage.shared_lineage_functions import *
from modules.lineage.sharepoint_lineage import *
from modules.lineage.sql_server_lineage import *

from modules.glossary_propagation.shared_glossary_functions import *
from modules.glossary_propagation.sap_hana_glossary_propagation import *
from modules.glossary_propagation.sap_s4hana_glossary_propagation import *
from modules.glossary_propagation.datalake_glossary_propagation import *
from modules.glossary_propagation.sql_dw_glossary_propagation import *
from modules.entity import *
from modules.collection.collection_shared_functions import *
from modules.collection.sap_s4hana_collection_sorting import *
from modules.collection.azure_dw_collection_sorting import *
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

    # 1
    #manual_file = "df5e833e-1b9f-4c00-ab44-9f4933a24690"
    dl_stage_guid = "4bbb5abe-6de6-45b2-a0db-36358541d7ce"
    #build_lineage_from_data_lake_manual_file_to_data_lake_stage(prod_client, manual_file, dl_stage_guid)
    
    #oracle_guid = "bcc4fbe8-ea77-4e82-9aaf-51f6f6f60000"
    #dl_stage_guid = "ff50a3fd-b6df-4e00-978c-4e139b625942" # FIRST ONE
    #build_lineage_from_oracle_to_data_lake_stage(prod_client, oracle_guid, dl_stage_guid)


    # 2
    dl_stage_guid = "4bbb5abe-6de6-45b2-a0db-36358541d7ce"
    dl_curated_guid = "8ea6f622-e702-4fc6-bb8e-56e6edc9987b"
    #build_lineage_from_data_lake_stage_to_curated(prod_client, dl_stage_guid, dl_curated_guid)
    
    
    #2.5 Curated to Curated
    """source_dl_curated_guid = "bdacd724-28c8-43e5-a246-01046bc7cba0" # dim item lifecycle
    target_dl_curated_guid = "8a759261-1c79-4b35-a212-4fe295da9e57" # amz fact daily
    #build_lineage_from_data_lake_curated_to_data_lake_curated(prod_client, source_dl_curated_guid, target_dl_curated_guid)
    """

    # 3
    dl_curated_guid = "8ea6f622-e702-4fc6-bb8e-56e6edc9987b"
    dw_guid = "55248dad-cd9e-42b7-987b-4af6f6f60000"
    #build_lineage_from_data_lake_curated_to_data_warehouse_stage(prod_client, dl_curated_guid, dw_guid)
    

    """connection_names_excel = "All_connections.xlsx"
    directories = ["informatica"]
    build_mass_lineage_for_folders(prod_client, connection_names_excel, directories)"""

    # Parse the Excel file
    magento_excel = "Magento_Upload.xlsx"
    entity_dict = parse_excel_file(magento_excel)

    # Upload entities to Purview
    result = upload_entities_to_purview(prod_client, entity_dict, "product_feed")
    print(result)


  
if __name__ == '__main__':
    main()
