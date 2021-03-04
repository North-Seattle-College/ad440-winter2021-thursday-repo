param(

    [Parameter(Mandatory = $True)]
    [string]
    $TenantId,

    [Parameter(Mandatory = $True)]
    [string]
    $SPApplicationId,

    [Parameter(Mandatory = $True)]
    [string]
    $SPSecret,

    [Parameter(Mandatory = $True)]
    [string]
    $SubscriptionId,

    [Parameter(Mandatory = $True)]
    [string]
    $ResourceGroupName,

    [Parameter(Mandatory = $True)]
    [string]
    $Location,

    [Parameter(Mandatory = $True)]
    [string]
    $DeploymentName,

    [Parameter(Mandatory = $True)]
    [string]
    $KeyVaultName,

    [Parameter(Mandatory = $True)]
    [string]
    $ObjectId,
    
    [string]
    $templateFilePath = "./template.json"

)

# Login using Larissa's Login module & contains error handling)
Import-Module ..\..\Login
Login $TenantId $SPApplicationId $SPSecret $SubscriptionId

#Check for existing resource group
$resourceGroup = Get-AzResourceGroup -Name $ResourceGroupName -ErrorAction SilentlyContinue
if (!$resourceGroup) {
    Write-Host "Resource group '$ResourceGroupName' does not exist."
    exit
}
else {

    $templateParams = @{
        keyVaultName = $KeyVaultName
        policies     = @(
            @{
                tenantId     = $TenantId
                objectId     = $ObjectId
                keys         = @()
                secrets      = @('get')
                certificates = @()
            },
            @{
                tenantId     = $TenantId
                objectId     = $ObjectId
                keys         = @()
                secrets      = @()
                certificates = @('list')
            }
        )
    }

    Write-Host "Using existing resource group '$ResourceGroupName'"
  
    # Create the Key Vault (enabling it for Disk Encryption, Deployment and Template Deployment)
    New-AzKeyVault -ResourceGroupName $resourceGroup `
        -EnabledForDiskEncryption -EnabledForDeployment -EnabledForTemplateDeployment `
        -Name $DeploymentName  `
        -TemplateFile $templateFilePath `
        -Location $location `
        -TemplateParameterObject $templateParams -Verbose
}
