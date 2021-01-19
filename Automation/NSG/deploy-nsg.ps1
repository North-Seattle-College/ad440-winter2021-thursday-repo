param(
    # Change value if you want a different region limit notification
    $ResourceLimit = 15,
    $TemplateFilePath = "./template.json",
    $ParameterFilePath = "./parameters.json",

    # Found in Azure secrets
    [Parameter(Mandatory=$True)]
    [string]
    $ServicePrincipalUsername,

    # Your tenant Id in Azure
    [Parameter(Mandatory=$True)]
    [string]
    $TenantId,

    # Name for the resource group you will create
    [Parameter(Mandatory=$True)]
    [string]
    $ResourceGroupName,

    # Region. ex. westus, eastus...
    [Parameter(Mandatory=$True)]
    [string]
    $Region,

    [Parameter(Mandatory=$True)]
    [string]
    $DeploymentName
)

# Service principal login, will prompt user for password
Write-Host "`n"
$credential = Get-Credential -Username $ServicePrincipalUsername

Connect-AzAccount `
    -ServicePrincipal `
    -Credential $credential `
    -Tenant $TenantId `

# Function to check initial region limits before creation
function Get-RegionLimit {
    Get-AzNetworkUsage `
        -Location $Region `
        | Where-Object {$_.CurrentValue -gt $ResourceLimit}
}

# Check other regions for limits
function Find-OtherRegionsLimits {
    param (
        [Parameter(Mandatory=$True)]
        [string]
        $RegionName
    )

    Get-AzNetworkUsage `
        -Location $RegionName `
        | Where-Object {$_.CurrentValue -gt -1} ` # -1 to show all resources
        | Format-Table ResourceType, CurrentValue, Limit
}

# Tell user if their region is almost at resource capacity and let them switch regions.
if (Get-RegionLimit) {
    Write-Host -ForegroundColor Red " `n This region is almost, or at capacity, you may want to create resources in a different region."

    # Display limit table along with limit message
    Get-AzNetworkUsage `
        -Location $Region `
        | Where-Object {$_.CurrentValue -gt $ResourceLimit} ` # Change this value (15) for different minimum resource limit
        | Format-Table ResourceType, CurrentValue, Limit

    $CheckOtherRegions = Read-Host -Prompt " `n Would you like to check another region? (Y/N) "

    # Only allows one more region check
    if ($CheckOtherRegions -eq "Y" ) {
        Find-OtherRegionsLimits
    }

    Write-Host -ForegroundColor Green " `n Select a region for your resource group creation."

    # Create new resource group but prompt location
    New-AzResourceGroup `
    -Name $ResourceGroupName

} else {
    New-AzResourceGroup `
    -Name $ResourceGroupName `
    -Location $Region 
}

# Deploy with template + parameters
New-AzResourceGroupDeployment `
    -Name $DeploymentName `
    -ResourceGroupName $ResourceGroupName `
    -TemplateFile $TemplateFilePath `
    -TemplateParameterFile $ParameterFilePath

