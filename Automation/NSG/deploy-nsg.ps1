param(
    $TemplateFilePath = "./template.json",

    # Your tenant Id in Azure
    [Parameter(Mandatory=$True)]
    [string]
    $TenantId,

    # Found in Azure secrets as appId
    [Parameter(Mandatory=$True)]
    [string]
    $ServicePrincipalUsername,

    # Found in Azure secrets as secret
    [Parameter(Mandatory=$True)]
    [string]
    $ServicePrincipalSecret,

    # Your tenant Id in Azure
    [Parameter(Mandatory=$True)]
    [string]
    $SubscriptionId,

    # Name for the resource group you will create
    [Parameter(Mandatory=$True)]
    [string]
    $ResourceGroupName,

    # Region. ex. westus, eastus...
    [Parameter(Mandatory=$True)]
    [string]
    $Location,

    [Parameter(Mandatory=$True)]
    [string]
    $DeploymentName,

    # For tags, please include your email
    [Parameter(Mandatory=$True)]
    [string]
    $OwnerEmail,

    # Security group name ex. automation-nsg-<initials>
    [Parameter(Mandatory=$True)]
    [string]
    $SecurityGroupName,

    # Security rule params, see example below in $params line 125 if unsure of inputs
    [Parameter(Mandatory=$True)]
    [string]
    $SecurityRuleName,

    [Parameter(Mandatory=$True)]
    [string]
    $Protocol,

    [Parameter(Mandatory=$True)]
    [string]
    $SourcePortRange,

    [Parameter(Mandatory=$True)]
    [string]
    $DestinationPortRange,

    [Parameter(Mandatory=$True)]
    [string]
    $SourceAddressPrefix,

    [Parameter(Mandatory=$True)]
    [string]
    $DestinationAddressPrefix,

    [Parameter(Mandatory=$True)]
    [string]
    $Access,

    [Parameter(Mandatory=$True)]
    [string]
    $Priority,

    [Parameter(Mandatory=$True)]
    [string]
    $Direction,

    # Note, below are not mandatory params and are here if further nsg specs are needed
    [Parameter(Mandatory=$False)]
    [string]
    $SourcePortRanges,

    [Parameter(Mandatory=$False)]
    [string]
    $DestinationPortRanges,

    [Parameter(Mandatory=$False)]
    [string]
    $SourceAddressPrefixes,

    [Parameter(Mandatory=$False)]
    [string]
    $DestinationAddressPrefies
)

$params = @{
    tags = @{
        "ownerEmail" = $OwnerEmail
    }
    networkSecurityGroups_name = @{
        "securityGroupName" = $SecurityGroupName
    }
    securityRules = @{
        "name" = $SecurityRuleName
        "protocol" = $Protocol    
        "sourcePortRange" = $SourcePortRange  
        "destinationPortRange" = $DestinationPortRange
        "sourceAddressPrefix" = $SourceAddressPrefix
        "destinationAddressPrefix" = $DestinationAddressPrefix
        "access" = $Access          
        "priority" = $Priority
        "direction" = $Direction
        "sourcePortRanges" = $SourcePortRanges
        "destinationPortRanges" = $DestinationPortRanges     
        "sourceAddressPrefixes" = $SourceAddressPrefixes
        "destinationAddressPrefixes" = $DestinationAddressPrefies
    }
# Example SSH security rule
<#
        "name" = SSH_Access;
        "protocol" = "TCP";         
        "sourcePortRange"= "*";   
        "destinationPortRange"= "22";
        "sourceAddressPrefix"= "97.113.101.80/32";
        "destinationAddressPrefix"= "*"
        "access"= "Allow";              
        "priority"= 100;                 
        "direction"= "Inbound";         
        "sourcePortRanges"= "";         
        "destinationPortRanges"= "";     
        "sourceAddressPrefixes"= "";    
        "destinationAddressPrefixes"= "";
#>
}
# Logs in and sets subscription      
& "../login.ps1" $TenantId $ServicePrincipalUsername $ServicePrincipalSecret $SubscriptionId

# Creates/Updates resource group
New-AzResourceGroup -Name $ResourceGroupName -Location $Location -Force

# Deploy with template + parameters
New-AzResourceGroupDeployment `
    -Name $DeploymentName `
    -ResourceGroupName $ResourceGroupName `
    -TemplateFile $TemplateFilePath `
    -TemplateParameterObject $params -Verbose
