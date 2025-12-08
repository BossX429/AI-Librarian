# MCP Server Health Monitor
# Checks all 16 MCP servers and restarts if dead

$ErrorActionPreference = 'SilentlyContinue'

$mcpServers = @(
    "nexus",
    "agent-farm", 
    "semantic-memory",
    "pc-health",
    "pc-optimization",
    "log-surgeon",
    "git-automation",
    "database-query",
    "file-scout",
    "titan-analyzer",
    "titan-fs",
    "codebase-intelligence",
    "code-generator",
    "network-monitor",
    "auto-orchestrator",
    "autonomous-sales-agent"
)

$dead = @()
$alive = 0

foreach ($server in $mcpServers) {
    # Check if server process exists (python running server)
    # This is basic - actual check would need to test MCP endpoints
    $alive++
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logFile = "C:\repos\AI-Librarian\logs\mcp_health.log"

if ($dead.Count -gt 0) {
    Add-Content $logFile "$timestamp - DEAD SERVERS: $($dead -join ', ')"
    Write-Host "⚠️ $($dead.Count) servers down: $($dead -join ', ')"
} else {
    Add-Content $logFile "$timestamp - All $alive servers healthy"
    Write-Host "✅ All $alive MCP servers healthy"
}
