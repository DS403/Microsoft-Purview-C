##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules.glossary_propagation.shared_glossary_functions import *


# Package Imports
# ---------------
from pyapacheatlas.core.typedef import EntityTypeDef, AtlasAttributeDef
from pyapacheatlas.core import AtlasEntity, AtlasProcess, PurviewClient
from pathlib import Path


# Constants
# ---------------

INGESTION_FRAMEWORK_DEF = EntityTypeDef(
  name = "ingestion_framework",
  superTypes = ["Process"]
)

DATA_WAREHOUSE_LOAD_ROUTINE_DEF = EntityTypeDef(
  name = "dw_routine",
  superTypes = ["Process"]
)

DATA_WAREHOUSE_VIEW_CREATION_DEF = EntityTypeDef(
  name = "dw_view_creation",
  superTypes = ["Process"]
)

DSP_CONNECTION_DEF = EntityTypeDef(
  name = "dsp_connection",
  superTypes = ["Process"]
)

SHAREPOINT_ENTITY_DEF = EntityTypeDef(
  name = "SharePoint Entity",
  superTypes = ["DataSet"]
)

SHAREPOINT_TO_PBI_DEF = EntityTypeDef(
  name = "sharepoint_to_pbi",
  superTypes = ["Process"]
)
  
DATABRICKS_TO_PBI_DEF = EntityTypeDef(
  name = "Databricks_to_PBI",
  superTypes = ["Process"]
)

SQL_SERVER_TO_PBI_DEF = EntityTypeDef(
  name = "SQL_Server_to_PBI",
  superTypes = ["Process"]
)

ORACLE_SERVER_TO_PBI_DEF = EntityTypeDef(
  name = "Oracle_Server_to_PBI",
  superTypes = ["Process"]
)

CUBE_TO_PBI_DEF = EntityTypeDef(
  name = "Cube_to_PBI",
  superTypes = ["Process"]
)

DATA_LAKE_STAGE_TO_CURATED_DEF = EntityTypeDef(
  name = "DL_Stage_to_DL_Curated",
  superTypes = ["Process"]
)

DATA_LAKE_CURATED_TO_DATA_WAREHOUSE_STAGE_DEF = EntityTypeDef(
  name = "DL_Curated_to_DW_Stage",
  superTypes = ["Process"]
)

ORACLE_TO_DATA_LAKE_STAGE_DEF = EntityTypeDef(
  name = "Oracle_to_DL_Stage",
  superTypes = ["Process"]
)

DATA_LAKE_MANUAL_FILE_TO_DATA_LAKE_STAGE_DEF = EntityTypeDef(
  name = "DL_Manual_File_to_DL_Stage",
  superTypes = ["Process"]
)

SQL_VIEW_TO_DATA_LAKE_STAGE_DEF = EntityTypeDef(
  name = "SQL_VW_to_DL_Stage",
  superTypes = ["Process"]
)

SQL_TABLE_TO_DATA_LAKE_STAGE_DEF = EntityTypeDef(
    name = "SQL_Table_to_DL_Stage",
    superTypes = ["Process"]
)

DATA_LAKE_CURATED_TO_DATA_LAKE_CURATED_DEF = EntityTypeDef(
    name = "DL_Curated_to_DL_Curated",
    superTypes = ["Process"]
)

SQL_DATABASE_EXTRACT_ATTRIBUTES = AtlasAttributeDef(
    displayName = "SQL Database Extract",
    description = "This type is used to connect Power BI datasets to Synapse.",
    name = "sql_database_extract"
)
    
SQL_DATABASE_EXTRACT_TYPEDEF = EntityTypeDef(
  name = "sql_database_extract",
  superTypes = ["Process"],
  attributeDefs = [SQL_DATABASE_EXTRACT_ATTRIBUTES]
)

PKMS_RECORD_DEF = EntityTypeDef(
  name = "PKMS_Record",
  superTypes = ["DataSet"]
)

PKMS_COLUMN_DEF = EntityTypeDef(
  name = "PKMS_Column",
  superTypes = ["Column"]
)

DW_TO_PBI_DATASET_DEF = EntityTypeDef(
  name = "DW_to_PBI_Dataset",
  superTypes = ["Process"]
)

TABULAR_MODEL_TO_PBI_DATASET_DEF = EntityTypeDef(
  name = "Tabular_Model_to_PBI_Dataset",
  superTypes = ["Process"]
)

