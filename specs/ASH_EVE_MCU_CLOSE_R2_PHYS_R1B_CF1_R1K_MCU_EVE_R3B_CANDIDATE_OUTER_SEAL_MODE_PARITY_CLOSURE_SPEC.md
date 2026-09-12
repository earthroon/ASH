# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1K

## MCU EVE R3B CANDIDATE EXECUTION / OUTER-SEAL MODE PARITY CLOSURE

### Revision

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1K

Class:
PRODUCTION MODE / EXECUTION PARITY CLOSURE
R3B CANDIDATE MATERIALIZATION AUTHORITY SEAL
EARLY FAIL-CLOSED ADMISSION

Direct semantic parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1J

Execution-harness parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1
```

R1K preserves R1J reader subgroup authority closure and CANARY-R1 and starts at the next physical first failure:

```text
E_MCU_EVE_R3B_CANDIDATE_COMPLETE_MISSING_AT_OUTER_SEAL
```

## 1. Confirmed contradiction

Canonical R1B/Canary configuration admits:

```text
admit_mcu_eve_adamw_target_ram_writeback_r3b = true
```

`HybridDeviceCommitRuntimeMode::from_environment()` defaults to `Off` when `ASH_HYBRID_DEVICE_COMMIT_MODE` is unset, while real R3B materialization is reachable only under `ActiveVerified`.

The previous graph therefore permitted:

```text
R3B=true
B06=Off / MirrorVerified
→ legacy RAM candidate path
→ no R3A/R3B active materialization
→ outer seal still requires CandidateComplete
→ E_MCU_EVE_R3B_CANDIDATE_COMPLETE_MISSING_AT_OUTER_SEAL
```

R1K makes this state illegal before candidate mutation.

## 2. Preflight parity

Changed file:

```text
crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs
```

For R3B admission:

```text
R3B=true
→ R3A=true REQUIRED
→ B06=ActiveVerified REQUIRED
```

Fail-closed errors:

```text
E_MCU_EVE_R1K_R3B_ACTIVE_VERIFIED_REQUIRED
E_MCU_EVE_R1K_R3B_R3A_ADMISSION_PARITY
```

Witness:

```text
[ASH-MCU-EVE-R1K][preflight]
```

The self-materialized preflight receipt records:

```text
r1kR3bB06Mode
r1kR3bB06ParityPass
```

R1K never writes `ASH_HYBRID_DEVICE_COMMIT_MODE` itself.

## 3. Runtime candidate-entry parity

Changed file:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Before `resident.begin_candidate_r1(...)`, R1K records and validates:

```text
resident Adam presence
production Muon runtime presence
R3A admission
R3B admission
actual B06 mode
selected candidate branch
resident phase before candidate
```

Witness:

```text
[ASH-MCU-EVE-R1K][candidate-branch]
```

Candidate branch vocabulary:

```text
RamResidentActiveDeviceProjection
RamResidentLegacy
PackedNonResident
```

For R3B=true the runtime gate requires resident Adam, production runtime, R3A=true and B06=ActiveVerified before `begin_candidate_r1()`.

## 4. R3A / R3B witness chain

R1K preserves real R3A handoff and adds:

```text
[ASH-MCU-EVE-R1K][r3a-handoff]
```

Before real R3B materialization:

```text
[ASH-MCU-EVE-R1K][r3b-materialize-enter]
```

After real materialization:

```text
[ASH-MCU-EVE-R1K][r3b-materialize-exit]
```

The exit witness includes:

```text
candidate_complete
commit_permit_ready
commit_performed
resident phase
RAM/EVE candidate seal digests
M/V digests
writeback submission epoch count
```

The existing R3B materializer remains the only authority that may create `CandidateComplete`.

## 5. R3B receipt propagation closure

The active-device path already constructed `McuEveAdamWritebackCandidateCompleteReceiptR3B`, but retained it only in a local variable. The returned `PackedCandidateOutput` therefore did not carry the real R3B receipt to the scheduler outer boundary.

R1K closes this seam with:

```text
output.eve_r3b_candidate_complete_receipt =
    eve_r3b_candidate_complete_receipt;
```

This propagates the real materializer receipt. It does not synthesize a receipt.

## 6. Candidate-return / outer-seal proof

R1K adds:

```text
[ASH-MCU-EVE-R1K][candidate-return]
[ASH-MCU-EVE-R1K][outer-seal]
```

For R3B=true outer seal now requires:

```text
B06=ActiveVerified
branch=RamResidentActiveDeviceProjection
resident phase=CandidateComplete
real R3B receipt present
receipt.validate() passes
candidate_complete=true
commit_permit_ready=true
commit_performed=false
receipt target generation exact
existing M/V digest parity exact
```

The existing deep guard remains:

```text
E_MCU_EVE_R3B_CANDIDATE_COMPLETE_MISSING_AT_OUTER_SEAL
```

New outer errors include:

```text
E_MCU_EVE_R1K_R3B_ACTIVE_VERIFIED_REQUIRED_AT_OUTER_SEAL
E_MCU_EVE_R1K_R3B_CANDIDATE_BRANCH_DRIFT
E_MCU_EVE_R1K_R3B_RECEIPT_MISSING_AT_OUTER_SEAL
E_MCU_EVE_R1K_R3B_RECEIPT_TERMINAL_STATE_DRIFT
E_MCU_EVE_R1K_R3B_RECEIPT_GENERATION_DRIFT
```

## 7. Forbidden repairs

R1K does not:

```text
Off → ActiveVerified automatically
MirrorVerified → ActiveVerified automatically
set ASH_HYBRID_DEVICE_COMMIT_MODE from library code
call legacy seal_candidate_r1() to fake R3B completion
force resident phase to CandidateComplete
fabricate an R3B receipt
relax the old CandidateComplete guard
```

Outer seal consumes proof. It does not manufacture proof.

## 8. Preserved parent code

Byte-preserved key files:

```text
crates/base_train/src/eve_mcu_close_r2_physical_canary_r1.rs
018bc0e5883a5ec249c8740b31d464f038ec6de8842eba5f9678154c9a291adb

crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
894f2961bfb85520dc0859f9e015c4e568a82b74b52527cc7a345a71b521b9e6

crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
c4050d90c0b4174409c2e26cffe7f1e7bdef9172a7b5db4b94f7cbf60936d8e8

crates/burn_webgpu_backend/src/tensorcube_fused_pair_muon.rs
064ff4fc784fad88ae3b043dea672184c23304fb9f5ec5aadacac0e1b9d8c437

crates/burn_webgpu_backend/src/buffer_submission_lease.rs
7e3cc0617d2bc076f3239eab6779b541e0aee2fcf92351391e43b5140b85cf4d

crates/burn_webgpu_backend/src/himuon_packed_gradient_r7a1.rs
4d438f9aae3ad1976447ba7b1b8c06f9c38d0f1c185057f69ed4639a157f7ccf
```

## 9. Actual source delta

Relative to CANARY-R1 code parent:

```text
ADD 0
MOD 2
DEL 0
```

```text
crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs
parent: dfd11b4aa3a77a7067d33dec6028490540249214ae29961abca6830c4df03891
R1K:    49b4ffe5e150badfed22caf79e1137a93f2de7f13fac66c1f90a58ce2bbd7b86

crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
parent: 7d7455bcb70225778e090f7bfe2fa35e425b4733ffb7426e2dbc67cad0dda2e4
R1K:    47d009aea934f024f3629c46fdbe4c1afe7224c02a4d2e8ec5f2caeb74dda008
```

Source-delta digest:

```text
d3c34a3e2abe216af198b51f6561d5499d79ba47ee0d8e79bc2a1a0d053ea538
```

## 10. Archive seal

Full code-only:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1K_MCU_EVE_R3B_CANDIDATE_OUTER_SEAL_MODE_PARITY_CLOSURE_CODE_ONLY.zip
SHA-256:
5866bf4bc24e142b8e36b51901c04bd232e1aec0d843c28da136e5c3a37cdf30
Files: 8424
CRC: PASS
```

Overlay code-only:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1K_MCU_EVE_R3B_CANDIDATE_OUTER_SEAL_MODE_PARITY_CLOSURE_OVERLAY_CODE_ONLY.zip
SHA-256:
860ce3155b674101d19e25e38ebbc51c94ef0666c34c5ceb5edb6ac47b032bef
Files: 2
CRC: PASS
```

Neither ZIP contains `specs/`, `artifacts/`, generated manifest/receipt JSON, or this specification.

## 11. Evidence boundary

Bake environment has no `cargo`, `rustc`, or `rustfmt`.

```text
SOURCE       CONFIRMED
STATIC       CONFIRMED
ARCHIVE      CONFIRMED
COMPILE      NOT VERIFIED
RUNTIME      NOT VERIFIED
PHYSICAL     NOT VERIFIED
PERFORMANCE  NOT MEASURED
```

## 12. Invocation contract

Because canonical R1B and CANARY-R1 admit R3B, valid physical execution now requires:

```text
ASH_HYBRID_DEVICE_COMMIT_MODE=ACTIVE_VERIFIED
```

Without it, preflight must reject with `E_MCU_EVE_R1K_R3B_ACTIVE_VERIFIED_REQUIRED` rather than spending a full candidate and failing at outer seal.

## 13. Physical closure

Preferred physical test is CANARY-R1.

Expected chain:

```text
[ASH-MCU-EVE-R1K][preflight]
  hybrid_mode=ActiveVerified parity_admitted=true

[ASH-MCU-EVE-R1K][candidate-branch]
  branch=RamResidentActiveDeviceProjection

[ASH-MCU-EVE-R1K][r3a-handoff]
  r3b_handoff_ready=true

[ASH-MCU-EVE-R1K][r3b-materialize-enter]
  phase=CandidateFilling

[ASH-MCU-EVE-R1K][r3b-materialize-exit]
  candidate_complete=true
  commit_permit_ready=true
  commit_performed=false
  phase=CandidateComplete

[ASH-MCU-EVE-R1K][candidate-return]
  r3b_receipt_present=true

[ASH-MCU-EVE-R1K][outer-seal]
  expected_outer_action=ConsumeR3BPresealedCandidate
```

R1K local physical PASS requires execution to cross the previous `E_MCU_EVE_R3B_CANDIDATE_COMPLETE_MISSING_AT_OUTER_SEAL` boundary without synthetic sealing.

## Final law

> R3B admission commits execution to the real ActiveVerified candidate path that can create CandidateComplete.

> Off and MirrorVerified are rejected before candidate mutation. They are not auto-promoted.

> R3A handoff, R3B materialization, candidate seal and R3B receipt are real production proof. Outer seal consumes that proof.

> A receipt created by the real materializer must reach the outer scheduler rather than disappear in a local variable.

> No synthetic CandidateComplete, no fake legacy seal, no weakened R3B guard.
