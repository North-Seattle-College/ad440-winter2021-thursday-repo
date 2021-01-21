#parameters
param(
    [Parameter(Mandatory=$True)]
    [string]
    $Subscription_Id,

    [Parameter(Mandatory=$True)]
    [string]
    $Tenant_Id,

    [Parameter(Mandatory=$True)]
    [string]
    $ServicePrincipal_Id,

    [Parameter(Mandatory=$True)]
    [SecureString]
    $ServicePrincipalpw,

    [Parameter(Mandatory=$True)]
    [string]
    $R_G_Name,

    [Parameter(Mandatory=$True)]
    [string]
    $function_name,

    [Parameter(Mandatory=$True)]
    [string]
    $storageAccount_name,

    [Parameter(Mandatory=$True)]
    [string]
    $app_service_plan_name,

    [Parameter(Mandatory=$True)]
    [string]
    $location,

    [Parameter(Mandatory=$True)]
    [string]
    $templatefile_path



)

$securePassword = ConvertTo-SecureString -String $ServicePrincipalPassword -AsPlainText -Force;
$credentials = New-Object -TypeName System.Management.Automation.PSCredential($ServicePrincipalId, $securePassword);

Connect-AzAccount -Credential $credentials -Tenant $Tenant_Id -SubscriptionId $Subscription_Id -ServicePrincipal

New-AzResourceGroup -Name $R_G_Name -Location $location

