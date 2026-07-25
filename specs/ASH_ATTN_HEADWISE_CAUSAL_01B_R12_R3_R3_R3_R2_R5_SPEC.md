# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R5

## Lexical Static Self-Match Elimination /
## Kernel-Only and Guarded End-to-End Performance Surface Separation /
## Probe Speed Evidence and Order-Bias Validity Decoupling /
## Tail-Closure Failure Attribution Seal

## Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R5
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R4
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r5.runtime_artifact.v1
local_manifest_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r5.local_manifest.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R5
static_lexical_authority_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R5
performance_surface_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R5
probe_evidence_validity_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R5
tail_failure_attribution_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R5
promotion_scope=incremental_decode_only
```

R2-R5 changes evidence ownership and verdict attribution. Attention arithmetic, Q/K/V values, route kernels, Reference scratch ownership, guard math, ring capacities and rollback policy remain unchanged.

## Bound evidence

R2-R4 completed both probe epochs and both production epochs after the dedicated Reference scratch repair. The remaining HOLD separated into static lexical self-match, probe speed evidence contaminated by order-bias validity, bare Reference versus guarded Atlas surface mismatch and tail labels collapsing unrelated dimensions.

Observed GQA2-to-Single median ratios were below 1.0 for every probe bucket from 512 through 2048. Order-bias validity failed at selected buckets. The old production comparison measured bare Reference attention against Atlas attention plus guard and downstream work.

## Static lexical authority

Executable function identity is owned by the comment-safe and string-literal-safe Rust lexical extractor.

Forbidden:

```rust
gate.matches("fn digest_f32_inputs").count() == 1
```

Required:

```rust
let helper = extract_rust_function_by_name(
    &gate,
    "digest_f32_inputs",
)?;
```

The extractor proves one executable definition with balanced delimiters. Source-wide substring counts, comment occurrences, string literals and specification text have no static authority.

```text
static_self_match_count=0
source_wide_substring_count_check_count=0
canonical_static_baseline_pass=true
```

## Performance surfaces

R2-R5 defines three distinct surfaces:

```text
kernel-only route surface
matched guarded end-to-end surface
unmatched diagnostic surface
```

Kernel-only Single and GQA2 use identical Q/K/V leases, shape, mask semantics, command topology, AB/BA order and timestamp topology. Guard decision and downstream work are excluded. This surface alone owns route-speed evidence.

Matched guarded end-to-end compares:

```text
Guarded Reference E2E
  = Reference attention
  + device guard decision
  + guarded downstream operation

Guarded Atlas E2E
  = selected Atlas attention
  + identical device guard decision
  + identical guarded downstream operation
```

The post-attention contract is `headwise.guard_and_downstream.matched.v1`. The only permitted difference is the attention implementation.

Bare Reference versus guarded Atlas may remain only as overhead context:

```text
route_authority=false
kernel_regression_authority=false
promotion_authority=false
```

## Matched measurement topology

Each production round contains 32 paired samples and one 64-slot measurement decision ring:

```text
Reference guarded slots=0..31
Atlas guarded slots=32..63
```

Each pair preserves AB/BA order. Each round owns one query resolve and one queue submission. Reference and Atlas each use a distinct guarded encoder.

```text
fused_command_encoder_count=sample_count*2
fused_queue_submit_count=measurement_round_count
separate_guard_submission_count=0
```

## Probe evidence factorization

Required fields:

```text
kernel_speed_evidence_pass
measurement_validity_pass
route_candidate
route_promotable
```

Kernel speed evidence owns parity, median ratio, p95 ratio and direct-sign probability. Measurement validity owns order bias, thermal consistency, sample integrity and pair balance. Order bias and thermal validity do not rewrite observed speed ratios.

```text
kernel_speed_evidence_pass=true
measurement_validity_pass=false
route_candidate=GQA2
route_promotable=false
```

The production route remains unchanged while promotion is HOLD.

Route monotonicity and crossover-neighbor stability are evaluated from kernel-speed evidence, not route-promotable flags. A validity failure is not a speed reversal.

## Tail failure attribution

Tail receipts for 512, 1024 and 2048 preserve these dimensions independently:

```text
kernel_speed
kernel_parity
measurement_order_bias
measurement_thermal
matched_guarded_e2e
scratch_and_alias_integrity
```

A guarded E2E failure may not be reported as a thermal failure. Multiple failed dimensions remain visible in `failed_dimensions`.

```text
tail_failure_misattribution_count=0
```

## Verdict authority

```text
route candidate authority=kernel-only speed evidence
route promotion authority=kernel speed plus measurement validity
runtime promotion authority=route promotability plus matched guarded E2E plus guard, canary, rollback and static truth
```

R2-R5 does not loosen thresholds, discard failed buckets, filter unfavorable samples or auto-promote GQA2.

## CLI additions

```text
--performance-surface-policy separated-v1
--kernel-only-route-evidence true
--matched-guarded-e2e-evidence true
--retain-unmatched-surface-diagnostic true
--require-kernel-and-guarded-surface-separation true
--require-matched-post-attention-contract true
--probe-speed-order-bias-decoupled true
--route-candidate-authority kernel-speed-only
--route-promotion-authority kernel-speed-plus-validity
--route-monotonicity-source kernel-speed-evidence
--crossover-neighbor-source kernel-speed-evidence
--require-order-bias-validity-for-promotion true
--require-thermal-validity-for-promotion true
--require-tail-failure-dimension-attribution true
--forbid-tail-failure-misattribution true
--static-truth-extractor rust-lexical-v2
--forbid-static-source-wide-substring-counts true
--require-canonical-static-baseline-pass true
--expected-negative-controls 1080
```

## Negative controls

R2-R5 inherits 1040 controls and adds 40:

```text
static lexical controls=10
surface separation controls=10
probe authority controls=10
tail attribution controls=10

total=1080
executed=1080
skipped=0
fail=0
```

## PASS boundary

PASS requires exact R2-R4 parent binding, R2-R4 scratch/dealias truth, zero static self-match, canonical static baseline PASS, kernel-only speed and monotonicity PASS, measurement validity PASS, route candidate promotable, matched guarded E2E non-regression PASS, exact tail dimension attribution with all required dimensions PASS, guard/canary/rollback PASS, 1080 controls and artifact digest truth.

PASS proves evidence separation and exact attribution. It does not prove universal adapter performance, transactional KV rollback, canonical full-model decode or model-quality improvement.

## Expected tokens

PASS:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R5_LEXICAL_STATIC_SELF_MATCH_ELIMINATION_KERNEL_ONLY_AND_MATCHED_GUARDED_END_TO_END_PERFORMANCE_SURFACE_SEPARATION_PROBE_SPEED_EVIDENCE_ORDER_BIAS_VALIDITY_DECOUPLING_TAIL_CLOSURE_FAILURE_ATTRIBUTION_INCREMENTAL_ONLY_NO_MODEL_QUALITY_OVERCLAIM
```

HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R5_KERNEL_ROUTE_CANDIDATE_PRESENT_MEASUREMENT_VALIDITY_OR_MATCHED_GUARDED_E2E_INCOMPLETE
```
