# Commit 16P-3 — Runtime Telemetry Completion Seal

## Purpose

16P-3 completes the telemetry bridge for embedding row-gather bytes.

Before this patch, row-gather executed and printed byte count to stderr, but `NativeVocabAllocationProbe.embedding_row_gather_bytes`, response `nativeEmbeddingRowGatherBytes`, and artifact `native_embedding_row_gather_bytes` stayed `null`.

## Changed files

- `crates/model_core/src/native_wgpu.rs`
- `crates/runtime/src/infer.rs`
- `infer_debug/probe_16P3_telemetry_completion_A.jsonl`

## Patch summary

### NativeWgpuModel

- Keeps the existing `last_embedding_row_gather_bytes: Mutex<Option<usize>>` as the SSOT.
- Adds a public getter:

```rust
pub fn last_embedding_row_gather_bytes(&self) -> Option<usize>
```

- Adds explicit store telemetry:

```text
[16P-3][telemetry] stored_embedding_row_gather_bytes=... source=NativeWgpuModel
```

### Runtime propagation

`run_standard_infer_impl()` now carries row-gather bytes through the inner `generate_ids()` closure as a fourth tuple item:

```rust
Result<(Vec<u32>, String, Option<GenerationTelemetry>, Option<usize>)>
```

The 16AC safe-generation branch reads `native_model.last_embedding_row_gather_bytes()` before returning, so the value survives the CPU/reference safe-generation handoff.

### Probe completion

After `NativeVocabAllocationProbe::new(...)`, runtime fills:

```rust
native_vocab_allocation_probe.embedding_row_gather_bytes = Some(bytes)
```

when a real value exists. It does not invent `0`; unknown remains `None`.

### Orchestrator

`infer_entry.rs` already copies from `result.native_vocab_allocation_probe.embedding_row_gather_bytes` into response and artifact, so it did not need structural changes.

## Expected value for current probe

For the known probe:

```text
prompt_len = 135
hidden = 2048
bytes = 135 * 2048 * 4 = 1105920
```

Expected response/artifact fields:

```json
"nativeEmbeddingRowGatherBytes": 1105920
```

```json
"native_embedding_row_gather_bytes": 1105920,
"native_vocab_allocation_probe": {
  "embedding_row_gather_bytes": 1105920
}
```

## Validation commands

```powershell
cargo build -p native_host --bin native_host --release
```

```powershell
$env:RUST_BACKTRACE = "1"
$Json = Get-Content ".\infer_debug\probe_16P3_telemetry_completion_A.jsonl" -Raw
$Json | & ".\target\release\native_host.exe" `
  1> ".\infer_debug\run_16P3_stdout.txt" `
  2> ".\infer_debug\run_16P3_stderr.txt"
$LASTEXITCODE
```

```powershell
Select-String ".\infer_debug\run_16P3_stderr.txt" `
  -Pattern "16P-3|native-embedding-row-gather|stored_embedding_row_gather_bytes|embedding_row_gather_bytes|panic|response"
```

```powershell
$responseLine = Get-Content ".\infer_debug\run_16P3_stdout.txt" |
  Where-Object { $_ -like '{"type":"response"*' } |
  Select-Object -Last 1
$response = $responseLine | ConvertFrom-Json
$response.ok
$response.payload.nativeEmbeddingRowGatherBytes
$response.payload.nativeVocabAllocationProbe.embedding_row_gather_bytes
$response.payload.resolvedBackend
$response.payload.text
```

```powershell
$outputPath = $response.payload.outputPath
$text = [System.IO.File]::ReadAllText(
  (Resolve-Path $outputPath),
  [System.Text.Encoding]::UTF8
)
$obj = $text | ConvertFrom-Json
$obj.output
$obj.native_embedding_row_gather_bytes
$obj.native_vocab_allocation_probe.embedding_row_gather_bytes
$obj.resolved_backend
```

## Acceptance criteria

- `nativeEmbeddingRowGatherBytes` is not null.
- `native_vocab_allocation_probe.embedding_row_gather_bytes` is not null.
- Response and artifact values match.
- `ok:true` remains intact.
- `resolved_backend` remains `cpu_reference_full+16AC_reference_safe_generation+packed_compact+lane0` for the safe-generation probe.
- Artifact parses through explicit UTF-8 `ConvertFrom-Json`.

## Build note

Cargo is not available in the bake container, so local `cargo build` remains the final SSOT.
