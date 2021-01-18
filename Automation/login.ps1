param(
        [string] [Parameter(Mandatory=$true)] $tenantId,
        [string] [Parameter(Mandatory=$true)] $applicationId,
        [SecureString] [Parameter(Mandatory=$true)] $secret,
        [string] [Parameter(Mandatory=$true)] $subscriptionId
      )

$pscredential = New-Object -TypeName System.Management.Automation.PSCredential($applicationId, $secret)
Connect-AzAccount -ServicePrincipal -Credential $pscredential -Tenant $tenantId      
write-output "Logged into the account $applicationId"

Set-AzContext -Subscription $subscriptionId
write-output "Set to subscription $subscriptionId"