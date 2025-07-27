<!-- Improved compatibility of Back to Top link -->
<a name="VM & IR Setup-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Setting up Virtual Machine and Self-hosted Integration Runtime

*Setting up a Virtual Machine and a Self-hosted Integration Runtime in Azure Purview facilitates a comprehensive and flexible data governance strategy, accommodating the diverse needs of modern data environments.A Virtual Machine is a software emulation of a physical computer that runs an operating system and applications. In the context of Azure Purview, setting up a VM provides a dedicated environment for running tasks related to data integration and processing.Integration Runtimes in Azure Purview facilitate data movement and processing. The self-hosted integration runtime allows organizations to extend Purview's capabilities to on-premises environments by deploying an agent on a Virtual Machine. This agent acts as a bridge between Purview services in the cloud and data sources on-premises.Many organizations operate in hybrid environments with a mix of cloud and on-premises resources. Setting up a VM and self-hosted integration runtime enables seamless data governance across both environments.*

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Provisioning a Virtual Machine](#provisioning-a-virtual-machine)
- [Configuring the Virtual Machine](#configuring-the-virtual-machine)
- [Setting Up Self-hosted Integration Runtime](#setting-up-self-hosted-integration-runtime)
- [Testing the Integration Runtimes](#testing-the-integration-runtimes)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Introduction

Azure Purview is a data governance service that helps organizations discover and manage their data assets. To leverage Purview's capabilities effectively, it's crucial to set up a Virtual Machine (VM) and Self-hosted Integration Runtime. This documentation provides a step-by-step guide to achieve this setup.

<p align="right">(<a href="#VM & IR Setup-top">Back to Top</a>)</p>

## Prerequisites

1. **Azure Subscription**: Ensure you have an active Azure subscription.

2. **Purview Account**: You must have an Azure Purview account.

3. **Virtual Machine**: Provision a Virtual Machine in Azure.

<p align="right">(<a href="#VM & IR Setup-top">Back to Top</a>)</p>

## Provisioning a Virtual Machine

1. Log in to the Azure portal (https://portal.azure.com/).
2. Click on "Create a resource."
3. Search for "Virtual Machine" in the Azure Marketplace and select the desired VM offering.
4. Follow the wizard to configure the VM. Key settings include:
   - **Basic settings**: Provide a name, region, and resource group.
   - **Authentication**: Choose authentication type (e.g., SSH key or password).
   - **Networking**: Configure networking settings, such as virtual network and subnet.
5. Review and create the VM.

<p align="right">(<a href="#VM & IR Setup-top">Back to Top</a>)</p>

## Configuring the Virtual Machine

1. Once the VM is created, connect to it using SSH or Remote Desktop, depending on the chosen authentication method.

2. Install any required software or dependencies needed for your specific integration runtime tasks.

<p align="right">(<a href="#VM & IR Setup-top">Back to Top</a>)</p>

## Setting Up Self-hosted Integration Runtime

1. In the Azure portal, navigate to your Purview account.

2. In the Purview account, go to the "Data Map" section.

3. Click on "Integration Runtimes."

4. Select "New Integration Runtime."

5. Choose "Self-hosted" as the integration runtime type.

6. Provide a name for the integration runtime and any required configuration settings.

7. Download and install the integration runtime agent on the previously configured VM.

8. Follow the agent installation wizard, providing necessary information such as Purview account details.

9. Once installed, go back to the Azure portal and refresh the Integration Runtimes page. Your new self-hosted integration runtime should be listed and connected.

<p align="right">(<a href="#VM & IR Setup-top">Back to Top</a>)</p>

## Testing the Integration Runtime

1. Create a new data asset or use an existing one in Purview.

2. Configure the data asset to use the self-hosted integration runtime for scanning or extraction.

3. Run a test scan or extraction job to validate the setup.

<p align="right">(<a href="#VM & IR Setup-top">Back to Top</a>)</p>


## Best Practices

- **Optimize VM Resources**: Ensure the Virtual Machine for the self-hosted integration runtime is provisioned with adequate resources based on data processing requirements, optimizing performance and scalability.

- **Regularly Update Integration Runtime**: Stay current with updates for the self-hosted integration runtime to benefit from the latest features, security patches, and improvements in Azure Purview.

- **Implement Monitoring and Logging**: Establish robust monitoring and logging practices for the self-hosted integration runtime to quickly identify and address any issues, ensuring the reliability of data integration processes.

<p align="right">(<a href="#VM & IR Setup-top">Back to Top</a>)</p>

## Troubleshooting

Please refer to the Purview documentation or please don't hesitate to [reach out to the Data Governance Team](mailto:data_governance_team@hanes.com). We are here to assist you promptly and ensure a smooth experience with our project.

<p align="right">(<a href="#VM & IR Setup-top">Back to Top</a>)</p>

## References

- [Microsoft Purview Documentation](https://docs.microsoft.com/en-us/azure/purview/)

<p align="right">(<a href="#VM & IR Setup-top">Back to Top</a>)</p>








