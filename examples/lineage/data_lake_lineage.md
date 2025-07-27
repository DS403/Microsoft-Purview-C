## Establishes a  lineage connection between a data lake curated and a data warehouse stage using guid

```python
from scripts.modules.lineage import *
import json

def example_build_lineage_from_data_lake_curated_to_data_warehouse_stage():
    dl_curated_guid = "b04f2019-f01b-48b6-a723-98fda351c442"
    dw_stage_guid = "e80d2227-5f7e-4cc0-a4bf-d7f6f6f60000"
    result = build_lineage_from_data_lake_curated_to_data_warehouse_stage(dl_curated_guid,dw_stage_guid)
    print(result)
```
<br />

## Establishes a  lineage connection between a data lake stage and a data lake curated using guid

```python
from scripts.modules.lineage import *
import json

def example_build_lineage_from_data_lake_stage_to_curated():
    stage_guid = "2d5051af-7157-4e85-8b1b-b3f6f6f60000"
    curated_guid = "3be3ed28-803e-48ee-90e0-b98519c18f76"
    result = build_lineage_from_data_lake_stage_to_curated(stage_guid,curated_guid)
    print(result)
```
<br />

## Establishes a  lineage connection between a manual file and a data lake stage using guid

```python
from scripts.modules.lineage import *
import json

def example_build_lineage_from_data_lake_manual_file_to_data_lake_stage():
    manual_file_guid = "55fb011c-8680-4963-ad55-64f6f6f60000"
    dl_stage_guid = "3be3ed28-803e-48ee-90e0-b98519c18f76"
    result = build_lineage_from_data_lake_manual_file_to_data_lake_stage(manual_file_guid,dl_stage_guid)
    print(result)
```
<br />

## Establishes a  lineage connection between a data lake curated and a data lake curated using guid

```python
from scripts.modules.lineage import *
import json

def example_build_lineage_from_data_lake_curated_to_data_lake_curated():
    source_curated_guid = "55fb011c-8680-4963-ad55-64f6f6f60000"
    target_curated_guid = "3be3ed28-803e-48ee-90e0-b98519c18f76"
    result = build_lineage_from_data_lake_curated_to_data_lake_curated(source_curated_guid,target_curated_guid)
    print(result)
```
<br />