## Establishes a  lineage connection between a Data Bricks and a PowerBI using qualified names

```python
from scripts.modules.lineage import *
import json

def example_build_lineage_from_databricks_to_pbi():
    databricks_qualified_name = "dna.inventory_archive@adb-8254318150804149.9.azuredatabricks.net"
    pbi_dataset_qualified_name = "https://app.powerbi.com/groups/87418287-152f-44c8-931d-7fd6228dda48/datasets/06fa1311-2951-4f57-9037-4b07824fabde"
    result = build_lineage_from_databricks_to_pbi(databricks_qualified_name,pbi_dataset_qualified_name)
    print(result)
```
<br />