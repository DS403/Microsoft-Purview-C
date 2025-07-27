## Parses tables from an Excel file and uploads them to Apache Atlas in a predefined structure.

```python
from scripts.modules.lineage import *
import json

def example_parse_pkms_tables_from_excel():
    file_name="lineage.json"
    result = parse_pkms_tables_from_excel(file_name)
    print(result)
```
<br />