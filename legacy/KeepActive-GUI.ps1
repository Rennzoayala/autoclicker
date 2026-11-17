Add-Type -AssemblyName PresentationFramework

[xml]$xaml = @"
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        Title="Keep Active" Height="160" Width="260"
        ResizeMode="CanMinimize" WindowStartupLocation="CenterScreen">
    <StackPanel VerticalAlignment="Center" HorizontalAlignment="Center">
        <Button Name="ToggleBtn" Content="Turn On" Width="120" Height="40"
                FontSize="16" FontWeight="Bold" Foreground="Green"/>
        <TextBlock Name="StatusLabel" Text="Status: Off"
                   HorizontalAlignment="Center" Margin="0,10,0,0"
                   FontSize="12" Foreground="Gray"/>
    </StackPanel>
</Window>
"@

$reader = New-Object System.Xml.XmlNodeReader $xaml
$window = [Windows.Markup.XamlReader]::Load($reader)

$toggleBtn   = $window.FindName("ToggleBtn")
$statusLabel = $window.FindName("StatusLabel")

$wshell = New-Object -ComObject WScript.Shell

function Send-KeepAlive {
    $wshell.SendKeys("{SCROLLLOCK}")
    Start-Sleep -Milliseconds 100
    $wshell.SendKeys("{SCROLLLOCK}")
}

$timer = New-Object System.Windows.Threading.DispatcherTimer
$timer.Interval = [TimeSpan]::FromSeconds(60)
$timer.Add_Tick({ Send-KeepAlive })

$script:isRunning = $false

$toggleBtn.Add_Click({
    if ($script:isRunning) {
        $timer.Stop()
        $toggleBtn.Content    = "Turn On"
        $toggleBtn.Foreground = [System.Windows.Media.Brushes]::Green
        $statusLabel.Text     = "Status: Off"
        $script:isRunning     = $false
    } else {
        Send-KeepAlive
        $timer.Start()
        $toggleBtn.Content    = "Turn Off"
        $toggleBtn.Foreground = [System.Windows.Media.Brushes]::Red
        $statusLabel.Text     = "Status: Running"
        $script:isRunning     = $true
    }
})

$window.Add_Closing({
    $timer.Stop()
})

$window.ShowDialog() | Out-Null
