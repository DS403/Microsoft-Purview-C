
## Parses tables from an Excel file and uploads them to Apache Atlas in a predefined structure.

```python
from scripts.modules.lineage import *
import json

def example_build_powerbi_lineage_from_sql_query():
    source_entities_qualified_paths=["mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/Common/DimStyle","mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/Common/DimDate"]
    
    target_entity_qualified_path="https://app.powerbi.com/groups/8864c31d-1a84-42cb-8ae3-a769271b334f/datasets/4b9b5c4c-d93f-42f8-99df-f39bf8d82236"
    
    target_name_without_special_char = "5114AmazonKPIReporting"

    result = build_powerbi_lineage_from_sql_query(source_entities_qualified_paths, target_entity_qualified_path, target_name_without_special_char)
    print(result)
```
<br />