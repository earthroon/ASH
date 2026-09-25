# TENSORCUBE-TABLE-R4C-CF2

## EVIDENCE ORIGIN / SCOPE / TIMING TRUTH REPAIR
## + LITERAL-ZERO MEASUREMENT REJECTION
## + OBSERVED-ZERO AUTHORITY
## + CROSS-WAVE SUBMISSION-TIME REOBSERVATION
## + OFF-MODE TERMINAL SEAL CLOSURE
## + NO PHYSICAL-OVERLAP CLAIM PROMOTION

## 0. Revision

```text
Patch ID:
TENSORCUBE-TABLE-R4C-CF2

Canonical name:
ASH-BASETRAIN-TENSORCUBE-TABLE-R4C-CF2-
EVIDENCE-ORIGIN-SCOPE-TIMING-TRUTH-REPAIR-
LITERAL-ZERO-MEASUREMENT-REJECTION-
OBSERVED-ZERO-AUTHORITY-
CROSS-WAVE-SUBMISSION-TIME-REOBSERVATION-
OFF-MODE-TERMINAL-SEAL-CLOSURE-
NO-PHYSICAL-OVERLAP-CLAIM-PROMOTION
```

Direct implementation parent:

```text
ASH_PASS3_TENSORCUBE_TABLE_R4C_CF1_COMPILE_BOUNDARY_FIX_R2_CODE_ONLY.zip
SHA-256:
eac654e43ab45548e6c95556131e7a6a8d43242fb61ce6a107423f17d9c6f154
files=8507
CRC=PASS
```

Class:

```text
EVIDENCE SEMANTICS REPAIR
OBSERVATION AUTHORITY REPAIR
OBSERVER LIFECYCLE REPAIR
CROSS-WAVE TIMING ATTRIBUTION REPAIR

NO TRAINING MATH CHANGE
NO OPTIMIZER MATH CHANGE
NO WEIGHT CONTENT CHANGE
NO GPU KERNEL CHANGE
NO CACHE POLICY CHANGE
NO SLOT COUNT CHANGE
NO H2D ALGORITHM REWRITE
NO GENERATION COMMIT AUTHORITY CHANGE
```

## 1. Parent debt

Historical CF1 sealed the following fields with unconditional scalar zero:

```text
weight_prefetch_exact_wait_count
ordinary_weight_global_wait_count
unclassified_weight_wait_count
weight_prefetch_d2h_bytes
weight_refill_hdd_read_bytes
```

Scheduler then promoted the ordinary-global-wait scalar through `Some(...)`, and parent R4C treated `Option::is_some()` as measured authority.

The invalid inference was:

```text
literal zero
-> Some(0)
-> measured=true
```

CF2 removes that inference.

## 2. Truth law

```text
UNOBSERVED
    no valid observation authority
    -> None / UNKNOWN

OBSERVED ZERO
    valid observation authority
    + exact generation / optimizer scope
    + closed observation interval
    + zero matching events
    -> Observed(0)

OBSERVED NONZERO
    same authority and scope
    + N matching events
    -> Observed(N)
```

A zero-valued runtime counter initialization is not itself an observation.

## 3. Observation authority

Materialized in R4C:

```text
ObservationOriginR4CCF2
ObservedU64R4CCF2
```

`ObservedU64R4CCF2` binds:

```text
value
origin
source_generation
optimizer_step
scope_open_epoch
scope_close_epoch
```

Current admitted origins:

```text
RuntimeEventCounter
SubmissionStatusObservation
```

Malformed reversed scopes fail closed.

## 4. Literal-zero measurement rejection

CF1 receipt fields are now:

```text
Option<ObservedU64R4CCF2>
```

for:

```text
weight_prefetch_exact_wait_count
ordinary_weight_global_wait_count
unclassified_weight_wait_count
weight_prefetch_d2h_bytes
weight_refill_hdd_read_bytes
```

Current production code has no complete runtime source for those five fields, therefore the canonical receipt emits:

```text
None
```

not synthetic zero.

Observed zero remains representable through the authority-bearing observation constructor and is covered by unit-test source.

## 5. Parent R4C admission

`seal_with_cf1(...)` consumes the child observations themselves.

Parent derives:

```text
global_wave_wait_count_measured
unclassified_blocking_wait_count_measured
```

only from admitted observations.

Scalar compatibility views are derived as:

```text
observation.as_ref().map(|observation| observation.value)
```

Parent rejects observation scope whose generation or optimizer step differs from the final R4C seal scope.

No scheduler-side `Some(child_scalar)` wrapping remains.

## 6. Cross-wave timing truth

CF1 now keeps two explicit observation points:

