# BasicSearch.ps1 - Example: Open browser and search

# Import Core (now it imports its own dependencies)
$CurrentDir = $PSScriptRoot
Import-Module (Join-Path $CurrentDir ".." "core" "DesktopEngine.ps1")
Import-Module (Join-Path $CurrentDir ".." "actions" "ShellActions.ps1")

Start-DesktopSession -SessionName "GoogleSearch"

# 1. Open Edge
Open-Application -Path "msedge.exe"
Start-Sleep -Seconds 2

# 2. Find Search Bar (Simplified)
$searchBar = Get-DesktopElement -Name "Search or enter web address"
if ($searchBar) {
    Invoke-DesktopAction -Action Type -Target $searchBar -Value "https://www.google.com{ENTER}"
}

Stop-DesktopSession
