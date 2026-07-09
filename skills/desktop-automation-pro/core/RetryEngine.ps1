# RetryEngine.ps1 - Intelligent retry & fallback logic

Function Invoke-WithRetry {
    [CmdletBinding()]
    Param(
        [ScriptBlock]$Action,
        [int]$MaxRetries = 3,
        [int]$DelaySeconds = 2
    )

    $attempt = 0
    $success = $false

    while (-not $success -and $attempt -lt $MaxRetries) {
        try {
            $attempt++
            Write-Host "Attempt $attempt of $MaxRetries..." -ForegroundColor Gray
            &$Action
            $success = $true
        } catch {
            Write-Warning "Attempt $attempt failed: $($_.Exception.Message)"
            if ($attempt -lt $MaxRetries) {
                Start-Sleep -Seconds $DelaySeconds
            }
        }
    }

    if (-not $success) {
        throw "Action failed after $MaxRetries attempts."
    }
}

Function Invoke-AIFallback {
    Param($Context, $Goal)
    Write-Host "Deterministic methods failed. Triggering AI Fallback..." -ForegroundColor Magenta
    # Logic to send screenshot + context to LLM
}
