##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules.entity import *
from modules.lineage.shared_lineage_functions import *


# Imports
# ---------------

from pathlib import Path
import json
import os


# Constants
# ---------------

LINEAGE_CONNECTIONS = {
    "inputs": [
        {"name": "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw/stage/Facility_SAP_HBI_DW_DLY_FACILITY_SAP",
         "type": "azure_sql_dw_table"},
        {"name": "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw/Common/FactFGInventoryAvailability",
         "type": "azure_sql_dw_table"},
        {"name": "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw/mount/Business_Seg_Hierarchy_Samba_DIV_BIPAOSQL",
         "type": "azure_sql_dw_table"},
        {"name": "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw/Common/DimWinningPortfolioSkuList",
         "type": "azure_sql_dw_table"},
    ],
    "outputs": [{
        "name": "https://app.powerbi.com/groups/87418287-152f-44c8-931d-7fd6228dda48/datasets/5bf85a38-bac9-4101-afc2-0a9ab0717a1a",
        "type": "powerbi_dataset"
    }]
}


# Functions
# ---------------

def reformat_payload_name(name: str):
    """
    Reformat the given payload name by adding a leading slash if necessary,
    replacing "/mnt" with an empty string, and replacing periods with slashes.

    Args:
        name (str): The input payload name.

    Returns:
        str: The reformatted payload name.
    """
    try:
        if name[0] != "/":
            name = "/" + name
        name = name.replace("/mnt", "")
        name = name.replace(".", "/")
        return name
    except IndexError:
        raise ValueError("Invalid input. 'name' argument must not be an empty string.")
    except AttributeError:
        raise ValueError("Invalid input. 'name' argument must be a string.")


def get_info_from_entity_dict(entity_dict: dict, qualified_name_headers: dict):
    """
    Extracts information from the given entity dictionary based on the available keys
    and returns a dictionary containing the table name and qualified name.

    Args:
        entity_dict (dict): The entity dictionary.
        qualified_name_headers (dict): A dictionary containing the qualified name headers for different types of entities.

    Returns:
        dict: A dictionary with the table name and qualified name.
    """
    try:
        name = ""
        header = ""

        if "path" in entity_dict:
            name = reformat_payload_name(entity_dict["path"])
            header = qualified_name_headers["ingestion_header"]
        elif "synapseTable" in entity_dict:
            name = reformat_payload_name(entity_dict["synapseTable"])
            header = qualified_name_headers["synapse_table_header"]

        table_info = {
            "name": name,
            "qualified_name": header + name
        }

        return table_info

    except KeyError as e:
        raise ValueError(f"Invalid entity dictionary. Missing key: {str(e)}")
    except TypeError:
        raise ValueError("Invalid entity dictionary. 'entity_dict' argument must be a dictionary.")


def upload_lineage_from_payload(client, payload: dict, qualified_name_headers: dict, entity_type_name: str) -> list:
    """
    Uploads lineage information from the given payload dictionary by extracting source and target information
    and creating lineage relationships between them.

    Args:
        payload (dict): The payload dictionary.
        qualified_name_headers (dict): A dictionary containing the qualified name headers for different types of entities.
        entity_type_name (str): The name of the entity type for lineage relationships.

    Returns:
        list: A list of results from uploading the lineage relationships.
    """
    try:
        processes = payload["process"]
        results = []

        for p in processes:
            if "sourceDataPayload" in p and "targetDataPayload" in p:
                source_info = get_info_from_entity_dict(p["sourceDataPayload"], qualified_name_headers)
                target_info = get_info_from_entity_dict(p["targetDataPayload"], qualified_name_headers)
                all_info = {
                    "source_name": source_info["name"],
                    "target_name": target_info["name"],
                    "source_qualified_name": source_info["qualified_name"],
                    "target_qualified_name": target_info["qualified_name"]
                }

                result = get_and_add_lineage_from_payload_process(client, all_info, entity_type_name)
                results.append(result)

        return results

    except KeyError as e:
        raise ValueError(f"Invalid payload dictionary. Missing key: {str(e)}")
    except TypeError:
        raise ValueError("Invalid payload dictionary. 'payload' argument must be a dictionary.")


def get_and_add_lineage_from_payload_process(client, all_info: dict, entity_type_name: str) -> dict:
    """
    Gets source and target entities from the given information, and adds a lineage relationship between them.

    Args:
        all_info (dict): A dictionary containing source and target information.
        entity_type_name (str): The name of the entity type for lineage relationships.

    Returns:
        dict: A dictionary containing the result of adding the lineage relationship.
    """
    try:
        source_entity = get_entity_from_qualified_name(client, all_info["source_qualified_name"])
        target_entity = get_entity_from_qualified_name(client, all_info["target_qualified_name"])

        result = add_manual_lineage(client, [source_entity], [target_entity], entity_type_name)
        return result

    except KeyError as e:
        raise ValueError(f"Invalid information dictionary. Missing key: {str(e)}")
    except TypeError:
        raise ValueError("Invalid information dictionary. 'all_info' argument must be a dictionary.")
    

