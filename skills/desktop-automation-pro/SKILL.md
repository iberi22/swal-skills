---
name: desktop-automation-pro
description: "Desktop Automation Pro v2.0 - AI Computer Use for Windows. Powerful automation leveraging Windows UI Automation API, workflow state persistence, and smart AI fallback."
license: MIT
metadata:
  author: swal
  version: "2.0.0"
  gitcore_protocol: "3.6.0"
  tags: [windows, automation, ui-automation, mcp, powershell]
  agents: [openclaw, codex, claude, qwen, opencode]
---

# Desktop Automation Pro v2.0

> **Powerful AI Computer Use for Windows**

Desktop Automation Pro v2.0 is a professional-grade automation skill designed for AI agents to interact with the Windows desktop natively. Unlike coordinate-based or OCR-only solutions, it leverages the **Windows UI Automation (UIA) API** to interact with elements directly through the Accessibility Tree.

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| **UI Automation** | Direct interaction with the Windows Accessibility Tree (no OCR needed). |
| **Workflow Memory** | Persists state between steps using JSON for complex multi-step tasks. |
| **Retry Engine** | Smart logic that tries deterministic methods first before falling back to AI. |
| **Screenshot Analysis** | Visual fallback using OpenAI/Gemini for complex UI scenarios. |
| **MCP Integration** | Bridge to use as an MCP tool for Codex, Claude Desktop, and others. |
| **Safety Mode** | Confirmation prompts, dry-run mode, and undo capabilities. |

## 🏗️ Architecture

```text
desktop-automation-pro/
├── core/
│   ├── DesktopEngine.ps1        # Main orchestration engine (Imports core deps)
│   ├── UIAutomation.ps1         # UIA API & Accessibility Tree integration
│   ├── WorkflowState.ps1        # State persistence & JSON management
│   ├── RetryEngine.ps1          # Intelligent retry & fallback logic
│   └── ScreenshotAnalyzer.ps1   # Visual analysis fallback
├── actions/
│   ├── MouseActions.ps1         # Click, drag, scroll (Win32 P/Invoke)
│   ├── KeyboardActions.ps1      # Type, hotkeys (SendKeys)
│   ├── WindowActions.ps1        # Move, resize, focus, close
│   └── ShellActions.ps1         # CMD/PowerShell execution (Secure Start-Process)
├── tools/
│   ├── ElementFinder.ps1        # Search for UI elements by name/ID/class
│   ├── WorkflowRecorder.ps1     # Record actions to JSON
│   ├── TaskBuilder.ps1          # Construct complex automation tasks
│   └── MCPBridge.ps1            # CLI bridge for MCP integration
└── examples/
    └── BasicSearch.ps1          # Example: Open browser and search
```

## 🚀 Quick Start

### Requirements
- Windows 10/11
- PowerShell 7.x (recommended) or 5.1
- Administrator privileges (for certain UI interactions)

### Basic Usage

```powershell
# Import the engine
Import-Module ./core/DesktopEngine.ps1

# Start session
Start-DesktopSession -SessionName "MySession"

# Find an element and click it
$element = Get-DesktopElement -Name "Start"
Invoke-DesktopAction -Action Click -Target $element

# Type into a focused field
Invoke-DesktopAction -Action Type -Value "Hello Windows Automation!"

# Close session
Stop-DesktopSession
```

## 🛠️ Modules Detail

### Core Engine (`DesktopEngine.ps1`)
The main entry point that coordinates actions and manages the lifecycle of an automation session. It automatically handles module imports.

### UI Automation (`UIAutomation.ps1`)
Wraps the `System.Windows.Automation` namespace. It allows finding elements by:
- `AutomationId`
- `Name`
- `ClassName`

### Workflow State (`WorkflowState.ps1`)
Maintains a `state.json` file during execution. This allows the agent to "remember" what it has done and handle interruptions.

### Retry Engine (`RetryEngine.ps1`)
Implements an exponential backoff and alternate strategy pattern.

### Shell Actions (`ShellActions.ps1`)
CMD/PowerShell execution. **⚠️ WARNING:** Use with caution. Always validate input. Uses `Start-Process` for security.

## 🛡️ Safety & Reliability

- **Dry Run**: Use `-DryRun` on any action to see what would happen without executing.
- **Confirmations**: Set `$ConfirmPreference = 'High'` to require manual approval.

## 🤖 MCP Integration

To use as a CLI tool within an MCP configuration:

```json
{
  "mcpServers": {
    "desktop-automation": {
      "command": "pwsh",
      "args": ["-File", "path/to/tools/MCPBridge.ps1", "-Action", "Click", "-TargetName", "Start"],
      "env": {
        "SAFETY_MODE": "enabled"
      }
    }
  }
}
```

---
*Last updated: 2026-04-17*
*Part of the SWAL Skills ecosystem.*
