param(
        [string] [Parameter(Mandatory=$true)] $tenantId,
        [string] [Parameter(Mandatory=$true)] $applicationId,
        [string] [Parameter(Mandatory=$true)] $secret,
        [string] [Parameter(Mandatory=$true)] $subscriptionId
      )

[securestring]$secureSecret = ConvertTo-SecureString $secret -AsPlainText -Force      
[pscredential]$credObject = New-Object System.Management.Automation.PSCredential ($applicationId, $secureSecret)
Connect-AzAccount -ServicePrincipal -Credential $credObject -Tenant $tenantId      
write-output "Logged into the account $applicationId"

Set-AzContext -Subscription $subscriptionId
write-output "Set to subscription $subscriptionId"
