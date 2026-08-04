10. borrow five resident views
11. validate WGPU26 shader ABI
12. run staged GPU path
13. run CPU-f64 oracle
14. compare every stage element
15. execute positive proof matrix
16. execute negative-control matrix
17. seal TensorCube live handoff
18. write ordered artifacts atomically
19. read every artifact back and verify SHA-256
20. write local manifest last
21. print exactly one PASS token
```

## 22.3 No panic contract

Expected validation failures must be returned as typed `Result` errors.

The gate should use WGPU error scopes or pre-validation so malformed negative-control shaders do not terminate the process through an uncaptured panic.

Unexpected panic count must be zero.

---

# 23. CLI contract

Required keys:

```text
--repo-root
--aw00-runtime-artifact
--prior-aw01-local-manifest
--fixture-output-dir
--runtime-output-dir
--executor-mode
--device-epoch
--queue-epoch
--atlas-residency-generation
--max-host-staging-bytes
--max-slot-bytes
--upload-verification-mode
--numerical-profile
```

Canonical values:

```text
executor-mode               CanonicalGpuOracle
upload-verification-mode    FullBoundedSliceReadback
numerical-profile           CanonicalF64Parity
```

Response-file format:

```text
--key
value
```

`--key=value` is forbidden for this parser.

Unknown keys fail closed.

Duplicate keys fail closed.

Missing keys fail closed.

---

# 24. Rust-generated artifacts

Output root:

```text
workspace/runtime/basetrain/atlas_wave/02_r5/
```

Required artifacts:

```text
01_parent_transaction_receipt.json
02_prior_aw01_lineage_receipt.json
03_same_process_runtime_receipt.json
04_live_aw01_residency_receipt.json
05_resident_tensor_view_receipt.json
06_wgsl_repository_inventory_receipt.json
07_wgsl_canonical_abi_receipt.json
08_parameter_binding_receipt.json
09_position_rope_authority_receipt.json
10_embedding_stage_receipt.json
11_rmsnorm_stage_receipt.json
12_qkv_stage_receipt.json
13_rope_stage_receipt.json
14_attention_executor_receipt.json
15_embedding_parity_receipt.json
16_rmsnorm_parity_receipt.json
17_qkv_parity_receipt.json
18_rope_parity_receipt.json
19_context_parity_receipt.json
20_padding_exact_zero_receipt.json
21_positive_proof_ledger.json
22_negative_control_ledger.json
23_tensorcube_live_handoff_receipt.json
24_mutation_firewall_receipt.json
25_no_receipt_overclaim_receipt.json
26_static_source_closure_receipt.json
27_artifact_write_receipt.json
ash_basetrain_atlas_wave_02_r5_local_manifest.json
```

No canonical runtime artifact is included pre-generated in the source ZIP.

## 24.1 Artifact manifest fields

```text
patch ID
build revision
parent AW-00 digest
prior AW-01 manifest digest
same-process AW-01 receipt digest
runtime holder ID
device epoch
queue epoch
source weight generation
atlas residency generation
executor kind
stage receipt digests
parity receipt digests
positive proof count
negative control count
handoff receipt digest
artifact entry list
artifact manifest digest
PASS token
pass
```

The manifest is written last.

---

# 25. Static source closure

The gate and repair script must verify:

```text
R5 model-core contract module exported
R5 live residency view module exported
R5 staged backend module exported
five canonical WGSL files present
R5 CPU-f64 oracle present
R5 proof ledger present
R5 physical gate binary registered
R5 CLI registry present
R5 response file present
AW-01 ring includes STORAGE usage
AW-02 R5 backend contains no host weight slice fields
AW-02 R5 backend contains no weight queue writes
canonical WGSL contains no ptr<storage> parameter
oracle mode source contains no Headwise authority claim
all required zero counters present
PASS token present exactly once
```

Static source closure does not replace physical execution.

---

# 26. Implementation surface

## 26.1 New model-core files

```text
crates/model_core/src/base_train_atlas_wave_02_r5_contract.rs
crates/model_core/src/base_train_atlas_wave_02_r5_proof_ledger.rs
```

## 26.2 Modified AW-01 files

```text
crates/burn_webgpu_backend/src/base_train_atlas_wave_01_residency.rs
crates/base_train/src/base_train_atlas_wave_01_residency_coordinator.rs
```

Required changes:

```text
STORAGE-capable ring slots
live owner retention
resident tensor view API
no AW-01 forward authority expansion
```

## 26.3 New backend files

```text
crates/burn_webgpu_backend/src/base_train_atlas_wave_02_r5_staged_prefill.rs
crates/burn_webgpu_backend/src/base_train_atlas_wave_02_r5_abi.rs
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r5_embedding.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r5_rmsnorm.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r5_qkv_projection.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r5_rope.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r5_attention_oracle.wgsl
```

## 26.4 New BaseTrain files

```text
crates/base_train/src/base_train_atlas_wave_02_r5_same_process_coordinator.rs
crates/base_train/src/base_train_atlas_wave_02_r5_cpu_reference.rs
crates/base_train/src/base_train_atlas_wave_02_r5_live_handoff.rs
```

## 26.5 New gate files

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r5_cli_registry.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r5_physical_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r5.args
tools/repair_aw02_r5_compile_and_run.ps1
```

## 26.6 Modified roots

```text
crates/model_core/src/lib.rs
crates/base_train/src/lib.rs
crates/burn_webgpu_backend/src/lib.rs
crates/orchestrator_local/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

---

# 27. Gate contract

Required final values:

```text
same-process AW-01 live owner                true
AW-01 slot count                            3
AW-01 current resident group                aw02.layer0.prefill_bundle
resident tensor view count                  5
AW-02 checkpoint open count                 0
AW-02 weight buffer create count            0
AW-02 weight queue-write count              0
canonical WGSL ptr<storage> arg count        0
canonical shader parse failures             0
canonical shader validation failures        0
canonical pipeline creation failures        0
position binding count                      1
RoPE theta binding count                    1
stage count                                 5
embedding mismatch count                    0
RMSNorm mismatch count                      0
Q mismatch count                            0
K mismatch count                            0
V mismatch count                            0
RoPE Q mismatch count                       0
RoPE K mismatch count                       0
context mismatch count                      0
padded exact-zero violation count           0
executed positive proof count               >= 96
executed negative-control count             >= 128
TensorCube live handoff count               1
TensorCube Stage10 dispatch count            0
