param ($rgname, $vmname)
#Following code to create a VM from:
#https://docs.microsoft.com/en-us/azure/virtual-machines/windows/quick-create-powershell

'''
Currently, script will ask for 2 params: desired ResourceGroupName and desired VirtualMachineName.
Script will then create Resource Group with said name using the New-AzResourceGroup command.
Then, using New-AzVm command, the script will create a virtual machine with desired VirtualMachineName.
'''



#Check to see if resource group name exists. If not it will create one by that name.
Get-AzResourceGroup -Name $rgname -ErrorVariable norg -ErrorAction SilentlyContinue
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

New-AzVm `
    -ResourceGroupName $rgname `
    -Name $vmname `
    -Location "West US2" `
    -OpenPorts 80,3389

    # New-AzVm `
    # -ResourceGroupName $rgname `
    # -Name $vmname `
    # -Location "West US2" `
    # -VirtualNetworkName "myVnet" `
    # -SubnetName "mySubnet" `
    # -SecurityGroupName "myNetworkSecurityGroup" `
    # -PublicIpAddressName "myPublicIpAddress" `
    # -OpenPorts 80,3389