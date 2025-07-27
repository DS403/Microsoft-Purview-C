## Establishes a  lineage connection between a cube and a power BI using guid

```python
from scripts.modules.lineage import *
import json

def example_build_lineage_from_cube_to_pbi():
    source_curated_guid = "64f6f6f60000-55fb011c-8680-4963-ad55"
    target_curated_guid = "803e-48ee-90e0-b98519c18f76-3be3ed28"
    result = build_lineage_from_cube_to_pbi(source_curated_guid,target_curated_guid)
    print(result)
```
<br />