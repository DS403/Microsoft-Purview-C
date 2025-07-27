##! /usr/bin/env python3
 
 
# Import Functions
# ---------------
from modules.connection.build_lineage import *
from modules.entity import *
from modules.catalog.qube_ingestion import ingest_qube_data
from utils import get_credentials, create_purview_client
# Import Packages
# ---------------
from pathlib import Path
 
 
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

def main():
    
    # Ingest QUBE data dictionary
    qube_summary = ingest_qube_data(prod_client, 'modules/catalog/QUBE MRI Data Dictionary.csv')
    print(f"QUBE Ingestion Summary: {qube_summary}")

if __name__ == "__main__":
    main()