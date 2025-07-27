## Establishes a  lineage connection between a sql server and a power bi using qualified name

```python
from scripts.modules.lineage import *
import json

def example_build_lineage_from_sql_server_to_pbi():
    sql_asset_qualified_name = "mssql://BIPAOSQL.res.hbi.net/MSSQLSERVER/HBIDW/Samba/dim_Promo"
    pbi_dataset_qualified_name = "https://app.powerbi.com/groups/87418287-152f-44c8-931d-7fd6228dda48/datasets/06fa1311-2951-4f57-9037-4b07824fabde"
    result = build_lineage_from_sql_server_to_pbi(sql_asset_qualified_name,pbi_dataset_qualified_name)
    print(result)
```
<br />

## Establishes a  lineage connection between a sql view and a data lake stage using guid

```python
from scripts.modules.lineage import *
import json

def example_build_lineage_from_sql_vw_to_data_lake_stage():
    sql_vw_guid = "2d5051af-7157-4e85-8b1b-b3f6f6f60000"
    dl_stage_guid = "3be3ed28-803e-48ee-90e0-b98519c18f76"
    result = build_lineage_from_sql_vw_to_data_lake_stage(sql_vw_guid,dl_stage_guid)
    print(result)
```
<br />

## Establishes a  lineage connection between a sql table and a data lake stage using guid

```python
from scripts.modules.lineage import *
import json

def example_build_lineage_from_sql_table_to_data_lake_stage():
    sql_table_guid = "28a46c6f-c679-4ddf-8e2f-1df6f6f60000"
    dl_stage_guid = "3be3ed28-803e-48ee-90e0-b98519c18f76"
    result = build_lineage_from_sql_table_to_data_lake_stage(sql_table_guid,dl_stage_guid)
    print(result)
```
<br />