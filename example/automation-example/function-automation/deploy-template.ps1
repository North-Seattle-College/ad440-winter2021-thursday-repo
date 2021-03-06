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
    [string]
    $ServicePrincipalPassword,

    [Parameter(Mandatory=$True)]
    [string]
    $TenantAbbreviation,

    [Parameter(Mandatory=$True)]
    [string]
    $Environment,

    [Parameter(Mandatory=$True)]
    [string]
    $ResourceGroupName
)

# Sign In
$securePassword = ConvertTo-SecureString -String $ServicePrincipalPassword -AsPlainText -Force;
$credentials = New-Object -TypeName System.Management.Automation.PSCredential($ServicePrincipalId, $securePassword);

Connect-AzAccount -Credential $credentials -ServicePrincipal -Tenant $TenantId -SubscriptionId $SubscriptionId;

$resourceGroupName = ("nsc-rg-{0}-test" -f $Environment).ToLower()

#Changing something here
#Connect-AzAccount
#New-AzResourceGroup -Name "toddysm-resource-group"
#New-AzResourceGroupDeployment

#New-AzResourceGroupDeployment -ResourceGroupName "toddysm-resource-group" -TemplateParameterFile 'parameters.json' -TemplateFile 'template.json'

$parameters = @{
    sites_nsc_fun_dev_usw2_tsmtestfunction_name="nscFUNDeV-usw2-tsmtestfunction";
    storageAccounts_nscstrdevusw2tsmtestfun_name="nscstrdevusw2tsmtestfun";
    serverfarms_ASP_nscrgdevusw2tsmtestfunction_8ab1_name="ASP-nscrgdevusw2tsmtestfunction-8ab1"
}

New-AzResourceGroupDeployment -ResourceGroupName $ResourceGroupName -TemplateFile "template.json" -TemplateParameterObject $parameters