# ASH-BASE-TRAIN-P1B-R1A2-R1-CARGO-PACKAGE-TARGET-IDENTITY-JSON-STREAM-FRAMING

## CARGO PACKAGE / TARGET IDENTITY
## + JSON STREAM FRAMING
## + FAILURE OBSERVATION DIAGNOSTIC RECEIPT
## + EXACT CARGO METADATA PACKAGE BINDING
## + FAILED-TARGET COMPILER-MESSAGE ADMISSION
## + RUST-ONLY OBSERVER REPAIR

---

# 0. Revision

```text
Patch ID:
ASH-BASE-TRAIN-P1B-R1A2-R1-CARGO-PACKAGE-TARGET-IDENTITY-JSON-STREAM-FRAMING

Short name:
P1B-R1A2-R1

Class:
OBSERVER CLASSIFICATION REPAIR
CARGO PACKAGE/TARGET IDENTITY REPAIR
JSON MESSAGE FRAMING REPAIR
FAILURE-TARGET OBSERVATION REPAIR
DIAGNOSTIC ONLY
RUST-ONLY
NO PRODUCTION RUNTIME CHANGE

Direct code parent:
ASH_PASS3_BASE_TRAIN_P1B_R1A2_FAIL_CLOSED_RELEASE_OBSERVATION_RECEIPT_AUTHORITY_CODE_ONLY.zip
```

---

# 1. Authoritative Parent Observation

Parent observer suite reported:

```text
burn-wgpu-local=BuildPass
burn_webgpu_backend=BuildPass
canonical-baseline=Unclassified
bisect-control=Unclassified
current-production-cut=BuildPass
paired-status=HoldCanonicalBaselineDrift
```

Both failing control receipts recorded:

```text
process_result=ExitFailure(101)
build_finished_observed=true
build_finished_success=false
package_matches=false
lib_target_observed=false
compiler_artifact_observed=false
fingerprint=null
```

Manual baseline evidence independently reproduces the canonical E0275 chain.

Therefore the parent machine state is classified as observer target-classification failure, not confirmed source baseline drift.

---

# 2. Purpose

R1A2-R1 repairs only the observer.

It answers:

```text
Which exact Cargo package and lib target emitted a failed compiler-message?
```

and:

```text
Which stdout lines are Cargo JSON candidates and which are auxiliary stdout?
```

The bisection closure and production runtime are unchanged.

---

# 3. Exact Cargo Metadata Authority

Added:

```text
crates/ash_p1br1a2_release_observer/src/metadata.rs
```

Before the suite the observer executes:

```text
cargo metadata --format-version 1 --no-deps
```

and materializes exact:

```text
package id
package name
manifest path
lib target name
lib target kind vector
crate types
lib target src_path
```

Package name selects the metadata package.

Exact package ID authenticates Cargo compiler messages.

Substring package matching is retired.

---

# 4. Metadata Types

Materialized:

```text
P1bR1a2R1TargetIdentity
P1bR1a2R1PackageIdentity
P1bR1a2R1WorkspaceMetadataIdentity
```

Metadata identity is SHA-256 bound and re-evaluated after the suite.

Metadata drift yields:

```text
HoldMetadataIdentityDrift
```

---

# 5. Exact Compiler-Message Target Binding

A Cargo message matches the intended target only when all are exact:

```text
message.package_id == metadata package id
message.target.name == metadata lib target name
message.target.kind == metadata lib target kind
normalized message.target.src_path == metadata lib target src_path
```

No `contains("base_train")` fallback remains.

---

# 6. Failure Target Evidence

Materialized:

```text
P1bR1a2R1TargetEvidence
    CompilerMessage
    CompilerArtifact
    CompilerMessageAndArtifact
    None
```

For a failed build:

```text
ExitFailure
+ exact matching compiler-message
+ build-finished(false)
```

is sufficient target evidence even when no compiler-artifact exists.

Successful `BuildPass` still requires the intended compiler-artifact and build-finished(true).

---

# 7. JSON Stream Framing

Cargo stdout is split into:

```text
JSON candidate line
Auxiliary stdout line
```

Law:

```text
trimmed line begins with '{'
    -> parse as JSON candidate

otherwise
    -> auxiliary stdout
```

Auxiliary stdout does not invalidate the Cargo message stream.

A JSON-looking line that fails JSON parsing yields fail-closed:

