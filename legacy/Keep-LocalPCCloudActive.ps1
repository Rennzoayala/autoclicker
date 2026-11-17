# Keep-LocalPCCloudActive.ps1
# Runs on your local (main) PC.
# Sends a harmless keypress (Scroll Lock) every 3 minutes to keep your PC Cloud remote session and Teams active.

$wshell = New-Object -ComObject WScript.Shell
$intervalMinutes = 1

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " Keep PC Cloud & Teams Active (Local Machine Script)" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "Running locally... Sending {SCROLLLOCK} every $intervalMinutes minutes." -ForegroundColor Green
Write-Host "Press Ctrl+C in this window to stop." -ForegroundColor Yellow
Write-Host ""

while ($true) {
    # Send Scroll Lock twice so toggling state doesn't remain changed
    $wshell.SendKeys("{SCROLLLOCK}")
    Start-Sleep -Milliseconds 100
    $wshell.SendKeys("{SCROLLLOCK}")
    
    $currentTime = Get-Date -Format "HH:mm:ss"
    Write-Host "[$currentTime] Sent keep-alive signal." -ForegroundColor Gray
    
    Start-Sleep -Seconds ($intervalMinutes * 60)
}
