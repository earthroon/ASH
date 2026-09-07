# ASH-BASE-TRAIN-P1B-R1A2-R1B-CARGO-JSON-DIAGNOSTIC-CHANNEL-AUTHORITY

## CARGO JSON DIAGNOSTIC CHANNEL AUTHORITY
## + COMPILER-MESSAGE PRESERVATION
## + OBSERVATION PROGRESS TELEMETRY

### 0. Revision

```text
Patch ID:
ASH-BASE-TRAIN-P1B-R1A2-R1B-CARGO-JSON-DIAGNOSTIC-CHANNEL-AUTHORITY

Short name:
P1B-R1A2-R1B

Direct parent:
ASH_PASS3_BASE_TRAIN_P1B_R1A2_R1A_REQUIRED_PACKAGE_METADATA_PROJECTION_CODE_ONLY.zip

Class:
OBSERVER DIAGNOSTIC CHANNEL REPAIR
CARGO COMPILER-MESSAGE AUTHORITY
RUST-ONLY DIAGNOSTIC INFRASTRUCTURE
NO PRODUCTION RUNTIME CHANGE
```

### 1. Parent observation

R1A2-R1A reached the five-stage suite and reported:

```text
burn-wgpu-local=BuildPass
burn_webgpu_backend=BuildPass
canonical-baseline=WrongTarget
bisect-control=WrongTarget
current-production-cut=BuildPass
paired-status=HoldInvalidObservation
```

Both failing control audits recorded zero `compiler-message` and zero expected-target messages. Independent user-side no-cut release compilation already reproduces the canonical E0275 chain, so those `WrongTarget` results are not admitted as real target mismatch evidence.

### 2. Root cause

Parent observer invoked Cargo with:

```text
--message-format=json-render-diagnostics
```

while its fingerprint parser requires structured Cargo:

```text
reason = compiler-message
```

messages. R1B therefore changes the authoritative diagnostic transport to:

```text
--message-format=json
```

No stderr E0275 fallback is introduced.

### 3. Single machine diagnostic authority

```text
Cargo --message-format=json
    -> JSON stdout
    -> compiler-message
    -> exact metadata-bound package / lib target
    -> rustc diagnostic
    -> canonical E0275 fingerprint
```

stderr remains raw/human evidence only.

### 4. Message-format SSOT

Materialized in `crates/ash_p1br1a2_release_observer/src/observation.rs`:

```rust
pub const P1BR1A2_CARGO_MESSAGE_FORMAT_R1B: &str = "--message-format=json";
```

All authoritative observation plans append this constant. `json-render-diagnostics` remains only as a negative regression-test literal.

### 5. Existing target laws preserved

Failed build target evidence remains:

```text
ExitFailure
+ exact matching compiler-message
+ build-finished(false)
```

Successful `BuildPass` still requires:

```text
ExitSuccess
+ exact compiler-artifact
+ build-finished(true)
```

The exact metadata package-id / target-name / target-kind / target-src-path binding remains unchanged.

### 6. Canonical E0275 law preserved

`SameE0275` still requires:

```text
E0275
validation::NumericDimension: Sync
ShaderModule
Device
Queue
PendingWrites
and at least one of:
    RenderPipeline
    BindGroupLayout
```

No fingerprint threshold is weakened.

### 7. Progress telemetry

The CurrentProduction suite emits non-authoritative progress before each child Cargo build:

```text
[P1B-R1A2-R1B][1/5] burn-wgpu-local
[P1B-R1A2-R1B][2/5] burn_webgpu_backend
[P1B-R1A2-R1B][3/5] canonical-baseline
[P1B-R1A2-R1B][4/5] bisect-control
[P1B-R1A2-R1B][5/5] current-production-cut
```

Progress is emitted by observer `eprintln!` before `Command::output()`. It carries no PASS/FAIL/promotion claim and does not enter child Cargo stdout/stderr digests.

### 8. Runtime/schema identity

Successful summary header:

```text
[P1B-R1A2-R1B]
```

Pre-receipt header:

```text
[P1B-R1A2-R1B-PRE-RECEIPT-FAIL]
```

Observation/suite receipt schema revision is `P1B-R1A2-R1B`.

### 9. Regression tests

R1B materializes a test requiring every authoritative plan to:

```text
contain --message-format=json
not contain --message-format=json-render-diagnostics
```

Existing failure-target, InvalidSlice, BuildPass, SameE0275 and paired-promotion tests remain.

### 10. Production non-goals

R1B modifies no source under:

```text
crates/base_train/src/**
crates/burn_webgpu_backend/src/**
vendor_fork_scaffold/burn-wgpu-local/src/**
```

No optimizer, MCU, WGPU authority, Soft Matrix, Atlas, checkpoint, kernel, Send/Sync, Arc/Mutex or recursion-limit change is introduced.

### 11. Actual source delta

```text
ADD 0
MOD 3
DEL 0
```

Modified:

```text
crates/ash_p1br1a2_release_observer/src/observation.rs
crates/ash_p1br1a2_release_observer/src/receipt.rs
crates/ash_p1br1a2_release_observer/src/main.rs
```

No Cargo.toml / Cargo.lock / base_train feature change.

### 12. Static qualification actually executed

```text
source delta MOD3 only                    PASS
production source delta                   0
active message-format                     --message-format=json
active json-render-diagnostics argument    0
new if tokens in changed Rust files        0
R1A exact runtime/schema header remnants   0
balanced braces/parens/brackets            PASS
progress stage order 1..5                  MATERIALIZED
runtime/schema R1B header                  PRESENT
```

These are SOURCE/STATIC checks only. Cargo/rustc are unavailable in the bake environment, so observer compile/tests and paired release execution were NOT RUN.

### 13. Bake artifacts

Overlay code-only:

```text
ASH_BASE_TRAIN_P1B_R1A2_R1B_CARGO_JSON_DIAGNOSTIC_CHANNEL_AUTHORITY_OVERLAY_CODE_ONLY.zip
SHA-256: d3fb5e1798b847d742d0c90e7441f56e5220c5c7258cb576cf59d49b335dfc39
Files: 3
CRC: PASS
```

Full applied code-only:

```text
ASH_PASS3_BASE_TRAIN_P1B_R1A2_R1B_CARGO_JSON_DIAGNOSTIC_CHANNEL_AUTHORITY_CODE_ONLY.zip
SHA-256: 301f6b15993c8335d17970a0ba9cf9b2e73592b921ce49c72f02e485d2ca89d0
Files: 8,432
CRC: PASS
```

Both ZIPs contain zero generated `specs/`, `docs/`, `artifacts/`, `target/`, or `.ps1` paths. No Python or PowerShell loader is added.

### 14. User-side qualification

```powershell
cargo clean -p ash_p1br1a2_release_observer
cargo test -p ash_p1br1a2_release_observer --release
cargo build -p ash_p1br1a2_release_observer --release
cargo run -p ash_p1br1a2_release_observer --release -- current-production
```

Expected from existing external evidence, but not pre-promoted:

```text
burn-wgpu-local=BuildPass
burn_webgpu_backend=BuildPass
canonical-baseline=SameE0275
bisect-control=SameE0275
current-production-cut=BuildPass
paired-status=CurrentProductionClosureRequired
```

### 15. Stop law

Once R1B emits `CurrentProductionClosureRequired`, stop observer parser/transport revisions unless contradictory evidence appears. Next revision becomes P1B-R1A3 CurrentProduction internal classification with dependency-closed MCU / Muon / Scheduler subcuts and SharedCore materialization.
