# KeyboardActions.ps1 - Type, hotkeys

Add-Type -AssemblyName System.Windows.Forms

Function Invoke-KeyboardType {
    Param([string]$Text)
    Write-Host "Typing: $Text" -ForegroundColor DarkGreen
    [System.Windows.Forms.SendKeys]::SendWait($Text)
}

Function Invoke-Hotkey {
    Param([string]$Keys)
    Write-Host "Pressing hotkey: $Keys"
    [System.Windows.Forms.SendKeys]::SendWait($Keys)
}