```text
InvalidCargoMessageStream
```

---

# 8. Cargo Message Audit

Materialized:

```text
P1bR1a2R1CargoMessageAudit
P1bR1a2R1ObservedPackageAudit
P1bR1a2R1ObservedTargetAudit
```

Receipt audit fields include:

```text
total stdout lines
JSON candidate lines
parsed JSON messages
malformed JSON candidates
auxiliary stdout lines
compiler-message count
compiler-artifact count
build-finished count
expected package message count
expected target message count
observed package IDs
observed target names
observed target kinds
```

Audit lists are bounded.

---

# 9. Diagnostic Flattening

Canonical diagnostic marker search aggregates:

```text
diagnostic.message
child messages
child rendered text
diagnostic.rendered
```

The exact-target diagnostic only may contribute to the E0275 fingerprint.

Dependency diagnostics cannot become the `base_train` fingerprint.

---

# 10. Explicit Missing-Fingerprint State

Materialized:

```text
P1bR1a2R1CanonicalDiagnosticState
    NotObserved
    Observed { sha256 }

P1bR1a2R1FingerprintAbsenceReason
    NoMatchingCompilerMessage
    MatchingMessageButNoE0275
    InvalidCargoMessageStream
    WrongTarget
    NotApplicableBuildPass
```

`NotObserved` is no longer represented only by the hash of empty bytes.

---

# 11. Release Classification Repair

R1A2-R1 classification includes:

```text
SameE0275
DifferentE0275
BuildPass
InvalidSlice
WrongTarget
InvalidCargoMessageStream
OtherCompilerFailure
SpawnFailure
SourceDrift
ToolchainDrift
Unclassified
```

Failure classification law:

```text
exact target compiler-message + canonical E0275
    -> SameE0275

exact target compiler-message + different E0275
    -> DifferentE0275

active cut + structural compile error
    -> InvalidSlice

failure + no exact target compiler-message
    -> WrongTarget
```

---

# 12. Receipt Schema Revision

Observation and suite receipts now record:

```text
schema_revision=P1B-R1A2-R1
```

Observation receipt adds:

```text
metadata identity
expected package id
expected manifest path digest
expected target name/kind/src-path digests
compiler_message_observed
target_evidence
auxiliary stdout digest
canonical diagnostic state
fingerprint absence reason
Cargo message audit
observed package audit
observed target audit
```

Promotion-capable fields remain derived and private.

---

# 13. Paired Suite Law

The strong paired law remains:

```text
burn-wgpu-local             = BuildPass
burn_webgpu_backend         = BuildPass
CanonicalBaseline           = SameE0275
BisectControl               = SameE0275
CurrentProductionCut        = BuildPass
```

plus:

```text
source stable
toolchain stable
environment stable
metadata identity stable
```

Only then:

```text
CurrentProductionClosureRequired
```

---

# 14. Non-Promoted Audit Rendering

On a HOLD result the observer prints concise audit counters for canonical/control observations:

```text
messages=<count>
expected=<exact-target-message-count>
absence=<fingerprint absence reason>
```

This is display-only and does not become a second authority.

---

# 15. Branch Style

New/modified observer Rust source introduces no new `if` branch token.

State transitions remain match/enum oriented.

---

# 16. Production Non-Goals

R1A2-R1 modifies no production source under:

```text
crates/base_train/src
crates/burn_webgpu_backend/src
vendor_fork_scaffold/burn-wgpu-local/src
```

No changes to:

```text
optimizer mathematics
Adam/HiMuon state
MCU ownership
WGPU Device/Queue authority
Soft Matrix
R3C/R3C1
Atlas runtime
checkpoint format
kernel code
```

No:

```text
unsafe impl Send
unsafe impl Sync
Arc<Mutex> conversion
recursion_limit increase
```

is introduced.

---

# 17. Actual Source Delta

Relative to P1B-R1A2 parent:

```text
ADD 1
MOD 4
DEL 0
```

Added:

```text
crates/ash_p1br1a2_release_observer/src/metadata.rs
```

Modified:

```text
crates/ash_p1br1a2_release_observer/src/fingerprint.rs
crates/ash_p1br1a2_release_observer/src/main.rs
crates/ash_p1br1a2_release_observer/src/observation.rs
crates/ash_p1br1a2_release_observer/src/receipt.rs
```

