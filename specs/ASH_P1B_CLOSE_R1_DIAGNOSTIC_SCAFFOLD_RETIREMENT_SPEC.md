# ASH-P1B-CLOSE-R1

# DIAGNOSTIC SCAFFOLD RETIREMENT
# + FIX-R2/R3 PRODUCTION REPAIR PRESERVATION
# + P1B FEATURE / WITNESS MODULE REMOVAL
# + RELEASE OBSERVER RETIREMENT
# + DEFAULT FEATURE GRAPH CLEANUP
# + CANONICAL TEST / RELEASE REVALIDATION
# + FINAL CLOSURE SEAL

## Revision

```text
Patch ID:
ASH-P1B-CLOSE-R1-DIAGNOSTIC-SCAFFOLD-RETIREMENT

Short name:
P1B-CLOSE-R1

Direct code parent:
ASH_PASS3_P1B_FIX_R3_FULL_HYBRID_VALID_PROJECTION_RETIREMENT_CODE_ONLY.zip

Physical parent suite:
4026ee0b1538fd26e46f38a0dcb293f486bd5c8195bc7cc41204ff442aa2e3ca

Parent final status:
FullBaseTrainReleaseClosed
```

## 1. Parent physical authority

FIX-R3 physically established:

```text
V0-direct-checkpoint=BuildPass
V1-full-hybrid-valid-negative=SameE0275
root-cause-status=FullHybridValidProjectionDemandRootConfirmed
production-whole-model-valid-count=0
direct-base-snapshot-seal=true
direct-adapter-snapshot-seal=true
canonical-release=BuildPass
stage-fences=5 stable=true
final-status=FullBaseTrainReleaseClosed
```

CLOSE-R1 does not reopen attribution. It removes P1B-only experimental infrastructure and then requires post-cleanup canonical revalidation on the user machine.

## 2. Production KEEP authority

The FIX-R2/R3 production repair is preserved byte-for-byte in `hybrid.rs` and `training.rs` relative to FIX-R3.

```text
TrainableAdapterSet<B>
  = gradient extraction authority
  = optimizer authority

HybridTrainModel<B>
  = forward composition authority

production Adam<TrainableAdapterSet<B>> count = 2
production GradientsParams<TrainableAdapterSet<B>> count = 2
production model.valid() count = 0
direct &model.base checkpoint sites = 4
direct &model.adapters checkpoint sites = 4
```

Key preserved hashes:

```text
crates/base_train/src/hybrid.rs
b9caf014fbfc9a676968e45d9866fe60bc05f80a93ca81ae72dc8fe2c89d8ec8

crates/base_train/src/training.rs
253967afdf26ace8005f28c9cc279c5bb919b68d7c6cc228a2527796628b5770
```

## 3. Actual cleanup delta

Relative to FIX-R3:

```text
ADD 1
MOD 6
DEL 31
```

Source-delta digest:

```text
2f667236f9b451c433607b708eacef2db7d0b9d28767f291f1fe930ce7e6a2f7
```

Added permanent non-P1B regression coverage:

```text
crates/base_train/src/training_authority_regression.rs
```

Modified:

```text
Cargo.toml
Cargo.lock
crates/base_train/Cargo.toml
crates/base_train/src/lib.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

## 4. Release observer retirement

`crates/ash_p1br1a2_release_observer` is removed entirely because its remaining executable command surface is P1B-specific and has no source-proven non-P1B consumer.

Workspace member reference is removed from root `Cargo.toml` and the observer workspace-package block is removed from `Cargo.lock`.

Expected post-cleanup:

```text
ash_p1br1a2_release_observer workspace member count = 0
ash_p1br1a2_release_observer Cargo.lock package count = 0
P1B observer CLI command references = 0
```

## 5. base_train feature graph cleanup

All P1B-only feature declarations are retired, including broad Send/Sync probes, R1/R1A cuts, D001/D002 cuts, TrainBackend probes, R1A4 prefix features, FIX-R1 B0/B1, FIX-R2 C0/C1/C2 and FIX-R3 V0/V1.

Post-cleanup feature section:

```toml
[features]
default = []
```

No compatibility aliases are retained.

## 6. lib.rs diagnostic gate retirement

P1B cut features had inserted many `#[cfg(...p1br1...)]` guards around ordinary production modules. CLOSE-R1 removes those P1B cfg attributes so the ordinary module graph returns to unconditional production declarations.

