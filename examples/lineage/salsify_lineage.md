## create column and entity name mappings for a given salsify excel file

```python
from scripts.modules.salsify import *
import json

def example_parse_salsify():
    file="Salsify_Import_to_Run_May_2024.xlsx"
    result = parse_salsify(file)
    print(result)
```
<br />

## create a dataframe with column mappings and save it to csv.

```python
from scripts.modules.salsify import *
import json

def example_parse_salsify_dict():
    salsify_dict=parse_salsify("Salsify_Import_to_Run_May_2024.xlsx")
    result = parse_salsify_dict(salsify_dict)
    print(result)
```
<br />

## Get the hierarchy relationship between the colums for the given salsify file.

```python
from scripts.modules.salsify import *
import json

def example_get_salsify_hierarchy():
    file="Salsify_Import_to_Run_May_2024.xlsx"
    hierarchy_cols=['a','b','c']
    result = get_salsify_hierarchy(file,hierarchy_cols)
    print(result)
```
<br />

## Parse the file to get column names mapped to their descriptions

```python
from scripts.modules.salsify import *
import json

def example_get_salsify_descriptions():
    file_path="Salsify_Import_to_Run_May_2024.xlsx"
    col_lst=['a','b','c']
    result = get_salsify_descriptions(file_path, col_lst)
    print(result)
```
<br />

## Create classification if it do not exist

```python
from scripts.modules.salsify import *
import json

def example_create_classification():
    client="qa"
    classification_name="ABC"
    classification_desc="This is ABC Classification"
    attribut_name="XYZ"
    result = create_classification(client,classification_name,classification_desc,attribut_name)
    print(result)
```
<br />

## Create a tabular relationship for the given record_guid and tab_guid

```python
from scripts.modules.salsify import *
import json

def example_get_tab_dataset_relationship():
    record_guid="55fb011c-8680-4963-ad55-64f6f6f60000"
    tab_guid="3be3ed28-803e-48ee-90e0-b98519c18f76"
    result = get_tab_dataset_relationship(record_guid,tab_guid)
    print(result)
```
<br />


## Upload column entities for the given record_guid and tab_guid

```python
from scripts.modules.salsify import *
import json

def example_upload_column_entities():
    client="prod"
    record_guid="55fb011c-8680-4963-ad55-64f6f6f60000"
    tab_guid="3be3ed28-803e-48ee-90e0-b98519c18f76"
    result = upload_column_entities(client,columns_to_add,record_guid,tab_guid)
    print(result)
```
<br />

## Retrieves an entity from the catalog based on the provided qualified name.

```python
from scripts.modules.salsify import *
import json

def example_get_entity_from_qualified_name():
    client="qa"
    qualified_name="salsify://parent_style"
    result = get_entity_from_qualified_name(client, qualified_name)
    print(result)
```
<br />

## Check if an asset is already present with the qualified name

```python
from scripts.modules.salsify import *
import json

def example_is_asset_exists():
    client="qa"
    qualified_name="salsify://parent_style"
    result = is_asset_exists(client,qualified_name)
    print(result)
```
<br />

## Check if an asset is already present with the qualified name

```python
from scripts.modules.salsify import *
import json

def example_get_all_columns_from_qualified_name():
    client="qa"
    qualified_name="salsify://parent_style"
    result = get_all_columns_from_qualified_name(client,qualified_name)
    print(result)
```
<br />

## Delete entity for a given purview client by entity

```python
from scripts.modules.salsify import *
import json

def example_delete_entity_by_qualified_name():
    client="qa"
    entity={'guid:'18abc679-0dfe-41fe-b05c-b4ca8f261902'}
    result = delete_entity_by_qualified_name(client,entity)
    print(result)
```
<br />

## Get all classification in the given purview client

```python
from scripts.modules.salsify import *
import json

def example_get_all_classifications_names():
    client="qa"
    result = get_all_classifications_names(client)
    print(result)
```
<br />

## Parses tables from an Excel file and uploads them to Apache Atlas in a predefined structure

```python
from scripts.modules.salsify import *
import json

def example_salsify_lineage():
    client="qa"
    file_name="salsify_mappings_test.csv"
    result = salsify_lineage(client, file_name)
    print(result)
```
<br />