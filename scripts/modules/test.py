##! /usr/bin/env python3

# Function Imports
# ---------------

from pyapacheatlas.core import AtlasEntity ,AtlasClassification
from pyapacheatlas.core.entity import AtlasEntity, AtlasProcess
from pyapacheatlas.core.typedef import EntityTypeDef, AtlasAttributeDef
from pyapacheatlas.readers import ExcelConfiguration,ExcelReader
from utils import get_credentials,create_purview_client


# Imports
# ---------------

import pandas as pd
import json
from pathlib import Path
import random
import string

# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
qa_client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)

REFERENCE_NAME_PURVIEW = "hbi-pd01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
prod_client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)



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
'''
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
'''

#search_by_entity_type(qa_client, 'entity_type_name')

def get_entity_typename_from_qualified_name(client, qualified_name):
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
    print(entity_typename)

#get_entity_typename_from_qualified_name(qa_client, "sap_s4hana://vhhbrmd1ci_MD1_00_220/$/1BEA/BBEA")    
    
#result = qa_client.get_entity(typeName='sap_s4hana_package_packages')
#with open(r"C:\Users\Sravanthi.Dasam\Desktop\SAP_S4_Hana.txt",'w') as file:
#    file.write(str(result))    
    
# result = qa_client.get_entity(qualifiedName='sap_s4hana://vhhbrmd1ci_MD1_00_220/$/1BEA/BBEA')
# with open(r"C:\Users\Sravanthi.Dasam\Desktop\SAP.txt",'w') as file:
#     file.write(str(result))


# browse_result = qa_client.discovery.browse(entityType='sap_s4hana_application_component')  
# filtered_data = [
#     item for item in browse_result["value"]
#     if item["qualifiedName"].startswith("sap_s4hana://vhhbrmd1ci_MD1_00_220")
# ]
# with open(r"C:\Users\Sravanthi.Dasam\Desktop\SAP_package.txt",'w') as file:
#       file.write(str(filtered_data))


'''
guid=[item["id"] for item in filtered_data]
qa_client.delete_entity(guid=guid)

result=qa_client.get_entity(guid='ca8e2d15-2b24-4880-9b51-8b52644844b6')
print(result)
''' 

# page_token = None

# while True:
#     browse_result = qa_client.discovery.browse(
#         entityType='sap_s4hana_application_component',
#         pageToken=page_token  # Pass the page token to fetch the next set of results
#     )

#     filtered_data = [
#     item for item in browse_result["value"]
#     if item["qualifiedName"].startswith("sap_s4hana://vhhbrmd1ci_MD1_00_220")
#     ]
#     with open(r"C:\Users\Sravanthi.Dasam\Desktop\SAP_package.txt",'w') as file:
#       file.write(str(filtered_data))

#     # Check if there is a next page token
#     page_token = browse_result.get('nextPageToken')
#     if not page_token:
#         break


# browse_result = qa_client.discovery.query(keywords='sap_s4hana_package')
# with open(r"C:\Users\Sravanthi.Dasam\Desktop\SAP_application_component.txt",'w') as file:
#     file.write(str(browse_result))

result_generator = qa_client.discovery.search_entities(query='sap_s4hana_package')
result = list(result_generator)
with open(r"C:\Users\Sravanthi.Dasam\Desktop\SAP_application_component.txt",'w') as file:
     file.write(str(result))

# def get_all_entities_nested_from_qualified_name(client, qualified_name):
#     entities_found = client.discovery.search_entities(query=qualified_name)
#     '''
#     # Extract entities from the generator
#     entities = []
#     for entity in entities_found:
#         entities.append(entity)
#     if len(entities) == 0:
#         raise ValueError(f"No entities were found with this qualified name: {qualified_name}")

#     return entities
  
#get_all_entities_nested_from_qualified_name(qa_client, "sap_s4hana://vhhbrmd1ci_MD1_00_220/")
    

# result = qa_client.get_entity(guid='3f646751-25de-40c2-a724-ff2280fffe89')
# with open(r"C:\Users\Sravanthi.Dasam\Desktop\SAP_S4_Hana.txt",'w') as file:
#     file.write(str(result))


# result_generator = qa_client.discovery.search_entities(query='sap_s4hana://vhhbrmd1ci_MD1_00_220/')
# result = list(result_generator)
# with open(r"C:\Users\Sravanthi.Dasam\Desktop\SAP_S4_Hana.txt",'w') as file:
#      file.write(str(result))


# result_generator = qa_client.discovery.search_entities(query='sap_s4hana://vhhbrmd1ci_MD1_00_220//MSG/4_STR_PM_CONNECTION')
# result = list(result_generator)
# with open(r"C:\Users\Sravanthi.Dasam\Desktop\SAP_S4_Hana.txt",'w') as file:
#      file.write(str(result))
