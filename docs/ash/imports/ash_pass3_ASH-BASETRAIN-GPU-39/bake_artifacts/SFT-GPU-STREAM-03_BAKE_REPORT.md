# SFT-GPU-STREAM-03 Bake Report

## Commit

SFT-GPU-STREAM-03 — Runner Stream Transport Intake / JSONL Pipe Ledger Bridge

## Patched Files

- `crates/ash_core/src/sft_gpu_stream_transport_intake.rs`
- `crates/ash_core/tests/sft_gpu_stream_03_transport_intake.rs`
- `crates/ash_core/src/lib.rs`
- `acceptance_reports/SFT-GPU-STREAM-03_runner_stream_transport_intake.md`
- `bake_artifacts/SFT-GPU-STREAM-03_BAKE_REPORT.md`
- `bake_artifacts/SFT-GPU-STREAM-03_STATIC_VALIDATION.txt`

## Opened

- transport intake receipt
- raw JSONL line evidence intake
- canonical parsed step event bridge
- canonical step ledger digest
- partial running transport resume marker
- STREAM-01 bridge readiness

## Closed

- runner process spawn in ash_core
- SFT training execution in ash_core
- gradient write in ash_core
- optimizer step in ash_core
- artifact write in ash_core
- slot ready
- synapse binding
- runtime attach
- promotion apply
- current pointer update

## Tests Added

- `sft_gpu_stream_03_accepts_stdout_jsonl_transport_intake`
- `sft_gpu_stream_03_rejects_malformed_json_line`
- `sft_gpu_stream_03_rejects_no_parsable_events`
- `sft_gpu_stream_03_rejects_runner_execution_mismatch`
- `sft_gpu_stream_03_rejects_step_sequence_gap`
- `sft_gpu_stream_03_rejects_cpu_fallback_event`
- `sft_gpu_stream_03_rejects_runner_process_spawn_in_core_flag`
- `sft_gpu_stream_03_accepts_partial_running_transport_with_resume_marker`

## Validation Note

The current execution environment has no `cargo`, `rustc`, or `rustfmt`, so runtime Rust compilation was not executed here. Static file, module export, and delimiter-balance validation were performed.
