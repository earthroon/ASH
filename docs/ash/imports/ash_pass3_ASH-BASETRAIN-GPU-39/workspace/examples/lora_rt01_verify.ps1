Get-Content .\workspace\lora_rt01_scale025_attach_receipt.json -Raw |
  ConvertFrom-Json |
  ConvertTo-Json -Depth 30

Get-ChildItem .\workspace\artifacts -Recurse -File -Filter "*lora_rt01_scale025_greeting_01*output.json" |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1 |
  ForEach-Object {
    $Raw = [System.IO.File]::ReadAllText($_.FullName, [System.Text.UTF8Encoding]::new($false))
    $Json = $Raw | ConvertFrom-Json

    "output = $($Json.outputTextPreview)"
    "finish = $($Json.generation_finish_reason)"
    "adapter = $($Json.domainAdapterId)"
    "scale = $($Json.domainAdapterScale)"
    "attach_status = $($Json.domainAdapterAttachReceipt.status)"
    $Json.domainAdapterDeltaStats | ConvertTo-Json -Depth 20
  }
