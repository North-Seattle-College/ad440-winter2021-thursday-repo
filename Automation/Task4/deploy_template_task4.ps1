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
    $Resource_Group_Name,

    [Parameter(Mandatory=$True)]
    [string]
    $function_name,

    [Parameter(Mandatory=$True)]
    [string]
    $storage_account_name,

    [Parameter(Mandatory=$True)]
    [string]
    $app_service_plan_name,

    [Parameter(Mandatory=$True)]
    [string]
    $location
)


Clear-AzContext -Force;
#$securePassword = ConvertTo-SecureString -String $ServicePrincipalPassword -AsPlainText -Force;
$credentials = New-Object -TypeName System.Management.Automation.PSCredential($ServicePrincipalId, $ServicePrincipalPassword);


Connect-AzAccount -Credential $credentials -ServicePrincipal -Tenant $TenantId -SubscriptionId $SubscriptionId;

New-AzResourceGroup -Name $Resource_Group_Name -Location $location

New-AzResourceGroupDeployment -ResourceGroupName $Resource_Group_Name -TemplateFile "./template.json" -function_name $function_name -storage_account_name $storage_account_name -app_service_plan_name $app_service_plan_name -location $location

