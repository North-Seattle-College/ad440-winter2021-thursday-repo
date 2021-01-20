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
    [string]
    $ServicePrincipalPassword
)

# Changing something here
#Connect-AzAccount
#New-AzResourceGroup
#New-AzResourceGroupDeployment