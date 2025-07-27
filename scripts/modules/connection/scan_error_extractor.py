import uuid
from azure.purview.scanning import PurviewScanningClient
from azure.purview.administration.account import PurviewAccountClient
from azure.identity import DefaultAzureCredential 
from azure.core.exceptions import HttpResponseError

def get_failed_scans(client, ds_name, scan_names):
    """
    Retrieves all failed scans for a specific data source.

    Args:
        client (PurviewScanningClient): The Purview Scanning Client.
        ds_name (str): The name of the data source.
        scan_names (list): List of scan names associated with the data source.

    Returns:
        list: A list of failed scans with their details.
    """
    failed_scans = []
    try:
        for scan_name in scan_names:
            # Retrieve the scan history for each scan
            scan_history = client.scan_result.list_scan_history(data_source_name=ds_name, scan_name=scan_name)
            for history in scan_history:
                if history["status"] == "Failed":
                    failed_scans.append({"scanName": scan_name, "details": history})
        
        print(f"Found {len(failed_scans)} failed scans for data source '{ds_name}'.")
    except HttpResponseError as e:
        print(f"Error retrieving scan results for data source '{ds_name}': {e}")
    
    return failed_scans

# Replace with your actual values
ds_name = "SAPHana-DSP-DV"  # Name of your registered data source
scan_names = ["Scan-Fin-Rep", "Scan-Md-Stg"]  # List of known scan names
reference_name_purview = "hbi-qa01-datamgmt-pview"  # Your Purview account name

# Use DefaultAzureCredential for authentication
credentials = DefaultAzureCredential()

# Initialize the Purview clients
purview_scan_endpoint = f"https://{reference_name_purview}.scan.purview.azure.com/"
client = PurviewScanningClient(endpoint=purview_scan_endpoint, credential=credentials, logging_enable=True)

# Retrieve failed scans
failed_scans = get_failed_scans(client, ds_name, scan_names)
for failed_scan in failed_scans:
    print(f"Failed Scan: {failed_scan}")
