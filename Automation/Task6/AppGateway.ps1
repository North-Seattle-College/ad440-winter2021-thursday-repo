param(

    # Login parameters
    [string] [Parameter(Mandatory=$true)] $tenantId,
    [string] [Parameter(Mandatory=$true)] $applicationId,
    [string] [Parameter(Mandatory=$true)] $secret,
    [string] [Parameter(Mandatory=$true)] $subscriptionId,

    # parameters
    [string] [Parameter(Mandatory=$true)] $resourceGroupName,
    [string] [Parameter(Mandatory=$true)] $location,
    [string] [Parameter(Mandatory=$true)] $applicationGatewayName

)

Start-Transcript -Path "$PSScriptRoot\create_Azure_log.log"
Write-Host "Logging to $PSScriptRoot\create_Azure_log.log"


# Imports Login Module
Import-Module ..\Login
# Path to Template File
$templateFilePath = "./template.json"

# Login Inputs
Login $tenantId $applicationId $secret $subscriptionId


# Creates/Updates resource group
New-AzResourceGroup -Name $ResourceGroupName -Location $Location -Force


#Creates New Application Gateway
$sku = New-AzApplicationGatewaySku `
  -Name Standard_v2 `
  -Tier Standard_v2 `
  -Capacity 2
New-AzApplicationGateway `
  -Name $applicationGatewayName `
  -ResourceGroupName $resourceGroupName `
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