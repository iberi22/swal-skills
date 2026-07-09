# WindowActions.ps1 - Move, resize, focus, close

Function Set-WindowFocus {
    Param($Element)
    if ($Element) {
        Write-Host "Focusing window: $($Element.Current.Name)"
        $Element.SetFocus()
    }
}

Function Close-Window {
    Param($Element)
    # logic to close window via pattern or Alt+F4
}

Function Resize-Window {
    Param($Element, $Width, $Height)
    # logic to resize
}
