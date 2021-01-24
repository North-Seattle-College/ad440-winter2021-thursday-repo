param(
        [string] [Parameter(Mandatory=$true)] $tenantId,
        [string] [Parameter(Mandatory=$true)] $applicationId,
        [string] [Parameter(Mandatory=$true)] $secret,
        [string] [Parameter(Mandatory=$true)] $subscriptionId
      )

# If the Subscription Id is NOT null, the user is logged in
$loggedIn = ((Get-AzContext).Tenant.Id -eq $tenantId)

if ($loggedIn) {
  Write-Host("Already logged in")

  # Check we're on the correct Subscription
  $correctSub = (Get-AzContext).Subscription.Id -eq $subscriptionId
  if ($correctSub) {
    Write-Host("Correct subscription")
  } else {
    Write-Host("Wrong subscription. Logging out...")
    Disconnect-AzAccount
    $loggedIn = False
  }

} 
if (!$loggedIn) {
  # Log In
  Write-Host("Logging in...")
  [securestring]$secureSecret = ConvertTo-SecureString $secret -AsPlainText -Force      
  [pscredential]$credObject = New-Object System.Management.Automation.PSCredential ($applicationId, $secureSecret)
  Connect-AzAccount -ServicePrincipal -Credential $credObject -Tenant $tenantId      
  Write-Host "Logged into the account $applicationId"

  # Set Subscription
  Set-AzContext -Subscription $subscriptionId
  Write-Host "Set to subscription $subscriptionId"
} 
