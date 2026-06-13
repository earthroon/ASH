Get-Content .\workspace\lora_rt02_scale025_apply_receipt.json -Raw |
  ConvertFrom-Json |
  ConvertTo-Json -Depth 30

Get-Content .\workspace\lora_rt02_scale025_delta_trace.json -Raw |
  ConvertFrom-Json |
  ConvertTo-Json -Depth 30

Get-ChildItem .\workspace\artifacts -Recurse -File -Filter "*lora_rt02_scale025_greeting_01*output.json" |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1 |
  ForEach-Object {
    $Raw = [System.IO.File]::ReadAllText($_.FullName, [System.Text.UTF8Encoding]::new($false))
    $Json = $Raw | ConvertFrom-Json
    "output = $($Json.outputTextPreview)"
    "finish = $($Json.generation_finish_reason)"
    "adapter_delta_applied = $($Json.domainAdapterDeltaApplied)"
    "adapter_scale = $($Json.domainAdapterScale)"
    "apply_status = $($Json.domainAdapterApplyReceipt.status)"
    $Json.domainAdapterDeltaStats | ConvertTo-Json -Depth 20
  }
