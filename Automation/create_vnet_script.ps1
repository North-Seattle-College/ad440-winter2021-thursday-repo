# https://github.com/Azure-Samples/resource-manager-python-template-deployment
# https://docs.microsoft.com/en-us/azure/templates/microsoft.resources/deploymentscripts
# example: https://raw.githubusercontent.com/Azure/azure-docs-json-samples/master/deployment-script/deploymentscript-helloworld.ps1
# https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/deployment-script-template
# https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-tutorial-deployment-script
# https://docs.microsoft.com/en-us/learn/modules/extend-resource-manager-template-deployment-scripts/
# https://dev.to/omiossec/an-introduction-to-deployment-scripts-resource-in-azure-resource-manager-m8g
# also go to Azure to see if you can get the script from there

param(
        [string] [Parameter(Mandatory=$true)] $parameter1,
        [string] [Parameter(Mandatory=$true)] $parameter2,
        [string] [Parameter(Mandatory=$true)] $parameter3
      )

$output = 'Hello {0}. The username is {1}, the password is {2}.' -f $name,${Env:UserName},${Env:Password}
Write-Output $output
$DeploymentScriptOutputs = @{}
$DeploymentScriptOutputs['text'] = $output