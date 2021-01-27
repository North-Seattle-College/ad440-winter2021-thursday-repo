[CmdletBinding()]
param (
    [Parameter(Mandatory=$true)]
    [string]
    $SubscriptionId,

    [Parameter(Mandatory=$true)]
    [string]
    $TenantId,

    [Parameter(Mandatory=$true)]
    [string]
    $ServicePrincipalId,

    [Parameter(Mandatory=$true)]
    [securestring]
    $ServicePrincipalPassword,

    [Parameter(Mandatory=$true)]
    [string]
    $ResourceGroupName,

    [Parameter(Mandatory=$true)]
    [string]
    $FunctionName,

    [Parameter(Mandatory=$true)]
    [string]
    $StorageAccountName,

    [Parameter(Mandatory=$true)]
    [string]
    $AppServiceplaneName,

    [Parameter(Mandatory=$true)]
    [string]
    $location,

    [Parameter(Mandatory=$true)]
    [string]
    $TemplatefilePath
)

Clear-AzContext -Force;
#$securePassword = ConvertTo-SecureString -String $ServicePrincipalPassword -AsPlainText -Force; 
$credentials = New-Object -TypeName System.Management.Automation.PSCredential($ServicePrincipalId, $ServicePrincipalPassword );

Connect-AzAccount -Credential $credentials -ServicePrincipal -Tenant $TenantId -Subscription $SubscriptionId;

New-AzResourceGroup -Name $ResourceGroupName -Location $location;

New-AzResourceGroupDeployment -ResourceGroupName $ResourceGroupName -TemplateFile $TemplatefilePath -Location $location -StorageAccountName $StorageAccountName -AppServiceplaneName $AppServiceplaneName -FunctionName $FunctionName;