# Creates resource group and Azure SQL logical server

param(
<<<<<<< HEAD
        # Login parameters
        [string] [Parameter(Mandatory=$true)] $tenantId,          
        [string] [Parameter(Mandatory=$true)] $applicationId,
        [string] [Parameter(Mandatory=$true)] $secret,
        [string] [Parameter(Mandatory=$true)] $subscriptionId,
        # Azure SQL server parameters
        [string] [Parameter(Mandatory=$true)] $location,
        [string] [Parameter(Mandatory=$true)] $resourceGroupName,
        [string] [Parameter(Mandatory=$true)] $serverName,
        [string] [Parameter(Mandatory=$true)] $administratorLogin,
        [string] [Parameter(Mandatory=$true)] $administratorLoginPassword
)

=======
    # Login parameters
    [string] [Parameter(Mandatory=$true)] $tenantId,          
    [string] [Parameter(Mandatory=$true)] $applicationId,
    [string] [Parameter(Mandatory=$true)] $secret,
    [string] [Parameter(Mandatory=$true)] $subscriptionId,
    # Azure SQL server parameters
    [string] [Parameter(Mandatory=$true)] $location,
    [string] [Parameter(Mandatory=$true)] $resourceGroupName,
    [string] [Parameter(Mandatory=$true)] $serverName,
    [string] [Parameter(Mandatory=$true)] $administratorLogin,
    [string] [Parameter(Mandatory=$true)] $administratorLoginPassword,
    # Azure SQL db parameters
    
    # Tag paramenters
    [string] [Parameter(Mandatory=$true)] $createdBy,
    [string] [Parameter(Mandatory=$true)] $creatorsEmail              
)
>>>>>>> d82162f... added interactive tags
[securestring] $administratorLoginPassword = ConvertTo-SecureString $administratorLoginPassword -AsPlainText -Force

# Log in and set the SubscriptionId in which to create these objects
Import-Module ..\Login
Login $tenantId $applicationId $secret $subscriptionId

$pathToAzSqlTemplate = "./azureDeploy.json"

# Check for or create a resource group
$resourceGroupExists = (Get-AzResourceGroup -Name $resourceGroupName `
-ErrorVariable notPresent -ErrorAction SilentlyContinue).ResourceGroupName `
-eq $resourceGroupName 

if (!$resourceGroupExists) {
        New-AzResourceGroup -Name $resourceGroupName -Location "$location" -Force
        Write-Host "Created resource group $resourceGroupName"
} else {
<<<<<<< HEAD
        Write-Host "Resource group already exists."
=======
        Write-Host "Resource group $resourceGroupName already exists."
>>>>>>> d82162f... added interactive tags
}

# Deploy template
Write-host "Creating primary server..."
New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName `
-TemplateFile $pathToAzSqlTemplate -administratorLogin $administratorLogin `
<<<<<<< HEAD
-administratorLoginPassword $administratorLoginPassword
=======
-administratorLoginPassword $administratorLoginPassword -createdBy $createdBy -creatorsEmail $creatorsEmail
>>>>>>> d82162f... added interactive tags


# Clear deployment 
# Remove-AzResourceGroup -ResourceGroupName $resourceGroupName