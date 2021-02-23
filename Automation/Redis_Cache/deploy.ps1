
# to run this, navigate to the Powershell  /Automation/Redis_Cache/deploy.ps1


param(
        [string] [Parameter(Mandatory=$true)] $ResourceGroupName,
        [string] [Parameter(Mandatory=$true)] $RedisServerName

      )

$pathToRedisTemplate = "./template.json"   



# Creates REDIS CACHE if one of the same name does not already exist in the Resource Group
$RedisExists = (Get-AzRedisCache -ResourceGroupName $ResourceGroupName -Name $RedisServerName) 
      
if (!$RedisExists) { 
    Write-Host "Redis Cache does not exist. Creating now."
    # create redis with given name (can also add address prefix and location if not same as rg)
    New-AzResourceGroupDeployment -ResourceGroupName $ResourceGroupName -TemplateFile $pathToRedisTemplate 
} else {
    Write-Host "Redis Cache with name " $RedisServerName "already exists."
}

# -ResourceGroupName “nsc-rg-dev-usw2-thursday”
# -RedisServerName “nsc-redis-dev-usw2-thursday”
