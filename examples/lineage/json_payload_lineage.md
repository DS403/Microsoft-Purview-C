## Extracts the source location and target table name from an SQL file

```python
from scripts.modules.lineage import *
import json

def example_get_info_from_entity_dict():
    entity_dict = {
        "path": "database.schema.table",
        "name": "DimInvoice"
    }

    qualified_name_headers = {
        "ingestion_header": "ingestion_database"
    }
    result = get_info_from_entity_dict(entity_dict, qualified_name_headers)
    print(result)
```
<br />

## Uploads lineage information from the given payload dictionary

```python
from scripts.modules.lineage import *
import json

def example_upload_lineage_from_payload():
    payload = {
    "process": [
        {
            "sourceDataPayload": {"name": "SourceTable", "qualified_name": "source_table_1"},
            "targetDataPayload": {"name": "TargetTable", "qualified_name": "target_table_1"}
        },
        {
            "sourceDataPayload": {"name": "SourceTable2", "qualified_name": "source_table_2"},
            "targetDataPayload": {"name": "TargetTable2", "qualified_name": "target_table_2"}
        }
    ]
    }
    entity_dict = {
        "path": "database.schema.table",
        "name": "DimInvoice"
    }

    qualified_name_headers = {
        "ingestion_header": "ingestion_database"
    }
    entity_type_name="power_bi_table"
    result = upload_lineage_from_payload(payload, qualified_name_headers, entity_type_name)
    print(result)
```
<br />

## Process the JSON file and extract the source, target, and process payloads.

```python
from scripts.modules.lineage import *
import json

def example_process_json_file():
    file_path="scripts\ProcessPayloads\Curated\Amazon\Explore.Amz.Fact.Daily.json"
    result = process_json_file(file_path)
    print(result)
```
<br />

## Process the JSON file and extract the source, target, and process payloads.

```python
from scripts.modules.lineage import *
import json

def example_process_payload():
    data = {} # specify the required data in dict 
    result = process_payload(data)
    print(result)
```
<br />

## Processes a JSON payload containing lineage information from a data lake to a data warehouse

```python
from scripts.modules.lineage import *
import json

def example_process_payload():
    file_name = "Explore.Amz.Fact.Daily.sql"
    result = datalake_to_data_warehouse_lineage_from_payload(file_name)
    print(result)
```
<br />


## Establishes a  lineage connection between a Data Lake (DL) and a Data Warehouse (DW) using qualified names

```python
from scripts.modules.lineage import *
import json

def example_manually_connect_dl_to_dw_via_qualified_names():
    source_qual_name = "pyapacheatlas://datalake_entity"
    target_qual_name = "pyapacheatlas://datawarehouse_entity"
    result = manually_connect_dl_to_dw_via_qualified_names(source_qual_name, target_qual_name)
    print(result)
```
<br />