P1B diagnostic module declarations/reexports are removed.

## 7. pipeline demand-wrapper retirement

D001/D002 bisection wrappers and their HOLD stubs are removed.

Production callsites now call directly:

```text
run_base_training_loop_streaming::<TrainBackend>
run_base_training_loop::<TrainBackend>
```

One production callsite of each is present.

## 8. live Send/Sync probe retirement

P1B-only live assertions are removed from `production_multistep_loop_accumulation8_scheduler.rs`.

Production scheduler semantics outside those diagnostic assertions are unchanged.

## 9. Deleted files

```text
crates/ash_p1br1a2_release_observer/Cargo.toml
crates/ash_p1br1a2_release_observer/src/codegen_continuation_r1c.rs
crates/ash_p1br1a2_release_observer/src/demand_pair_r1a3_r2.rs
crates/ash_p1br1a2_release_observer/src/demand_r1a3_r1.rs
crates/ash_p1br1a2_release_observer/src/fast_observer_r3d.rs
crates/ash_p1br1a2_release_observer/src/fingerprint.rs
crates/ash_p1br1a2_release_observer/src/fix_r1_backward_gradient.rs
crates/ash_p1br1a2_release_observer/src/fix_r2_adapter_authority.rs
crates/ash_p1br1a2_release_observer/src/fix_r3_valid_projection.rs
crates/ash_p1br1a2_release_observer/src/internal_r1a3.rs
crates/ash_p1br1a2_release_observer/src/main.rs
crates/ash_p1br1a2_release_observer/src/metadata.rs
crates/ash_p1br1a2_release_observer/src/obs_r1.rs
crates/ash_p1br1a2_release_observer/src/obs_r1a_source_seal.rs
crates/ash_p1br1a2_release_observer/src/obs_r1b_execution_authority.rs
crates/ash_p1br1a2_release_observer/src/observation.rs
crates/ash_p1br1a2_release_observer/src/receipt.rs
crates/ash_p1br1a2_release_observer/src/source_identity.rs
crates/ash_p1br1a2_release_observer/src/trainbackend_r1a3_r3.rs
crates/ash_p1br1a2_release_observer/src/training_body_r1a4_r1.rs
crates/base_train/src/composite_send_sync_locus_probe_p1b.rs
crates/base_train/src/core_composition_bisection_p1b_r1a.rs
crates/base_train/src/current_production_demand_edge_ledger_p1b_r1a3_r1.rs
crates/base_train/src/current_production_demand_pair_p1b_r1a3_r2.rs
crates/base_train/src/current_production_internal_classification_p1b_r1a3.rs
crates/base_train/src/current_trainbackend_obligation_decomposition_p1b_r1a3_r3.rs
crates/base_train/src/release_trait_demand_attribution_p1b_r1.rs
crates/base_train/src/training_loop_body_obligation_bisection_p1b_r1a4_r1.rs
tools/validate_ash_base_train_composite_send_sync_locus_p1b_static.py
tools/validate_ash_base_train_core_composition_bisection_p1b_r1a_static.py
tools/validate_ash_base_train_release_trait_demand_p1b_r1_static.py
```

## 10. Permanent regression coverage

`training_authority_regression.rs` retains only ordinary architectural assertions:

```text
adapter-only Adam owner exists at both training routes
adapter-only GradientsParams owner exists at both training routes
production model.valid() count = 0
direct model.base checkpoint sites = 4
direct model.adapters checkpoint sites = 4
TrainableAdapterSet owns adapters and does not own AshModel/HybridTrainModel
```

It does not reproduce E0275 and contains no P1B identifiers.

## 11. Known unrelated local drift

The user's working tree contains:

```text
crates/base_train/src/manifest_digest_gate.rs
```

which is not present in the baked FIX-R3 parent archive but is already declared by `base_train/src/lib.rs` and was present in the physically passing user tree.

CLOSE-R1 does not delete, replace, or synthesize this unrelated local file. When applying cleanup to the existing working tree, preserve it.

