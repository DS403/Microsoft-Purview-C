##! /usr/bin/env python3


# Imports
# ---------------
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient, AtlasClient, AtlasEntity
from azure.purview.administration.account import PurviewAccountClient
from azure.purview.catalog import PurviewCatalogClient
from azure.purview.scanning import PurviewScanningClient
from azure.purview.scanning.operations import ClassificationRulesOperations
from azure.purview.catalog.aio.operations import EntityOperations
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from typing import Union
import json


# Functions
# ---------------

def get_credentials(cred_type: str, client_id: str = None, client_secret: str = None, tenant_id: str = None) -> Union[DefaultAzureCredential, ClientSecretCredential, ServicePrincipalAuthentication]:
    """
    Returns either a DefaultAzureCredential or ClientSecretCredential based on the provided arguments.

    Args:
        cred_type (str): The type of the credentials to create. Can be 'default' or 'client_secret'.
        client_id (str, optional): The client ID of the service principal. Required if cred_type is 'client_secret'.
        client_secret (str, optional): The client secret of the service principal. Required if cred_type is 'client_secret'.
        tenant_id (str, optional): The tenant ID of the service principal. Required if cred_type is 'client_secret'.

    Returns:
        Union[DefaultAzureCredential, ClientSecretCredential]: The created credentials.
    """
    if cred_type == 'default':
        return DefaultAzureCredential()
    elif cred_type == 'client_secret':
        if not all([client_id, client_secret, tenant_id]):
            raise ValueError("client_id, client_secret, and tenant_id are required when cred_type is 'client_secret'.")
        return ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    elif cred_type == 'pyapacheatlas_secret':
        if not all([client_id, client_secret, tenant_id]):
            raise ValueError("client_id, client_secret, and tenant_id are required when cred_type is 'client_secret'.")
        return ServicePrincipalAuthentication(tenant_id=tenant_id,client_id=client_id,client_secret=client_secret)
    else:
        raise ValueError(f"Invalid cred_type provided: {cred_type}")
    
    
def create_purview_client(credentials: Union[DefaultAzureCredential, ClientSecretCredential, ServicePrincipalAuthentication], purview_account: str, mod_type: str) -> PurviewClient:
    """
    Creates and returns a PurviewClient object authenticated with Azure AD Service Principal.

    Args:
        mod_type (str): The type of python module to use for the operations
        tenant_id (str): The Azure AD tenant ID.
        client_id (str): The client ID (Application ID) of the Azure AD Service Principal.
        client_secret (str): The client secret (Application Secret) of the Azure AD Service Principal.
        purview_account (str): The name of the Azure Purview account.

    Returns:
        PurviewClient: An authenticated PurviewClient object.
    """
    # Instantiate the PurviewClient
    endpoint = f"https://{purview_account}.purview.azure.net"
    if mod_type == 'pyapacheatlas':
        return PurviewClient(endpoint=endpoint, authentication=credentials)


def get_entity_properties(endpoint: str, qualified_name: str):
    """
    Retrieves entity properties from Azure Purview catalog.

    Args:
        endpoint (str): The endpoint URL of the Azure Purview account.
        qualified_name (str): The qualified name of the entity to retrieve.

    Returns:
        dict: A dictionary containing the extracted entity properties,
            or None if the entity is not found or an error occurs.
    """
    credential = DefaultAzureCredential()
    client = PurviewCatalogClient(endpoint=endpoint, credential=credential, api_version="2021-07-01-preview")
    entity = client.entity.get_entities_by_unique_attributes("resource_set", attr_n_qualified_name=qualified_name)
    try:
        json_string = json.dumps(entity)
        data = json.loads(json_string)
        pulled_qualified_name = data["entities"][0]["attributes"]["qualifiedName"]
        if qualified_name == pulled_qualified_name:
            entity_properties = {
                "name": data["entities"][0]["attributes"]["name"],
                "guid": data["entities"][0]["guid"],
                "type_name": data["entities"][0]["typeName"],
                "status": data["entities"][0]["status"],
                "last_modified_TS": data["entities"][0]["lastModifiedTS"]
            }
            return entity_properties
               
    except json.JSONDecodeError:
        print("Invalid JSON string:", entity)
        
    return None

