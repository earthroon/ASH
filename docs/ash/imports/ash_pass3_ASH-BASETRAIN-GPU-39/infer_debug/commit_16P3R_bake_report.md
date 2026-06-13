# Commit 16P-3R — Row Gather Telemetry Fallback Calculation Seal

## SSOT

16P-3 1차에서 `NativeWgpuModel.last_embedding_row_gather_bytes()` getter는 `None`을 반환했다. 그러나 request/probe 상태는 `effective_embedding_mode=row_gather`, `prompt_len=135`, `hidden_size=2048`로 확정 가능하므로, response/artifact telemetry는 검증 가능한 fallback 계산값을 봉인해야 한다.

## Patch summary

- `NativeVocabAllocationProbe`에 `embedding_row_gather_bytes_source: Option<String>` 추가.
- `native_embedding_row_gather_bytes`가 `Some(bytes)`이면 기존 getter 값을 우선 사용.
- getter가 `None`이고 `effective_embedding_mode == "row_gather"`이면 `prompt_len * hidden_size * sizeof::<f32>()`로 계산.
- 계산 fallback 사용 시 source를 `computed_from_prompt_len_hidden_size`로 남김.
- artifact에는 `native_embedding_row_gather_bytes_source`를 추가.
- response에는 `nativeEmbeddingRowGatherBytesSource`를 추가.

## Expected value for probe_16P3R_telemetry_completion_A

```text
prompt_len = 135
hidden = 2048
sizeof_f32 = 4
embedding_row_gather_bytes = 135 * 2048 * 4 = 1105920
source = computed_from_prompt_len_hidden_size
```

## Acceptance

- stderr contains `[16P-3R][telemetry] embedding_row_gather_bytes=1105920 source=computed_from_prompt_len_hidden_size ...` when getter is None.
- response `nativeEmbeddingRowGatherBytes == 1105920`.
- response `nativeEmbeddingRowGatherBytesSource == "computed_from_prompt_len_hidden_size"`.
- artifact `native_embedding_row_gather_bytes == 1105920`.
- artifact `native_embedding_row_gather_bytes_source == "computed_from_prompt_len_hidden_size"`.
- `native_vocab_allocation_probe.embedding_row_gather_bytes == 1105920`.
- `native_vocab_allocation_probe.embedding_row_gather_bytes_source == "computed_from_prompt_len_hidden_size"`.
- `ok:true` and `cpu_reference_full+16AC_reference_safe_generation+packed_compact+lane0` remain unchanged.

## Build note

Cargo is not available in the bake container, so local `cargo build -p native_host --bin native_host --release` remains the final SSOT.
