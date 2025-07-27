# Managed Attributes Examples

## Create a Managed Attribute Group and Attributes

In order to create managed attributes, you have to first create a managed attribute group for those attributes. Thus you must specifiy the group name as well as all of the attribute names for within that group.

```python
from scripts.modules.managed_attributes import *
import json

def example_create_managed_attribute_group_and_attributes():
    # Create an attribute group and attributes
    attribute_group_name = "PRODUCT"
    attribute_names = ["SIZE", "STRUCTURE"]

    # Upload and create the attribute group and attributes
    response = create_attribute(CLIENT, attribute_group_name, attribute_names)
    print(json.dumps(response))
```


## Add Managed Attributes to an Entity

With an exisiting managed attribute, you can add a value to that attribute for a particular entity. You will need to first pull the entity you would like to associate this attribute with. Then you specify the attribute's name and the value you want to give it for this entity. Finally, you upload and add the attribute to the entity.

```python
from scripts.modules.managed_attributes import *
from scripts.modules.entity import *
import json

def example_add_attributes_to_entity():
    # Get an entity
    qualified_name = "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw/Common/DimWinningPortfolioSkuList"
    entity = get_entity_from_qualified_name(qualified_name)
    entity_type = AtlasEntity(
        name = entity["name"],
        typeName = entity["typeName"],
        guid = entity["guid"]
    )

    # Add attribute values to an entity
    attribute_name = "SIZE"
    attribute_value = "15.5"
    response = add_attributes_to_entity(CLIENT, entity_type, attribute_group_name, attribute_name, attribute_value)
    print(json.dumps(response))
```

## Delete Managed Attributes from an Entity

With an exisiting managed attribute, you can delete a value to that attribute for a particular entity. You will need to first pull the entity you would like to associate this attribute with. Then you specify the attribute's name and the value you want to delete it for this entity. Finally, you delete the attribute to the entity.

```python
from scripts.modules.managed_attributes import *
from scripts.modules.entity import *
import json

def example_delete_attributes_to_entity():
    # Get an entity
    qualified_name = "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw/Common/DimWinningPortfolioSkuList"
    entity = get_entity_from_qualified_name(qualified_name)
    entity_type = AtlasEntity(
        name = entity["name"],
        typeName = entity["typeName"],
        guid = entity["guid"]
    )

    # Delete attribute values to an entity
    attribute_group_name = "PRODUCT"
    attribute_names = "SIZE"
    response = delete_attribute(CLIENT, guid, attribute_group_name, attribute_name)
    print(json.dumps(response))
```