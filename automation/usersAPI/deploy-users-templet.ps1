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
    [ValidateNotNullOrEmpty()]
    [String]$ServicePrincipalPassword=$(Throw "Password required."),
   
    
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
Clear-AzContext -Force;
$securePassword = ConvertTo-SecureString -String $ServicePrincipalPassword -AsPlainText -Force;
$credentials = New-Object -TypeName System.Management.Automation.PSCredential($ServicePrincipalId, $securePassword);


Connect-AzAccount -Credential $credentials -ServicePrincipal -Tenant $TenantId -SubscriptionId $SubscriptionId;

New-AzResourceGroup -Name $ResourceGroupName -Location $location

New-AzResourceGroupDeployment -ResourceGroupName $ResourceGroupName -TemplatePath "./template.json" -functionName $functionName -storageAccountName $storageAccountName -app_service_plan_name $AppServicePlanName -location $location

