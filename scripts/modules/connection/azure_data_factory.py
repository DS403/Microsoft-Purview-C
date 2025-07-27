from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient

# Initialize ADF client using Managed Identity
def get_adf_client(subscription_id):
    credential = DefaultAzureCredential()
    client = DataFactoryManagementClient(credential, subscription_id)
    return client

from datetime import datetime, timedelta, timezone

def list_pipeline_runs(client, resource_group_name, factory_name, last_hours=24):
    """
    Fetch all datasets in the given Data Factory.

    Args:
        client: DataFactoryManagementClient object.
        resource_group_name: The name of the resource group containing the Data Factory.
        factory_name: The name of the Data Factory.

    Returns:
        A list of dictionaries representing the datasets in the Data Factory.
    """
    
    # Define the time window using timezone-aware UTC objects
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=last_hours)

    # Fetch pipeline runs
    pipeline_runs = client.pipeline_runs.query_by_factory(
        resource_group_name=resource_group_name,
        factory_name=factory_name,
        filter_parameters={
            "lastUpdatedAfter": start_time.isoformat(),
            "lastUpdatedBefore": end_time.isoformat()
        }
    )
    return pipeline_runs.value  # Returns a list of pipeline runs

def list_datasets(client, resource_group_name, factory_name):
    """
    Fetch all datasets in the given Data Factory.

    Args:
        client: DataFactoryManagementClient object.
        resource_group_name: The name of the resource group containing the Data Factory.
        factory_name: The name of the Data Factory.

    Returns:
        A list of dictionaries representing the datasets in the Data Factory.
    """
    datasets = client.datasets.list_by_factory(
        resource_group_name=resource_group_name,
        factory_name=factory_name
    )
    return [dataset.as_dict() for dataset in datasets]

def get_unique_reference_names(datasets):
    """
    Extracts all unique reference names from the list of datasets.

    Args:
        datasets: List of dictionaries representing datasets.

    Returns:
        A set of unique reference names.
    """
    reference_names = set()

    for dataset in datasets:
        properties = dataset.get("properties", {})
        linked_service = properties.get("linked_service_name", {})
        reference_name = linked_service.get("reference_name")

        if reference_name:
            reference_names.add(reference_name)

    return reference_names

def list_triggers(client, resource_group_name, factory_name):
    triggers = client.triggers.list_by_factory(
        resource_group_name=resource_group_name,
        factory_name=factory_name
    )
    return [trigger.as_dict() for trigger in triggers]

def list_operations(client):
    operations = client.operations.list()
    return [op.as_dict() for op in operations]

def list_datasets(client, resource_group_name, factory_name):
    datasets = client.datasets.list_by_factory(
        resource_group_name=resource_group_name,
        factory_name=factory_name
    )
    return [dataset.as_dict() for dataset in datasets]

def list_data_flows(client, resource_group_name, factory_name):
    data_flows = client.data_flows.list_by_factory(
        resource_group_name=resource_group_name,
        factory_name=factory_name
    )
    return [data_flow.as_dict() for data_flow in data_flows]

def extract_dataset_references_from_pipelines(client, resource_group_name, factory_name):
    """
    Extracts dataset references from pipeline activities.

    Args:
        client: Azure Data Factory Management client.
        resource_group_name: Name of the resource group.
        factory_name: Name of the data factory.

    Returns:
        A mapping of pipeline names to referenced datasets.
    """
    pipelines = client.pipelines.list_by_factory(resource_group_name, factory_name)
    dataset_references = {}

    for pipeline in pipelines:
        pipeline_name = pipeline.name
        definition = client.pipelines.get(resource_group_name, factory_name, pipeline_name)
        datasets = set()

        for activity in definition.activities:
            if hasattr(activity, "inputs"):
                datasets.update(ref.reference_name for ref in activity.inputs)
            if hasattr(activity, "outputs"):
                datasets.update(ref.reference_name for ref in activity.outputs)

        dataset_references[pipeline_name] = list(datasets)

    return dataset_references


