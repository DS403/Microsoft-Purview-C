## Establishes a  lineage connection between a Oracle and a PowerBI using qualified names

```python
from scripts.modules.lineage import *

import json

def example_build_lineage_from_oracle_server_to_pbi():
    oracle_asset_qualified_name = "oracle://10.1.17.241/STAGING/%1000b7b2_ObjectReference"
    pbi_dataset_qualified_name = "https://app.powerbi.com/groups/87418287-152f-44c8-931d-7fd6228dda48/datasets/06fa1311-2951-4f57-9037-4b07824fabde"
    result = build_lineage_from_oracle_server_to_pbi(oracle_asset_qualified_name,pbi_dataset_qualified_name)
    print(result)
```
<br />

## Establishes a  lineage connection between a Oracle and a Datalake using GUID

```python
from scripts.modules.lineage import *
import json

def example_build_lineage_from_oracle_to_data_lake_stage():
    oracle_guid = "e55a7cd9-6318-4708-9205-c3cee51e1b59"
    dl_stage_guid = "3be3ed28-803e-48ee-90e0-b98519c18f76"
    result = build_lineage_from_oracle_to_data_lake_stage(oracle_guid,dl_stage_guid)
    print(result)
```
<br />