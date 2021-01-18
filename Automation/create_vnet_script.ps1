# https://github.com/Azure-Samples/resource-manager-python-template-deployment
# https://docs.microsoft.com/en-us/azure/templates/microsoft.resources/deploymentscripts
# example: https://raw.githubusercontent.com/Azure/azure-docs-json-samples/master/deployment-script/deploymentscript-helloworld.ps1
# https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/deployment-script-template
# https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-tutorial-deployment-script
# https://docs.microsoft.com/en-us/learn/modules/extend-resource-manager-template-deployment-scripts/
# https://dev.to/omiossec/an-introduction-to-deployment-scripts-resource-in-azure-resource-manager-m8g
# also go to Azure to see if you can get the script from there

param(
        [string] [Parameter(Mandatory=$true)] $tenantId,
        [string] [Parameter(Mandatory=$true)] $applicationId,
        [SecureString] [Parameter(Mandatory=$true)] $secret,
        [string] [Parameter(Mandatory=$true)] $subscriptionId,
        [string] [Parameter(Mandatory=$true)] $resourceGroupName,
        [string] [Parameter(Mandatory=$true)] $location,
        [string] [Parameter(Mandatory=$true)] $vNetName,
        [string] [Parameter(Mandatory=$false)] $vNetAddressPrefix
      )

$pathToVNetTemplate = "./vnet_template.json"    
# $pathToVNetTemplate = "D:\VSCode\ad440-winter2021-thursday-repo\Automation\vnet_template.json"  

# Logs in and sets subscription      
& "$PSScriptRoot\login.ps1" $tenantId $applicationId $secret $subscriptionId

# create/update the resource group
New-AzResourceGroup -Name $resourceGroupName -Location $location
Write-Output "Created Resource Group $resourceGroupName"


New-AzResourceGroupDeployment -Name $vNetName -ResourceGroupName $resourceGroupName -TemplateFile $pathToVNetTemplate -vNetName $vNetName

New-AzResourceGroupDeployment -Name $vNetName -ResourceGroupName $resourceGroupName -TemplateFile $pathToVNetTemplate

# $output = 'Hello {0}. The username is {1}, the password is {2}.' -f $name,${Env:UserName},${Env:Password}
# Write-Output $output
# $DeploymentScriptOutputs = @{}
# $DeploymentScriptOutputs['text'] = $output