```text
prefetch_start_pending_observation_count
upload_submission_pending_observation_count
```

The early prefetch-start observation remains diagnostic only.

For a cache-miss H2D path, authoritative structural cross-wave admission is now:

```text
NEXT real Weight writes queued
-> A01 upload fence submitted
-> pending-upload record retained
-> CURRENT compute status reobserved nonblocking
-> cross-wave classification
```

Only a nonterminal CURRENT observation at that submission boundary increments:

```text
weight_cross_wave_h2d_submit_count
weight_cross_wave_h2d_submit_bytes
weight_submit_while_current_compute_pending_count
```

The old `current_compute_pending_at_prefetch_start: bool` parameter is retired from `register_uploaded_prefetch(...)`.

## 7. Resource-lifetime safety during reobservation

Submission-time reobservation occurs after the upload fence has been submitted.

Before the nonblocking observation is attempted, CF2 stores the new pending upload record with its tracked submission and physical-allocation identities. This prevents a post-submit observation error from leaving the new submission outside the runtime's retirement ledger.

The record initially has:

```text
cross_wave_submission=false
```

and is promoted to true only after the submission-time CURRENT status is observed nonterminal.

## 8. OFF-mode terminal seal closure

Historical parent and child `observe_generation_commit(...)` returned immediately in OFF mode, leaving lifecycle generation/optimizer identity stale while final seal still required exact identity.

CF2 separates lifecycle truth from telemetry activation.

For all modes:

```text
OFF
OBSERVE_ONLY
ACTIVE_VERIFIED
```

commit notification validates:

```text
target_generation == current_generation + 1
target_optimizer_step == current_optimizer_step + 1
```

and advances lifecycle identity.

OFF still does not:

```text
open measurement authority
issue CF1 prefetch
submit CF1 fences
produce measured wait/D2H/HDD evidence
```

Final exact generation/optimizer seal remains fail-closed.

## 9. Physical-overlap firewall

CF2 preserves:

```text
TENSORCUBE_TABLE_R4C_CF1_MEASURED_WEIGHT_COPY_COMPUTE_OVERLAP_MATERIALIZED=false
TENSORCUBE_TABLE_R4C_MEASURED_PHYSICAL_OVERLAP_MATERIALIZED=false

measured_weight_copy_compute_overlap_supported=false
measured_weight_copy_compute_overlap_ns=None

measured_physical_overlap_supported=false
measured_physical_overlap_ns=None
```

Structural facts such as:

```text
CURRENT submission nonterminal
NEXT upload fence submitted
callback pending
```

must not promote hardware copy/compute overlap measurement.

## 10. Receipt surface

CF1 receipt remains the existing compatibility type and now includes:

```text
evidence_truth_patch_id=TENSORCUBE-TABLE-R4C-CF2
prefetch_start_pending_observation_count
upload_submission_pending_observation_count
literal_zero_measurement_rejection_materialized
observed_zero_authority_materialized
unknown_preservation_materialized
submission_time_reobservation_materialized
off_mode_terminal_seal_closure_materialized
```

Enabled CF1 runs additionally write:

```text
tensorcube_table_r4c_cf2_evidence_truth_receipt.json
```

The receipt carries the same authority-bearing evidence object used by parent R4C admission.

## 11. Exact implementation delta

Compared with the direct parent:

```text
MOD 6
ADD 1
DEL 0
```

Modified production source:

