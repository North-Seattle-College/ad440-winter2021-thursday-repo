# to run this, navigate to the repo and run ./Automation/create_vnet_script.ps1 
# with the 1st 7 parameters inline -location westus2

param(
        [string] [Parameter(Mandatory=$true)] $tenantId,          
        [string] [Parameter(Mandatory=$true)] $applicationId,     #username for SP
        [string] [Parameter(Mandatory=$true)] $secret,            #password for SP
        [string] [Parameter(Mandatory=$true)] $subscriptionId,
        [string] [Parameter(Mandatory=$true)] $resourceGroupName,
        [string] [Parameter(Mandatory=$true)] $location,
        [string] [Parameter(Mandatory=$true)] $vNetName,
        [string] [Parameter(Mandatory=$false)] $vNetAddressPrefix
      )

$pathToVNetTemplate = "./vnet_template.json"   

# Logs in and sets subscription      
& "../login.ps1" $tenantId $applicationId $secret $subscriptionId

# Creates/Updates resource group
New-AzResourceGroup -Name $resourceGroupName -Location $location -Force

# Creates VNet if one of the same name does not already exist in the Resource Group
$vNetExists = (Get-AzVirtualNetwork -Name $vNetName -ResourceGroupName $resourceGroupName -ErrorAction SilentlyContinue).Name -eq $vNetName
if (!$vNetExists) { 
    Write-Host "Virtual Network did not exist. Creating now."
    # create vNet with given name (can also add address prefix and location if not same as rg)
    New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName -TemplateFile $pathToVNetTemplate -vNetName $vNetName
} else {
    Write-Host "Virtual Network already exists."
}
