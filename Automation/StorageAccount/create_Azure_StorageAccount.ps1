Start-Transcript -Path "$PSScriptRoot\create_Azure_StorageAccountlog.log"
Write-Host "Logging to $PSScriptRoot\create_Azure_StorageAccountlog.log"
Write-Host "Create Azure Storage Account"

param(
    [string] [Parameter(Mandatory=$true)] $resourceGroup, # Name of resource group to put storage account in
    [string] [Parameter(Mandatory=$true)] $location, # Regional location EG "westus2" or "japaneast"
    [string] [Parameter(Mandatory=$true)] $storageAccountName # Name to give storage account
)