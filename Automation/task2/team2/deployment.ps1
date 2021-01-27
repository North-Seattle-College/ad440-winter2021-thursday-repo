[CmdletBinding()]
param (
    [Parameter(Mandatory=$true)]
    [string]
    $SubscriptionId,

    [Parameter(Mandatory=$true)]
    [string]
    $rgName,

    [Parameter(Mandatory=$true)]
    [string]
    $location,

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
    $TemplatefilePath,

    [Parameter(Mandatory=$true)]
    [string]
    $DeployName
)

$credentials = New-Object -TypeName System.Management.Automation.PSCredential($ServicePrincipalId, $ServicePrincipalPassword );

Connect-AzAccount -Credential $credentials -ServicePrincipal -Tenant $TenantId -Subscription $SubscriptionId;

Set-AzContext $SubscriptionId

New-AzResourceGroup `
  -Name $rgName `
  -Location $location

New-AzResourceGroupDeployment `
  -Name blanktemplate `
  -ResourceGroupName $rgName `
  -TemplateFile $TemplatefilePath