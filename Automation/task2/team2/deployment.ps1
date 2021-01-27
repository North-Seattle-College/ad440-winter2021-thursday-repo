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
    $TemplatefilePath
)

Connect-AzAccount

Set-AzContext $SubscriptionId

New-AzResourceGroup `
  -Name $rgName `
  -Location $location

New-AzResourceGroupDeployment `
  -Name blanktemplate `
  -ResourceGroupName $rgName `
  -TemplateFile $TemplatefilePath