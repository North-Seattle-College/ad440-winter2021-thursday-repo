# Connect-AzAccount

##TODO: add key vault entry
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
        [SecureString] [Parameter(Mandatory=$true)] $administratorLoginPassword,
        [string] [Parameter(Mandatory=$true)] $startIp,
        [string] [Parameter(Mandatory=$true)] $endIp
)

$pathToAzSqlTemplate = "./azureDeploy.json"

# Log in and set the SubscriptionId in which to create these objects
& "../login.ps1" $tenantId $applicationId $secret $subscriptionId

# Create a resource group
$resourceGroupExists = (Get-AzResourceGroup -Name $resourceGroupName).ResourceGroupName `
-eq $resourceGroupName

if (!$resourceGroupExists) {
        New-AzResourceGroup -Name $resourceGroupName -Location "$location" -Force
        Write-Host "Created resource group $resourceGroupName"
} else {
        Write-Host "Resource group already exists."
}

# Deploy template
Write-host "Creating primary server..."
New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName `
-TemplateFile $pathToAzSqlTemplate -administratorLogin $administratorLogin `
-administratorLoginPassword $administratorLoginPassword `
 -StartIpAddress $startIp -EndIpAddress $endIp

# Clear deployment 
# Remove-AzResourceGroup -ResourceGroupName $resourceGroupName