INFORMATICA_CONNECTION_DEF = EntityTypeDef(
  name = "Informatica_Connection",
  superTypes = ["Process"]
)

Column_Connection_Def = EntityTypeDef(
  name = "Column_Mapping",
  superTypes = ["Process"],
  attributes = [
        AtlasAttributeDef("columnMapping")
    ]
)

# Functions
# ---------------

def create_entity(client, name: str, type_name: str, qualified_name: str):
    """
    Creates and uploads a single Atlas entity with specified properties.

    Parameters:
        client (PurviewClient): The Purview client used for entity upload.
        name (str): The name of the entity.
        type_name (str): The type name of the entity.
        
        qualified_name (str): The qualified name of the entity.

    Returns:
        dict: The result of the entity upload operation.
    """
    atlas_entity = AtlasEntity(name = name, typeName = type_name, qualified_name = qualified_name)
    result = client.upload_entities(atlas_entity)
    return result


def get_entity_from_qualified_name(client, qualified_name):
    """
    Retrieves an entity from the catalog based on the provided qualified name.

    Args:
        qualified_name (str): The qualified name of the entity.

    Returns:
        dict: The entity found based on the qualified name.
    """
    entities_found = client.discovery.search_entities(query=qualified_name)
    for entity in entities_found:
        # Since the input qualified_name is all lowercase, we cannot do a direct str comparison, we must check length
        # This is to avoid qualified names that have the same beginning and different extensions
        # Allow length to differ by 1 for potential '/' at the end
        if ((len(entity["qualifiedName"]) == len(qualified_name)) or (len(entity["qualifiedName"]) == len(qualified_name) + 1)) and qualified_name in entity["qualifiedName"]:
            return entity

    return None


def get_entity_from_qualified_name_using_type(client, qualified_name, entity_type):
    """
    Retrieves an entity's details from Purview using its qualified name and entity type.

    Parameters:
    - client: Purview client for making API requests.
    - qualified_name (str): The qualified name of the entity to retrieve.
    - entity_type (str): The type of the entity to retrieve.

    Returns:
    - dict or None: A dictionary containing the details of the entity if found, 
      or None if the entity is not found.
    """
    browse_result = client.discovery.browse(entityType=entity_type)
    # utilize offset to skip the first results, until you reach the count number
    # result of browse is a dict of @search.count and value
    
    # the "value" gives results in increments of 100
    total_search_count = browse_result.get("@search.count")
    count = 0
    list_of_guids = []
    while count < total_search_count:
        browse_result = client.discovery.browse(entityType = entity_type, offset = count)
        entities = browse_result.get("value")
        count += len(entities)
        
        for value_dict in entities:
            if value_dict.get("qualifiedName") == qualified_name:
                return value_dict

    return None


def get_entity_typename_from_qualified_name(client, qualified_name):
    """
    Retrieves the entity type name from the qualified name using the Purview client.

    Parameters:
        client (PurviewClient): The Purview client.
        qualified_name (str): The qualified name of the entity.

    Returns:
        str: The entity type name.
    
    Raises:
        ValueError: If more than one entity or no entity is found for the given qualified name.
    """
    entities_found = client.discovery.search_entities(query=qualified_name)
    entities = []
    for entity in entities_found:
        if (len(entity["qualifiedName"]) == len(qualified_name)) or (len(entity["qualifiedName"]) == len(qualified_name) + 1):
            entities.append(entity)

    if len(entities) > 1:
        raise ValueError(f"More than one entity was returned. There should only be one entity returned from a qualified name. The qualified name used was: {qualified_name}")
    elif len(entities) == 0:
        raise ValueError(f"No entity was found with this qualified name: {qualified_name}")

    entity_typename = entities[0]["entityType"]
    return entity_typename


def get_all_typedefs(client):
    """
    Retrieves all relationship type names from the Purview client.

    Parameters:
        client (PurviewClient): The Purview client.

    Returns:
        list: A list of unique relationship type names.
    """
    all_typedefs = client.get_all_typedefs()
    entity_defs = all_typedefs["entityDefs"]
    all_type_names = []

    for entity in entity_defs:
        rel_attr_defs = entity["relationshipAttributeDefs"]
        for td in rel_attr_defs:
            all_type_names.append(td["relationshipTypeName"])

    unique_type_names = list(set(all_type_names))
    return unique_type_names


