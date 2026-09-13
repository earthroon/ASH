# ASH-EVE-MCU-R3C-R1

## RELEASE-SAFE PREPARED GENERATION TRANSITION

```text
+ DEBUG / RELEASE SEMANTIC PARITY
+ PREPARE-TIME EVE NEXT-STATE MATERIALIZATION
+ COMMIT-TAIL SIDE-EFFECT REMOVAL
+ RELEASE-ACTIVE PREPARED INVARIANT
+ EVE CANDIDATE SEAL / LAYOUT / COMMIT-PERMIT PREPARE VALIDATION
+ NO OPTIMIZER MATH CHANGE
+ NO SHA / BP-DK / RESIDENCY CHANGE
```

## 0. Revision

```text
Patch ID: ASH-EVE-MCU-R3C-R1
Class: RELEASE SEMANTIC PARITY / PREPARED GENERATION TRANSITION CLOSURE
Primary source: crates/base_train/src/ram_resident_adam_mv.rs
```

Parent implementation basis:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF5
FULL-DURABLE MUON DEVICE-TARGET / HOST-CANDIDATE GUARD AUTHORITY CLOSURE
```

## 1. Confirmed source defect

The parent `commit_prepared_candidate_no_fail_r3c(...)` executed the semantic EVE generation transition inside `debug_assert!`:

```rust
let mut next = current.clone();
debug_assert!(
    next.commit_candidate(
        AdamGenerationOrdinalR1::new(
            permit.target_training_generation,
            permit.target_optimizer_generation,
        )
    ).is_ok()
);
```

`EveMutableStateIdentityR3::commit_candidate(...)` mutates:

```text
committed_generation = target
candidate_generation = None
phase = Committed
```

Therefore the transition must not depend on debug-assert execution.

Classification:

```text
CONFIRMED / SOURCE·STATIC
```

No previous runtime failure is attributed to this defect by this revision.

## 2. Authority law

```text
SEMANTIC STATE TRANSITION MUST NOT LIVE INSIDE debug_assert!
```

R3C-R1 establishes:

```text
prepare = fallible semantic transition preparation
commit  = release-safe prepared-state validation + move/install
```

## 3. Prepared future state

`PreparedEveAdamCommitR3C` now owns a private prepared future state:

```rust
eve_next_state_r3: Option<EveMutableStateIdentityR3>
```

This field is created only by `RamResidentAdamMv::prepare_commit_candidate_r3c(...)`.

The prepared future state is not constructed by scheduler code.

## 4. Prepare-time EVE transition

When EVE mutable authority exists, prepare now validates:

```text
EVE candidate seal exists
candidate seal validates
backend candidate seal digest matches R3C permit
candidate M digest matches R3C permit
candidate V digest matches R3C permit
EVE layout exists
candidate seal layout digest matches current layout
EveMutableCommitPermitR3 validates
```

Then prepare clones the current EVE metadata state and executes:

```rust
next.commit_candidate(target)?;
```

Failure returns `Err` before resident commit mutation begins.

When no EVE mutable authority exists:

```text
None -> None
```

No compatibility state is fabricated.

## 5. Prepared invariant

`PreparedEveAdamCommitR3C::validate()` now fail-closes the prepared future state.

For `Some(next)`:

```text
next.committed_generation == permit target generation
next.phase == Committed
next.candidate_generation == None
eve candidate seal witness is present
```

The prepared digest ABI is preserved.

## 6. Commit-tail semantics

`commit_prepared_candidate_no_fail_r3c(...)` no longer calls `EveMutableStateIdentityR3::commit_candidate(...)`.

At entry it performs release-active prepared validation:

```rust
prepared
    .validate()
    .expect("E_R3C_EVE_PREPARED_INVALID_AT_COMMIT");
```

The prepared future state is then moved into the resident at the existing installation boundary.

The existing RAM Adam payload commit ordering remains:

```text
candidate M/V application
transactional generation update
candidate state retirement
optimizer step increment
prepared EVE state install
EVE candidate seal retirement
```

## 7. Regression test

Added to the existing `ram_resident_adam_mv.rs` test module:

```text
r3c_release_safe_prepared_generation_transition
```

The test verifies:

```text
source = model G7 / optimizer G11
target = model G8 / optimizer G12

before prepare:
    resident EVE generation = source
    EVE phase = CandidateComplete

prepared artifact:
    future EVE generation = target
    future EVE phase = Committed
    future candidate generation = None

before commit:
    resident generation remains source

post commit:
    resident EVE generation = target
    RAM Adam training generation = 8
    RAM Adam optimizer generation = 12
    EVE phase = Committed
    EVE candidate generation = None
