# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6-R1

## Matched Downstream COPY_DST Usage Contract /
## Role-Aware Native Scratch Factory /
## Matched Guard First-Fault Validation Scope /
## Poisoned Encoder Suppression Seal

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6-R1
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r6.r1.runtime_artifact.v1
local_manifest_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r6.r1.local_manifest.v1
promotion_scope=incremental_decode_only
negative_control_count=1160
```

R6-R1 repairs WGPU resource usage ownership and first-fault handling. Attention arithmetic, Single/GQA2/Reference shader math, Q/K/V values, route thresholds, mirrored input policy, paired non-inferiority policy, guard math and rollback policy remain unchanged.

## 1. Bound failure

R2-R6 created matched downstream native scratch with `STORAGE` only, then passed it to `CommandEncoder::clear_buffer`. WGPU requires `COPY_DST` for `clear_buffer`. The clear operation invalidated the encoder; the next compute-pass operation emitted the secondary `Encoder is invalid` panic.

```text
semantic_first_fault_stage=matched_downstream_clear
resource_role=MatchedDownstreamOutput
required_usage=STORAGE|COPY_DST
actual_usage=STORAGE
```

## 2. Scratch role SSOT

Required roles:

```text
ReferenceMeasurementOutput
KernelOnlySingleOutput
KernelOnlyGqa2Output
MatchedReferenceCandidate
MatchedAtlasCandidate
MatchedReferenceDownstream
MatchedAtlasDownstream
```

The role owns usage bits, allocator label, contract class, clear eligibility, storage-binding eligibility and mapped-at-creation policy. Caller-selected arbitrary usage is forbidden.

## 3. Canonical usage matrix

| Role | Usage |
|---|---|
| ReferenceMeasurementOutput | `STORAGE` |
| KernelOnlySingleOutput | `STORAGE` |
| KernelOnlyGqa2Output | `STORAGE` |
| MatchedReferenceCandidate | `STORAGE` |
| MatchedAtlasCandidate | `STORAGE` |
| MatchedReferenceDownstream | `STORAGE | COPY_DST` |
| MatchedAtlasDownstream | `STORAGE | COPY_DST` |

`COPY_SRC`, `MAP_READ` and `MAP_WRITE` remain absent. R6-R1 may not broaden every scratch to `COPY_DST`.

## 4. Role-aware factory

Authoritative allocation resolves usage from `HeadwiseNativeScratchRole` and records the actual allocation bits.

```rust
fn create_native_measurement_scratch_with_label(
    &self,
    prepared: &PreparedAtlasInputs,
    role: HeadwiseNativeScratchRole,
    label: &'static str,
) -> Result<HeadwiseReferenceMeasurementScratch>
```

Required receipt truth:

```text
required_usage_bits=actual_usage_bits
reference_copy_dst=false
kernel_copy_dst=false
candidate_copy_dst=false
downstream_copy_dst=true
```

## 5. Downstream clear precondition

Before any matched downstream clear:

```text
role is MatchedReferenceDownstream or MatchedAtlasDownstream
STORAGE present
COPY_DST present
size > 0
size aligned to 4 bytes
range within allocation
```

The precheck occurs outside all performance timestamp spans.

## 6. Physical contract parity

Parity compares role-equivalent resources:

```text
MatchedReferenceCandidate == MatchedAtlasCandidate
MatchedReferenceDownstream == MatchedAtlasDownstream
```

Candidate and downstream contracts are intentionally different because only downstream is cleared. The physical digest includes contract class, usage, size, mapping state, arena ownership, guard geometry, slot policy and submission topology.

## 7. First-fault validation

R6-R1 adds a dedicated fresh-encoder downstream-clear preflight and validation error scopes around matched warmup and timed round recording, encoder finish and queue submission.

Required behavior:

```text
push validation scope before recording
encode stage
finish encoder
poll outside timed span
pop validation scope
on error: discard and do not submit
on success: submit under a second validation scope
```

Failure messages retain the original WGPU text and semantic stage.

## 8. Poisoned encoder suppression

Allowed lifecycle:

```text
Fresh -> Recording -> Validated -> Finished -> Submitted
Fresh -> Recording -> Poisoned -> Discarded
```

Forbidden:

```text
Poisoned -> Recording
Poisoned -> Finished
Poisoned -> Submitted
Discarded -> Recording
```

Required counters:

```text
poisoned_encoder_reuse_count=0
poisoned_encoder_finish_attempt_count=0
poisoned_encoder_submit_attempt_count=0
secondary_encoder_invalid_count=0
validation_panic_count=0
uncaptured_validation_error_count=0
```

## 9. CLI policy

```text
--native-scratch-usage-policy role-aware-v1
--require-reference-scratch-storage true
--require-reference-scratch-copy-dst false
--require-kernel-scratch-storage true
--require-kernel-scratch-copy-dst false
--require-matched-candidate-storage true
--require-matched-candidate-copy-dst false
--require-matched-downstream-storage true
--require-matched-downstream-copy-dst true
--require-role-equivalent-usage-parity true
--forbid-global-copy-dst-broadening true
--require-downstream-clear-contract-precheck true
--require-downstream-clear-range-validation true
--require-downstream-clear-parity true
--matched-guard-validation-mode staged-first-fault-v1
--require-fresh-encoder-per-matched-validation-stage true
--require-matched-downstream-clear-validation true
--require-matched-guard-map-validation true
--require-matched-guard-finalize-validation true
--require-matched-downstream-dispatch-validation true
--require-matched-encoder-finish-validation true
--require-matched-queue-submit-validation true
--require-poisoned-encoder-discard true
--require-poisoned-encoder-reuse-zero true
--require-poisoned-encoder-finish-zero true
--require-poisoned-encoder-submit-zero true
--require-secondary-encoder-invalid-zero true
--require-validation-panic-zero true
--require-uncaptured-validation-error-zero true
--require-matched-validation-outside-timed-spans true
--require-matched-validation-population-zero true
--expected-negative-controls 1160
```

## 10. Negative controls

R6-R1 inherits 1120 controls and adds 40:

```text
role-aware usage controls=10
clear contract controls=10
first-fault validation controls=10
poisoned encoder controls=10
```

Required aggregate:

```text
count=1160
executed=1160
skipped=0
fail=0
```

## 11. PASS boundary

PASS requires exact parent binding, preserved R2-R6 kernel/input/physical/statistical truth, exact role-derived usage, legal matched downstream clear, role-equivalent physical parity, first-fault capture, zero poisoned-encoder continuation, zero secondary encoder-invalid error, zero validation panic, validation outside performance populations, matched guarded E2E policy, guard/canary/rollback truth, 1160 controls and artifact digest truth.

R6-R1 may repair the validation panic and still return a legitimate performance HOLD.

## 12. Expected tokens

PASS:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R6_R1_MATCHED_DOWNSTREAM_COPY_DST_USAGE_CONTRACT_ROLE_AWARE_NATIVE_SCRATCH_FACTORY_MATCHED_GUARD_FIRST_FAULT_VALIDATION_SCOPE_POISONED_ENCODER_SUPPRESSION_INCREMENTAL_ONLY_NO_MODEL_QUALITY_OVERCLAIM
```

Resource/validation HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R6_R1_MATCHED_DOWNSTREAM_USAGE_OR_FIRST_FAULT_VALIDATION_INCOMPLETE
```

Performance HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R6_R1_RESOURCE_AND_VALIDATION_TRUTH_ESTABLISHED_MATCHED_GUARDED_E2E_NON_INFERIORITY_INCOMPLETE
```
