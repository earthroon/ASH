# ASH-BASE-TRAIN-P1B-R1A1-COMPILE-DISCOVERED-TRANSITIVE-CLOSURE-R1

## CURRENT-PRODUCTION / ATLAS CHECKPOINT ROOT-SYMBOL REVERSE-CLOSURE COMPLETION
## + USER RELEASE E0432 INVALID-SLICE EVIDENCE BINDING
## + RUST-SIDE FIXED-POINT MANIFEST / GATE AUTHORITY
## + NO PRODUCTION RUNTIME SEMANTIC CHANGE

---

# 0. Revision

```text
Patch ID:
ASH-BASE-TRAIN-P1B-R1A1-COMPILE-DISCOVERED-TRANSITIVE-CLOSURE-R1

Direct parent:
ASH-BASE-TRAIN-DEPENDENCY-CLOSED-ROOT-SYMBOL-REEXPORT-CLOSURE-P1B-R1A1

Class:
COMPILE-DISCOVERED INVALID-SLICE CLOSURE REPAIR
ROOT-SYMBOL REVERSE DEPENDENCY FIXED POINT
DIAGNOSTIC ONLY
RUST-SIDE AUTHORITY
```

---

# 1. New Authoritative Input

The user executed:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1a-cut-current-production
```

The cut did not reach a valid E0275 attribution result.

It failed with `error[E0432]` unresolved crate-root imports in nine retained modules.

Therefore the previous R1A1 CurrentProduction slice is classified:

```text
INVALID_SLICE
```

The previous SOURCE/STATIC statement that the closure was complete is superseded by this COMPILE evidence.

No E0275 family attribution is admitted from that run.

---

# 2. Compile-Discovered Retained Consumers

The nine retained consumer modules are:

```text
bp_delta_k_fusion_policy_candidate_canary_qualification
bp_delta_k_fusion_policy_production_soak_and_rollback_health
bp_delta_k_fusion_policy_production_long_horizon_stability
bp_delta_k_fusion_policy_production_evidence_recalibration_bridge
bp_delta_k_fusion_policy_production_evidence_calibration_adoption
bp_delta_k_fusion_policy_production_aware_calibration_recommendation
base_train_atlas_wave_02_r5_same_process_coordinator
base_train_atlas_wave_02_r6_r5_receipts
base_train_atlas_wave_02_r6_checkpoint_tensor_decode
```

They consume root symbols whose producer modules were removed by the coarse cut.

---

# 3. Confirmed Producer Families

Compile-discovered symbol origins bind to:

```text
tensorcube_local_muon_production_callsite_adoption
production_multistep_loop_accumulation8_scheduler
bp_delta_k_fusion_policy_calibration_recommendation
bp_delta_k_fusion_fission_planner
bp_delta_k_fusion_objective_long_horizon_trajectory
bp_delta_k_fusion_policy_explicit_production_activation
base_train_atlas_wave_01_residency_coordinator
base_train_atlas_wave_02_r6_r5_authority
base_train_atlas_wave_02_r5_r6_checkpoint_tensor_set_authority
```

Together with the prior R1A1 edge:

```text
dataset
→ BaseBatchCpu
→ base_train_atlas_wave_02_r5_r3_geometry_authority
```

the Rust authority now materializes:

```text
root symbol origins  = 22
root symbol consumers = 30
root symbol edges     = 30
```

---

# 4. CurrentProduction Closure Repair

Previous R1A1 CurrentProduction closure:

```text
127 modules
```

R1 adds the nine compile-discovered consumers.

New CurrentProduction closure:

```text
136 modules
```

Added:

```text
base_train_atlas_wave_02_r5_same_process_coordinator
base_train_atlas_wave_02_r6_checkpoint_tensor_decode
base_train_atlas_wave_02_r6_r5_receipts
bp_delta_k_fusion_policy_candidate_canary_qualification
bp_delta_k_fusion_policy_production_aware_calibration_recommendation
bp_delta_k_fusion_policy_production_evidence_calibration_adoption
bp_delta_k_fusion_policy_production_evidence_recalibration_bridge
bp_delta_k_fusion_policy_production_long_horizon_stability
bp_delta_k_fusion_policy_production_soak_and_rollback_health
```

---

# 5. AtlasCheckpoint Closure Repair

Six of the compile-discovered BP/DeltaK consumers were also retained by the AtlasCheckpointSupport cut while their producer modules were already removed by that cut.

Therefore AtlasCheckpointSupport was also structurally invalid under the same root-symbol law.

Previous Atlas closure:

```text
147 modules
```

Added to Atlas closure:

```text
bp_delta_k_fusion_policy_candidate_canary_qualification
bp_delta_k_fusion_policy_production_aware_calibration_recommendation
bp_delta_k_fusion_policy_production_evidence_calibration_adoption
bp_delta_k_fusion_policy_production_evidence_recalibration_bridge
bp_delta_k_fusion_policy_production_long_horizon_stability
bp_delta_k_fusion_policy_production_soak_and_rollback_health
```

New Atlas closure:

```text
153 modules
```

The three Atlas modules newly added to CurrentProduction were already members of AtlasCheckpointSupport.

Therefore:

```text
P1BR1A_ATLAS_CHECKPOINT_ONLY
20 → 17
```

---

# 6. lib.rs Gate Law

For every newly admitted consumer, both its `pub mod` declaration and root `pub use` are guarded by the repaired coarse-cut predicate.

Current/Atlas shared predicate:

```text
not(any(
    p1br1a-cut-current-production,
    p1br1a-cut-atlas-checkpoint-support
))
```

The six BP/DeltaK consumers now use this predicate for both coarse cuts.

The three pre-existing Atlas-only consumers now additionally participate in the CurrentProduction cut.

Normal feature-OFF compilation remains unchanged.

---

# 7. Rust-Side Fixed-Point Authority

R1 expands:

```text
P1BR1A1_ROOT_SYMBOL_ORIGINS
P1BR1A1_ROOT_SYMBOL_CONSUMERS
P1BR1A1_DEPENDENCY_EDGES
```

and materializes regression tests that require every recorded root-symbol edge to satisfy:

```text
origin in CurrentProduction cut
    → consumer in CurrentProduction cut

