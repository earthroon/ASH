# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1C

## FRESH GENESIS OUTPUT AUTHORITY PUBLICATION ORDERING CLOSURE

### 1. Scope

This correction closes the FreshGenesis R1B production-path filesystem ownership inversion where Fresh-specific receipts were durably published before the canonical run output authority existed.

Primary source scope:

- `crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs`

No dataset, R1A source, RAM36 arithmetic, Muon implementation, checkpoint ABI, WGSL, or WGPU bootstrap semantics are changed.

### 2. Confirmed defect

Before this correction, FreshGenesis constructed and immediately wrote:

- `EVE_MCU_CLOSE_R2_PHYS_R1B_N8_FRESH_SOURCE_BINDING.json`
- `n8_fresh_genesis_scheduler_admission_r1b.json`

through `write_json_sync(&output.join(...), ...)` before:

```rust
let run_output_authority = acquire_fresh_run_output_directory(&output)?;
```

`write_json_sync()` does not create its parent directory. On a fresh Leg-A output path this can surface as Windows `os error 3` before canonical output authority acquisition.

Root-cause classification: **CONFIRMED**.

### 3. Authority law

Fresh-specific evidence may be constructed before output authority acquisition, but no output-bound receipt may be durably published before `acquire_fresh_run_output_directory()` succeeds.

Canonical ordering:

1. Fresh source validation.
2. Fresh packed genesis adoption.
3. Fresh binding receipt construction, memory only.
4. Fresh storage/RAM36/Muon/scheduler admissions.
5. Fresh scheduler receipt construction, memory only.
6. Runtime preparation.
7. `acquire_fresh_run_output_directory()`.
8. Fresh binding receipt publication through `run_output_authority.path()`.
9. Fresh scheduler receipt publication through `run_output_authority.path()`.
10. Existing R4A/D10 publication and production execution.

### 4. Implementation

The two Fresh receipts are now held as pending `Option<serde_json::Value>` values before output acquisition.

The original eager writes were removed.

After canonical output authority acquisition, the two pending receipts are published to `run_output_authority.path()`.

Publication failures are wrapped with explicit role and target-path context:

- `E_EVE_MCU_CLOSE_R2_PHYS_R1B_FRESH_BINDING_PUBLICATION_FAILED`
- `E_EVE_MCU_CLOSE_R2_PHYS_R1B_FRESH_SCHEDULER_PUBLICATION_FAILED`

No eager `create_dir_all()` bypass and no duplicate Fresh output-directory authority were introduced.

### 5. Historical preservation

Historical resume behavior remains unchanged.

The correction does not relax or replace:

- physical N2 parent requirements for historical origin,
- historical inventory evidence,
- historical scheduler lineage,
- historical Muon lineage,
- historical R6 source identity.

### 6. FreshGenesis preservation

The correction does not alter FreshGenesis identity semantics:

- source origin remains FreshGenesis,
- generation 0,
- optimizer step 0,
- no historical N2/N8 source-state reuse,
- no historical cursor/optimizer/scheduler reuse,
- no physical N2 parent for Fresh origin.

### 7. Re-materialization contract

Dataset regeneration: **NOT REQUIRED**.

R1A source regeneration: **NOT REQUIRED**.

Because `base_train` source identity changes, the following are required:

1. rebuild `base_train --release`,
2. reseal Native CF1 against the rebuilt binary,
3. use a fresh R1B campaign output root,
4. rerun R1B-CF1 preflight,
5. rerun physical A/B/C.

### 8. Static bake evidence

Static ordering observed in baked source:

- Fresh binding pending assignment: line 8586
- Fresh scheduler pending assignment: line 8598
- canonical output authority acquisition: line 9241
- Fresh binding publication target: line 9245
- Fresh scheduler publication target: line 9256

No target Fresh receipt `write_json_sync()` remains before canonical output acquisition.

Archive integrity:

- Overlay file count: 1
- Full code-only file count: 8423
- Overlay ZIP CRC test: PASS
- Full ZIP CRC test: PASS

### 9. Bake identity

Source SHA-256:

`38cb9f897aada6b6b70de65530ed1abfad19550178b3ef782525e72772b922fe`

Overlay ZIP SHA-256:

`fb086163e3afc566a26454897e5c3675148063502b7c9a5428e70cdd7af67bee`

Full code-only ZIP SHA-256:

`d60ed0387a11b2a57d8b7d1f78603015705ff6162db853566dadc45f16e0a7b9`

### 10. Verification status

- Root cause: **CONFIRMED**
- Code ordering correction: **CONFIRMED STATIC**
- Archive integrity: **CONFIRMED**
- Rust formatting: **UNKNOWN in bake environment** (`rustfmt` unavailable)
- Release compile: **NOT VERIFIED in bake environment** (Rust toolchain unavailable)
- Native CF1: **NOT YET VERIFIED**
- Physical A/B/C: **NOT YET VERIFIED**

No compile or physical promotion PASS is claimed by this specification.

### 11. Physical acceptance gates

Required local gates:

1. `cargo build -p base_train --bin base_train --release --locked -j 1` passes.
2. Native CF1 reseal passes for the rebuilt binary.
3. R1B-CF1 preflight returns `PASS_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_CONFIG_SELF_MATERIALIZATION`.
4. Fresh binding and scheduler receipts are published only after output authority acquisition.
5. The prior bare Windows `os error 3` at Fresh output publication does not recur.
6. Full physical A/B/C reaches its next valid production gate.
7. Final promotion is claimed only if the canonical physical PASS receipts are produced.

### 12. Closure statement

The correction establishes one rule:

> Evidence construction may precede ownership. Durable publication may not.

Fresh R1B receipt publication is now subordinate to the canonical run output authority rather than implicitly creating or assuming it.
