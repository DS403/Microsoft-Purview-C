## Confirm that the tables in the source_tables list are not present in the target_tables list

```python
from scripts.modules.lineage import *
import json

def example_confirm_source_not_target():
    source_tables=["dimstyle","dimdate","AmzFactDaily"]
    target_tables=["51.17 - Media Campaign KPI Reporting"]
    result = confirm_source_not_target(source_tables, target_tables)
    print(result)
```
<br />

## Extract the source and target tables from a stored procedure SQL file.

```python
from scripts.modules.lineage import *
import json

def example_extract_source_and_target_from_stored_procedure():
    sql_file_path="examples/source_code/DimWinningPortfolioSkuList.sql"
    result = extract_source_and_target_from_stored_procedure(sql_file_path)
    print(result)
```
<br />