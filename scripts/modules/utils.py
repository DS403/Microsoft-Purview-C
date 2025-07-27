##! /usr/bin/env python3


# Imports
# ---------------

from pyapacheatlas.core import PurviewClient
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
import json
from pathlib import Path
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from typing import Union


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

    Raises:
        ValueError: If the provided cred_type is not supported or if cred_type is 'client_secret' but client_id, client_secret, or tenant_id are not provided.
    """
    if cred_type == 'default':
        return DefaultAzureCredential(exclude_shared_token_cache_credential=True)
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
        credentials (Union[DefaultAzureCredential, ClientSecretCredential, ServicePrincipalAuthentication]): The credentials for authentication.
        purview_account (str): The name of the Azure Purview account.
        mod_type (str): The type of python module to use for the operations.

    Returns:
        PurviewClient: An authenticated PurviewClient object.

    Raises:
        ValueError: If an unsupported module type is specified.
        Exception: If an error occurs during the PurviewClient instantiation.
    """
    try:
        # Instantiate the PurviewClient
        if mod_type == 'pyapacheatlas':
            return PurviewClient(account_name=purview_account, authentication=credentials)
        else:
            raise ValueError("Unsupported module type: " + mod_type)
    except Exception as e:
        raise Exception("Error occurred during PurviewClient instantiation.") from e


def save_dict_to_json(data: dict, path: Path, filename: str):
    """
    Save a dictionary to a JSON file nested within the specified directory.

    Args:
        data (dict): The dictionary to be saved.
        path (Path): The directory path where the JSON file will be saved.
        filename (str): The name of the JSON file.
    """
    try:
        # Convert the dictionary to JSON format
        json_data = json.dumps(data, indent=2)

        # Create a Path object for the output file
        file_path = path.joinpath(filename)

        # Write the JSON data to the file
        with file_path.open(mode='w') as file:
            file.write(json_data)
    except IOError as e:
        raise IOError("Error occurred while writing the JSON file.") from e
