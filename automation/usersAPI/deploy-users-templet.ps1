
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
    [string][ValidateNotNullOrEmpty()]
    $ServicePrincipalPassword,
   
    
    [Parameter(Mandatory=$True)]
    [string]
    $resourceGroupName,

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

#open log
$prefix = "yergu-Arm-deplo"
$stamp = (Get-Date).toString().Replace("/","-").Replace(":","-")
Start-Transcript "./$prefix-$stamp.log"


Clear-AzContext -Force;
$securePassword = ConvertTo-SecureString -String $servicePrincipalPassword -AsPlainText -Force;

$credentials = New-Object -TypeName System.Management.Automation.PSCredential($servicePrincipalId, $securePassword);


Connect-AzAccount -Credential $credentials -ServicePrincipal -Tenant $TenantId -Subscription $SubscriptionId;

Set-AzContext $SubscriptionId
New-AzResourceGroup -Name $resourceGroupName -Location $location

New-AzResourceGroupDeployment -resourceGroupName $resourceGroupName -functionName $functionName -storageAccountName $storageAccountName -AppServicePlanName  $AppServicePlanName -location $location -TemplatePath $TemplatePath
Stop-Transcript





