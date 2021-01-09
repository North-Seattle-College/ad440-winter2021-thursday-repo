Write-Host "Create Azure Storage Account"

# Name of resource group
$resourceGroup = "nsc-ad440-winter2021-Th-StorageRG"
# Location for Azure resources
$location = "westus2"
#Name of storage account
$storageAccountName = "nscad440thsa"

#Check if the resource group exists
Get-AzResourceGroup -Name $resourceGroup -ErrorVariable noRG -ErrorAction SilentlyContinue
if($noRG){
    #Resource group does not exist
    Write-Host "Creating Resource Group $resourceGroup"
    New-AzResourceGroup -Name $resourceGroup -Location $location
}

#Check if storage account exists
#Returns a CheckNameAvailabilityResult object, use property NameAvailable to get boolean value of if the name is available
$doesntExist = Get-AzStorageAccountNameAvailability -Name $storageAccountName

if($doesntExist.NameAvailable){
    #If the storage account does not exist
    Write-Host "Creating Storage Account $storageAccountName"
    New-AzStorageAccount -ResourceGroupName $resourceGroup `
        -Name $storageAccountName `
        -Location $location `
        -SkuName Standard_RAGRS `
        -Kind StorageV2
    
    if(Get-AzStorageAccount -ResourceGroupName $resourceGroup -Name $storageAccountName){
        Write-Host "Successfully created storage account $storageAccountName"
    } else {
        #Exists for testing purposes, replace with error logging instead for actual deployment
        throw "Failed to create storage account. Failure in create_Azure_StorageAccount.ps1"
    }
} else {
    #If the storage account already exists
    #Code below exists for testing purposes, replace with error logging instead for actual deployment
    Write-Host "Storage Account $storageAccountName already exists"
    $prompt = Read-Host -Prompt "Would you like to delete for script testing? y/n"
    if($prompt = "y"){
        Write-Host "Deleting Storage Account $storageAccountName"
        Remove-AzStorageAccount -Name $storageAccountName -ResourceGroupName $resourceGroup
    }
}

Read-Host -Prompt "Press enter to continue"