```

This source bake environment has no Rust toolchain, so debug/release test execution remains unverified here.

## 8. Preserved boundaries

R3C-R1 changes no:

```text
optimizer arithmetic
candidate M/V digest contract
ExactSha256 / RuntimeIdentity policy
BP-DK begin/finalize behavior
R3G lease architecture
cursor authority
Muon generation ownership
WGPU submission/wait behavior
arena policy
source/target residency
checkpoint format
scheduler-level commit ordering
R3C1 full generation APIs
CF5 durable Muon target authority
R1G Disabled finalize symmetry
```

## 9. Meaning change

Valid-state intended behavior:

```text
NO INTENDED SEMANTIC CHANGE
```

Invalid internal prepared state:

```text
BEFORE: release could skip debug-only invariant checking
AFTER:  commit entry fails closed
```

This is an intentional safety semantic change for invalid internal state only.

## 10. Static acceptance

Baked source satisfies:

```text
commit_prepared_candidate_no_fail_r3c:
    commit_candidate calls = 0
    debug_assert calls      = 0

prepare_commit_candidate_r3c:
    commit_candidate calls = 1
    debug_assert calls      = 0

PreparedEveAdamCommitR3C:
    private eve_next_state_r3 present

release-active prepared.validate() at commit entry present
regression test present
```

## 11. Compile / runtime acceptance

Required on the campaign machine:

```powershell
cargo test -p base_train --lib --locked `
  r3c_release_safe_prepared_generation_transition
```

```powershell
cargo test -p base_train --lib --release --locked `
  r3c_release_safe_prepared_generation_transition
```

```powershell
cargo build -p base_train --lib --release --locked -j 1
```

If the production authority is the binary, additionally:

```powershell
cargo build -p base_train --bin base_train --release --locked -j 1
```

No compile/runtime PASS is claimed by this bake environment.

## 12. Forbidden repairs

```text
NO global debug-assertions=true workaround
NO release-profile semantic dependency
NO duplicate commit_candidate call
NO live resident EVE mutation during prepare
NO full Adam M/V clone
NO silent generation repair
NO SHA retirement in R3C-R1
NO BP-DK mode change
NO R3G redesign
NO cursor redesign
NO residency change
```

## 13. Bake seal

Source delta:

```text
ADD 0
MOD 1
DEL 0
```

Modified source:

```text
crates/base_train/src/ram_resident_adam_mv.rs
```

Parent source SHA-256:

```text
b0a641ef28c26ecfd6d65d1f0552b32c2e45eeada899272c06ea1d6bd817135d
```

R3C-R1 source SHA-256:

```text
60a8d90cae0fb842039c5809c0cb45432dc3efb1e2e94de914c1f010296f7285
```

Full code-only ZIP:

```text
ASH_PASS3_EVE_MCU_R3C_R1_RELEASE_SAFE_PREPARED_GENERATION_TRANSITION_CODE_ONLY.zip
SHA-256: 1292f97ee27fe241e78d2daadc2d8d55c556d332565d343f847a5d16a1b9cddc
Files: 8424
ZIP CRC: PASS
```

ZIP exclusion seal:

```text
specs/ directory entries     = 0
artifacts/ directory entries = 0
manifest data entries        = 0
spec markdown entries        = 0
```

Cargo workspace build files are preserved.
Source modules whose Rust symbol/file names contain the word `manifest` are code and are not data-manifest artifacts.

## 14. Evidence level

```text
SOURCE / STATIC: PASS
ARCHIVE CRC:      PASS
COMPILE:          UNVERIFIED
RUNTIME:          UNVERIFIED
PHYSICAL:         UNVERIFIED
PERFORMANCE:      UNMEASURED
```

## 15. Promotion token

After campaign-machine compile plus debug/release regression parity:

```text
PASS_EVE_MCU_R3C_R1_RELEASE_SAFE_PREPARED_GENERATION_TRANSITION
```

Until then:

```text
HOLD_EVE_MCU_R3C_R1_RELEASE_SEMANTIC_PARITY_UNPROVEN
```

## 16. Final law

> A semantic generation transition executes because the production state machine requires it, not because debug assertions happen to be enabled.

> R3C prepare is the fallible boundary. It validates EVE candidate authority and materializes the next EVE generation state on a clone.

> R3C commit validates the prepared artifact under release semantics and installs the already-transitioned state. It does not discover generation-transition validity after irreversible RAM Adam commit work has started.

> R3C-R1 closes only release/debug generation-transition semantics. It does not claim consuming full-generation authority, GPU completion-bound mutation authority, cursor atomicity, SHA retirement, residency closure or performance improvement.
