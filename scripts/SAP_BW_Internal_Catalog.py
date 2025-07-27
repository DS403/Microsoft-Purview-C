import csv
import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.purview.catalog import PurviewCatalogClient
from azure.core.exceptions import HttpResponseError

# Purview Account Name and Endpoint
# Replace with your Purview account name as per the requirement QA/PROD
purview_account_name = "hbi-pd01-datamgmt-pview" 
purview_endpoint = f"https://{purview_account_name}.purview.azure.com"

# Authenticate with Default Azure Credentials (using environment-based credentials like Azure CLI)
credential = DefaultAzureCredential()

# PurviewCatalogClient for catalog operations
catalog_client = PurviewCatalogClient(endpoint=purview_endpoint, credential=credential)

# Prompt user for CSV file name and collection ID
# Note: Ensure the CSV file is in the same directory as this script or provide the full path.
csv_file_path = input("Enter the CSV file name (with .csv extension): ").strip()
collection_id = input("Enter the collection ID: ").strip()

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path, sep=',', dtype=str, usecols=["DEVCLASS", "COMPONENT", "PARENTCL", "CTEXT"]).fillna("")

# Clean the column names (remove leading/trailing spaces and convert to uppercase)
df.columns = df.columns.str.strip().str.upper()

# Iterate over the rows of the DataFrame to create assets
for index, row in df.iterrows():
    # Access cleaned column names
    asset_name = row["DEVCLASS"]  
    asset_description = row["CTEXT"]

    #Construct the asset
    entity = {
        "entity": {
            "typeName": "sap_bw_instance",  # Asset type
            "attributes": {
                "name": asset_name, # Asset name
                "description": asset_description, # Asset description
                "qualifiedName": f"sap_bw://{collection_id}/{asset_name}"  # Qualified name
            }
        }
    }

    # Create or update the asset in the specified collection
    try:
        response = catalog_client.collection.create_or_update(collection_id, entity)
        print(f"[SUCCESS] Imported asset '{asset_name}' into collection '{collection_id}'")
    except HttpResponseError as e:
        print(f"[FAILED] Could not import asset '{asset_name}' - {e.message}")
    except Exception as e:
        print(f"[FAILED] Unexpected error for asset '{asset_name}' - {str(e)}")
