<!-- Improved compatibility of Back to Top link -->
<a name="SAP HANA-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Scanning SAP HANA

*Microsoft Purview's integration with SAP HANA as a source provides organizations with a unified platform for discovering, managing, and governing data assets within the SAP HANA environment. SAP HANA is a powerful in-memory database and application platform known for its speed and versatility in handling large volumes of data. By registering and scanning SAP HANA in Purview, organizations can extend their data catalog to include SAP HANA data assets, enabling comprehensive data governance and lineage tracking.Registering SAP HANA in Purview is the initial step towards integrating SAP HANA into the broader data landscape.*


## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Registering SAP HANA in Purview](#registering-sap-hana-in-purview)
- [Configuring Credentials in Purview](#configuring-credentials-in-purview)
- [Configuring Connection Details](#configuring-connection-details)
- [Required Permissions for Scan](#required-permissions-for-scan)
- [Whitelisting the VM's IP Address in Datasphere](#whitelisting-the-vm's-ip-address-in-datasphere)
- [Scanning SAP HANA Data Assets](#scanning-sap-hana-data-assets)
- [Verifying Registration and Scanning](#verifying-registration-and-scanning)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Introduction

SAP HANA scanning in Purview allows organizations to capture metadata related to tables, views, stored procedures, and other objects within SAP HANA.Integrating SAP HANA as a source in Microsoft Purview enhances data governance by providing a centralized view of SAP HANA data assets. Registering and scanning activities form a seamless process that begins with establishing a connection, configuring details, and culminates in extracting valuable insights to enrich the organization's data catalog. This integration ensures that SAP HANA data is governed, discoverable, and transparent within the overarching data management framework.

<p align="right">(<a href="#SAP HANA-top">Back to Top</a>)</p>

## Prerequisites

Ensure the following prerequisites are met before registering and scanning SAP HANA in Purview:

- Access to the SAP HANA instance.
- Make sure that VM/IR is configured and Running.
- Purview account with the necessary permissions for SAP HANA registration.

<p align="right">(<a href="#SAP HANA-top">Back to Top</a>)</p>

## Registering SAP HANA in Purview

Registering SAP HANA in Purview is a pivotal step that integrates SAP HANA as a recognized data source within the centralized catalog. This process begins by accessing the Purview portal and navigating to the "Sources" or "Connectors" section. Selecting "Add Source" and choosing "SAP HANA" initiates the registration. Users provide a distinct name for the SAP HANA source, facilitating easy identification within the Purview environment. Saving the registration details triggers the commencement of the integration process, laying the foundation for subsequent configuration and scanning.This registration process establishes a connection between Purview and SAP HANA, facilitating subsequent configuration and scanning activities. It is crucial for ensuring that SAP HANA data becomes an integral part of the centralized data catalog.

<p align="right">(<a href="#SAP HANA-top">Back to Top</a>)</p>

## Configuring Credentials in Purview

- To enhance security and manage sensitive credentials effectively, you can create a secret in Azure Key Vault.  
- Begin by navigating to the Azure Portal, accessing or creating a Key Vault, and adding a new secret with its respective details.  
- Note the Secret Identifier (URL) for future reference.  
- Subsequently, in Microsoft Purview, navigate to management center and access the credentials section, create a new credential for the desired data source (e.g., SAP HANA), and opt for an authentication method using a username and password. 
- Instead of entering the password directly, reference the secret from Azure Key Vault using the obtained Secret Identifier.  
- Ensure that the Azure AD application or identity used by Purview has appropriate permissions to access the Azure Key Vault secrets.  
- Finally, test the connection to confirm that Purview can securely retrieve the credentials from Azure Key Vault, adhering to best practices for credential management.

<p align="right">(<a href="#SAP HANA-top">Back to Top</a>)</p>

## Configuring Connection Details

1. After registration, configuring connection details is essential to enable Purview to communicate seamlessly with SAP HANA. 
2. Users locate the registered SAP HANA source and access configuration settings.
3. Enter the required connection details:
   - SAP HANA server address
   - Authentication credentials
   - Port number
   - Database details, if applicable.
4. The configuration step ensures a secure and accurate link between Purview and SAP HANA, laying the groundwork for successful scanning and metadata retrieval.

<p align="right">(<a href="#SAP HANA-top">Back to Top</a>)</p>

## Required Permissions for Scan

- To successfully scan SAP HANA in Microsoft Purview, configure a user with basic authentication (username and password).  

   CREATE USER `<user>` PASSWORD `<password>` NO FORCE_FIRST_PASSWORD_CHANGE;

- Ensure this user has the necessary permissions, such as SELECT METADATA on target schemas (e.g., `<schema1>`, `<schema2>`)  

   GRANT SELECT METADATA ON SCHEMA `<schema1>` TO `<user>`;

- SELECT on system tables like _SYS_REPO.ACTIVE_OBJECT and system schemas (_SYS_BI, _SYS_BIC).

   GRANT SELECT ON _SYS_REPO.ACTIVE_OBJECT TO `<user>`;  
   GRANT SELECT ON SCHEMA _SYS_BI TO `<user>`;  

- Utilize the provided SQL commands to create the user, grant required permissions, and facilitate seamless metadata retrieval during the scanning process. Refer to Microsoft Purview documentation for detailed instructions and updates.

<p align="right">(<a href="#SAP HANA-top">Back to Top</a>)</p>

## Whitelisting the VM's IP Address in Datasphere

- In order to connect to a Datasphere instance, the IP address of the virtual machine being used to scan DSP must be whitelisted in HANA cloud.

<p align="right">(<a href="#SAP HANA-top">Back to Top</a>)</p>

## Scanning SAP HANA Data Assets

- Scanning SAP HANA data assets is the process by which Purview retrieves comprehensive metadata and lineage information from the registered SAP HANA source. 
- In the "Scans" section of Purview, users initiate a new scan and select the previously registered SAP HANA source. 
- The scan configuration allows users to define parameters such as scan frequency and scope. Executing the scan triggers the retrieval of valuable information, including data asset characteristics and the flow of data within SAP HANA.This step is crucial for maintaining an up-to-date and accurate catalog of SAP HANA assets.

<p align="right">(<a href="#SAP HANA-top">Back to Top</a>)</p>

## Verifying Registration and Scanning

After a successful scan, navigate to the "Data Catalog" to view SAP HANA metadata. Explore tables, views, stored procedures, and other SAP HANA objects to gain insights into the structure and content of the SAP HANA environment.

1. Navigate to the "Assets" or "Catalog" section in Purview.
2. Confirm the presence of SAP HANA data assets.
3. Explore metadata and lineage details associated with SAP HANA assets.
4. Verify that scheduled scans are running successfully.

<p align="right">(<a href="#SAP HANA-top">Back to Top</a>)</p>

## Best Practices

- Regularly schedule SAP HANA scans to keep metadata up to date.
- Document configuration details for future reference.
- Collaborate with SAP HANA administrators to align scanning processes with SAP HANA best practices.

<p align="right">(<a href="#SAP HANA-top">Back to Top</a>)</p>

## Troubleshooting

If you encounter issues during the SAP HANA scanning process:

- Check the connectivity and credentials configured for SAP HANA.
- Review Purview logs and notifications for error details.
- Ensure that the SAP HANA instance is accessible from the Purview environment.

Please refer to the Purview documentation or please don't hesitate to [reach out to the Data Governance Team](mailto:data_governance_team@hanes.com). We are here to assist you promptly and ensure a smooth experience with our project.

<p align="right">(<a href="#SAP HANA-top">Back to Top</a>)</p>

## References

- [Microsoft Purview Documentation](https://docs.microsoft.com/en-us/azure/purview/)

<p align="right">(<a href="#SAP HANA-top">Back to Top</a>)</p>









