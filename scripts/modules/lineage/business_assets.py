from pyapacheatlas.core import AtlasEntity, AtlasException
import uuid

# Define variables
SERVICE_NAME = "Magento Service"
QUALIFIED_NAME = "magento://application_service"
TYPE_NAME = "Purview_ApplicationService"  # Built-in asset type for Application Service

def create_application_service(client):
    """
    Create an application service entity in Microsoft Purview.

    Args:
        client (AtlasClient): The initialized AtlasClient for Purview.

    Returns:
        dict: The response from the Purview client if successful.
    """
    try:
        # Create an AtlasEntity object for the application service
        app_service = AtlasEntity(
            qualified_name=QUALIFIED_NAME,  # Pass qualified_name as a positional argument
            name=SERVICE_NAME,
            typeName=TYPE_NAME,  # The built-in asset type for Application Service
            guid=f"-{uuid.uuid4()}"  # Optional GUID generation
        )

        # Upload the entity to Purview
        response = client.upload_entities([app_service])
        print("Application service created successfully:", response)
        return response

    except AtlasException as e:
        print("An error occurred while creating the application service:", str(e))
        return None
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        return None

from pyapacheatlas.core import AtlasClient

def list_types(client):
    """
    List all available types in the Purview account.

    Args:
        client (AtlasClient): The initialized AtlasClient for Purview.
    """
    try:
        # Retrieve all type definitions
        type_defs = client.get_all_typedefs()
        entity_defs = type_defs.get("entityDefs", [])
        
        for entity_def in entity_defs:
            print(f"Type Name: {entity_def['name']}, Category: {entity_def.get('category', 'No category')}")
    except Exception as e:
        print("An error occurred while listing all asset types:", str(e))


app_service_qualified_name = "Purview_ApplicationService://SAMBA"
dataset_qualified_name = "mssql://sqlq1bus16.res.hbi.net/Q1BUS16/AMSO_COMMON/dbo/dim_Item"

def add_dataset_relationship(client):
    """
    Add a dataset relationship to an application service in Microsoft Purview.

    Args:
        client (AtlasClient): The initialized AtlasClient for Purview.
        app_service_qualified_name (str): Qualified name of the application service.
        dataset_qualified_name (str): Qualified name of the dataset.

    Returns:
        dict: The response from the Purview client if successful.
    """
    try:
        # Fetch Application Service
        app_service_entity = client.get_entity(
            qualifiedName=app_service_qualified_name,
            typeName="Purview_ApplicationService"
        )
        app_service_guid = app_service_entity["entities"][0]["guid"]

        # Fetch Dataset
        dataset_entity = client.get_entity(
            qualifiedName=dataset_qualified_name,
            typeName="mssql_table"  # Use the correct type name from your environment
        )
        dataset_guid = dataset_entity["entities"][0]["guid"]

        # Prepare the relationship attributes
        relationship = {
            "typeName": "ApplicationService_DataSet_Application_Service_to_Dataset",
            "end1": {"guid": app_service_guid, "typeName": "Purview_ApplicationService"},
            "end2": {"guid": dataset_guid, "typeName": "mssql_table"}
        }

        # Upload the relationship
        response = client.upload_relationship(relationship)
        print("Successfully added the dataset relationship:", response)
        return response

    except AtlasException as e:
        print("An error occurred:", str(e))
        return None
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        return None