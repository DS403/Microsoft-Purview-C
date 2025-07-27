## Build lineage between a SharePoint entity and a Power BI dataset by creating AtlasEntities

```python
from scripts.modules.lineage import *
import json

def example_build_sharepoint_to_pbi_lineage():
    sharepoint_source = {
        "name": "SharePoint Document Library",
        "entityType": "sharepoint_entity_type",
        "qualifiedName": "sharepoint://example.com/documents",
        "id": "sharepoint_entity_id"
    }
    sharepoint_short_name = "sharepoint_docs"
    pbi_target = {
        "name": "Sales Dashboard Dataset",
        "entityType": "powerbi_dataset_entity_type",
        "qualifiedName": "powerbi://workspace/sales_dashboard",
        "id": "powerbi_dataset_id"
    }
    pbi_short_name = "sales_dashboard"
    process_type_name = "data_transformation"
    result = build_sharepoint_to_pbi_lineage(sharepoint_source, sharepoint_short_name, pbi_target, pbi_short_name, process_type_name)
    print(result)
```
<br />


## Create a SharePoint entity in the Purview Atlas

```python
from scripts.modules.lineage import *
import json

def example_create_sharepoint_entity():
    entity_name="Control Table ASIN Distribution"

    entity_qualified_name="sharepoint://hanes.sharepoint.com/Control_Table_ASIN_Distribution"

    actual_sharepoint_link="https://hanes.sharepoint.com/:x:/r/sites/GrowthTeamSupport/_layouts/15/Doc.aspx?sourcedoc=%7B124ACCA7-B22B-4B87-A2F8-ADCCC2CF5563%7D&file=Control%20Table%20ASIN%20Distribution..xlsx&wdLOR=c2860C007-B39E-422A-8453-942CA6124878&action=default&mobileredirect=true"

    result = create_sharepoint_entity(entity_name, entity_qualified_name, actual_sharepoint_link)
    print(result)
```
<br />

## Create a SharePoint entity and build lineage to a Power BI dataset

```python
from scripts.modules.lineage import *
import json

def example_create_sharepoint_entity_and_build_lineage_to_pbi():
    entity_qualified_name="sharepoint://hanes.sharepoint.com/Control_Table_ASIN_Distribution"

    actual_sharepoint_link="https://hanes.sharepoint.com/:x:/r/sites/GrowthTeamSupport/_layouts/15/Doc.aspx?sourcedoc=%7B124ACCA7-B22B-4B87-A2F8-ADCCC2CF5563%7D&file=Control%20Table%20ASIN%20Distribution..xlsx&wdLOR=c2860C007-B39E-422A-8453-942CA6124878&action=default&mobileredirect=true"
    
    pbi_dataset_qualified_name="https://app.powerbi.com/groups/8864c31d-1a84-42cb-8ae3-a769271b334f/datasets/d2e8f683-32cb-4647-a7d6-c85f701239a7"

    pbi_short_name="Amazon"
    result = create_sharepoint_entity_and_build_lineage_to_pbi(entity_name, actual_sharepoint_link, pbi_dataset_qualified_name, pbi_short_name)
    print(result)
```
<br />

