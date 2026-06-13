$Rows = @()

1..5 | ForEach-Object {
  $i = $_

  $Before = Get-Process orchestrator_local -ErrorAction SilentlyContinue |
    Select-Object -First 1 Id, WorkingSet64, PrivateMemorySize64, VirtualMemorySize64, Handles

  .\workspace\examples\mem03_lora_rt02_scale025.ps1 | Out-Null

  Start-Sleep -Seconds 2

  $After = Get-Process orchestrator_local -ErrorAction SilentlyContinue |
    Select-Object -First 1 Id, WorkingSet64, PrivateMemorySize64, VirtualMemorySize64, Handles

  $Rows += [PSCustomObject]@{
    Run = $i
    BeforeWS = $Before.WorkingSet64
    AfterWS = $After.WorkingSet64
    BeforePrivate = $Before.PrivateMemorySize64
    AfterPrivate = $After.PrivateMemorySize64
    BeforeVirtual = $Before.VirtualMemorySize64
    AfterVirtual = $After.VirtualMemorySize64
    AfterHandles = $After.Handles
  }
}

$Rows | Format-Table -AutoSize