origin in AtlasCheckpoint cut
    → consumer in AtlasCheckpoint cut
```

The Rust manifest remains the diagnostic SSOT.

No Python or PowerShell loader is introduced.

---

# 8. Source-Level Fixed-Point Check

Static analysis of crate-root symbol imports and direct crate module references after the R1 repair gives:

```text
CurrentProduction cross-boundary violations = 0
AtlasCheckpoint cross-boundary violations   = 0
```

This is SOURCE/STATIC evidence.

It does not replace the next Rust release compilation.

---

# 9. Gate / Manifest Equality

After repair:

```text
CurrentProduction actual cfg modules = 136
CurrentProduction Rust manifest      = 136
membership equality                  = true

AtlasCheckpoint actual cfg modules   = 153
AtlasCheckpoint Rust manifest        = 153
membership equality                  = true

AtlasCheckpointOnly Rust manifest    = 17
```

The `lib.rs` equality tests remain Rust-side via `include_str!("lib.rs")`.

---

# 10. Production Non-Goals

R1 changes no:

```text
optimizer math
Adam / HiMuon state
McuSessionRuntimeR7 ownership
R7B ownership
Rc<RefCell<...>>
WGPU Device/Queue authority
Soft Tensor Matrix
R3C / R3C1 commit semantics
Atlas runtime execution
checkpoint format
```

No:

```text
unsafe impl Send
unsafe impl Sync
Arc<Mutex> conversion
recursion_limit increase
stub module
fake root symbol
```

is admitted.

---

# 11. Actual Source Delta

Relative to the previous R1A1 code bake:

```text
ADD 0
MOD 2
DEL 0
```

Modified:

```text
crates/base_train/src/core_composition_bisection_p1b_r1a.rs
crates/base_train/src/lib.rs
```

No Cargo feature change is required by this compile-discovered closure revision.

---

# 12. Loader / ZIP Law

New Python loader:

```text
0
```

New PowerShell loader:

```text
0
```

All newly added authority is Rust source.

Delivered code ZIPs exclude generated specification, documentation and artifact directories.

The specification is committed separately to GitHub.

---

# 13. Bake Artifacts

Overlay code-only:

```text
ASH_BASE_TRAIN_P1B_R1A1_COMPILE_DISCOVERED_TRANSITIVE_CLOSURE_R1_OVERLAY_CODE_ONLY.zip
SHA-256: f363c69204e6f43f587d0c79c14e4a540161ffb60f805f2da71b6f2a03b32d40
Files: 2
CRC: PASS
```

Full applied code-only:

```text
ASH_PASS3_BASE_TRAIN_P1B_R1A1_COMPILE_DISCOVERED_TRANSITIVE_CLOSURE_R1_CODE_ONLY.zip
SHA-256: 5d221c9f7b60ae34cbb50cd557575eac934d94009e3e1beb24149be5bac60679
Files: 8550
CRC: PASS
```

The full ZIP contains no `specs/`, `docs/`, `artifacts/`, or `.ps1` entries.

No new Python file is part of the source delta.

---

# 14. Qualification Boundary

User evidence:

```text
R1A1 CurrentProduction release cut
    COMPILE = INVALID_SLICE by E0432
```

R1 repair bake environment:

```text
cargo unavailable
rustc unavailable
```

Therefore the R1 repair itself currently has:

```text
SOURCE       CONFIRMED
STATIC       SUPPORTED
ZIP CRC      PASS
COMPILE      NOT RUN ON REPAIRED SOURCE
RELEASE      NOT RUN ON REPAIRED SOURCE
RUNTIME      NOT RUN
PHYSICAL     NOT RUN
```

No repaired-source compile PASS is claimed.

---

# 15. Required Next Command

Run the repaired CurrentProduction cut again:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1a-cut-current-production
```

Interpretation:

```text
new cut-induced E0432/E0412/E0425/etc.
    → INVALID_SLICE
    → feed exact new edge back into closure

SAME_E0275
    → structurally repaired CurrentProduction cut preserves reproducer

E0275 absent with structurally valid compile progression
    → E0275_ABSENT candidate
    → final promotion still waits for R1A2 observation authority
```

---

# 16. Completion Law

This R1 source bake is complete when:

```text
all 9 compile-discovered retained consumers enter the required coarse closures
all 30 materialized root-symbol edges satisfy reverse-closure law
CurrentProduction gate set == 136-member Rust manifest
AtlasCheckpoint gate set == 153-member Rust manifest
source-level fixed-point scan finds zero known cross-boundary violations
normal feature-OFF graph is unchanged
no external loader is introduced
```

Release closure remains HOLD until the repaired source compiles in the user's Rust toolchain.

---

# 17. Final Law

> The user's E0432 output outranks the earlier static claim. The prior R1A1 slice was INVALID.
>
> R1 does not repair individual error lines with substitute symbols. It extends the reverse cut closure to every compile-discovered retained consumer and records the corresponding root-symbol edges in Rust.
>
> Both coarse cuts are repaired where they share the same missing producer/consumer relation.
>
> Static fixed-point zero is not compile PASS. The next release build decides whether another dependency edge remains.
