## Command to create a public ip ##

# Name of the resource group
$rg = 'nsc-ad440-winter2021-Th-StorageRG'

# Location of Azure resources
$loc = 'westus2'

# Name of the azure public address
$pubIP = 'public-ip-standard-nsc-ad440'

# Make the public IP a standard zonal public IP address in Zone 2
$sku = 'Standard'
$alloc = 'Static'
$zone = 2

New-AzPublicIpAddress -ResourceGroupName $rg -Name $pubIP -Location $loc -AllocationMethod $alloc -SKU $sku -zone $zone