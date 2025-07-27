<!-- Improved compatibility of Back to Top link -->
<a name="Lineage-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Lineage

*Lineage is a critical feature of the Microsoft Purview Data Catalog to support quality, trust, and audit scenarios. The goal of a data catalog is to build a robust framework where all the data systems within your environment can naturally connect and report lineage. Once the metadata is available, the data catalog can bring together the metadata provided by data systems to power data governance use cases. Data lineage is broadly understood as the lifecycle that spans the data’s origin, and where it moves over time across the data estate. It's used for different kinds of backwards-looking scenarios such as troubleshooting, tracing root cause in data pipelines and debugging. Lineage is also used for data quality analysis, compliance and “what if” scenarios often referred to as impact analysis. Lineage is represented visually to show data moving from source to destination including how the data was transformed.*


## Table of Contents

- [Introduction](#introduction)
- [Key Concepts](#key-concepts)
- [Viewing Lineage](#viewing-lineage)
- [Understanding Lineage Diagrams](#understanding-lineage-diagrams)
- [Navigating Lineage Details](#navigating-lineage-details)
- [Different Types of Lineage](#different-types-of-lineage)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Introduction

Lineage functionality in Purview enables users to visualize and comprehend the journey of data from its source to destination. It enhances data transparency, governance, and supports informed decision-making.

Microsoft Purview can capture lineage for data in different parts of your organization's data estate, and at different levels of preparation including:

- Raw data staged from various platforms
- Transformed and prepared data
- Data used by visualization platforms

<p align="right">(<a href="#Lineage-top">Back to Top</a>)</p>

## Key Concepts

- **Lineage Diagram:** A graphical representation of data flow.
- **Source and Destination:** Identifies the origin and endpoint of data.
- **Transformation Nodes:** Represents processes or transformations applied to the data.

<p align="right">(<a href="#Lineage-top">Back to Top</a>)</p>

## Viewing Lineage

To view lineage in Microsoft Purview:

1. Navigate to the Purview portal.
2. Select a data asset to view its lineage.
3. After accessing asset click on "Lineage" section.

Upon accessing the "Lineage" section of the portal, a rich interface unfolds, revealing a dynamic visual representation of how data traverses through the organization. Users can seamlessly explore and analyze the intricate connections, sources, transformations, and endpoints of their data assets. This intuitive process enhances data transparency and empowers users to make informed decisions by comprehending the complex interplay of data within the organization.

<p align="right">(<a href="#Lineage-top">Back to Top</a>)</p>

## Understanding Lineage Diagrams

Lineage diagrams within Purview serve as dynamic, graphical narratives of data flow. These diagrams intricately showcase the origin of data, the transformations it undergoes, and its final destinations. Key symbols and connections in the diagrams provide valuable context, allowing users to grasp the chronological sequence of data movement. This understanding is pivotal for stakeholders to gain insights into dependencies, identify potential bottlenecks, and ensure the accuracy and integrity of the data as it evolves throughout its lifecycle.

<p align="right">(<a href="#Lineage-top">Back to Top</a>)</p>

## Navigating Lineage Details

When exploring lineage details in Purview:

- Click on nodes to view metadata.
- Use zoom and pan features for a comprehensive view.
- Follow connections to trace data flow.

In the "Navigating Lineage Details" phase, users are equipped with interactive tools to delve deeper into the intricacies of data lineage. By clicking on specific nodes within the lineage diagram, users can access detailed metadata associated with each data asset. The platform's user-friendly zoom and pan features facilitate a comprehensive exploration, enabling users to traverse through the lineage graph effortlessly. Following connections between nodes provides a guided journey, revealing the relationships between different data elements and shedding light on the entire data flow landscape.

<p align="right">(<a href="#Lineage-top">Back to Top</a>)</p>

## Different Types of Lineage

There are different types of lineage.Few of them are:
1. **Internal Data Warehouse Lineage:**
   - This lineage type focuses on the data flow within an internal data warehouse. It reveals how data moves and transforms within the organization's data warehousing infrastructure, providing insights into the end-to-end journey of data assets.

2. **External Table Lineage:**
   - External table lineage tracks the flow of data associated with external tables. It illustrates how data is sourced from external tables, transformed, and utilized within the organization's data ecosystem, enhancing visibility into the integration of external data sources.

3. **JSON Payload Lineage:**
   - JSON payload lineage explores the lineage of data represented in JSON format. It showcases how JSON data is ingested, transformed, and utilized across various processes within the organization, offering clarity on the handling of JSON data payloads.

4. **PKMS Lineage:**
   - PKMS lineage centers around the flow of data within a PKMS (Public Key Management Service) environment. It outlines the journey of data assets as they traverse through PKMS processes, providing an understanding of data security and encryption practices.

5. **PowerBI SQL Query Lineage:**
   - PowerBI SQL query lineage reveals the lineage of data manipulated through SQL queries within PowerBI. It illustrates how SQL queries are applied to shape and analyze data within PowerBI, contributing to a comprehensive view of data transformations.

6. **PowerBI Tabular Model Lineage:**
   - PowerBI Tabular Model lineage focuses on the relationships and dependencies within PowerBI's tabular data model. It showcases how data entities are structured and interconnected within PowerBI, aiding in understanding the composition of analytical models.

7. **SAP HANA Internal Lineage:**
   - SAP HANA Internal Lineage traces the movement and transformations of data within the SAP HANA environment. It provides insights into how data is processed and utilized within SAP HANA, supporting transparency and governance of SAP HANA data assets.

8. **Stored Procedure Lineage:**
   - Stored Procedure lineage elucidates the path of data through stored procedures. It showcases how data is manipulated and processed within stored procedures, offering visibility into the execution and impact of stored procedures on data assets.

<p align="right">(<a href="#Lineage-top">Back to Top</a>)</p>

## Best Practices

- **Consistent Naming:** Maintain consistent naming conventions for assets.
- **Regular Lineage Reviews:** Periodically review and update lineage information.
- **Collaboration:** Encourage collaboration between data stakeholders for accurate lineage representation.

<p align="right">(<a href="#Lineage-top">Back to Top</a>)</p>

## Troubleshooting

If you encounter issues with lineage visualization:

- Check data source connections.
- Review and update metadata for accurate lineage representation.

Please refer to the Purview documentation or please don't hesitate to [reach out to the Data Governance Team](mailto:data_governance_team@hanes.com). We are here to assist you promptly and ensure a smooth experience with our project.

<p align="right">(<a href="#Lineage-top">Back to Top</a>)</p>

## References

- [Microsoft Purview Documentation](https://docs.microsoft.com/en-us/azure/purview/)

<p align="right">(<a href="#Lineage-top">Back to Top</a>)</p>