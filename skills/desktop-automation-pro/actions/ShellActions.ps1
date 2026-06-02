# ShellActions.ps1 - CMD/PowerShell execution

Function Invoke-ShellCommand {
    Param([string]$Command, [string[]]$ArgumentList)
    Write-Host "Executing Shell Command: $Command $ArgumentList" -ForegroundColor DarkCyan
    Start-Process -FilePath $Command -ArgumentList $ArgumentList -Wait -NoNewWindow
}

Function Open-Application {
    Param([string]$Path)
    Write-Host "Opening application: $Path"
    Start-Process $Path
}
