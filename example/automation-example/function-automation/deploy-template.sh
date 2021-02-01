#!/bin/bash

# Parameter for tenantId
# Parameter for SubscriptionId
# Parameter for Service Principal App Id
# Parameter for Service Principal Secret

TenantId=$1
echo $TenantId
SubscriptionId=$2
echo $SubscriptionId
SPAppId=$3
echo $SPAppId
ServicePrincipaSecret=$4
echo $ServicePrincipaSecret
ResourceGroupName=$5

az login -u $SPAppId -p $ServicePrincipaSecret -t $TenantId
az account set -s $SubscriptionId

# az group create ---- for creation of the RG
# az deployment create ---- for doing the actual deployment and passing the template.json and parameters.json