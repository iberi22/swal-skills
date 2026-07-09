# DesktopEngine.ps1 - Main orchestration engine for Desktop Automation Pro v2.0

$CoreRoot = $PSScriptRoot
Import-Module (Join-Path $CoreRoot "UIAutomation.ps1") -Force
Import-Module (Join-Path $CoreRoot "WorkflowState.ps1") -Force
Import-Module (Join-Path $CoreRoot "RetryEngine.ps1") -Force
Import-Module (Join-Path $CoreRoot "ScreenshotAnalyzer.ps1") -Force

$ActionRoot = Join-Path $CoreRoot ".." "actions"
Import-Module (Join-Path $ActionRoot "MouseActions.ps1") -Force
Import-Module (Join-Path $ActionRoot "KeyboardActions.ps1") -Force

Function Start-DesktopSession {
    [CmdletBinding()]
    Param(
        [string]$SessionName = "DefaultSession"
    )
    Write-Host "Starting Desktop Automation Session: $SessionName" -ForegroundColor Cyan
    # Initialize state
    Initialize-WorkflowState -SessionName $SessionName
}

Function Stop-DesktopSession {
    Write-Host "Stopping Desktop Automation Session." -ForegroundColor Cyan
    Save-WorkflowState
}

Function Invoke-DesktopAction {
    [CmdletBinding()]
    Param(
        [Parameter(Mandatory=$true)]
        [ValidateSet("Click", "Type", "RightClick", "DoubleClick", "Scroll")]
        [string]$Action,

        [Parameter(Mandatory=$true)]
        $Target,

        [string]$Value,

        [switch]$DryRun
    )

    if ($DryRun) {
        Write-Host "[DRY RUN] Would perform $Action on $Target" -ForegroundColor Yellow
        return
    }

    Write-Host "Performing $Action on $Target" -ForegroundColor Green

    # Logic to dispatch to MouseActions or KeyboardActions
    try {
        switch ($Action) {
            "Click"       { Invoke-MouseClick -Element $Target }
            "Type"        { Invoke-KeyboardType -Text $Value }
            "RightClick"  { Invoke-MouseRightClick -Element $Target }
            "DoubleClick" {
                Invoke-MouseClick -Element $Target
                Start-Sleep -Milliseconds 100
                Invoke-MouseClick -Element $Target
            }
            "Scroll"      { Scroll-Desktop -Amount ([int]$Value) }
        }
        Add-WorkflowStep -Action $Action -Target $Target -Status "Success"
    }
    catch {
        Write-Error "Action $Action failed: $_"
        Add-WorkflowStep -Action $Action -Target $Target -Status "Failed: $_"
        throw
    }
}
