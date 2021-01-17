#Script to create a Virtual Machine on Azure.
#https://docs.microsoft.com/en-us/azure/virtual-machines/windows/quick-create-powershell

#Create a VM on Azure.
param (
    [Parameter(Mandatory)] $rgname, #Resource Group Name required.
    [Parameter(Mandatory)] $vmname, #VM Name required
    $location='West US2', #Default value
    $vnetname='myVnet',  #Default value
    $subnetname='mySubnet', #Default value
    $nsgname='myNetworkSecurityGroup', #Default value
    $publicipname='myPublicIpAddress' #Default value
    )

#Check to see if resource group name exists. If not it will create one by that name.
Get-AzResourceGroup -Name $rgname -ErrorVariable norg -ErrorAction SilentlyContinue
Write-Output $test
if ($norg)
{
    # ResourceGroup doesn't exist
    Write-Output "Resource group did not exist. Creating now."
    New-AzResourceGroup -Name $rgname -Location WestUS2
}
else
{
    # ResourceGroup exist
    Write-Output "Resource group already exists, proceeding to create VM."
}

#Create VM. Will add the same error handling as resource groups in next push.
New-AzVm `
    -ResourceGroupName $rgname `
    -Name $vmname `
    -Location $location `
    -VirtualNetworkName $vnetname `
    -SubnetName $subnetname `
    -SecurityGroupName $nsgname `
    -PublicIpAddressName $publicipname `
    -OpenPorts 80,3389



