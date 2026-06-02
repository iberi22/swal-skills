# WorkflowState.ps1 - State persistence & JSON management

$global:DesktopWorkflowState = @{
    SessionId = [guid]::NewGuid().ToString()
    StartTime = Get-Date
    Steps = @()
    CurrentContext = "Desktop"
}

Function Initialize-WorkflowState {
    Param($SessionName)
    $global:DesktopWorkflowState.SessionName = $SessionName
    Write-Host "Workflow State Initialized" -ForegroundColor Gray
}

Function Add-WorkflowStep {
    Param($Action, $Target, $Status)

    $TargetInfo = "Unknown"
    if ($Target -is [System.Windows.Automation.AutomationElement]) {
        $TargetInfo = @{
            Name = $Target.Current.Name
            AutomationId = $Target.Current.AutomationId
            ClassName = $Target.Current.ClassName
        }
    } else {
        $TargetInfo = $Target.ToString()
    }

    $Step = @{
        Timestamp = Get-Date
        Action = $Action
        Target = $TargetInfo
        Status = $Status
    }
    $global:DesktopWorkflowState.Steps += $Step
}

Function Save-WorkflowState {
    $Path = "workflow_state.json"
    $global:DesktopWorkflowState | ConvertTo-Json -Depth 10 | Out-File $Path
    Write-Host "State saved to $Path" -ForegroundColor Gray
}

Function Get-WorkflowState {
    return $global:DesktopWorkflowState
}