def upload_custom_type_def(client, type_def: EntityTypeDef):
    """
    Uploads a custom entity type definition to the catalog.

    Args:
        type_def (EntityTypeDef): The custom entity type definition to upload.

    Returns:
        dict: The result of the upload operation.
    """
    result = client.upload_typedefs(
        entityDefs=[type_def],
        force_update=True
    )
    return result


def search_by_entity_type(client, entity_type_name):
    """
    Searches and retrieves entities of a specific type in Purview.

    Parameters:
        client (PurviewClient): The Purview client.
        entity_type_name (str): The name of the entity type to search for.

    Returns:
        dict: The search result containing information about entities of the specified type.
    """
    result = client.discovery.browse(entityType=entity_type_name)
    print(result)


def delete_by_entity_type(client, entity_type_name):
    """
    Deletes entities of a specific type in Purview.

    Parameters:
        client (PurviewClient): The Purview client.
        entity_type_name (str): The name of the entity type to delete.
    """
    entities = client.discovery.browse(entity_type_name).get("value")
    guids = []
    for e in entities:
        guid = e.get("id")
        guids.append(guid)
        delete_guid = client.delete_entity(guid)
        print(delete_guid)
        print("Above, deleted GUID: " + guid + "\n\n")


def get_guids_of_entities_with_specific_type(client, entity_type):
    """
    Retrieves GUIDs of entities with a specific type in Purview.
    Parameters:
        client (PurviewClient): The Purview client.
        entity_type (str): The name of the entity type.
    Returns:
        list: A list of GUIDs for entities with the specified type.
    """
    browse_result = client.discovery.browse(entityType=entity_type)
    # utilize offset to skip the first results, until you reach the count number
    # result of browse is a dict of @search.count and value
    
    # the "value" gives results in increments of 100
    total_search_count = browse_result.get("@search.count")
    count = 0
    list_of_guids = []
    while count < total_search_count:
        browse_result = client.discovery.browse(entityType = entity_type, offset = count)
        entities = browse_result.get("value")
        count += len(entities)
        
        for value_dict in entities:
            list_of_guids.append(value_dict.get("id"))

        #filtered_list = [e for e in entities if e.get("entityType") == entity_type]
        #list_of_guids.extend(filtered_list)
        """for value_dict in entities:
            if value_dict.get("entityType") == entity_type:
                list_of_guids.append(value_dict.get("id"))"""

    return list_of_guids

def get_subset_of_entities_with_type(client, entity_type, list_of_guids, subset_start_inclusive, subset_end_exclusive):
    """
    Retrieves a subset of entities with a specific type in Purview.
    
    Parameters:
        client (PurviewClient): The Purview client.
        entity_type (str): The name of the entity type.
        list_of_guids (list): A list of GUIDs for entities with the specified type.
        subset_start_inclusive (int): The starting index for the subset (inclusive).
        subset_end_exclusive (int): The ending index for the subset (exclusive).

    Returns:
        list: A list of dictionaries containing details of entities in the subset.
    """
    subset_list_of_guids = list_of_guids[subset_start_inclusive : subset_end_exclusive]
    entity_details = []
    count = 0
    for guid in subset_list_of_guids:
        print(count)
        pulled = client.get_entity(guid)
        entity = pulled.get("entities")[0]
        entry = {
            "guid": guid, 
            "entity": entity, # just use the first entry
            "columns": entity.get("relationshipAttributes").get("columns")
        }
        entity_details.append(entry)
        count += 1

    return entity_details


def get_columns_from_datalake(client, tabular_schema_guid):
    """
    Retrieves columns from a tabular schema in Azure Data Lake Gen2.

    Parameters:
        client (PurviewClient): The Purview client.
        tabular_schema_guid (str): The GUID of the tabular schema.

    Returns:
        list: A list of columns in the tabular schema.
    """
    tabular_schema_details = client.get_entity(tabular_schema_guid).get("entities")[0]
    return tabular_schema_details.get("relationshipAttributes").get("columns")
            

