import requests
import json
from datetime import datetime
from azure.identity import DefaultAzureCredential

# Constants
REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
API_VERSION = "2023-09-01"


# Initialize authentication and session
credentials = DefaultAzureCredential()
purview_scan_endpoint = f"https://{REFERENCE_NAME_PURVIEW}.scan.purview.azure.com/"

# Fetch the token and set the headers
def get_headers():
    """Returns the authentication headers."""
    token = credentials.get_token("https://purview.azure.net/.default").token
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

# Fetch data sources
def fetch_data_sources(session):
    """Fetches all data sources from Purview."""
    url = f"{purview_scan_endpoint}datasources?api-version={API_VERSION}"
    response = session.get(url)
    response.raise_for_status()
    return response.json().get("value", [])

# Fetch scans for a given data source
def fetch_scans(session, data_source_name):
    """Fetches scans for a given data source."""
    url = f"{purview_scan_endpoint}datasources/{data_source_name}/scans?api-version={API_VERSION}"
    response = session.get(url)
    response.raise_for_status()
    return response.json().get("value", [])

# Fetch failed scans for a given scan
def fetch_failed_scans(session, data_source_name, scan_name):
    """Fetches failed scan runs for a given scan."""
    url = f"{purview_scan_endpoint}datasources/{data_source_name}/scans/{scan_name}/runs?api-version={API_VERSION}"
    response = session.get(url)
    response.raise_for_status()
    scan_runs = response.json().get("value", [])
    return [run for run in scan_runs if run.get("status") == "Failed"]

# Main function to fetch and display Purview scan details
def main():
    """Main execution function to fetch and display Purview scan details."""
    with requests.Session() as session:
        session.headers.update(get_headers())

        try:
            # Fetch data sources
            data_sources = fetch_data_sources(session)

            # Initialize JSON file for failed scan data with current date in the format YYYY_MM_DD
            current_date = datetime.now().strftime("%Y_%m_%d")  # Format: YYYY_MM_DD
            output_file = f"{current_date}_scan_errors.json"  # Example: 2024_11_28_scan_QA_errors.json

            # Initialize list to store failed scan data
            failed_scan_data = []
            
            # Iterate over data sources
            for ds in data_sources:
                data_source_name = ds["name"]

                # Fetch scans
                scans = fetch_scans(session, data_source_name)

                if not scans:
                    print("No scans found for this data source.")
                    continue

                for scan in scans:
                    scan_name = scan["name"]
                    print(f"Scan Name: {scan_name}")

                    # Fetch failed scans
                    failed_scans = fetch_failed_scans(session, data_source_name, scan_name)

                    # Append failed scan data to list
                    if failed_scans:
                        for failed_scan in failed_scans:

                            # Prepare failed scan info
                            failed_scan_info = {
                                "Data Source Name":data_source_name,
                                "Scan Name": scan_name,
                                "Failed Scan ID": failed_scan["id"],
                                "Status": failed_scan["status"],
                                "Error Message": failed_scan["errorMessage"]
                            }
                            failed_scan_data.append(failed_scan_info)

                    # Print message if no failed scans found        
                    else:
                        print("No failed scans for this scan.")
                
                # Write to JSON file
                with open(output_file, "w") as json_file:
                    json.dump({"failed_scans": failed_scan_data}, json_file, indent=4)

                # Print success message
                print(f"JSON file '{output_file}' generated successfully!")

        # Handle exceptions
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")

# Execute the script
if __name__ == "__main__":
    main()
