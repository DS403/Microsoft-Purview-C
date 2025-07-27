## Move the packages and all the nested packages and tables to the specified collection

```python
from modules.collection.sap_s4hana_collection_sorting import *

def move_sap_s4hana_to_collection():
    REFERENCE_NAME_PURVIEW = "hbi-pd01-datamgmt-pview"
    CREDS = get_credentials(cred_type= 'default')
    client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)
    
    application_component_guid = "5107e860-54fd-4ef6-b960-3fb7284504a7"
    collection_id = "x9hxp5"
    result = pull_and_move_s4hana_application_component_and_nested_entities_to_collection(CLIENT, application_component_guid, collection_id)
    print(result)

```