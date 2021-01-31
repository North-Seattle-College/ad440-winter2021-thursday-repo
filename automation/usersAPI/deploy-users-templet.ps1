
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

   
    [Parameter(Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string]$ServicePrincipalPassword=$(Throw "Password required."),
   
    
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
    $appServicePlanName,

    [Parameter(Mandatory=$True)]
    [string]
    $location,

    [Parameter(Mandatory=$True)]
    [string]
    $templateFilePath
)

#open log
$prefix = "yergu-Arm-deplo"
$stamp = (Get-Date).toString().Replace("/","-").Replace(":","-")
Start-Transcript "./$prefix-$stamp.log"


Clear-AzContext -Force;
$securePassword = $servicePrincipalPassword | ConvertTo-SecureString -AsPlainText -Force

$credentials = New-Object -TypeName System.Management.Automation.PSCredential($servicePrincipalId, $securePassword);


Connect-AzAccount -Credential $credentials -ServicePrincipal -Tenant $TenantId -Subscription $SubscriptionId;

Set-AzContext $SubscriptionId
New-AzResourceGroup -Name $resourceGroupName -Location $location
New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName -TemplateFile  $templateFilePath -functionName $functionName -storageAccountName $storageAccountName -appServicePlanName $appServicePlanName -location $location


Stop-Transcript



