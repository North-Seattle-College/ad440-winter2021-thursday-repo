#Script to create a Virtual Machine on Azure.
#https://docs.microsoft.com/en-us/azure/virtual-machines/windows/quick-create-powershell

#Create a VM on Azure.
param (
    [string] [Parameter(Mandatory=$true)] $tenantId, #Tenant ID used to login to Azure with Service Provider
    [string] [Parameter(Mandatory=$true)] $applicationId, #App ID used to login to Azure with Service Provider
    [string] [Parameter(Mandatory=$true)] $secret, #Azure Secret used to login to Azure with Service Provider
    [string] [Parameter(Mandatory=$true)] $subscriptionId, #Subscr. ID used to login to Azure with Service Provider
    [string] [Parameter(Mandatory)] $rgname, #Resource Group Name required.
    [string] [Parameter(Mandatory)] $vmname, #VM Name required
    [string] $location='West US2', #Default value for RG/VM Location
    [string] $vnetname='myVnet',  #Default value
    [string] $subnetname='mySubnet', #Default value
    [string] $nsgname='myNetworkSecurityGroup', #Default value
    [string] $publicipname='myPublicIpAddress', #Default value
    [string] $dnsLabelPrefix=$rgname #Default value
    )

$templatefile = "$PSScriptRoot\vm_parameters.json" #template file for Virtual Machine Resource
$adminUsername = Read-Host -Prompt "Enter the admin username for new VM"
$adminPassword = Read-Host -Prompt "Enter the admin password for new VM" -AsSecureString
    
# Logs in and sets subscription      
& "$PSScriptRoot\login.ps1" $tenantId $applicationId $secret $subscriptionId


#Check to see if resource group name exists. If not it will create one by that name.
#If Resource Group already exists, the script this step and proceed to the VM.
#This should probably be broken down in to a reuseable funtion.

Write-Output "Checking to see if Azure Resource Group exists."
Get-AzResourceGroup -Name $rgname -ErrorVariable norg -ErrorAction SilentlyContinue
if ($norg)
{ 
    Write-Output "Resource group did not exist. Creating now."
    New-AzResourceGroup -Name $rgname -Location $location
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

    #Create VM using provided template file
    New-AzResourceGroupDeployment `
    -ResourceGroupName $rgname `
    -TemplateFile $templatefile `
    -vmName $vmname `
    -adminUsername $adminUsername `
    -adminPassword $adminPassword `
    -dnsLabelPrefix $dnsLabelPrefix
}
else {
    Write-Output "Error: A Virtual Machine by this name already exists in Resource Group $rgname."  
}


