02_model_spec_source_receipt.json
03_checkpoint_header_geometry_receipt.json
04_model_geometry_authority_receipt.json
05_model_spec_transaction_parity_receipt.json
06_derived_params_receipt.json
07_projection_shape_derivation_receipt.json
08_resident_geometry_binding_receipt.json
09_fixture_profile_isolation_receipt.json
10_atlas_shape_derived_plan_receipt.json
11_geometry_negative_control_receipt.json
12_rope_scope_boundary_receipt.json
13_gqa_scope_boundary_receipt.json
14_production_admission_firewall_receipt.json
15_static_geometry_literal_audit_receipt.json
16_artifact_write_receipt.json
ash_basetrain_atlas_wave_02_r5_r3_local_manifest.json
```

Runtime output root:

```text
workspace/runtime/basetrain/atlas_wave/02/r5_r3/<run_digest>/
```

Existing R5, R5-R1 and R5-R2 artifacts must not be modified.

---

# 15. Receipt requirements

## 15.1 ModelSpec source receipt

Required fields:

```text
source kind
repository-relative or checkpoint-relative path
byte count
SHA-256
model_spec_id
semantic model-spec digest
deserialization pass
validate_spec_consistency pass
fixture profile digest, when fixture
```

## 15.2 Header geometry receipt

Required fields:

```text
checkpoint identity digest
header digest
required tensor keys
observed dtype per tensor
observed shape per tensor
missing key count
unexpected selected-group tensor count
shape product overflow count
shape mismatch count
```

## 15.3 Geometry authority receipt

Required fields:

```text
all authority fields from section 4
source digest parity
transaction digest parity
header reconciliation pass
geometry digest
production admission false
```

## 15.4 Derived Params receipt

For every field:

```text
field name
source authority ID
source value
bound value
conversion kind
conversion error or exactness evidence
```

The receipt may not contain only the final Params object.

## 15.5 Projection receipt

Required independently recorded shapes:

```text
Q expected and observed
K expected and observed
V expected and observed
q_projection_dim
kv_projection_dim
MHA equality incidental flag
```

---

# 16. Static literal audit

R5-R3 must scan the admitted gate and runtime call graph for independent model-geometry literals.

Minimum files:

```text
ash_basetrain_atlas_wave_02_r5_physical_gate.rs
base_train_atlas_wave_02_r5_abi.rs
base_train_atlas_wave_02_r5_staged_prefill.rs
base_train_atlas_wave_02_r5_same_process_coordinator.rs
base_train_atlas_wave_02_r5_cpu_reference.rs
fixture generation module introduced by R5-R3
```

## 16.1 Forbidden patterns in gate/runtime

Outside the one fixture profile constructor and named expected-value test data:

```text
vocab_size: 32
hidden_size: 8
num_heads: 2
num_kv_heads: 2
head_dim: 4
rope_theta: 10_000.0
attention_scale: 0.5
shape: [32, 8]
shape: [8, 8]
logical_element_count: 256
logical_element_count: 64
```

The scanner must identify AST or structured-field context where practical. Raw substring count alone is insufficient for final admission.

## 16.2 Allowed literal location

Exactly one canonical constructor may contain fixture model values:

```rust
Aw02R5FixtureProfileV1::canonical()
```

Every other fixture artifact must be derived from its returned value.

## 16.3 No hidden defaults

`unwrap_or`, `max(1)`, default head counts, and silent fallback geometry are forbidden in the R5-R3 authority path.

Missing fields must cause explicit HOLD.

---

# 17. Positive proofs

R5-R3 positive proofs are geometry-authority proofs, not general R5 proof-ledger requalification.

Minimum executed assertions:

```text
ModelSpec source read                                 1
ModelSpec digest recomputation                        1
validate_spec_consistency execution                   1
transaction ModelSpec ID parity                       1
transaction ModelSpec digest parity                   1
checkpoint identity parity                            1
header digest parity                                  1
required tensor key resolution                        5
per-tensor dtype validation                           5
per-tensor shape reconciliation                       5
Q dimension derivation                                1
KV dimension derivation                               1
batch-size derivation                                 1
sequence-length derivation                            1
RoPE theta derivation                                 1
RMS epsilon derivation                                1
