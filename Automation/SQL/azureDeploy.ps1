# Connect-AzAccount

param(
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
        [SecureString] [Parameter(Mandatory=$true)] $administratorLoginPassword
)

$pathToAzSqlTemplate = "./azureDeploy.json"

# The SubscriptionId in which to create these objects
& "../login.ps1" $tenantId $applicationId $secret $subscriptionId

# Create a resource group
New-AzResourceGroup -Name $resourceGroupName -Location "$location" -Force

# Deploy template
Write-host "Creating primary server..."
New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName `
-TemplateFile $pathToAzSqlTemplate -administratorLogin $administratorLogin `
-administratorLoginPassword $administratorLoginPassword

# Clear deployment 
# Remove-AzResourceGroup -ResourceGroupName $resourceGroupName