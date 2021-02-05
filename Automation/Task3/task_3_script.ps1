$resourceGroupName = $args[0]
$location = $args[1]
$templateUri = $args[2]

New-AzResourceGroup -Name $resourceGroupName -Location $location
New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName -TemplateUri $templateUri