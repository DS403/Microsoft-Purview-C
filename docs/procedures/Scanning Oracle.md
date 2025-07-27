<!-- Improved compatibility of Back to Top link -->
<a name="Oracle-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Scanning Oracle

*Azure Purview is a comprehensive data governance solution that empowers organizations to discover, understand, and manage their data assets across various sources. One crucial aspect of data governance is the ability to integrate and govern data from diverse platforms, including relational databases like Oracle. The integration of Oracle sources in Azure Purview enhances the platform's capability to deliver end-to-end data governance. By seamlessly connecting to Oracle databases, organizations can foster a culture of data collaboration, compliance, and informed decision-making within the broader context of their data ecosystem.*

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Registering Oracle in Purview](#registering-oracle-in-purview)
- [Configuring Connection Details](#configuring-connection-details)
- [Scanning Oracle Data Assets](#scanning-oracle-data-assets)
- [Verifying Registration and Scanning](#verifying-registration-and-scanning)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Introduction

The Oracle source integration in Azure Purview allows organizations to seamlessly connect, register, and scan metadata from Oracle databases. This integration facilitates a unified view of Oracle data within the Azure Purview environment, enabling users to gain insights into the structure, relationships, and characteristics of the data stored in Oracle databases.

<p align="right">(<a href="#Oracle-top">Back to Top</a>)</p>

## Prerequisites

Before proceeding, ensure the following prerequisites are met:
- **Azure Purview Account:** Have access to an Azure Purview account.
- **Oracle Database:** Access to the Oracle database instance with the necessary credentials.
- **Self-Hosted Integration Runtime:** Set up a self-hosted integration runtime in the Azure Purview Management Center.

<p align="right">(<a href="#Oracle-top">Back to Top</a>)</p>

## Registering Oracle in Purview

The registration process in Azure Purview involves initiating a new source to connect to an Oracle database. Users access the Purview Management Center, navigate to the Sources tab, and select + New Source. They specify the source type as Oracle Database and provide essential details like a descriptive name, connection string, and authentication credentials. Testing the connection ensures the accuracy of the provided information before finalizing the registration with a click on the Create button.

<p align="right">(<a href="#Oracle-top">Back to Top</a>)</p>

## Configuring Connection Details

Configuring connection details is a crucial step following the successful registration of Oracle in Purview. During the registration process, users configure critical connection details to establish a seamless link between Azure Purview and the Oracle database.

1. After registering, Users locate the registered Oracle source in the Purview portal.
2. Access the configuration settings.
3. Enter the required connection details:
   - Specifying the hostname or IP address (Host)
   - Port number (Port)
   - Service name of the Oracle database
4. Save the configuration.

These connection details ensure a secure and accurate linkage, forming the foundation for subsequent scanning processes and metadata extraction.

<p align="right">(<a href="#Oracle-top">Back to Top</a>)</p>

## Scanning Oracle Data Assets

The scanning process in Azure Purview is initiated post-registration to extract metadata from the Oracle source. Users select the registered Oracle source, click + New Scan, and provide a unique name for the scan. They choose the extraction method, such as metadata extraction from the Oracle catalog, and select the configured self-hosted integration runtime. Additional configurations involve specifying the schema and, optionally, defining particular tables or views to include in the scan. Upon completion, the scan is created, initiating the metadata extraction process.

<p align="right">(<a href="#Oracle-top">Back to Top</a>)</p>

## Verifying Registration and Scanning

Verification is a crucial step in ensuring the accuracy and success of both the registration and scanning processes. Users can verify the registration by checking the successful connection status and ensuring that the Oracle source appears in the Purview Management Center. Similarly, during the scanning process, users monitor progress within the Purview Management Center to confirm successful metadata extraction. Verification guarantees that the Oracle source is seamlessly integrated into Azure Purview, providing users with reliable and up-to-date metadata for effective data governance and management.

<p align="right">(<a href="#Oracle-top">Back to Top</a>)</p>

## Troubleshooting

If encountering issues during registration or scanning:

- Check Oracle connection details.
- Review Purview logs for error messages.
- Verify Oracle permissions for the Purview account.

Please refer to the Purview documentation or please don't hesitate to [reach out to the Data Governance Team](mailto:data_governance_team@hanes.com). We are here to assist you promptly and ensure a smooth experience with our project.

<p align="right">(<a href="#Oracle-top">Back to Top</a>)</p>

## References

- [Microsoft Purview Documentation](https://docs.microsoft.com/en-us/azure/purview/)

<p align="right">(<a href="#Oracle-top">Back to Top</a>)</p>