def extract_dataflow_references_from_pipelines(client, resource_group_name, factory_name):
    """
    Extracts dataflow references from all pipelines in a specified Azure Data Factory.

    :param client: Data Factory management client.
    :param resource_group_name: Name of the resource group.
    :param factory_name: Name of the data factory.
    :return: Dictionary with pipeline names as keys and a list of referenced dataflows as values.
    """
    pipelines = client.pipelines.list_by_factory(resource_group_name, factory_name)
    dataflow_references = {}

    for pipeline in pipelines:
        pipeline_name = pipeline.name
        definition = client.pipelines.get(resource_group_name, factory_name, pipeline_name)
        dataflows = set()

        for activity in definition.activities:
            # Debugging output to track activity processing
            print(f"Processing Activity: {activity.name}, Type: {activity.type}")

            # Only process if the activity type is ExecuteDataFlow
            if activity.type == "ExecuteDataFlow":
                type_properties = getattr(activity, "type_properties", None)

                if type_properties:
                    # Safely get the dataflow reference
                    dataflow_ref = getattr(type_properties, "dataflow", None)
                    if dataflow_ref:
                        dataflows.add(dataflow_ref.reference_name)
                    else:
                        print(f"No dataflow reference found for activity: {activity.name}")
                else:
                    print(f"No type_properties found for activity: {activity.name}")

        dataflow_references[pipeline_name] = list(dataflows)

    return dataflow_references



def construct_purview_qualified_name(reference_name, schema, table):
    """
    Constructs a Purview qualified name for a given dataset.

    Args:
        reference_name: The linked service name.
        schema: The schema of the dataset.
        table: The table name.

    Returns:
        A qualified name for Purview.
    """
    return f"{reference_name}://{schema}/{table}"


if __name__ == "__main__":
    # Your Azure Data Factory details
    subscription_id = "02bd12d0-66f6-45d0-b12b-4878abfa6b07"
    resource_group_name = "AnalyticsQA-RG"
    factory_name = "hbi-qa01-analytics-df"

    # Initialize client
    adf_client = get_adf_client(subscription_id)

    # List pipeline runs
    pipeline_runs = list_pipeline_runs(adf_client, resource_group_name, factory_name)
    print("\nPipeline Runs:", pipeline_runs)

    # Fetch datasets
    datasets = list_datasets(adf_client, resource_group_name, factory_name)
    print("\nDatasets:", datasets)

    # Fetch unique reference names
    unique_reference_names = get_unique_reference_names(datasets)
    print("\nUnique Reference Names:", unique_reference_names)

    # List triggers
    triggers = list_triggers(adf_client, resource_group_name, factory_name)
    print("\nTriggers:", triggers)

    # List operations
    operations = list_operations(adf_client)
    print("\nOperations:", operations)

    # List datasets
    datasets = list_datasets(adf_client, resource_group_name, factory_name)
    print("\nDatasets:", datasets)

    # List data flows
    data_flows = list_data_flows(adf_client, resource_group_name, factory_name)
    print("\nData Flows:", data_flows)

    # Extract dataset references
    dataset_references = extract_dataset_references_from_pipelines(
        client=adf_client,
        resource_group_name=resource_group_name,
        factory_name=factory_name
    )

    # Extract data flow references
    dataflow_references = extract_dataflow_references_from_pipelines(
        client=adf_client,
        resource_group_name=resource_group_name,
        factory_name=factory_name
    )

    # Combine the results
    print("Pipeline Mapping Summary:")
    for pipeline in set(dataset_references.keys()).union(dataflow_references.keys()):
        print(f"Pipeline: {pipeline}")
        print(f" - Datasets: {dataset_references.get(pipeline, [])}")
        print(f" - Data Flows: {dataflow_references.get(pipeline, [])}")

