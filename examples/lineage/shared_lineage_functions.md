## Add manual lineage by creating AtlasEntities for source and target entities

```python
from scripts.modules.lineage import *
import json

def example_add_manual_lineage():
    source_entities=["dimstyle","dimdate","AmzFactDaily"] # specify the source table names
    target_entities=["51.17 - Media Campaign KPI Reporting"]
    process_type_name="sql_database_source"
    result = add_manual_lineage(source_entities, target_entities, process_type_name)
    print(result)
```

<br />


## Get and Add Lineage for a JSON Payload

To populate and upload lineage based on a JSON Payload, you must have a JSON file containing information on the source and target tables within a process. Then, you will use the functions within this repository to extract the source and target table names from that file. Next, you will grab the appropriate entities associated with those table names within Purview. Finally, you will link the entities, adding lineage between them. You will now be able to see a "ingestion_framework" process in Purview that connects the entities.

```python
from scripts.modules.lineage.json_payload_lineage import *
from scripts.modules.lineage.shared_lineage_functions import *
from pathlib import Path
import json

PROJ_PATH = Path(__file__).resolve().parent

def example_get_and_add_lineage_from_payload():
    # Open the JSON file using `with open`
    with open(PROJ_PATH.joinpath('examples/source_code','FactFGInventoryAvailability.json')) as json_file:
        # Load the JSON data
        data = json.load(json_file)

    # Process the payload
    payload = process_payload(data = data)
    print(json.dumps(payload, indent=4))
      
    # Add in admin info
    qualified_name_headers = {
        "ingestion_header": "https://hbiqa01analyticsdls.dfs.core.windows.net",
        "synapse_table_header": "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw"
    }
    entity_type_name = "ingestion_framework"

    # Upload the lineage based off of the payload
    results = upload_lineage_from_payload(payload, qualified_name_headers, entity_type_name)
    for result in results:
        print(json.dumps(result, indent=4))
        print()
```

## Add manual lineage by creating AtlasEntities for source and target entities

```python
from scripts.modules.lineage import *
import json

def example_add_manual_lineage_with_specific_client():
    source_entities=["dimstyle","dimdate","AmzFactDaily"] # specify the source table names
    target_entities=["51.17 - Media Campaign KPI Reporting"]
    process_type_name="sql_database_source"
    source_type_name="azure_dedicated_sql_pool"
    target_type_name="power_bi_dataset"
    target_name_without_special_char="5117MediaCampaignKPIReporting"
    result = add_manual_lineage_with_specific_client(source_entities, target_entities, process_type_name, source_type_name, target_type_name, target_name_without_special_char)
    print(result)
```
<br />

## Add manual lineage by using GUIDS

```python
from scripts.modules.lineage import *
import json

def example_build_lineage_using_guids():
    result=build_lineage_using_guids()
    print(result)
```
<br />