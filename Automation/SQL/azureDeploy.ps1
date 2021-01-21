param(
        [string] [Parameter(Mandatory=$true)] $location,
        [string] [Parameter(Mandatory=$true)] $resourceGroupName,
        [string] [Parameter(Mandatory=$true)] $serverName,
        [string] [Parameter(Mandatory=$true)] $tenantId,          
        [string] [Parameter(Mandatory=$true)] $applicationId,
        [string] [Parameter(Mandatory=$true)] $secret,
        [string] [Parameter(Mandatory=$true)] $subscriptionId
)

$pathToAzSqlTemplate = "./azureDeploy.json"
   
& "../login.ps1" $tenantId $applicationId $secret $subscriptionId

New-AzResourceGroup -Name $resourceGroupName -Location "$location"

Write-host "Creating primary server..."
New-AzSqlServer -ResourceGroupName $resourceGroupName `
  -ServerName $serverName `
  -Location $location `
  -SqlAdministratorCredentials $(New-Object -TypeName System.Management.Automation.PSCredential `
  -ArgumentList $adminLogin, $(ConvertTo-SecureString -String $password -AsPlainText -Force))

New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName -TemplateFile $pathToAzSqlTemplate