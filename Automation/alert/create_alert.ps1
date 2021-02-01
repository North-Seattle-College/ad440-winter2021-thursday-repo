# to run this, navigate to the repo and run ./Automation/create_alert.ps1 
# with the 1st 7 parameters inline 

param(
        [string] [Parameter(Mandatory=$true)] $TenantId,          
        [string] [Parameter(Mandatory=$true)] $SPApplicationId,     #username for SP
        [string] [Parameter(Mandatory=$true)] $SPSecret,            #password for SP
        [string] [Parameter(Mandatory=$true)] $SubscriptionId,
        [string] [Parameter(Mandatory=$true)] $Location, 
        [string] [Parameter(Mandatory=$true)] $ResourceGroupName,
        [string] [Parameter(Mandatory=$true)] $AlertName,
        [string] $AlertDescription = "Check every 5 minutes to see if more than 30 5xx responses have been generated",
        [int] $AlertSeverity = 3,
        [string] $ResourceId = "/subscriptions/9f4dcf43-aa06-457b-b975-f0216baef20d/resourceGroups/nsc-functions-team1/providers/Microsoft.Web/sites/nsc-functionsapp-team1",
        [string] $MetricName = "Http5xx",       # get possible metric names: Get-AzMetricDefinition [resourceId]
        [string] $Operator = "GreaterThanOrEqual",
        [int] $Threshold = 30,
        [string] $TimeAggregation = "Count",
        [string] $WindowSize = "PT5M",
        [string] $EvaluationFrequency = "PT5M",
        [string] $ActionGroupId = "/subscriptions/9f4dcf43-aa06-457b-b975-f0216baef20d/resourcegroups/nataliasprint1test/providers/microsoft.insights/actiongroups/application insights smart detection"
      )

$pathToAlertTemplate = "./alert_template.json"   

# Logs in and sets subscription      
& "../login.ps1" $TenantId $SPApplicationId $SPSecret $SubscriptionId

# Creates/Updates resource group
New-AzResourceGroup -Name $ResourceGroupName -Location $Location -Force

# Creates VNet if one of the same name does not already exist in the Resource Group
$alertExists = (Get-AzMetricAlertRuleV2 -Name $AlertName -ResourceGroupName $ResourceGroupName -ErrorAction SilentlyContinue).Name -eq $AlertName
if (!$alertExists) { 
    Write-Host "Alert does not exist. Creating now."
    # create Alert with given name
    New-AzResourceGroupDeployment `
        -ResourceGroupName $ResourceGroupName `
        -TemplateFile $pathToAlertTemplate `
        -alertName $AlertName `
        -alertDescription $AlertDescription `
        -alertSeverity $AlertSeverity `
        -resourceId $ResourceId `
        -metricName $MetricName `
        -operator $Operator `
        -threshold $Threshold `
        -timeAggregation $TimeAggregation `
        -windowSize $WindowSize `
        -evaluationFrequency $EvaluationFrequency `
        -actionGroupId $ActionGroupId
} else {
    Write-Host "Alert with name $AlertName already exists."
}
