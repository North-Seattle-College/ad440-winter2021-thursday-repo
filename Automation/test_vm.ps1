#Script to create a Virtual Machine on Azure.
#https://docs.microsoft.com/en-us/azure/virtual-machines/windows/quick-create-powershell

#Note: This creates a Windows VM, but the end goal is a Linux VM. This will be the next sprint.
#Note: There are extra parameters that are not being used yet. These will be used when creating Linux machine.
param (
    [string] [Parameter(Mandatory)] $rgname, #Resource Group Name required.
    [string] [Parameter(Mandatory)] $vmname #VM Name required
    )

$templatefile = "$PSScriptRoot\ubuntu_vm_parameters.json" #template file for Virtual Machine Resource

Write-Output "Checking to see if Azure Resource Group exists."
Get-AzResourceGroup -Name $rgname -ErrorVariable norg -ErrorAction SilentlyContinue
if ($norg)
{ 
    Write-Output "Resource group did not exist. Creating now."
    New-AzResourceGroup -Name $rgname -Location "West US 2"
}
else
{

    Write-Output "Resource group already exists, proceeding to create VM."
}

#Check to see if VM exists
Write-Output "Checking to see if Virtual Machine by this name exists in resource group $rgname."
Get-AzVM -Name "$vmname" -ResourceGroupName $rgname -ErrorVariable notPresent -ErrorAction SilentlyContinue

if ($notPresent) {
    Write-Output "Virtual Machine did not exist in resource group $rgname. Creating Now."  
    New-AzResourceGroupDeployment `
    -ResourceGroupName "$rgname" `
    -TemplateFile $templatefile
}
else {
    Write-Output "Error: A Virtual Machine by this name already exists in Resource Group $rgname."  
}


