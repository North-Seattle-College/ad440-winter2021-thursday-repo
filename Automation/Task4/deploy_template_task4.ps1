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


Write-Host "The Resource group will have the name in this format : [project]-[resource-type]-[environment]-[location]-[other-stuff]"
$project = Read-Host "Please enter the project name"
$resourcetype = Read-Host "Please enter the resource type"
$environment = Read-Host "Please enter evironment"
$location = Read-Host "Please enter location"
$otherstuff = Read-Host "Please enter otherstuff"
$name = $project + '-' + $resourcetype + '-' + $environment + '-' + $location + '-' + $otherstuff; 
Write-Host "The name used will be" $name;

$location = Read-Host "Please enter a location for your resource group"

New-AzResourceGroup -Name $name -Location $location

New-AzResourceGroupDeployment -ResourceGroupName $name -TemplateFile "./template.json" -TemplateParameterFile "./parameters.json" -function_name $function_name -storage_account_name $storage_account_name -app_service_plan_name $app_service_plan_name -location $location -tenant_id $TenantId -service_plan_id $ServicePrincipalId

