[CmdletBinding()]
param (
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
    $ResourceGroupName,

    [Parameter(Mandatory=$True)]
    [string]
    $functionName,

    [Parameter(Mandatory=$True)]
    [string]
    $storageAccountName,

    [Parameter(Mandatory=$True)]
    [string]
    $AppServicePlanName,

    [Parameter(Mandatory=$True)]
    [string]
    $location,

    [Parameter(Mandatory=$True)]
    [string]
    $TemplatePath
)
$credentials = New-Object -TypeName System.Management.Automation.PSCredential($ServicePrincipalId, $ServicePrincipalPassword );

Connect-AzAccount -Credential $credentials -ServicePrincipal -Tenant $TenantId -Subscription $SubscriptionId;


Set-AzContext $SubscriptionId
New-AzResourceGroup -Name $ResourceGroupName -Location $location

New-AzResourceGroupDeployment -ResourceGroupName $ResourceGroupName -functionName $functionName -storageAccountName $storageAccountName 
-AppServicePlanName  $AppServicePlanName -location $location -TemplatePath $TemplatePath

 