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
$Credential
#logging in
#Select-AzContext
# $user = Read-Host "Please enter the user name"
# $password = Read-Host "Please enter the password" -AsSecureString

#$credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $user, $password


#Connect-AzAccount -Credential $Credential -Tenant $TenantId -ServicePrincipal
#Connect-AzAccount   -Credential $Credential -Tenant $TenantId -ServicePrincipal
# #creating a new resource group
# #New-AzResourceGroup
# #creating a new resource group deployment
# #New-AzResourceGroupDeployment

Connect-AzAccount -Tenant $TenantId -SubscriptionId $SubscriptionId;

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

New-AzResourceGroupDeployment -ResourceGroupName $name -TemplateFile "./template.json" -TemplateParameterFile "./parameters.json" -function_name Read-Host -storage_account_name Read-Host -app_service_plan_name Read-Host -location Read-Host -tenant_id Read-Host -service_plan_id Read-Host

