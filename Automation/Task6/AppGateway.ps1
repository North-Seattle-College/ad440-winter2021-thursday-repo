#Creates Azure Application Gateway 

param (
    [Parameter(Mandatory=$true)]
    [string]
    $applicationGatewayName,

    [Parameter(Mandatory=$true)]
    [string]
    $location,

    [Parameter(Mandatory=$true)]
    [string]
    $backendAddressPools,

    [Parameter(Mandatory=$true)]
    [string]
    $backendHttpSettingsCollection,

    [Parameter(Mandatory=$true)]
    [string]
    $frontendIPConfigurations,

    [Parameter(Mandatory=$true)]
    [string]
    $gatewayIPConfigurations,

    [Parameter(Mandatory=$true)]
    [string]
    $frontendPorts
    
    [Parameter(Mandatory=$true)]
    [string]
    $httpListeners
    
    [Parameter(Mandatory=$true)]
    [string]
    $requestRoutingRules
    
    [Parameter(Mandatory=$true)]
    [string]
    $sku
    
)

$templateFilePath = "./template.json"

New-AzResourceGroup 
  -Name myResourceGroupAG `
  -Location West US 2 `
  
New-AzApplicationGateway `
  -Name $applicationGatewayName `
  -ResourceGroupName myResourceGroupAG `
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