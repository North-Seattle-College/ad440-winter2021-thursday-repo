param(
        [string] [Parameter(Mandatory=$true)] $tenantId,
        [string] [Parameter(Mandatory=$true)] $applicationId,
        [string] [Parameter(Mandatory=$true)] $secret,
        [string] [Parameter(Mandatory=$true)] $subscriptionId
      )

# If the Subscription Id is NOT null, the user is logged in
$loggedIn = ((Get-AzContext).Tenant.Id -eq $tenantId)

if ($loggedIn) {
  Write-Output("Already logged in")

  # Check we're on the correct Subscription
  $correctSub = (Get-AzContext).Subscription.Id -eq $subscriptionId
  if ($correctSub) {
    Write-Output("Correct subscription")
  } else {
    Write-Output("Wrong subscription")
    Disconnect-AzAccount
    $loggedIn = False
  }

} 
if (!$loggedIn) {
  # Log In
  Write-Output("Logging in...")
  [securestring]$secureSecret = ConvertTo-SecureString $secret -AsPlainText -Force      
  [pscredential]$credObject = New-Object System.Management.Automation.PSCredential ($applicationId, $secureSecret)
  Connect-AzAccount -ServicePrincipal -Credential $credObject -Tenant $tenantId      
  Write-Output "Logged into the account $applicationId"

  # Set Subscription
  Set-AzContext -Subscription $subscriptionId
  Write-Output "Set to subscription $subscriptionId"
} 
