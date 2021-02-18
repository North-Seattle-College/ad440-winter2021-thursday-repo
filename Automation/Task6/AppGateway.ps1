param(
    [string] [Parameter(Mandatory=$true)] $resourceGroup, # Name of resource group

    [string] [Parameter(Mandatory=$true)] $location, # westus2

    [string] [Parameter(Mandatory=$true)] $applicationGatewayName, # Name of application gateway

    # Login parameters
    [string] [Parameter(Mandatory=$true)] $tenantId,
    [string] [Parameter(Mandatory=$true)] $applicationId,
    [string] [Parameter(Mandatory=$true)] $secret,
    [string] [Parameter(Mandatory=$true)] $subscriptionId
)

# Imports Login Module
Import-Module ..\Login
# Path to Template File
$templateFilePath = "./template.json"

# Login Inputs
Login $tenantId $applicationId $secret $subscriptionId

# Checks for resource group
Get-AzResourceGroup -Name $resourceGroup -ErrorVariable noRG -ErrorAction SilentlyContinue
if($noRG){
    Write-Host "Creating a New Resource Group $resourceGroup"
    New-AzResourceGroup 
      -Name $resourceGroup 
      -Location $location
} else {
    Write-Host "Resource Group $resourceGroup already exits"
}
#Creates New Application Gateway
New-AzApplicationGateway `
  -Name $applicationGatewayName `
  -ResourceGroupName $myResourceGroupAG `
  -TemplateFile  $templateFilePath `
  -Location $location `
  -BackendAddressPools $backendAddressPools `
  -BackendHttpSettingsCollection $backendHttpSettingsCollection `
  -FrontendIpConfigurations $frontendIPConfigurations `
  -GatewayIpConfigurations $gatewayIPConfigurations `
  -FrontendPorts $frontendPorts `
  -HttpListeners $httpListeners `
  -RequestRoutingRules $requestRoutingRules `
  -Sku $sku