<!-- Improved compatibility of Back to Top link -->
<a name="SAP S/4 HANA-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Scanning SAP S/4 HANA

*Microsoft Purview's integrating SAP S/4 HANA as a source in Microsoft Purview is instrumental for organizations seeking a unified approach to manage, govern, and discover data assets within their SAP S/4 HANA environment. SAP S/4 HANA stands out as an advanced enterprise resource planning (ERP) system, and Purview's integration allows for the seamless inclusion of SAP S/4 HANA data into the centralized data catalog.Integrating SAP S/4 HANA into Microsoft Purview empowers organizations to centralize their SAP S/4 HANA data assets, providing a unified platform for data management, governance, and discovery. The registration and scanning processes form a seamless workflow, establishing a robust connection and retrieving valuable insights to enhance the organization's data catalog.*

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Registering SAP S/4 HANA in Purview](#registering-sap-s4-hana-in-purview)
- [Configuring Credentials in Purview](#configuring-credentials-in-purview)
- [Configuring Connection Details](#configuring-connection-details)
- [Required Permissions for Scan](#required-permissions-for-scan)
- [Scanning SAP S/4 HANA Data Assets](#scanning-sap-s4-hana-data-assets)
- [Verifying Registration and Scanning](#verifying-registration-and-scanning)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Introduction

Integrating SAP S/4 HANA with Microsoft Purview extends the data catalog to include SAP S/4 HANA data assets, promoting comprehensive data governance, lineage tracking, and discoverability. This documentation provides step-by-step instructions for registering and scanning SAP S/4 HANA in Purview.

<p align="right">(<a href="#SAP S/4 HANA-top">Back to Top</a>)</p>

## Prerequisites

Ensure the following prerequisites are met before registering and scanning SAP S/4 HANA in Purview:

- Access to the SAP S/4 HANA instance.
- Make sure that VM/IR is configured and Running.
- Purview account with the necessary permissions for SAP S/4 HANA registration.

<p align="right">(<a href="#SAP S/4 HANA-top">Back to Top</a>)</p>

## Registering SAP S/4 HANA in Purview

Registering SAP S/4 HANA in Purview is a foundational step in integrating this powerful ERP system into the broader data landscape. Within the Purview portal, users navigate to the "Sources" or "Connectors" section, initiating the process of adding a new source. By selecting "SAP S/4 HANA" as the source type, users establish a connection between Purview and the SAP S/4 HANA instance. Providing a descriptive name for the source enhances identification within the Purview environment. The registration process lays the groundwork for subsequent configuration and scanning activities, enabling comprehensive data governance and cataloging.

<p align="right">(<a href="#SAP S/4 HANA-top">Back to Top</a>)</p>

## Configuring Credentials in Purview

- To enhance security and manage sensitive credentials effectively, you can create a secret in Azure Key Vault.  
- Begin by navigating to the Azure Portal, accessing or creating a Key Vault, and adding a new secret with its respective details.  
- Note the Secret Identifier (URL) for future reference.  
- Subsequently, in Microsoft Purview, navigate to management center and access the credentials section, create a new credential for the desired data source (e.g., SAP HANA), and opt for an authentication method using a username and password. 
- Instead of entering the password directly, reference the secret from Azure Key Vault using the obtained Secret Identifier.  
- Ensure that the Azure AD application or identity used by Purview has appropriate permissions to access the Azure Key Vault secrets.  
- Finally, test the connection to confirm that Purview can securely retrieve the credentials from Azure Key Vault, adhering to best practices for credential management.

<p align="right">(<a href="#SAP S/4 HANA-top">Back to Top</a>)</p>

## Configuring Connection Details

1. Configuring connection details is a critical step that follows the successful registration of SAP S/4 HANA in Purview.  Users locate the registered SAP S/4 HANA source in the Purview portal.
2. Access the configuration settings.
3. Enter the required connection details:
   - SAP S/4 HANA server address
   - Authentication credentials
   - Port number
   - Client ID and Secret, if applicable.
4. The accuracy of these details ensures a secure and reliable communication link between Purview and SAP S/4 HANA. Saving the configuration settings solidifies the connection, setting the stage for successful scanning and metadata retrieval.

<p align="right">(<a href="#SAP S/4 HANA-top">Back to Top</a>)</p>

## Required Permissions for Scan

For successful scan execution in Azure Purview, the user account utilized for the scan process must have sufficient permissions to connect to the SAP server and execute specific RFC (Remote Function Call) function modules. The following key RFC function modules are crucial for different aspects of the scan process:

1. **STFC_CONNECTION (Check Connectivity):**
   - Purpose: Verifies the connectivity to the SAP server.
   - Permissions: Ensure the user has the necessary permissions to execute this function module.

2. **RFC_SYSTEM_INFO (Check System Information):**
   - Purpose: Retrieves system information from the SAP server.
   - Permissions: Grant the user the required permissions to execute RFC_SYSTEM_INFO.

3. **OCS_GET_INSTALLED_COMPS (Check Software Versions):**
   - Purpose: Checks installed software versions on the SAP server.
   - Permissions: Authorize the user to execute OCS_GET_INSTALLED_COMPS.

4. **Z_MITI_DOWNLOAD (Main Metadata Import):**
   - Purpose: Main function module for metadata import, typically created following the Purview guide.
   - Permissions: The user must have sufficient permissions to execute Z_MITI_DOWNLOAD.

Additionally, it's important to note that the SAP Java Connector (JCo) libraries may invoke additional RFC function modules such as RFC_PING, RFC_METADATA_GET, etc., during the scan process.

<p align="right">(<a href="#SAP S/4 HANA-top">Back to Top</a>)</p>

## Scanning SAP S/4 HANA Data Assets

Scanning SAP S/4 HANA data assets is a pivotal step for extracting comprehensive metadata and lineage information from the registered source. In the "Scans" section of Purview, users initiate a new scan and select the SAP S/4 HANA source. The scan configuration allows users to define parameters such as scan frequency and scope, tailoring the scanning process to organizational needs. Executing the scan triggers the retrieval of valuable insights into SAP S/4 HANA data assets, including their characteristics, relationships, and data flow within the SAP S/4 HANA environment. This process is essential for maintaining an up-to-date and accurate catalog of SAP S/4 HANA data.

<p align="right">(<a href="#SAP S/4 HANA-top">Back to Top</a>)</p>

## Verifying Registration and Scanning

After a successful scan, navigate to the "Data Catalog" to view SAP S/4 HANA metadata. Explore tables, views, stored procedures, and other SAP HANA objects to gain insights into the structure and content of the SAP HANA environment.

1. Navigate to the "Assets" or "Catalog" section in Purview.
2. Confirm the presence of SAP S/4 HANA data assets.
3. Explore metadata and lineage details associated with SAP S/4 HANA assets.
4. Verify that scheduled scans are running successfully.

<p align="right">(<a href="#SAP S/4 HANA-top">Back to Top</a>)</p>

## Best Practices

- Regularly schedule SAP S/4 HANA scans to keep metadata up to date.
- Document configuration details for future reference.
- Collaborate with SAP S/4 HANA administrators to align scanning processes with SAP HANA best practices.

<p align="right">(<a href="#SAP S/4 HANA-top">Back to Top</a>)</p>

## Troubleshooting

If encountering issues during registration or scanning:

- Check SAP S/4 HANA connection details.
- Review Purview logs for error messages.
- Verify SAP S/4 HANA permissions for the Purview account.

Please refer to the Purview documentation or please don't hesitate to [reach out to the Data Governance Team](mailto:data_governance_team@hanes.com). We are here to assist you promptly and ensure a smooth experience with our project.

<p align="right">(<a href="#SAP S/4 HANA-top">Back to Top</a>)</p>

## References

- [Microsoft Purview Documentation](https://docs.microsoft.com/en-us/azure/purview/)

<p align="right">(<a href="#SAP S/4 HANA-top">Back to Top</a>)</p>








