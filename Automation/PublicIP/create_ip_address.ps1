## Command to create a public ip ##

# Take parameter used to create Public IP Address
param(
        [string] [Parameter(Mandatory=$true)] $tenantId,          
        [string] [Parameter(Mandatory=$true)] $applicationId, 
        [string] [Parameter(Mandatory=$true)] $secret,            
        [string] [Parameter(Mandatory=$true)] $subscriptionId,
        [string] [Parameter(Mandatory=$true)] $rgname, # Name of the resource group
        #[string] [Parameter(Mandatory=$true)] $location, # Location of Azure resources
        [string] [Parameter(Mandatory=$true)] $publicIp # Name of the azure public address
        #[string] [Parameter(Mandatory=$true)] $sku, # Type of SKU, Standard or Basic
        #[string] [Parameter(Mandatory=$true)] $allocation # AllocationMethod, Static or Dynamic
      )

      #Logs in and sets subscription      
      & "../login.ps1" $tenantId $applicationId $secret $subscriptionId

      $pathToPubIpTemplate = "./public_ip_template.json"

      # Checks if resource group exists
      if (!(Get-AzResourceGroup $rgname -ErrorAction SilentlyContinue)){ 
        Write-Output "The resource group $rgname doesn't exist!"
      }
      else{        
        $loc = Get-AzResourceGroup -Name $rgname | select-object -expandproperty location

        # Checks if the Public IP Address location matches the resource group's location 
        #if($loc.equals($location)){

          # Creates a public ip address in the given location
          New-AzResourceGroupDeployment -ResourceGroupName $rgname -TemplateFile $pathToPubIpTemplate -pubIpName $publicIp -location $loc
          
          # Creates a new Public IP Address based on the params.
          # New-AzPublicIpAddress -ResourceGroupName $rgname -Name $publicIp -Location $location -AllocationMethod $allocation -SKU $sku
          Write-Output "Successfully created public ip address named $publicIp for the resource group $rgname"
        #} 
        #else{
         # Write-Output "Make sure you entered the right location. Location should be $loc"
       # }
        
      }

