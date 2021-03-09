param(

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
    $TenantId,

    [Parameter(Mandatory = $True)]
    [string]
    $ObjectId,

    [Parameter(Mandatory = $True)]
    [string]
    $KeyVaultName,
    
    # ****************** Please Note - Hard Coded Values Below ******************
    # For the purpose of this task, and in order to minimize user input in the 
    # powershell, I am hard coding the TAGS, Deployment name and location.
    # This Azure Key Vault Deployment is specifically for Thursday Cohort.
    # To pass values/params dynamically, you may remove the hard coded values,
    # and set the [Parameter(Mandatory = $True)].
    # **************************************************************************

    [Parameter(Mandatory = $False)]
    [string]
    $ResourceGroupName = "nsc-rg-dev-usw2-thursday",

    [Parameter(Mandatory = $False)]
    [string]
    $Location = "westus2",

    [Parameter(Mandatory = $False)]
    [string]
    $OwnerName = "Jak",

    [Parameter(Mandatory = $False)]
    [string]
    $OwnerEmail = "Jakhongir.Ashuraliev@seattlecolleges.edu",

    [Parameter(Mandatory = $False)]
    [string]
    $NSCCohort = "Thursday",

    [Parameter(Mandatory = $False)]
    [string]
    $NSCYear = "2021",

    [string]
    $DeploymentName = "AzKeyVaultDeployThursday",

    [string]
    $templateFilePath = "./template.json"

)

# Login using Larissa's Login module & contains error handling)
Import-Module ..\..\Login
Login $TenantId $SPApplicationId $SPSecret $SubscriptionId

#Check for existing resource group, if rg exsists - deploy otherwise exit
$resourceGroup = Get-AzResourceGroup -Name $ResourceGroupName -ErrorAction SilentlyContinue
if (!$resourceGroup) {
    Write-Host "Resource group '$ResourceGroupName' does not exist.";
    exit
}
else {
    # Hash table for template deployment
    $templateParams = @{
        # Tags  
        tags              = @{
            "OwnerName"  = $OwnerName
            "OwnerEmail" = $OwnerEmail
            "NSCCohort"  = $NSCCohort
            "NSCYear"    = $NSCYear
        }
        keyVaultName      = $KeyVaultName
        location          = $Location
        resourceGroupName = $ResourceGroupName
        subscriptionId    = $SubscriptionId
        tenantId          = $TenantId
        objectId          = $ObjectId    
    }

    # Start the deployment
    Write-Host "Starting deployment...";
    Write-Host "Using existing resource group '$ResourceGroupName'"

    # Create the Key Vault (enabling it for Disk Encryption, Deployment and Template Deployment)
    New-AzResourceGroupDeployment `
        -DeploymentName $DeploymentName `
        -ResourceGroupName $ResourceGroupName `
        -TemplateFile $templateFilePath `
        -Location $location `
        -TemplateParameterObject $templateParams -Verbose
}
