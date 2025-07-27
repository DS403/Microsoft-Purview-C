## Propagate alternate parse load for data warehouse

```python
from scripts.modules.lineage import *

import json

def example_alternate_parse_load_routine_for_data_warehouse():
    load_routine_file="data_warehouse_install/Routines/AP.LoadAPDimApprovedFlag"
    result = alternate_parse_load_routine_for_data_warehouse(load_routine_file)
    print(result)
```
<br />

## Propagate parse load for data warehouse

```python
from scripts.modules.lineage import *

import json

def example_parse_load_routine_for_data_warehouse():
    load_routine_file="data_warehouse_install/Routines/AP/LoadAPDimApprovedFlag"
    result = parse_load_routine_for_data_warehouse(load_routine_file)
    print(result)
```
<br />

## Propagate alternate parse view for data warehouse

```python
from scripts.modules.lineage import *

import json

def example_alternate_parse_view_for_data_warehouse():
    view_file="Inventory.vwDimMarketingResponsibilityHierarchy.sql"
    result = alternate_parse_view_for_data_warehouse(view_file)
    print(result)
```
<br />

## Propagate parse view for data warehouse

```python
from scripts.modules.lineage import *

import json

def example_parse_view_for_data_warehouse():
    view_file="Inventory.vwDimMarketingResponsibilityHierarchy.sql"
    result = parse_view_for_data_warehouse(view_file)
    print(result)
```
<br />

## Propagate lineage from a source to a table in a data warehouse

```python
from scripts.modules.lineage import *

import json

def example_build_table_to_source_data_warehouse_internal_lineage():
    qualified_name_header = "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/"
    source="abc" #specify the source table name
    table="xyz" #specify the target table name
    result = build_table_to_source_data_warehouse_internal_lineage(qualified_name_header,table,source)
    print(result)
```
<br />

## Propagate lineage lineage from a stage source to a common source then to a view in a data warehouse

```python
from scripts.modules.lineage import *

import json

def example_build_stage_to_common_data_warehouse_internal_lineage():
    qualified_name_header = "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/"
    common_source_for_the_view="abc" #specify the source table name
    stage_source_for_common="xyz" #specify the target table name
    view_purview_partial_path=""
    result = build_stage_to_common_data_warehouse_internal_lineage(qualified_name_header, common_source_for_the_view, stage_source_for_common, view_purview_partial_path)
    print(result)
```
<br />

## Parses a data warehouse view file to establish internal lineage 

```python
from scripts.modules.lineage import *

import json

def example_prod_parse_data_warehouse_view_internal_lineage():
    view_file="Inventory.vwDimMarketingResponsibilityHierarchy.sql"
    result = prod_parse_data_warehouse_view_internal_lineage(view_file)
    print(result)
```
<br />


## Parses a data warehouse table file to establish internal lineage 

```python
from scripts.modules.lineage import *

import json

def example_prod_parse_data_warehouse_table_internal_lineage():
    table_file_name="AP.DimInvoice.sql"
    result = prod_parse_data_warehouse_table_internal_lineage(table_file_name)
    print(result)
```
<br />