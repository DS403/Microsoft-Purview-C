## Extracts the source location and target table name from an SQL file

```python
from scripts.modules.lineage import *
import json

def example_extract_source_and_target_from_external_table():
    sql_file_path="data_warehouse_install/RoutinesAP/DimInvoice.sql"
    result = extract_source_and_target_from_external_table(sql_file_path)
    print(result)
```
<br />