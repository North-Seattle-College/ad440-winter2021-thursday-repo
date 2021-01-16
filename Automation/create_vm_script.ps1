#Following code to create a VM from:
#https://docs.microsoft.com/en-us/azure/virtual-machines/windows/quick-create-powershell


param(
        [string] [Parameter(Mandatory=$true)] $ResourceGroupName,
        [string] [Parameter(Mandatory=$true)] $VirtualMachineName
      )

New-AzResourceGroup -Name $ResourceGroupName -Location WestUS2

New-AzVm `
    -ResourceGroupName $ResourceGroupName `
    -Name $VirtualMachineName `
    -Location "West US2" `
    -VirtualNetworkName "myVnet" `
    -SubnetName "mySubnet" `
    -SecurityGroupName "myNetworkSecurityGroup" `
    -PublicIpAddressName "myPublicIpAddress" `
    -OpenPorts 80,3389

