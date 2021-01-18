# to run this, navigate to the repo and run ./Automation/create_vnet_script.ps1 
# with the 1st 7 parameters inline -location westus2

param(
        [string] [Parameter(Mandatory=$true)] $tenantId,
        [string] [Parameter(Mandatory=$true)] $applicationId,
        [string] [Parameter(Mandatory=$true)] $secret,
        [string] [Parameter(Mandatory=$true)] $subscriptionId,
        [string] [Parameter(Mandatory=$true)] $resourceGroupName,
        [string] [Parameter(Mandatory=$true)] $location,
        [string] [Parameter(Mandatory=$true)] $vNetName,
        [string] [Parameter(Mandatory=$false)] $vNetAddressPrefix
      )

$pathToVNetTemplate = "./Automation/vnet_template.json"    
# $pathToVNetTemplate = "D:\VSCode\ad440-winter2021-thursday-repo\Automation\vnet_template.json"  

# Logs in and sets subscription      
& "$PSScriptRoot\login.ps1" $tenantId $applicationId $secret $subscriptionId

# create/update the resource group
New-AzResourceGroup -Name $resourceGroupName -Location $location -Force
Write-Output "Created Resource Group $resourceGroupName"

# create vNet with given name (can also add address prefix and location if not same as rg)
New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName -TemplateFile $pathToVNetTemplate -vNetName $vNetName
