<#
 .SYNOPSIS
    Deploys a template to Azure
 .DESCRIPTION
    Deploys an Azure Resource Manager template
 .PARAMETER subscriptionId
    The subscription id where the template will be deployed.
 .PARAMETER resourceGroupName
    The resource group where the template will be deployed. Can be the name of an existing or a new resource group.
 .PARAMETER templateFilePath
    Optional, path to the template file. Defaults to template.json.
 .PARAMETER parametersFilePath
    Optional, path to the parameters file. Defaults to parameters.json. If file is not found, will prompt for parameter values based on template.
#>

param(
   [Parameter(Mandatory = $True)]
   [string]
   $subscriptionId,

   [Parameter(Mandatory = $True)]
   [string]
   $resourceGroupName,

   [string]
   $deploymentName = "AzureKeyVaultDeploymentThursday",

   [string]
   $templateFilePath = "./template.json",

   [string]
   $parametersFilePath = "./template.parameters.json"
)

#******************************************************************************
# Script body
# Execution begins here
#******************************************************************************

$ErrorActionPreference = "Stop"

# sign in
Write-Host "Logging in...";
Connect-AzAccount;

# Select subscription
Write-Host "Selecting subscription '$subscriptionId'";
Get-AzSubscription -SubscriptionID $subscriptionId;

#Check for existing resource group
$resourceGroup = Get-AzResourceGroup -Name $resourceGroupName -ErrorAction SilentlyContinue
if (!$resourceGroup) {
   Write-Host "Resource group '$resourceGroupName' does not exist.";
   exit
}
else {
   Write-Host "Using existing resource group '$resourceGroupName'";
        
   # Start the deployment
   Write-Host "Starting deployment...";
   New-AzResourceGroupDeployment `
      -DeploymentName $deploymentName `
      -ResourceGroupName $resourceGroupName `
      -TemplateFile $templateFilePath `
      -TemplateParameterFile $parametersFilePath 
}