def process_json_file(file_path):
    """
    Process the JSON file and extract the source, target, and process payloads.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing the source, target, and process payloads.
    """

    with open(file_path, 'r') as file:
        data = json.load(file)

    try:
        # Extract data payloads and process payloads
        data_payloads = data['configurationPayload']['dataPayload']
        process_payloads = data['configurationPayload']['processPayload']

        # Process and extract source and target payloads
        source_payloads = []
        target_payloads = []
        process_info_list = []

        # Process and extract process payloads
        for payload in process_payloads:
            label = payload['label']
            process_config = payload['processConfig']

            # Split label into source and target
            source, target = label.split(' -> ')

            # Add in process to ensure "Curated" matches to "Curated Ingest" in the data payloads
            if target == 'Curated':
                target = "Curated Ingest"

            if source == 'Curated':
                source = "Curated Ingest"

            process_info = {
                'processSystem': payload['processSystem'],
                'processType': payload['processType'],
                'label': payload['label'],
                'source': source,
                'target': target,
            }

            # Get the databricks specific information
            if payload['processSystem'] == 'databricks':
                process_info['notebookPath'] = process_config['notebookPath']
                process_info['jobComplexity'] = process_config['linkedService']['jobComplexity']
                process_info['jobSize'] = process_config['linkedService']['jobSize']

            process_info_list.append(process_info)

        # Iterate over the data payloads to get the proper objects out
        for payload in data_payloads:

            # Get the label from the payload and extract the true source to link it to the payload
            label = payload['label']
            payload_label = label.replace(' Source', '').replace(' Sink', '')
            dataSystem = payload['dataSystem']
            file = payload.get('config', {}).get('file', '')  # Access 'config' dictionary and use dict.get() to handle missing 'config' or 'file' keys

            info = {
                'label': label,
                'dataSystem': dataSystem,
                "file": file
            }

            # Pull out the keys
            if 'dataSource' in payload:
                info['dataSource'] = payload['dataSource']

            # Pull out the data config if it is present
            if 'dataConfig' in payload:
                data_config = payload['dataConfig']

                # Include 'path' if present in dataConfig as well as 'synapseTable' and 'mergeProcedure'
                for attr in ['path', 'synapseTable', 'mergeProcedure']:
                    if attr in data_config:
                        # Replace placeholders in the path with curly braces
                        info[attr] = data_config[attr].replace('@@Year@@', '{Year}').replace('@@Month@@', '{Month}').replace('@@Day@@', '{Day}').replace("*", info["file"])

            # If data extractor is dataFactory, compile the full path of the data
            if payload['dataSystem'] == 'dataFactory':
                if 'config' in payload and 'container' in payload['config']:
                    # Craft the path based on the file components in the label
                    path = f"/{payload['config']['container']}/{payload['config']['directory']}/{{Year}}/{{Month}}/{{Day}}/{'/'.join(info['file'])}"
                    info['path'] = path
                    ##info['path'] = path.replace('Raw Ingest', '{Raw Ingest}').replace('Curated Ingest', '{Curated Ingest}')
                else:
                    info['path'] = ""

            # Include Extract the sink
            if 'Sink' in label:
                target_payloads.append(info)

            # Add to the source payloads list if the payload is a 'Source'
            elif 'Source' in label:
                source_payloads.append(info)

            # Iterate over all processes and find where the object is a source or sink
            for proc in process_info_list:
                if payload_label == proc['source'] and dataSystem == proc['processSystem']:
                    proc['sourceDataPayload'] = info
                elif payload_label == proc['target'] and dataSystem == proc['processSystem']:
                    proc['targetDataPayload'] = info

        # Create dictionary with source, target, and process payloads
        result = {
            "source": source_payloads,
            "target": target_payloads,
            "process": process_info_list
        }

        return result

    except KeyError as e:
        raise ValueError(f"Invalid payload. Missing key: {str(e)}")
    except (TypeError, IndexError):
        raise ValueError("Invalid payload. Invalid structure or format.")


