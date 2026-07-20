# ASH-TRUTH-AUDIT-01-R1
# Performed / Reported / Observed / Verified Semantic Separation / Self-Attested Verification Elimination / Runtime-Owned Evidence Binding / Governance Revision Freeze / LoRA and Decode Minimal Physical Proof Seal

- Patch class: cross-cutting truth audit
- New decode revision authorized: false
- New LoRA feature revision authorized: false
- Compile repair revision increment authorized: false
- New governance hierarchy authorized: false
- General production promotion authorized: false

## 1. Purpose

This seal removes the following invalid authority chain:

```text
caller says performed=true
→ planner copies performed=true
→ receipt emits verified=true
→ reducer accepts verified=true
→ promotion PASS
```

`requested`, `reported`, `observed`, and `verified` are separate evidence levels. A caller claim may populate `reported`; it may never create `observed` or `verified`.

## 2. Confirmed finding

`batch_reduced_lora_ab_update.rs` copied caller-owned performed flags into plan fields and then emitted those plan fields as verification results:

```rust
lora_a_update_performed: input.lora_a_update_performed,
lora_a_update_verified: plan.lora_a_update_performed,
```

The same pattern applied to cross-batch reduction, AdamW state update, LoRA A update, and LoRA B update. No GPU submission, buffer before/after state, optimizer state, timestamp query, or independent numerical reference was read by that verification path.

## 3. Evidence levels

### Requested

An operation was requested. It proves intent only.

### Reported

An executing component claims the operation was performed. It does not prove execution or correctness.

### Observed

Runtime-owned evidence shows that execution or a physical state transition occurred. Examples include GPU submission completion, a changed buffer digest, a same-device raw-resource borrow, or a completed compact readback.

### Verified

A physical result was compared with an independent expected result under an explicit equality or tolerance rule.

## 4. Forbidden patterns

The following are promotion-ineligible and must not be named independent verification:

```rust
verified: input.performed
verified: plan.performed
verified: receipt.reported_success
verified: dispatch_count > 0
verified: upstream_verified
```

Upstream receipt validation may be recorded as `upstream_verification_receipt_valid`; it must not be relabeled as a new independent verification.

## 5. Required LoRA semantic repair

The default batch-reduced LoRA planner/receipt path must emit:

```text
cross_batch_reduce_reported
adamw_state_update_reported
lora_a_update_reported
lora_b_update_reported
evidence_level=Reported
independent_reference_used=false
promotion_authority=false
guard_passed=false
```

Deprecated `*_verified` compatibility fields must remain false until runtime-owned physical evidence and an independent comparator are bound.

A delta norm estimate or caller-provided performed flag must not set `post_warm_step_a_delta_verified=true`.

## 6. Repository-wide truth audit

Rust must scan repository sources and classify suspicious verification assignments as:

```text
performed_claim
caller_input
planner_claim
upstream_receipt_claim
```

The audit artifact must include exact paths, lines, fields, source text, evidence class, and promotion eligibility.

Canonical runtime artifact:

```text
workspace/runtime/truth_audit/ash_truth_audit_01_r1_runtime_artifact.json
```

## 7. Governance and revision freeze

Until both minimal physical proofs pass, the project must not add another promotion hierarchy, ledger family, receipt family, manifest authority layer, or revision-only wrapper.

Compile repairs, imports, JSON assembly changes, warning cleanup, and field binding fixes stay within the same functional revision.

## 8. LoRA MIN1

The minimal LoRA proof uses a deterministic small fixture and one optimizer step. It must observe:

```text
GPU dispatch completed
LoRA A/B physical state captured before and after
AdamW m/v state captured before and after
parameter delta observed
optimizer state delta observed
GPU result compared with independent CPU reference
observed_execution_count > 0
verified_result_count > 0
```

Required artifact booleans:

```text
dispatch_observed=true
parameter_delta_observed=true
optimizer_state_delta_observed=true
reference_parity_verified=true
```

## 9. Decode MIN1

Before reconnecting the 16-worker matrix, decode must prove one token with:

```text
worker=1
prompt=1
generation=1
selected_token_target=1
live Fusion resolve once
same-device raw borrow once
GPU argmax once
compact readback once
```

Required artifact fields:

```text
fusion_resolve_ok=true
raw_resource_borrow_ok=true
same_device=true
same_queue=true
gpu_argmax_dispatch_ok=true
gpu_argmax_token_id=<u32>
readback_count=1
readback_bytes<=16
cpu_materialize_count=0
host_upload_count=0
legacy_fallback_count=0
cpu_oracle_count=0
```

## 10. Non-vacuous authority

Zero failures with zero successful operations is not PASS.

```text
observed_execution_count > 0
verified_result_count > 0
```

must hold for physical-proof promotion.

## 11. WGPU lifecycle

A validation panic, invalid command encoder, unfinalized lifecycle drop, or panic-contaminated execution is not promotion evidence.

```text
encoder created
→ pass opened
→ pass closed
→ command buffer finished
→ submitted
→ finalized
```

An encoder may not be reused after invalidation.

## 12. PASS

PASS requires all of the following:

```text
self-attested verified source matches=0
caller/planner/upstream-owned independent verified matches=0
batch-reduced LoRA reported-semantics repair PASS
LoRA MIN1 physical proof PASS
Decode MIN1 physical proof PASS
new governance hierarchy count=0
compile-repair functional revision increment count=0
```

## 13. HOLD

The audit remains HOLD when self-attested or propagated verification remains, or when either MIN1 artifact is missing or fails.

HOLD must not emit `verified=true` for unproven physical work.

## 14. Canonical seal

```text
A claim that work was performed is not evidence that it occurred.
Evidence that work occurred is not evidence that the result is correct.
A result is verified only when a runtime-owned physical outcome is
compared against an independent expected result under an explicit rule.
Governance must not grow faster than the physical computation it governs.
```
