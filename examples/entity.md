# Entity Examples

## Create an Entity to Use for Testing

```python
import json
import datetime
from modules import entity

def example_create_entity_for_testing():
    # Using a previously uploaded custom type def. If a new typedef was created for this, make sure to upload it first
    name = "TESTING_PURVIEW_DEV"   
    type_name = "dev_testing_typedef"
    timestamp = datetime.datetime.now().isoformat()
    qualified_name = "testing_for_purview_dev/" + timestamp
    result = create_entity(name, type_name, qualified_name)
    print(result)   

```

<br />

## Create and Upload a Custom Typedef

```python
import json
from modules import entity

TESTING_DEF = EntityTypeDef(
  name = "dev_testing_typedef",
  superTypes = ["DataSet"]
)

def example_upload_custom_typedef():
    result = upload_custom_type_def(TESTING_DEF)
    print(json.dumps(result))
```

<br />

## Get Entity from GUID

```python
def example_get_entity_from_guid():
    guid = "1c940301-a3a5-43a1-8977-479eaa338122"
    result = CLIENT.get_entity(guid)
    result_entities = result["entities"]
    print(result_entities)
```

<br />

## Get Entity from Qualified Name

```python
from modules import entity

def example_get_entity_from_qualified_name():
    qualified_name = "https://example"
    entity = get_entity_from_qualified_name(qualified_name)
    print(entity)
```
<br />

## Get Entity from Qualified Name and Entity Type

```python
from modules import entity

def example_get_entity_from_qualified_name_using_type():
    qualified_name = "https://example"
    entity_type="dev_testing_typedef"
    entity = get_entity_from_qualified_name_using_type(qualified_name,entity_type)
    print(entity)
```

<br />

## Get Entity Typename from Qualified Name

```python
from modules import entity

def example_get_entity_typename_from_qualified_name():
    qualified_name = "https://example"
    entity_typename = get_entity_typename_from_qualified_name(qualified_name)
    print(entity_typename)
```

<br />

## Upload a custom entity type

```python
from modules import entity

def example_upload_custom_type_def():
    type_def = EntityTypeDef(name = "dev_testing_typedef",superTypes = ["DataSet"])
    result = upload_custom_type_def(type_def)
    print(result)
```

## Get Entities by Typename, or Search by Entity Type

```python
from modules import entity

def example_search_by_entity_type():
    entity_type_name = "sap_s4hana_table"
    result = search_by_entity_type(entity_type_name)
    print(result)

def example_search_by_entity_type_with_limit():
    entity_type_name = "sap_s4hana_table"
    result = CLIENT.discovery.browse(entityType = entity_type_name, limit = 5)    
    print(result)   
```


## Delete entity by Entity Type

```python
from modules import entity

def example_delete_by_entity_type():
    entity_type_name = "sap_s4hana_table"
    result = delete_by_entity_type(entity_type_name)
    print(result)
    
```

## Get Entities GUID by Entity Type

```python
from modules import entity

def example_get_guids_of_entities_with_specific_type():
    entity_type_name = "sap_s4hana_table"
    result = get_guids_of_entities_with_specific_type(entity_type_name)
    print(result)
    
```

## Get all columns from datalake by using entity GUID 

```python
from modules import entity

def example_get_columns_from_datalake():
    tabular_schema_guid = "6523d0ca-8804-49fd-a09d-eac2f9ffa977" #example guid
    result = get_columns_from_datalake(tabular_schema_guid)
    print(result)
    
```
## Get all Entity details by Entity Type

```python
from modules import entity

def example_get_all_entities_with_type():
    entity_type_name = "sap_s4hana_table"
    result = get_all_entities_with_type(entity_type_name)
    print(result)
    
```

## Get all Entity from purview

```python
from modules import entity

def example_pull_entities_from_purview():
    purview_account_short_name = "qa" #example
    purview_account_full_name = "hbi-qa01-datamgmt-pview"
    result = pull_entities_from_purview(purview_account_short_name, purview_account_full_name)
    print(result)
    
```

## Upload custom type def's 

```python
from modules import entity

def example_upload_custom_type_def_with_specific_client():
    TESTING_DATASET_DEF = EntityTypeDef(
    name = "dev_testing_typedef",
    superTypes = ["DataSet"]
    )
    type_def=TESTING_DATASET_DEF
    result = upload_custom_type_def_with_specific_client(type_def: EntityTypeDef)
    print(result)
    
```
## Get all nested entities from qualified name 

```python
from modules import entity

def example_get_all_entities_nested_from_qualified_name():
    qualified_name="https://hbipd01analyticsdls.dfs.core.windows.net/raw/Example"
    result = get_all_entities_nested_from_qualified_name(qualified_name)
    print(result)
    
```

## Get all lineage connections for the specified purview account

```python
from modules import entity

def example_pull_lineage_connections_from_purview():
    purview_account_short_name = "pd" #example
    purview_account_full_name = "hbi-pd01-datamgmt-pview"
    result = pull_lineage_connections_from_purview(purview_account_short_name,purview_account_full_name)
    print(result)
    
```