Because this local-only file is not available to the bake environment, a pristine extraction of the full ZIP alone does not recreate that user-local drift. The authoritative application to the current working tree is therefore: apply the seven changed/new files and delete the explicit 31 retired paths, preserving unrelated local files.

## 12. Current source hashes

```text
Cargo.toml
e4bb6b5f0985f272e07b2e6475e0181f4766b736f0c0a54f9c9ed4cd30ee47a8

Cargo.lock
211fc82f84eacf6f19d676bae724c134028846af537dfe90205348f1bd047e6b

crates/base_train/Cargo.toml
448d03f52ef79092d43c1a59c66336f958ccc173c69878bb523b3fb9f62f31ba

crates/base_train/src/lib.rs
fd6bc881030abefbc60f8ff48bcc99ccc87dcafa386704e6fd29c1ec9dde8758

crates/base_train/src/pipeline.rs
1b62494ea01b9ba1ff29fd42e78d2e2f0b3076b856d1c8c509823d855746c7ce

crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
1f6218f63d752974ef89312a22da8f95d177d2b066e1d9df1c138a2e959b241d

crates/base_train/src/training_authority_regression.rs
70e40173579f45da2abe2623444f2aa824d48f6867fd116771d38d59bb8f92aa

base_train baked source digest
c73ae579f13448d7a1a98c79943f630900e39768e6f6411867343374bbdb6a03
```

## 13. Static qualification executed

```text
root Cargo.toml parse                         PASS
base_train Cargo.toml parse                   PASS
base_train feature graph                      default=[] only
active P1B feature/CLI references             0
P1B diagnostic base_train filenames           0
observer crate directory                      absent
observer workspace member                     0
observer Cargo.lock package                    0
pipeline direct streaming TrainBackend call   1
pipeline direct batch TrainBackend call       1
production adapter Adam owner count            2
production adapter from_grads count            2
production model.valid() count                 0
direct model.base snapshot count               4
direct model.adapters snapshot count           4
modified Rust lexical delimiter balance        PASS
ZIP CRC                                         PASS
```

The bake environment has no usable Cargo/rustc toolchain. `cargo metadata`, base_train tests and post-cleanup canonical release build were NOT RUN. `FullClosureSealed` is therefore not claimed by this bake; physical closure requires the user-side commands below.

## 14. Bake artifacts

```text
Overlay review-only:
ASH_P1B_CLOSE_R1_DIAGNOSTIC_SCAFFOLD_RETIREMENT_OVERLAY_REVIEW_ONLY_CODE_ONLY.zip
SHA-256:
baeb1270e57425ee37b1e22b7aa62b9e142dbf06384cc2696291fc9df94d7e00
Files: 7
CRC: PASS

Full baked tree:
ASH_PASS3_P1B_CLOSE_R1_DIAGNOSTIC_SCAFFOLD_RETIREMENT_CODE_ONLY.zip
SHA-256:
0a950ddd6791d2c784574f723e4250b3b463c663a966e3fa54fce2e184be4130
Files: 8,420
CRC: PASS
```

ZIP freshness:

```text
bake timestamp: 2026-09-09 13:41:50 Asia/Seoul
changed/new entries fresh mtime: 7/7 PASS
unchanged surviving parent entries preserve parent mtime: PASS
```

The overlay cannot encode deletions by ordinary extraction and is review-only. The full ZIP physically omits retired files but does not contain the user's unrelated local-only `manifest_digest_gate.rs`.

## 15. User-side physical qualification

After applying the changed/new files and deleting the 31 retired paths while preserving unrelated local files:

```powershell
cargo metadata --format-version 1 --locked
cargo test -p base_train --lib --locked
cargo build -p base_train --lib --release --locked -j 1
```

Required:

```text
metadata = PASS
base_train tests = PASS
canonical release = BuildPass
original E0275 absent
```

Final status after those physical results:

```text
FullClosureSealed
```

## 16. Final law

P1B-CLOSE-R1 removes the laboratory after the repair is proven. FIX-R2/R3 production authority remains intact; all P1B cuts, witnesses, negative controls, release-observer commands, receipt parsers, source manifests, stage fences and diagnostic feature aliases are retired. Post-cleanup canonical BuildPass proves that the production repair is self-contained and no longer depends on diagnostic scaffolding. `FullClosureSealed` is the terminal state of the P1B E0275 incident.
