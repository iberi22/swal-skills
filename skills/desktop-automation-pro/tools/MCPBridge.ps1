# MCPBridge.ps1 - Bridge between MCP Server and PowerShell Desktop Engine

Param(
    [string]$Action,
    [string]$TargetName,
    [string]$Value
)

# Import necessary modules
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Import-Module "$ScriptDir/../core/DesktopEngine.ps1"
Import-Module "$ScriptDir/../core/UIAutomation.ps1"
Import-Module "$ScriptDir/../actions/MouseActions.ps1"
Import-Module "$ScriptDir/../actions/KeyboardActions.ps1"

# Main loop or one-shot execution logic for MCP
# In a real MCP scenario, this would handle JSON-RPC from stdin/stdout

function Invoke-MCPAction {
    param($action, $targetName, $value)

    Start-DesktopSession -SessionName "MCP-Session"

    try {
        $element = Get-DesktopElement -Name $targetName
        if (-not $element) {
            return @{ error = "Element not found: $targetName" } | ConvertTo-Json
        }

        Invoke-DesktopAction -Action $action -Target $element -Value $value
        return @{ success = $true; action = $action; target = $targetName } | ConvertTo-Json
    }
    catch {
        return @{ error = $_.Exception.Message } | ConvertTo-Json
    }
    finally {
        Stop-DesktopSession
    }
}

if ($Action) {
    Invoke-MCPAction -action $Action -targetName $TargetName -value $Value
}
