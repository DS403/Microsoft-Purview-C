<!-- Improved compatibility of Back to Top link -->
<a name="Azure Datalake-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Scanning Datalake

*A data lake represents a scalable and centralized repository that allows organizations to store vast amounts of structured and unstructured data. Integrating a data lake with Microsoft Purview enhances the management, governance, and discoverability of diverse data assets. This integration is pivotal for organizations seeking to harness the full potential of their data landscape. The process involves registering the data lake within Purview and subsequently scanning its data assets to extract metadata and lineage information.Integrating a data lake with Microsoft Purview empowers organizations to effectively manage and leverage their data assets. This integration not only facilitates efficient data governance but also enhances the discoverability and understanding of data lineage, laying the groundwork for informed decision-making and analytics within the organization.*

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Registering Data Lake in Purview](#registering-data-lake-in-purview)
- [Configuring Connection Details](#configuring-connection-details)
- [Scanning Data Lake Data Assets](#scanning-data-lake-data-assets)
- [Verifying Registration and Scanning](#verifying-registration-and-scanning)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Introduction

Integrating a data lake with Microsoft Purview provides a centralized platform for managing, governing, and discovering diverse data assets. This documentation offers step-by-step instructions for registering and scanning a data lake in Purview, enabling organizations to enhance data governance, trace data lineage, and facilitate efficient data discovery.

<p align="right">(<a href="#Azure Datalake-top">Back to Top</a>)</p>

## Prerequisites

Ensure the following prerequisites are met before registering and scanning a data lake in Purview:

- Access to the data lake.
- Purview account with the necessary permissions for data lake registration.

<p align="right">(<a href="#Azure Datalake-top">Back to Top</a>)</p>

## Registering Data Lake in Purview

Registering a data lake in Microsoft Purview is a foundational step in unifying and governing diverse data assets.

1. Open the Purview portal in your web browser.
2. Navigate to the "Sources" or "Connectors" section.
3. Select "Add Source" or a similar option.
4. Choose the data lake type (e.g., Azure Data Lake Storage, Amazon S3).
5. Provide a name for the data lake source.
6. Save to initiate the registration process.

This registration establishes a secure connection, paving the way for seamless communication between Purview and the data lake.

<p align="right">(<a href="#Azure Datalake-top">Back to Top</a>)</p>

## Configuring Connection Details

Configuring connection details is a crucial step following successful registration, ensuring a secure and reliable communication link between Purview and the data lake. 

1. After registering, locate the data lake source in the Purview portal.
2. Access the configuration settings.
3. Enter the required connection details:
   - Data lake storage account information.
   - Authentication credentials or keys.
   - Endpoint details.
4. Saving these configuration settings solidifies the connection, setting the stage for successful scanning and metadata retrieval.

<p align="right">(<a href="#Azure Datalake-top">Back to Top</a>)</p>

## Scanning Data Lake Data Assets

Scanning data lake data assets is a pivotal process for extracting comprehensive metadata and lineage information. In the "Scans" section of Purview, users initiate a new scan and select the registered data lake source. Configuring scan settings, such as frequency and scope, allows organizations to tailor the scanning process to their specific needs. Executing the scan triggers the retrieval of valuable insights into data lake assets, including their characteristics, relationships, and data flow within the data lake environment. This process is essential for maintaining an up-to-date and accurate catalog of data lake data within the broader organizational landscape.

<p align="right">(<a href="#Azure Datalake-top">Back to Top</a>)</p>

## Verifying Registration and Scanning

Verifying the registration and scanning processes ensures the successful integration of the data lake into Purview's data catalog and validates the effectiveness of the scanning process. 

1. Navigate to the "Assets" or "Catalog" section in Purview.
2. Confirm the presence of data lake data assets.
3. Exploration of metadata and lineage details associated with these assets provides a deeper understanding of their structure, relationships, and data flow.
4.  Verification extends to scheduled scans, ensuring they run successfully and consistently update the catalog with the latest information from the data lake.

This verification step is crucial for maintaining data governance, accuracy, and transparency across data lake data assets within the organization.

<p align="right">(<a href="#Azure Datalake-top">Back to Top</a>)</p>

## Troubleshooting

If encountering issues during registration or scanning:

- Check data lake connection details.
- Review Purview logs for error messages.
- Verify data lake permissions for the Purview account.

Please refer to the Purview documentation or please don't hesitate to [reach out to the Data Governance Team](mailto:data_governance_team@hanes.com). We are here to assist you promptly and ensure a smooth experience with our project.

<p align="right">(<a href="#Azure Datalake-top">Back to Top</a>)</p>

## References

- [Microsoft Purview Documentation](https://docs.microsoft.com/en-us/azure/purview/)

<p align="right">(<a href="#Azure Datalake-top">Back to Top</a>)</p>

