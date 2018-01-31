# This configuration template applies to Microsoft RRAS running on Windows Server 2012 R2.
# It configures an IPSec VPN tunnel connecting your on-premise VPN device.
# !!! Please notice that we have the following restrictions in our support for RRAS:
# !!! 1. Only IKEv2 is currently supported
# !!! 2. Only route-based VPN configuration is supported.
# !!! 3. Admin priveleges are required in order to run this script

#对端的公网IP地址
$RIP = "####"
#对端的地址池，：100表示路由的跳数，默认即可
$Rsubnet = '10.124.0.0/16:100'
#预设两端PSK的密钥
$Key = "Hanppy321"

Function Invoke-WindowsApi( 
    [string] $dllName,  
    [Type] $returnType,  
    [string] $methodName, 
    [Type[]] $parameterTypes, 
    [Object[]] $parameters 
    )
{
  ## Begin to build the dynamic assembly 
  $domain = [AppDomain]::CurrentDomain 
  $name = New-Object Reflection.AssemblyName 'PInvokeAssembly' 
  $assembly = $domain.DefineDynamicAssembly($name, 'Run') 
  $module = $assembly.DefineDynamicModule('PInvokeModule') 
  $type = $module.DefineType('PInvokeType', "Public,BeforeFieldInit") 

  $inputParameters = @() 

  for($counter = 1; $counter -le $parameterTypes.Length; $counter++) 
  { 
     $inputParameters += $parameters[$counter - 1] 
  } 

  $method = $type.DefineMethod($methodName, 'Public,HideBySig,Static,PinvokeImpl',$returnType, $parameterTypes) 

  ## Apply the P/Invoke constructor 
  $ctor = [Runtime.InteropServices.DllImportAttribute].GetConstructor([string]) 
  $attr = New-Object Reflection.Emit.CustomAttributeBuilder $ctor, $dllName 
  $method.SetCustomAttribute($attr) 

  ## Create the temporary type, and invoke the method. 
  $realType = $type.CreateType() 

  $ret = $realType.InvokeMember($methodName, 'Public,Static,InvokeMethod', $null, $null, $inputParameters) 

  return $ret
}

Function Set-PrivateProfileString( 
    $file, 
    $category, 
    $key, 
    $value) 
{
  ## Prepare the parameter types and parameter values for the Invoke-WindowsApi script 
  $parameterTypes = [string], [string], [string], [string] 
  $parameters = [string] $category, [string] $key, [string] $value, [string] $file 

  ## Invoke the API 
  [void] (Invoke-WindowsApi "kernel32.dll" ([UInt32]) "WritePrivateProfileString" $parameterTypes $parameters)
}

# Install RRAS role
Import-Module ServerManager
Install-WindowsFeature RemoteAccess -IncludeManagementTools
Add-WindowsFeature -name Routing -IncludeManagementTools

# !!! NOTE: A reboot of the machine might be required here after which the script can be executed again.

# Install S2S VPN
Import-Module RemoteAccess
if ((Get-RemoteAccess).VpnS2SStatus -ne "Installed")
{
  Install-RemoteAccess -VpnType VpnS2S
}

# Add and configure S2S VPN interface
Add-VpnS2SInterface -Protocol IKEv2 -AuthenticationMethod PSKOnly -NumberOfTries 3 -ResponderAuthenticationMethod PSKOnly -Name $RIP -Destination $RIP -IPv4Subnet @($Rsubnet) -SharedSecret $Key

Set-VpnServerIPsecConfiguration -EncryptionType MaximumEncryption
Set-VpnS2Sinterface -Name $RIP -InitiateConfigPayload $false -Force

# Set S2S VPN connection to be persistent by editing the router.pbk file (required admin priveleges)
Set-PrivateProfileString $env:windir\System32\ras\router.pbk $RIP "IdleDisconnectSeconds" "0"
Set-PrivateProfileString $env:windir\System32\ras\router.pbk $RIP "RedialOnLinkFailure" "1"

# Restart the RRAS service
Restart-Service RemoteAccess

# Dial-in to Azure gateway
Connect-VpnS2SInterface -Name $RIP