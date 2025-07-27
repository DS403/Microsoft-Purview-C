import json
from modules.lineage.shared_lineage_functions import *
from modules.entity import *

'''
NOTE: call the function from the main.py file like this: build_lineage(qa_client, 'modules/connection/connections.json')
'''

def build_lineage(client, json_file_path):
    """
    Builds lineage connections based on the JSON configuration file.

    Args:
        client: The initialized client for interacting with the catalog.
        json_file_path (str): Path to the JSON file containing lineage connections.

    Returns:
        None
    """
    # Load the JSON file
    with open(json_file_path, "r") as f:
        lineage_data = json.load(f)

    # Iterate through connections in the JSON
    connections = lineage_data["Connections"]
    print("connections:", connections)

    for connection_name, details in connections.items():
        source = details["source"].replace('.', '/')
        source_type = details["source_type"]
        target = details["target"].replace('.', '/')
        target_type = details["target_type"]

        # Skip Analysis Services sources or targets
        if source_type == "microsoft_sql_services_analysis_services" or target_type == "microsoft_sql_services_analysis_services":
            print(f"Skipping connection {connection_name} due to Analysis Services.")
            continue

        # Fetch entities
        source_entity = get_entity_from_qualified_name(client, source)
        target_entity = get_entity_from_qualified_name(client, target)
        print("source:", source_entity, "\ntarget:", target_entity)

        # Ensure entities are found
        if not source_entity or not target_entity:
            print(f"Skipping connection {connection_name}: Unable to find source or target entity.")
            continue

        # # Define process type name
        # if source_type == "oracle" and target_type == "oracle":
        #     process_type_name = "Oracle_to_Oracle"
        # elif source_type == "oracle" and target_type == "microsoft_sql_services_analysis_services":
        #     process_type_name = "Oracle_Server_to_PBI"
        # else:
        #     process_type_name = "Default_Lineage"

        # # Add lineage
        # try:
        #     result = add_manual_lineage(client, [source_entity], [target_entity], process_type_name)
        #     print(f"Lineage successfully built for connection {connection_name}.")
        # except Exception as e:
        #     print(f"Failed to build lineage for connection {connection_name}. Error: {str(e)}")
