
# to run this, navigate to the Powershell  /Automation/Redis_Cache/deploy.ps1


param(
        [string] [Parameter(Mandatory=$true)] $SubscriptionId,
        [string] [Parameter(Mandatory=$true)] $ResourceGroupName,
        [string] [Parameter(Mandatory=$true)] $Location,
        [string] [Parameter(Mandatory=$true)] $Redis_nsc_redis_dev_usw2_thursday_name

      )

$pathToRedisTemplate = "/Users/student/Documents/GitHub/ad440-winter2021-thursday-repo/Automation/Redis_Cache/template.json"   



# Creates REDIS CACHE if one of the same name does not already exist in the Resource Group
$RedisExists = (Get-AzRedisCache -ResourceGroupName “nsc-rg-dev-usw2-thursday” -Name “nsc-redis-dev-usw2-thursday”) 
      
if (!$RedisExists) { 
    Write-Host "Redis Cache does not exist. Creating now."
    # create redis with given name (can also add address prefix and location if not same as rg)
    New-AzResourceGroupDeployment -ResourceGroupName $ResourceGroupName -TemplateFile $pathToRedisTemplate 
} else {
    Write-Host "Redis Cache with name nsc-redis-dev-usw2-thursday already exists."
}

