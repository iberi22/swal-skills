# UIAutomation.ps1 - Windows Accessibility API integration

# Import required .NET assemblies
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

Function Get-DesktopElement {
    [CmdletBinding()]
    Param(
        [string]$Name,
        [string]$AutomationId,
        [string]$ClassName
    )

    Write-Host "Searching for element: Name=$Name, ID=$AutomationId" -ForegroundColor DarkGray

    $root = [System.Windows.Automation.AutomationElement]::RootElement
    $condition = [System.Windows.Automation.Condition]::TrueCondition

    if ($Name) {
        $condition = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::NameProperty, $Name)
    } elseif ($AutomationId) {
        $condition = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::AutomationIdProperty, $AutomationId)
    }

    $element = $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $condition)
    return $element
}

Function Get-ElementProperties {
    Param($Element)
    if ($Element) {
        return @{
            Name = $Element.Current.Name
            ID = $Element.Current.AutomationId
            Class = $Element.Current.ClassName
            Rect = $Element.Current.BoundingRectangle
        }
    }
}
