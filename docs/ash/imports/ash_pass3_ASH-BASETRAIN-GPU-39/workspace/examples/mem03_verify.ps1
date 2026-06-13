Get-Content .\workspace\mem03_cache_owner_audit_receipt.json -Raw |
  ConvertFrom-Json |
  ConvertTo-Json -Depth 40

Get-Content .\workspace\mem03_hard_purge_receipt.json -Raw |
  ConvertFrom-Json |
  ConvertTo-Json -Depth 40

Get-Content .\workspace\mem03_cache_owner_ledger.jsonl -Tail 10
