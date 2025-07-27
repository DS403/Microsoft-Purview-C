<!-- Improved compatibility of Back to Top link -->
<a name="Azure Datawarehouse-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Scanning Databricks

*A data warehouse serves as a central repository for structured and often large volumes of data, facilitating business intelligence and analytics. Integrating a data warehouse with Microsoft Purview enhances data governance, promotes discoverability, and establishes a unified catalog for comprehensive data management. The process involves registering the data warehouse within Purview and subsequently scanning its data assets to extract crucial metadata and lineage information.Integrating a data warehouse with Microsoft Purview empowers organizations to harness the full potential of their data assets. This integration not only facilitates efficient data governance but also enhances the discoverability and understanding of data lineage, laying the groundwork for informed decision-making and analytics within the organization.*

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Registering Data Warehouse in Purview](#registering-data-warehouse-in-purview)
- [Configuring Connection Details](#configuring-connection-details)
- [Scanning Data Warehouse Data Assets](#scanning-data-warehouse-data-assets)
- [Verifying Registration and Scanning](#verifying-registration-and-scanning)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Introduction

Integrating a data warehouse with Microsoft Purview allows organizations to centralize data assets, enhance data governance,empowering organizations to harness the full potential of their data assets while maintaining governance and transparency and facilitate efficient data discovery. This documentation provides step-by-step instructions for registering and scanning a data warehouse in Purview.

<p align="right">(<a href="#Azure Datawarehouse-top">Back to Top</a>)</p>

## Prerequisites

Ensure the following prerequisites are met before registering and scanning a data warehouse in Purview:

- Access to the data warehouse.
- Purview account with the necessary permissions for data warehouse registration.

<p align="right">(<a href="#Azure Datawarehouse-top">Back to Top</a>)</p>

## Registering Data Warehouse in Purview

Registering a data warehouse in Microsoft Purview is a foundational step in unifying and governing data assets. 

1. Open the Purview portal in your web browser.
2. Navigate to the "Sources" or "Connectors" section.
3. Select "Add Source" or a similar option.
4. Choose the appropriate data warehouse type (e.g., SQL Server, Snowflake).
5. Provide a name for the data warehouse source.
6. Save to initiate the registration process.

This registration process forms the basis for subsequent configuration and scanning, enabling efficient data cataloging and governance.

<p align="right">(<a href="#Azure Datawarehouse-top">Back to Top</a>)</p>

## Configuring Connection Details
Configuring connection details is a pivotal step following successful registration, ensuring a secure and reliable communication link between Purview and the data warehouse. 

1. After registering, locate the data warehouse source in the Purview portal.
2. Access the configuration settings.
3. Enter the required connection details:
   - Data warehouse server address
   - Authentication credentials
   - Database name
   - Port number, if applicable.
4. Saving these configuration settings solidifies the connection, setting the stage for successful scanning and metadata retrieval.

<p align="right">(<a href="#Azure Datawarehouse-top">Back to Top</a>)</p>

## Scanning Data Warehouse Data Assets

Scanning data warehouse data assets is a crucial process for extracting comprehensive metadata and lineage information. In the "Scans" section of Purview, users initiate a new scan and select the registered data warehouse source. The configuration of scan settings, including frequency and scope, allows organizations to tailor the scanning process to their specific needs. Executing the scan triggers the retrieval of valuable insights into data warehouse data assets, including their characteristics, relationships, and data flow within the data warehouse environment. This process is essential for maintaining an up-to-date and accurate catalog of data warehouse data within the broader organizational landscape.

<p align="right">(<a href="#Azure Datawarehouse-top">Back to Top</a>)</p>

## Verifying Registration and Scanning

Verifying the registration and scanning processes ensures the successful integration of the data warehouse into Purview's data catalog and validates the effectiveness of the scanning process. In the "Assets" or "Catalog" section of Purview, users confirm the presence of data warehouse data assets. Exploration of metadata and lineage details associated with these assets provides a deeper understanding of their structure, relationships, and data flow. Verification extends to scheduled scans, ensuring they run successfully and consistently update the catalog with the latest information from the data warehouse. This verification step is crucial for maintaining data governance, accuracy, and transparency across data warehouse data assets within the organization.

<p align="right">(<a href="#Azure Datawarehouse-top">Back to Top</a>)</p>

## Troubleshooting

If encountering issues during registration or scanning:

- Check data warehouse connection details.
- Review Purview logs for error messages.
- Verify data warehouse permissions for the Purview account.

Please refer to the Purview documentation or please don't hesitate to [reach out to the Data Governance Team](mailto:data_governance_team@hanes.com). We are here to assist you promptly and ensure a smooth experience with our project.

<p align="right">(<a href="#Azure Datawarehouse-top">Back to Top</a>)</p>

## References

- [Microsoft Purview Documentation](https://docs.microsoft.com/en-us/azure/purview/)

<p align="right">(<a href="#Azure Datawarehouse-top">Back to Top</a>)</p>