def process_payload(data: dict):
    """
    Process the JSON payload and extract the source, target, and process payloads.

    Args:
        data (dict): The JSON payload.

    Returns:
        dict: A dictionary containing the source, target, and process payloads.
    """

    try:
        # Extract data payloads and process payloads
        data_payloads = data['configurationPayload']['dataPayload']
        process_payloads = data['configurationPayload']['processPayload']

        # Process and extract source and target payloads
        source_payloads = []
        target_payloads = []
        process_info_list = []

        print("HERE")

        # Process and extract process payloads
        for payload in process_payloads:
            label = payload['label']
            process_config = payload['processConfig']

            # Split label into source and target
            source, target = label.split(' -> ')

            # Add in process to ensure "Curated" matches to "Curated Ingest" in the data payloads
            if target == 'Curated':
                target = "Curated Ingest"
            
            if source == 'Curated':
                source = "Curated Ingest"

            process_info = {
                'processSystem': payload['processSystem'],
                'processType': payload['processType'],
                'label': payload['label'],
                'source': source,
                'target': target,
            }

            # Get the databricks specific information
            if payload['processSystem'] == 'databricks':
                process_info['notebookPath'] = process_config['notebookPath']
                process_info['jobComplexity'] = process_config['linkedService']['jobComplexity']
                process_info['jobSize'] = process_config['linkedService']['jobSize']
            
            process_info_list.append(process_info)

        # Iterate over the data payloads to get the proper objects out
        for payload in data_payloads:

            # Get the label from the payload and extract the true source to link it to the payload
            label = payload['label']
            payload_label = payload['label'].replace(' Source','').replace(' Sink','')
            dataSystem = payload['dataSystem']

            info = {
                'label': label,
                'dataSystem': dataSystem
            }  

            # Pull out the keys
            if 'dataSource' in payload.keys():
                info['dataSource'] = payload['dataSource']

            # Pull out the data config if it is present
            if 'dataConfig' in payload.keys():
                data_config = payload['dataConfig']

                # Include 'path' if present in dataConfig as well as 'synapseTable' and 'mergeProcedure'
                for attr in ['path','synapseTable','mergeProcedure']:
                    if attr in data_config:
                        info[attr] = data_config[attr]

            # If data extractor is dataFactory, compile the full path of the data
            if payload['dataSystem'] == 'dataFactory':
                info['path'] = f"/{payload['config']['container']}/{payload['config']['directory']}"

            # Include Extract the sink
            if 'Sink' in label:
                target_payloads.append(info)

            # Add to the source payloads list if the payload is a 'Source'
            elif 'Source' in label:
                source_payloads.append(info)

            # Iterate over all processes and find where the object is a source or sink
            for proc in process_info_list:
                if payload_label == proc['source'] and dataSystem == proc['processSystem']:
                    proc['sourceDataPayload'] = info 
                elif payload_label == proc['target'] and dataSystem == proc['processSystem']:
                    proc['targetDataPayload'] = info
                
        # Create dictionary with source, target, and process payloads
        result = {
            "source": source_payloads,
            "target": target_payloads,
            "process": process_info_list
        }

        return result
    
    except KeyError as e:
        raise ValueError(f"Invalid payload. Missing key: {str(e)}")
    except (TypeError, IndexError):
        raise ValueError("Invalid payload. Invalid structure or format.")


def datalake_to_data_warehouse_lineage_from_payload(client, file_name):
    """
    Processes a JSON payload containing lineage information from a data lake to a data warehouse
    and uploads the lineage details to Purview.

    Parameters:
    - client: Purview client for making API requests.
    - file_name (str): The name of the JSON file containing the lineage payload.

    Returns:
    - None
    """
    # Open the JSON file using `with open`
    with open(file_name) as json_file:
        # Load the JSON data
        data = json.load(json_file)

    # Process the payload
    payload = process_payload(data = data)
    print(json.dumps(payload, indent=4))
      
    # Add in admin info
    qualified_name_headers = {
        "ingestion_header": "https://hbipd01analyticsdls.dfs.core.windows.net",
        "synapse_table_header": "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw"
    }
    entity_type_name = "ingestion_framework"

    # Upload the lineage based off of the payload
    results = upload_lineage_from_payload(client, payload, qualified_name_headers, entity_type_name)
    for result in results:
        print(json.dumps(result, indent=4))
        print()


def manually_connect_dl_to_dw_via_qualified_names(client, source_qual_name, target_qual_name):
    """
    Manually establishes a data lineage connection between a Data Lake (DL) and a Data Warehouse (DW) 
    using their qualified names.

    Parameters:
    - client: Purview client for making API requests.
    - source_qual_name (str): The qualified name of the source entity (Data Lake).
    - target_qual_name (str): The qualified name of the target entity (Data Warehouse).

    Returns:
    - dict: Result of the lineage connection operation.
    """
    source_entity = get_entity_from_qualified_name(client, source_qual_name)
    target_entity = get_entity_from_qualified_name(client, target_qual_name)
    process_type_name = "ingestion_framework"
    result = add_manual_lineage(client, [source_entity], [target_entity], process_type_name)
    print(result)

    