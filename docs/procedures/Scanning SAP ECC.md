<!-- Improved compatibility of Back to Top link -->
<a name="SAP ECC-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Scanning SAP ECC

*Microsoft Purview's integration with SAP ECC (Enterprise Central Component) enables organizations to manage, govern, and discover data assets within their SAP ECC environment seamlessly. SAP ECC is a critical component in many enterprises, and integrating it with Purview ensures that the data from this robust ERP system is centralized within the organization's data catalog. This integration facilitates better data management, governance, and discovery, thereby enhancing overall data-driven decision-making.*

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Registering SAP ECC in Purview](#registering-sap-ecc-in-purview)
- [Configuring Credentials in Purview](#configuring-credentials-in-purview)
- [Configuring Connection Details](#configuring-connection-details)
- [Required Permissions for Scan](#required-permissions-for-scan)
- [Scanning SAP ECC Data Assets](#scanning-sap-ecc-data-assets)
- [Verifying Registration and Scanning](#verifying-registration-and-scanning)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Introduction

Integrating SAP ECC with Microsoft Purview extends the data catalog to include SAP ECC data assets, promoting comprehensive data governance, lineage tracking, and discoverability. This documentation provides step-by-step instructions for registering and scanning SAP ECC in Purview.

<p align="right">(<a href="#SAP ECC-top">Back to Top</a>)</p>

## Prerequisites

Ensure the following prerequisites are met before registering and scanning SAP ECC in Purview:

- Access to the SAP ECC instance.
- Ensure that VM/IR (Virtual Machine/Integration Runtime) is configured and running.
- A Purview account with the necessary permissions for SAP ECC registration.

<p align="right">(<a href="#SAP ECC-top">Back to Top</a>)</p>

## Registering SAP ECC in Purview

Registering SAP ECC in Purview is the first step in integrating this enterprise system into the broader data governance framework. Within the Purview portal, users can navigate to the "Sources" or "Connectors" section to initiate the process of adding a new source. By selecting "SAP ECC" as the source type, a connection between Purview and the SAP ECC instance is established. Providing a descriptive name for the source will aid in easy identification within the Purview environment. This registration is essential for subsequent configuration and scanning processes.

<p align="right">(<a href="#SAP ECC-top">Back to Top</a>)</p>

## Configuring Credentials in Purview

- Enhance security by storing sensitive credentials in Azure Key Vault.  
- Navigate to the Azure Portal, create or access an existing Key Vault, and add a new secret with the necessary details.  
- Note the Secret Identifier (URL) for later use.  
- In Microsoft Purview, go to the management center, access the credentials section, and create a new credential for the SAP ECC data source.
- For authentication, choose a username and password method, but instead of entering the password directly, reference the secret from Azure Key Vault using the previously noted Secret Identifier.
- Ensure the Azure AD application or identity used by Purview has the appropriate permissions to access the secrets stored in Azure Key Vault.
- Test the connection to verify that Purview can securely retrieve the credentials, ensuring secure and effective credential management.

<p align="right">(<a href="#SAP ECC-top">Back to Top</a>)</p>

## Configuring Connection Details

1. After successfully registering SAP ECC in Purview, proceed to configure the connection details.
2. Locate the registered SAP ECC source in the Purview portal and access the configuration settings.
3. Enter the required connection details:
   - SAP ECC server address
   - Authentication credentials
   - Port number
   - Client ID and Secret, if applicable.
4. Ensure the accuracy of these details to establish a secure and reliable communication link between Purview and SAP ECC.
5. Save the configuration settings to finalize the connection setup, preparing for successful scanning and metadata retrieval.

<p align="right">(<a href="#SAP ECC-top">Back to Top</a>)</p>

## Required Permissions for Scan

For a successful scan in Azure Purview, ensure the user account used for scanning has sufficient permissions to connect to the SAP ECC server and execute necessary RFC (Remote Function Call) function modules. The following key RFC function modules are essential for different aspects of the scan process:

1. **STFC_CONNECTION (Check Connectivity):**
   - Purpose: Verifies connectivity to the SAP ECC server.
   - Permissions: The user must have permission to execute this function module.

2. **RFC_SYSTEM_INFO (Check System Information):**
   - Purpose: Retrieves system information from the SAP ECC server.
   - Permissions: The user should be authorized to execute RFC_SYSTEM_INFO.

3. **OCS_GET_INSTALLED_COMPS (Check Software Versions):**
   - Purpose: Checks the installed software versions on the SAP ECC server.
   - Permissions: Ensure the user can execute OCS_GET_INSTALLED_COMPS.

4. **Z_MITI_DOWNLOAD (Main Metadata Import):**
   - Purpose: Primary function module for metadata import, typically created following Purview's guidance.
   - Permissions: The user must have sufficient permissions to execute Z_MITI_DOWNLOAD.

Additional RFC function modules may be invoked by the SAP Java Connector (JCo) libraries during the scan process, such as RFC_PING and RFC_METADATA_GET.

<p align="right">(<a href="#SAP ECC-top">Back to Top</a>)</p>

## Scanning SAP ECC Data Assets

Scanning SAP ECC data assets is a critical process for extracting comprehensive metadata and lineage information from the registered source. Users can initiate a new scan by navigating to the "Scans" section of Purview and selecting the SAP ECC source. The scan configuration allows users to set parameters like scan frequency and scope, tailoring the scanning process to meet specific organizational needs. Running the scan retrieves valuable insights into SAP ECC data assets, including their characteristics, relationships, and data flows within the SAP ECC environment. This is vital for maintaining an accurate and up-to-date catalog of SAP ECC data.

<p align="right">(<a href="#SAP ECC-top">Back to Top</a>)</p>

## Verifying Registration and Scanning

After a successful scan, it is important to verify that the SAP ECC data has been correctly cataloged in Purview. Follow these steps:

1. Navigate to the "Data Catalog" within Purview.
2. Confirm the presence of SAP ECC data assets.
3. Explore metadata and lineage details associated with SAP ECC assets.
4. Ensure scheduled scans are functioning correctly and producing accurate results.

<p align="right">(<a href="#SAP ECC-top">Back to Top</a>)</p>

## Best Practices

- Schedule regular scans of SAP ECC to ensure that metadata is current and accurate.
- Document all configuration settings for future reference and troubleshooting.
- Work closely with SAP ECC administrators to align scanning processes with SAP ECC best practices.

<p align="right">(<a href="#SAP ECC-top">Back to Top</a>)</p>

## Troubleshooting

If you encounter issues during the registration or scanning process:

- Double-check the SAP ECC connection details.
- Review Purview logs for any error messages or alerts.
- Ensure that the Purview account has the necessary permissions to access and scan the SAP ECC data.

For further assistance, refer to the official Purview documentation or contact your organization's Data Governance Team.

<p align="right">(<a href="#SAP ECC-top">Back to Top</a>)</p>

## References

- [Microsoft Purview Documentation](https://docs.microsoft.com/en-us/azure/purview/)

<p align="right">(<a href="#SAP ECC-top">Back to Top</a>)</p>