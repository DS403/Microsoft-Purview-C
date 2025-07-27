## Move the entity and all the nested entities to the specified collection

```python
from modules.collection.azure_dw_collection_sorting import *

def move_azure_dw_to_collection():
    REFERENCE_NAME_PURVIEW = "hbi-pd01-datamgmt-pview"
    CREDS = get_credentials(cred_type= 'default')
    client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)
    
    schema_guid = "0f6c798e-0b32-4d5d-867d-916e8b015071" # inventory in Prod
    collection_id = "mn8dqe" # inventory
    result = pull_and_move_azure_dw_schema_and_nested_entities_to_collections(client, schema_guid, collection_id)
    print()
    print(result)

```