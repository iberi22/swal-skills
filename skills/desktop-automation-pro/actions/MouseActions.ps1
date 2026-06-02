# MouseActions.ps1 - Click, drag, scroll with Win32 P/Invoke

# Add P/Invoke for mouse control
$signature = @"
[DllImport("user32.dll")]
public static extern void mouse_event(uint dwFlags, int dx, int dy, uint dwData, uint dwExtraInfo);
[DllImport("user32.dll")]
public static extern bool SetCursorPos(int x, int y);
"@
$User32 = Add-Type -MemberDefinition $signature -Name "User32" -Namespace "Win32" -PassThru

# Mouse event constants
$MOUSEEVENTF_LEFTDOWN = 0x0002
$MOUSEEVENTF_LEFTUP   = 0x0004
$MOUSEEVENTF_RIGHTDOWN = 0x0008
$MOUSEEVENTF_RIGHTUP   = 0x0010

Function Invoke-MouseClick {
    Param($Element)
    if ($Element) {
        $rect = $Element.Current.BoundingRectangle
        $x = [int]($rect.Left + ($rect.Width / 2))
        $y = [int]($rect.Top + ($rect.Height / 2))

        Write-Host "Clicking at ($x, $y)" -ForegroundColor DarkGreen

        # Move cursor
        [Win32.User32]::SetCursorPos($x, $y)
        Start-Sleep -Milliseconds 100

        # Click
        [Win32.User32]::mouse_event($MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        [Win32.User32]::mouse_event($MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    }
}

Function Invoke-MouseRightClick {
    Param($Element)
    if ($Element) {
        $rect = $Element.Current.BoundingRectangle
        $x = [int]($rect.Left + ($rect.Width / 2))
        $y = [int]($rect.Top + ($rect.Height / 2))

        Write-Host "Right-clicking at ($x, $y)" -ForegroundColor DarkGreen

        [Win32.User32]::SetCursorPos($x, $y)
        Start-Sleep -Milliseconds 100

        [Win32.User32]::mouse_event($MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        [Win32.User32]::mouse_event($MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    }
}

Function Scroll-Desktop {
    Param([int]$Amount)
    Write-Host "Scrolling by $Amount"
    $MOUSEEVENTF_WHEEL = 0x0800
    [Win32.User32]::mouse_event($MOUSEEVENTF_WHEEL, 0, 0, $Amount, 0)
}
