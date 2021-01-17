## Command to create a public ip ##

# Take a user input 
param(
        [string] [Parameter(Mandatory=$true)] $rgname, # Name of the resource group
        [string] [Parameter(Mandatory=$true)] $location, # Location of Azure resources
        [string] [Parameter(Mandatory=$true)] $publicIp, # Name of the azure public address
        [string] [Parameter(Mandatory=$true)] $sku, # Type of SKU, Standard or Basic
        [string] [Parameter(Mandatory=$true)] $allocation # AllocationMethod, Static or Dynamic
      )


New-AzPublicIpAddress -ResourceGroupName $rgname -Name $publicIp -Location $location -AllocationMethod $allocation -SKU $sku