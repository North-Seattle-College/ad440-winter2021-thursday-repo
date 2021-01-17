#parameters required to run the script.
param(
    [Parameter(Mandatory=$True)]
    [string]
    $SubscriptionId,

    [Parameter(Mandatory=$True)]
    [string]
    $TenantId,

    [Parameter(Mandatory=$True)]
    [string]
    $ServicePrincipalId,

    [Parameter(Mandatory=$True)]
    [SecureString]
    $ServicePrincipalPassword,

    [Parameter(Mandatory=$True)]
    [string]
    $ResourceGroupName

)
$Credential = Get-Credential
#logging in
Connect-AzAccount  -Credential $Credential -Tenant $TenantId -ServicePrincipal
#Get-AzContext -ListAvailable
# Select-AzContext
# #creating a new resource group
# #New-AzResourceGroup
# #creating a new resource group deployment
# #New-AzResourceGroupDeployment