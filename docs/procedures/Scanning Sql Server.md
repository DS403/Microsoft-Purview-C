<!-- Improved compatibility of Back to Top link -->
<a name="Sql Server-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Scanning Sql Server

*Azure Purview serves as a robust data governance solution, providing organizations with the tools needed to discover, manage, and govern their data assets. This guide focuses on the integration of on-premises SQL Server databases into Azure Purview, offering a seamless approach to enhancing data governance capabilities. By registering and scanning on-premises SQL Server sources, organizations can centralize metadata, enabling a unified view of their data landscape for efficient management and informed decision-making.*

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Registering Sql Server in Purview](#registering-sql-server-in-purview)
- [Configuring Connection Details](#configuring-connection-details)
- [Scanning Sql Server Data Assets](#scanning-sql-server-data-assets)
- [Verifying Registration and Scanning](#verifying-registration-and-scanning)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Introduction

This guide provides step-by-step instructions on how to register and scan an on-premises SQL Server source in Azure Purview. By completing these processes, you enable Azure Purview to discover and manage metadata from SQL Server databases hosted on-premises, facilitating comprehensive data governance within your organization.

<p align="right">(<a href="#Sql Server-top">Back to Top</a>)</p>

## Prerequisites

Before you begin, ensure the following prerequisites are met:
- An active Azure Purview account.
- Access to the on-premises SQL Server database with necessary credentials.
- A configured self-hosted integration runtime in the Azure Purview Management Center.

<p align="right">(<a href="#Sql Server-top">Back to Top</a>)</p>

## Registering Sql Server in Purview

1. **Authentication for Registration:** 

   On-Premises SQL Server Authentication setup can be done in 2 ways:
   - **SQL Authentication:** Ensure the SQL Server deployment is configured to allow SQL Server and Windows Authentication. To enable:
     - Open SQL Server Management Studio (SSMS).
     - Navigate to Server Properties.
     - Change Windows Authentication Mode to SQL Server and Windows Authentication Mode.
   - **Windows Authentication:** Configure the SQL Server deployment to use Windows Authentication mode.

2. **Creating New Login and User:** To scan your SQL Server, create a new login and user.
   - Navigate to SQL Server Management Studio (SSMS), connect to the server.
   - Navigate to security, select and hold (or right-click) on login and create New login. If Windows Authentication is applied, select Windows authentication. If SQL Authentication is applied, make sure to select SQL authentication.
   - On the left navigation, select Server roles and ensure that the public role is assigned.
   - Select User mapping on the left navigation, select all the databases in the map, and select the Database role: db_datareader.
   - Select OK to save.
   - If SQL Authentication is applied, navigate again to the user you created, selecting Properties.
   - Enter a new password and confirm it. Select the 'Specify old password' and enter the old password. It is required to change your password as soon as you create a new login.

3. **Store SQL Password in a Key Vault:** 
   To integrate SQL Server credentials into Azure Purview, navigate to Key Vault settings and create a new secret with the SQL login password. If your key vault isn't connected to Purview, establish a new connection. Then, create a credential using the username and password from SQL Server, ensuring to select the appropriate authentication method: "SQL authentication" for SQL Authentication and "Windows authentication" for Windows Authentication.

4. **Register SQL Server in Purview:**
   The registration process is the initial step in integrating on-premises SQL Server with Azure Purview. Users navigate to the Azure Purview Management Center, access the Sources tab, and initiate source registration. Selecting SQL Server as the source type, users provide crucial details such as a descriptive name, connection string, and authentication method. This process establishes the necessary link between Azure Purview and the on-premises SQL Server, laying the foundation for subsequent metadata extraction.

<p align="right">(<a href="#Sql Server-top">Back to Top</a>)</p>

## Configuring Connection Details

Configuring connection details is a pivotal step in the registration process. Users input vital information, including the server name or IP address, port number, and authentication details. This configuration ensures a secure and functional connection between Azure Purview and the on-premises SQL Server database. Verifying these details during the registration process is essential for the successful extraction of metadata and insights from the SQL Server source.These connection details ensure a secure and accurate linkage, forming the foundation for subsequent scanning processes and metadata extraction.

<p align="right">(<a href="#Sql Server-top">Back to Top</a>)</p>

## Scanning Sql Server Data Assets

The scanning process, initiated after successful registration, involves creating a new scan for the on-premises SQL Server source. Users provide a unique scan name, choose the extraction method (e.g., metadata extraction from SQL Server catalog), and select the self-hosted integration runtime for connection. Additional parameters, such as specifying the database and tables/views for scanning, allow users to tailor the scan to their specific requirements, ensuring a comprehensive view of the SQL Server metadata within Azure Purview.

<p align="right">(<a href="#Sql Server-top">Back to Top</a>)</p>

## Verifying Registration and Scanning

Verification is a critical step to ensure the success of both registration and scanning processes. During registration, users should verify the successful establishment of connections by testing connectivity. Subsequently, during scanning, monitoring the progress in the Purview Management Center ensures that metadata is being retrieved without errors. This verification step guarantees the accurate integration of on-premises SQL Server sources into Azure Purview, providing a unified data catalog.

<p align="right">(<a href="#Sql Server-top">Back to Top</a>)</p>

## Troubleshooting

If encountering issues during registration or scanning:

- Check Sql Server connection details.
- Review Purview logs for error messages.
- Verify Sql Server permissions for the Purview account.

Please refer to the Purview documentation or please don't hesitate to [reach out to the Data Governance Team](mailto:data_governance_team@hanes.com). We are here to assist you promptly and ensure a smooth experience with our project.

<p align="right">(<a href="#Sql Server-top">Back to Top</a>)</p>

## References

- [Microsoft Purview Documentation](https://docs.microsoft.com/en-us/azure/purview/)

<p align="right">(<a href="#Sql Server-top">Back to Top</a>)</p>

