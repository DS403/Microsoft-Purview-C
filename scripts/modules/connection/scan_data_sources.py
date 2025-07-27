import uuid
from azure.purview.scanning import PurviewScanningClient
from azure.purview.administration.account import PurviewAccountClient
from azure.identity import DefaultAzureCredential 
from azure.core.exceptions import HttpResponseError

# Replace with your actual values
ds_name = "HBIAnalyticsADLS"  # Name of your registered data source
scan_name = "Scan-DimWinningPortfolioSkuList"  # Name of the scan you want to run
reference_name_purview = "hbi-qa01-datamgmt-pview"  # Your Purview account name

# Use DefaultAzureCredential for authentication
credentials = DefaultAzureCredential()

# Initialize the Purview clients
purview_scan_endpoint = f"https://{reference_name_purview}.scan.purview.azure.com/"
client = PurviewScanningClient(endpoint=purview_scan_endpoint, credential=credentials, logging_enable=True)

# Check if the scan exists
try:
    scan_details = client.scans.get(data_source_name=ds_name, scan_name=scan_name)
    print(f"Scan '{scan_name}' exists: {scan_details}")
except HttpResponseError as e:
    print(f"Error retrieving scan '{scan_name}': {e}")
    print("Ensure the scan is already defined for this data source.")
    exit(1)  # Exit the script if the scan does not exist

# Generate a unique ID for the scan run
run_id = str(uuid.uuid4())

# Start the existing scan
try:
    response = client.scan_result.run_scan(data_source_name=ds_name, scan_name=scan_name, run_id=run_id)
    print(response)
    print(f"Scan '{scan_name}' successfully started with Run ID: {run_id}")
except HttpResponseError as e:
    print(f"Error starting scan '{scan_name}': {e}")