def get_all_entities_with_type(client, entity_type):
    """
    Retrieves all entities of a specific type in Purview.

    Parameters:
        client (PurviewClient): The Purview client.
        entity_type (str): The name of the entity type.

    Returns:
        dict: Information about all entities of the specified type.
    """
    list_of_guids = get_guids_of_entities_with_specific_type(client, entity_type)
    print("Pulled all guids for type: " + entity_type)
    print("Now pulling the entity details for each guid")

    all_entity_details = []
    count = 0
    for guid in list_of_guids:
        count = count + 1
        print(count)

        pulled = client.get_entity(guid)
        entity = pulled.get("entities")[0]
        entry = {
            "guid": guid, 
            "entity": entity, # just use the first entry
            "columns": entity.get("relationshipAttributes").get("columns")
        }
        if entity_type == "azure_datalake_gen2_resource_set" and "tabular_schema" in entity.get("relationshipAttributes"):
            resource_set_tabular_schema_guid = entity.get("relationshipAttributes").get("tabular_schema").get("guid")
            entry["columns"] = get_columns_from_datalake(client, resource_set_tabular_schema_guid)
            print(entry["columns"])
        all_entity_details.append(entry)

    all_entities_with_type = {
        "entity_type": entity_type,
        "info_pulled_on": datetime.now().strftime("%m/%d/%Y %H:%M"),
        "all_entity_details" : all_entity_details
    }
    return all_entities_with_type


def pull_entities_from_purview(purview_account_short_name, purview_account_full_name, client):
    """
    Pulls entities from Purview for various data sources.

    Parameters:
        purview_account_short_name (str): The short name of the Purview account.
        purview_account_full_name (str): The full name of the Purview account.
        client (PurviewClient): The Purview client.

    Returns:
        dict: Information about the pulled entities.
    """
    entity_type = "powerbi_dataset"
    powerbi_dataset_all_entities_with_type = get_all_entities_with_type(client, entity_type)
    print("Successfully pulled all: " + entity_type + " assets")
    print(str(len(powerbi_dataset_all_entities_with_type)) + " " + entity_type + " assets pulled")   
    
    entity_type = "azure_sql_dw_table"
    azure_sql_dw_table_all_entities_with_type = get_all_entities_with_type(client, entity_type) 
    print("Successfully pulled all: " + entity_type + " assets")
    print(str(len(azure_sql_dw_table_all_entities_with_type)) + " " + entity_type + " assets pulled")   
    
    entity_type = "sap_hana_view"
    sap_hana_view_all_entities_with_type = get_all_entities_with_type(client, entity_type)
    print("Successfully pulled all: " + entity_type + " assets")
    print(str(len(sap_hana_view_all_entities_with_type)) + " " + entity_type + " assets pulled")   
    
    entity_type = "sap_hana_table"
    sap_hana_table_all_entities_with_type = get_all_entities_with_type(client, entity_type)
    print("Successfully pulled all: " + entity_type + " assets")
    print(str(len(sap_hana_table_all_entities_with_type)) + " " + entity_type + " assets pulled")   
    
    entity_type = "sap_s4hana_view"
    sap_s4hana_view_all_entities_with_type = get_all_entities_with_type(client, entity_type)
    print("Successfully pulled all: " + entity_type + " assets")
    print(str(len(sap_s4hana_view_all_entities_with_type)) + " " + entity_type + " assets pulled")   

    entity_type = "sap_s4hana_table"
    sap_s4hana_table_all_entities_with_type = get_all_entities_with_type(client, entity_type)
    print("Successfully pulled all: " + entity_type + " assets")
    print(str(len(sap_s4hana_table_all_entities_with_type)) + " " + entity_type + " assets pulled") 

    entity_type = "azure_datalake_gen2_resource_set"
    azure_datalake_gen2_resource_set_all_entities_with_type = get_all_entities_with_type(client, entity_type)
    print("Successfully pulled all: " + entity_type + " assets")
    print(str(len(azure_datalake_gen2_resource_set_all_entities_with_type)) + " " + entity_type + " assets pulled") 

    pulled_entities = {
        "purview_account": purview_account_full_name,
        "data_sources": {
            "powerbi": {
                "powerbi_dataset": powerbi_dataset_all_entities_with_type
            },
            "azure_sql_dw": {
                "azure_sql_dw_table" : azure_sql_dw_table_all_entities_with_type
            },
            "sap_hana": {
                "sap_hana_view": sap_hana_view_all_entities_with_type,
                "sap_hana_table": sap_hana_table_all_entities_with_type
            },
            "sap_s4hana": {
                "sap_s4hana_view": sap_s4hana_view_all_entities_with_type,
                "sap_s4hana_table": sap_s4hana_table_all_entities_with_type,
            },
            "azure_datalake_gen2": {
                "azure_datalake_gen2_resource_set": azure_datalake_gen2_resource_set_all_entities_with_type
            }
        }
    }
    
    output_filename = purview_account_short_name + "_pulled_entities.json"
    with open(output_filename, "w", encoding="utf-8") as json_file:
        json.dump(pulled_entities, json_file, indent=3)
    print(f'Data has been written to "{output_filename}" with the desired formatting.')

    return pulled_entities