```text
crates/base_train/src/tensorcube_table_r4c_cf1_weight_cross_wave_h2d.rs
crates/base_train/src/tensorcube_table_r4c_cross_wave_residency_pipeline.rs
crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Modified validators:

```text
tools/validate_ash_tensorcube_table_r4c_cf1_weight_cross_wave_h2d_submission_static.py
tools/validate_ash_tensorcube_table_r4c_cross_wave_compute_transfer_overlap_static.py
```

Added validator:

```text
tools/validate_ash_tensorcube_table_r4c_cf2_evidence_truth_static.py
```

The implementation scope is one production file larger than the pre-bake estimate because the actual prefetch-start observation callsite lives in `packed_runtime_native_bootstrap_accumulation_wave_residency.rs`; submission-time truth cannot be closed solely inside the receipt/scheduler files.

## 12. Source SHA-256

```text
e4106e618cc93da60b4b4c1d21b22d312e2cd38e1abd091f0f115ae0598077e6  crates/base_train/src/tensorcube_table_r4c_cf1_weight_cross_wave_h2d.rs
90df8aed69add4ce4b94d02c6058a55cdc80b5b43f754d42af0e7f97e150e3e2  crates/base_train/src/tensorcube_table_r4c_cross_wave_residency_pipeline.rs
cf8245788c410c57dbf0dfc4cf5bcff56db786ce13e0e6b3805352162129ffd8  crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
10321325d59b83c02b0e380f17de6987294f9d2f98b721cb0fd76b90ea4913ab  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
901b54d2837d183cfc4e140c8a5982df8180306fe94dda76e06fdaaea3d7a44f  tools/validate_ash_tensorcube_table_r4c_cf1_weight_cross_wave_h2d_submission_static.py
88cd754f505a9150d9dc5aa0c5fb4908035bc2563895444cda508c9007f6a768  tools/validate_ash_tensorcube_table_r4c_cross_wave_compute_transfer_overlap_static.py
dfd61fc5d2f15d7a730ab88002ba6ea08821a1eed8c92265ddc8efe2c0d985c6  tools/validate_ash_tensorcube_table_r4c_cf2_evidence_truth_static.py
```

## 13. Static acceptance

Direct CF2 truth validator:

```text
PASS_TENSORCUBE_TABLE_R4C_CF2_EVIDENCE_TRUTH_STATIC checks=75
```

Maintained child validator:

```text
PASS_TENSORCUBE_TABLE_R4C_CF1_WEIGHT_CROSS_WAVE_H2D_SUBMISSION_STATIC checks=129
```

Maintained parent validator:

```text
PASS_TENSORCUBE_TABLE_R4C_CROSS_WAVE_COMPUTE_TRANSFER_OVERLAP_STATIC checks=82
```

Parent regression validators:

```text
R4B-CF2       118/118 PASS
R4B-CF1        77/77 PASS
R4B             58/58 PASS
R4A-CF2-CF1    90/90 PASS
R4A-CF2         40/40 PASS
R4A-CF1         90/90 PASS
R4A             66/66 PASS
```

## 14. Compile / runtime / physical status

Current bake environment has no Rust toolchain.

Therefore:

```text
SOURCE   APPLIED
STATIC   PASS
ARCHIVE  CRC PASS
COMPILE  UNVERIFIED
RUNTIME  UNVERIFIED
PHYSICAL UNVERIFIED
PERFORMANCE UNVERIFIED
```

No compile, runtime, physical or performance promotion is claimed by this specification.

Required next compile commands:

```powershell
cargo check -p base_train --lib --release --locked

cargo test `
  -p base_train `
  --lib `
  --release `
  --locked `
  tensorcube_table_r4c_cf2_ `
  -- --nocapture

cargo build `
  -p base_train `
  --bin base_train `
  --release `
  --locked
```

## 15. Unit-test source materialized

Source now contains tests for:

```text
UNOBSERVED -> UNKNOWN
OBSERVED(0) -> measured zero
wrong generation scope -> reject
R4C OFF two commits -> exact terminal seal
CF1 OFF two commits -> exact terminal seal + UNKNOWN measurement fields
```

These tests are source-materialized but are not claimed executed in the bake environment.

## 16. Baked archive

```text
ASH_PASS3_TENSORCUBE_TABLE_R4C_CF2_EVIDENCE_TRUTH_REPAIR_CODE_ONLY.zip
SHA-256:
6f0c76e259cbf25bce843b24a77f2593812082fb66a95bee2570df835ad2ed85
files=8506
CRC=PASS
```

Archive exclusion policy:

```text
specs/       excluded
artifacts/   excluded when present
manifest/    excluded when present
manifests/   excluded when present
```

The direct parent contained no top-level `artifacts/`, `manifest/` or `manifests/` directory. The baked archive contains zero entries from those roots and zero entries from `specs/`.

`Cargo.toml` and `Cargo.lock` remain present because they are build/package source authority, not runtime/data manifest artifacts. Source modules whose filenames contain the word `manifest` are also preserved because they are Rust/Python implementation source rather than generated manifest payloads.

## 17. Completion law

CF2 source truth is accepted only as:

```text
literal/default measured zero rejected
UNKNOWN preserved when no source exists
observed zero representable only with authority + scope
parent measured flags derived from admitted observations
cross-wave classification moved to submission-time reobservation
OFF lifecycle identity follows canonical commits
physical overlap remains unmeasured
```

No claim is made that CF2 improves training performance.

Final law:

> A zero is evidence only when a valid observation authority covered the exact scope and observed zero matching events. Unobserved is UNKNOWN, not zero.

> Cross-wave structural evidence is admitted from CURRENT status reobserved at the actual NEXT upload-submission boundary, not from an earlier prefetch-start snapshot.

> OFF disables evidence production, not lifecycle identity. Exact terminal generation and optimizer-step sealing remains intact.

> Structural queue/submission evidence is not physical hardware overlap measurement. CF2 does not promote physical-overlap support or duration.
