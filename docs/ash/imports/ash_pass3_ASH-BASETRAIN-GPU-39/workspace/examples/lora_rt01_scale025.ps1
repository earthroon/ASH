$PromptText = (
  [string][char]0xC9E7 + [string][char]0xC740 + " " +
  [string][char]0xC778 + [string][char]0xC0AC + [string][char]0xB9D0 + [string][char]0xC744 + " " +
  [string][char]0xC790 + [string][char]0xC5F0 + [string][char]0xC2A4 + [string][char]0xB7FD + [string][char]0xAC8C + " " +
  [string][char]0xC368 + [string][char]0xC918 + "."
)

$AdapterPath = ".\workspace\domain_adapters\tinyllama_1p1b_v5_guarded_dump_full_gpu_cap192_shared_hidden_head_lora.pilot64.safetensors"
$AdapterManifestPath = ".\workspace\domain_adapters\tinyllama_1p1b_v5_guarded_dump_full_gpu_cap192_shared_hidden_head_lora.pilot64.manifest.json"

$Req = @{
  id = "lora_rt01_scale025_greeting_01"
  cmd = "run.start"
  payload = @{
    kind = "infer"
    input = $PromptText
    task = "freeform"
    modelSpecPath = ".\specs\model_spec_v5_48259.toml"
    tokenizerManifestPath = ".\artifacts\tokenizer_manifest_v5_final.json"
    checkpointPaths = @(".\tokenizer_v5\artifacts\full_model_vocab_v5_resized.safetensors")
    maxNewTokens = 48
    minNewTokens = 8
    seed = 42
    temperature = 0.32
    topP = 0.90
    topK = 40
    minP = 0.05
    repetitionPenalty = 1.10
    domainAdapterEnabled = $true
    domainAdapterId = "tinyllama_1p1b_v5_guarded_dump_full_gpu_cap192_shared_hidden_head_lora_pilot64"
    domainAdapterPath = $AdapterPath
    domainAdapterManifestPath = $AdapterManifestPath
    domainAdapterScale = 0.25
    domainAdapterAttachReceiptPath = ".\workspace\lora_rt01_scale025_attach_receipt.json"
    eosRestoreEnabled = $true
    memoryBudgetEnabled = $true
    memoryBudgetReceiptPath = ".\workspace\lora_rt01_scale025_mem_receipt.json"
  }
} | ConvertTo-Json -Depth 30 -Compress

$Req | .\target\debug\orchestrator_local.exe 2>&1 |
  Tee-Object .\workspace\lora_rt01_scale025_greeting_01.log