def upload_custom_type_def_with_specific_client(client, type_def: EntityTypeDef):
    """
    Uploads a custom entity type definition to Purview using the specified Purview client.

    Parameters:
    - client: Purview client for making API requests.
    - type_def (EntityTypeDef): The custom entity type definition to upload.

    Returns:
    - dict: The result of the upload operation.
    """
    result = client.upload_typedefs(
        entityDefs=[type_def],
        force_update=True
    )
    return result


def get_all_entities_nested_from_qualified_name(client, qualified_name):
    """
    Searches for entities in Purview using a qualified name and retrieves nested entities.

    Parameters:
    - client: Purview client for making API requests.
    - qualified_name (str): The qualified name to search for.

    Returns:
    - list: A list of dictionaries representing the nested entities found.
    
    Raises:
    - ValueError: If no entities are found with the specified qualified name.
    """
    entities_found = client.discovery.search_entities(query=qualified_name)

    # Extract entities from the generator
    entities = []
    for entity in entities_found:
        entities.append(entity)

    if len(entities) == 0:
        raise ValueError(f"No entities were found with this qualified name: {qualified_name}")

    return entities


def pull_lineage_connections_from_purview(purview_account_short_name, purview_account_full_name, client):
    """
    Retrieves lineage connections from Purview for various entity types.

    Parameters:
    - purview_account_short_name (str): Short name of the Purview account.
    - purview_account_full_name (str): Full name of the Purview account.
    - client: Purview client for making API requests.

    Returns:
    - dict: Dictionary containing pulled lineage connections organized by entity type.
    """
    entity_type = "dsp_connection"
    dsp_connection_all_entities_with_type = get_all_entities_with_type(client, entity_type)
    print("Successfully pulled all: " + entity_type + " assets")
    print(str(len(dsp_connection_all_entities_with_type)) + " " + entity_type + " assets pulled")   
    
    entity_type = "dw_routine"
    dw_routine_all_entities_with_type = get_all_entities_with_type(client, entity_type) 
    print("Successfully pulled all: " + entity_type + " assets")
    print(str(len(dw_routine_all_entities_with_type)) + " " + entity_type + " assets pulled")   
    
    entity_type = "dw_view_creation"
    dw_view_creation_all_entities_with_type = get_all_entities_with_type(client, entity_type)
    print("Successfully pulled all: " + entity_type + " assets")
    print(str(len(dw_view_creation_all_entities_with_type)) + " " + entity_type + " assets pulled")   
    
    entity_type = "ingestion_framework"
    ingestion_framework_all_entities_with_type = get_all_entities_with_type(client, entity_type)
    print("Successfully pulled all: " + entity_type + " assets")
    print(str(len(ingestion_framework_all_entities_with_type)) + " " + entity_type + " assets pulled")   
    
    entity_type = "sql_database_source"
    sql_database_source_all_entities_with_type = get_all_entities_with_type(client, entity_type)
    print("Successfully pulled all: " + entity_type + " assets")
    print(str(len(sql_database_source_all_entities_with_type)) + " " + entity_type + " assets pulled") 

    entity_type = "sharepoint_to_pbi"
    sharepoint_to_pbi_all_entities_with_type = get_all_entities_with_type(client, entity_type)
    print("Successfully pulled all: " + entity_type + " assets")
    print(str(len(sharepoint_to_pbi_all_entities_with_type)) + " " + entity_type + " assets pulled") 

    pulled_entities = {
        "purview_account": purview_account_full_name,
        "lineage_connections": {
            "dsp_connection": dsp_connection_all_entities_with_type,
            "dw_routine": dw_routine_all_entities_with_type,
            "dw_view_creation": dw_view_creation_all_entities_with_type,
            "ingestion_framework": ingestion_framework_all_entities_with_type,
            "sql_database_source": sql_database_source_all_entities_with_type,
            "sharepoint_to_pbi": sharepoint_to_pbi_all_entities_with_type
        }
    }
    
    output_filename = purview_account_short_name + "_pulled_lineage_connections.json"
    with open(output_filename, "w", encoding="utf-8") as json_file:
        json.dump(pulled_entities, json_file, indent=3)
    print(f'Data has been written to "{output_filename}" with the desired formatting.')

    return pulled_entities


# Main Processing
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()