Workspace Cargo.toml and Cargo.lock are unchanged.

No new dependency is introduced.

---

# 18. Static Qualification Actually Executed

Bake-side checks:

```text
root Cargo.toml parse                    PASS
Cargo.lock TOML parse                    PASS
observer Cargo.toml parse                PASS
source delta ADD1 / MOD4 / DEL0          PASS
new observer `if` branch token count     0
cargo metadata authority surface         PRESENT
metadata identity digest                 PRESENT
compiler-message target evidence         PRESENT
InvalidCargoMessageStream                PRESENT
fingerprint absence reason               PRESENT
auxiliary stdout audit                   PRESENT
expected target message count            PRESENT
production source delta                  0
```

These are SOURCE/STATIC checks.

---

# 19. Toolchain Qualification Boundary

Bake environment has no usable local Cargo/rustc toolchain and cannot access the Rust distribution host from the container.

Therefore:

```text
observer Rust compile    NOT RUN
observer Rust tests      NOT RUN
paired release suite     NOT RUN
base_train release       NOT RUN IN BAKE ENVIRONMENT
```

No COMPILE PASS is claimed.

---

# 20. ZIP Law

Delivered code ZIPs exclude generated:

```text
specs/
docs/
artifacts/
target/
PowerShell loaders
runtime receipt output
```

No Python or PowerShell loader is added.

Specification is committed separately to GitHub.

---

# 21. Bake Artifacts

Overlay code-only:

```text
ASH_BASE_TRAIN_P1B_R1A2_R1_CARGO_PACKAGE_TARGET_IDENTITY_JSON_STREAM_FRAMING_OVERLAY_CODE_ONLY.zip
SHA-256: 4e597d911b09988cd7b82c0672b1b4105fbd2133b083aa8c0210a6f62c51bb9c
Bytes: 14,907
Files: 5
CRC: PASS
```

Full applied code-only:

```text
ASH_PASS3_BASE_TRAIN_P1B_R1A2_R1_CARGO_PACKAGE_TARGET_IDENTITY_JSON_STREAM_FRAMING_CODE_ONLY.zip
SHA-256: c12f03bcf161d83e36e2b68548bdb4160fbfec7f59611d164712912b4f8c4880
Bytes: 21,517,035
Files: 8,432
CRC: PASS
```

Forbidden ZIP path counts:

```text
specs/      0
docs/       0
artifacts/  0
target/     0
.ps1        0
```

---

# 22. First User-Side Qualification

First gate:

```powershell
cargo test -p ash_p1br1a2_release_observer --release
```

Then authoritative suite:

```powershell
cargo run -p ash_p1br1a2_release_observer --release -- current-production
```

Expected from existing external evidence, but not predeclared:

```text
canonical-baseline=SameE0275
bisect-control=SameE0275
current-production-cut=BuildPass
paired-status=CurrentProductionClosureRequired
```

---

# 23. Failure Audit Command

If the suite still holds, inspect the generated receipt fields:

```text
cargo_message_audit
observed_package_audit
observed_target_audit
fingerprint_absence_reason
target_observation
```

The R1A2-R1 receipt is designed to expose the next classification boundary directly.

---

# 24. Completion Law

R1A2-R1 source bake is complete when:

```text
substring package matching is retired
cargo metadata exact package/target identity exists
failed target can be admitted through exact compiler-message
success still requires compiler-artifact
auxiliary stdout is separated from Cargo JSON
malformed JSON candidate fails closed
message/package/target audit is materialized
fingerprint absence reason is explicit
NotObserved is explicit
paired promotion remains derived only
production source is untouched
no external loader exists
```

Release completion waits for user-side observer execution.

---

# 25. Final Law

> Failed Rust compilation does not need a compiler artifact to identify its target. An exact Cargo compiler-message bound through metadata package ID and target identity is sufficient failure-target evidence.
>
> Cargo package identity is metadata authority, not substring matching.
>
> Non-JSON auxiliary stdout does not invalidate a Cargo JSON message stream. JSON-looking malformed lines fail closed.
>
> Missing fingerprints carry an explicit reason, and missing diagnostics are represented as `NotObserved`, not an empty-byte digest masquerading as evidence.
>
> R1A2-R1 repairs the observer only. The production baseline, CurrentProduction cut and runtime semantics are unchanged.
