# ASH-BP-DK-R3

## RUNTIME-IDENTITY PRODUCTION AUTHORITY
## + EXACT-SHA AUDIT DECOUPLING

```text
+ PRODUCTION HOTPATH ExactSha256 RETIREMENT
+ RuntimeIdentity CANONICALIZATION
+ R3G-R2 PREPARED MUTATION RECEIPT BINDING
+ BP-DK NUMERICAL WITNESS PRESERVATION
+ EXACT SHA AUDIT / CHECKPOINT ONLY
+ NO CANARY BIT-EXACT CLAIM CHANGE
+ NO RESIDENCY POLICY CHANGE
```

## 0. Revision

```text
Patch ID:
ASH-BP-DK-R3

Direct parent implementation:
EVE-MCU-R3G-R2-CF1
SUBMISSION-BOUND MUTATION LEASE + GPU COMPLETION AUTHORITY
+ SYMBOL PARITY CLOSURE

Class:
PRODUCTION RUNTIME IDENTITY AUTHORITY
EXACT CONTENT DIGEST DECOUPLING
```

Parent operator evidence:

```text
R3G-R2 release regression PASS
base_train canonical release build PASS
```

This bake environment has no Rust toolchain. The R3 source is therefore sealed at SOURCE / STATIC / ARCHIVE only until the operator runs the commands in §24.

---

## 1. Confirmed parent condition

The parent backend already has:

```text
BpDkDevicePostUpdateDigestModeR1::ExactSha256
BpDkDevicePostUpdateDigestModeR1::RuntimeIdentity
```

and a hotpath constructor that omits the SHA pipeline in RuntimeIdentity mode.

The remaining production SHA re-promotion points were:

```text
ActiveDeviceCandidate / non-ActiveAsync execution-shape exact-digest forcing
FreshGenesis target-only hash_target_only_cf3() production path
```

R3 removes those production couplings. Exact SHA remains implemented for explicit audit.

---

## 2. Production authority policy

R3 materializes:

```text
BpDkPostUpdateAuthorityPolicyR3
    ProductionRuntimeIdentity
    ExactContentAudit
```

Canonical production selects:

```text
ProductionRuntimeIdentity
```

Explicit counterfactual / audit selection may select:

```text
ExactContentAudit
```

Execution shape does not automatically upgrade production to ExactSha256.

Forbidden:

```text
ActiveDeviceCandidate -> ExactSha256
non-ActiveAsync       -> ExactSha256
DEVICE_COMPACT        -> ExactSha256
```

---

## 3. Backend identity evidence separation

R3 adds semantically distinct evidence:

```text
BpDkRuntimeIdentitySetR3
BpDkExactContentDigestSetR3
BpDkPostUpdateIdentityEvidenceR3
    Runtime(...)
    ExactAudit(...)
```

RuntimeIdentity binds metadata authority. It is not content SHA.

ExactAudit carries actual W/M/U SHA-256 values.

Canonical generic consumption uses:

```text
BpDkPostUpdateSemanticDigestSetR3
    candidate_weight_digest
    candidate_momentum_digest
    orthogonal_update_digest
```

so RuntimeIdentity is not stored in a canonical `*_sha256` semantic field.

Legacy `BpDkDevicePostUpdateDigestSetR1` remains only as exact-audit compatibility storage and is empty under RuntimeIdentity production.

---

## 4. RuntimeIdentity inputs

Production RuntimeIdentity binds:

```text
canonical parameter index
source generation
target generation
element count
Weight PhysicalAllocationId
Momentum PhysicalAllocationId
Update PhysicalAllocationId
target backing / segment identity
Update backing identity
semantic plan digest
role domain
```

This metadata is hashed compactly. No W/M/U full payload read is performed solely to construct RuntimeIdentity.

---

## 5. FreshGenesis production closure

FreshGenesis production no longer directly calls:

```text
observer.hash_target_only(...)
hash_target_only_cf3(...)
```

from the base_train production callsite.

It now calls:

```text
build_target_identity(...)
```

Policy behavior:

```text
ProductionRuntimeIdentity
    -> metadata RuntimeIdentity
    -> no target-only SHA submission
    -> no synthetic submission epoch

ExactContentAudit
    -> existing hash_target_only_cf3 exact SHA path
```

FreshGenesis source numerical observation remains unchanged.

---

## 6. FreshGenesis submission law

RuntimeIdentity construction is CPU metadata authority and does not create GPU work.

Therefore:

```text
NO fake SHA submission
NO synthetic content-audit epoch
```

The compact production receipt keeps its actual source numerical observation submission epoch.

Exact audit records its content-audit submission epoch separately.

---

## 7. Production counters

For one normal observed parameter:

```text
identity_policy            = RUNTIME_IDENTITY
full_payload_sha_count     = 0
runtime_identity_count     = 3
```

For one explicit exact audit:

```text
identity_policy            = EXACT_CONTENT_SHA256
full_payload_sha_count     = 3
runtime_identity_count     = 0
```

No dual RuntimeIdentity + ExactSHA work is required in canonical production.

---

## 8. Numerical witness preservation

R3 preserves existing BP-DK numerical evidence:

```text
tile observations
pair observations
Weight RMS / delta RMS
Momentum RMS / delta RMS
Update RMS
cosine statuses / values
nonfinite counts
coverage
semantic plan digest
```

RuntimeIdentity does not replace numerical evidence.

---

## 9. Parameter identity candidate

R3 materializes:

```text
BpDkParameterIdentityCandidateR3
```

It binds:

```text
canonical parameter
source/target model generation
source/target optimizer generation
element count
identity policy
W/M/U physical allocation IDs
W/M/U semantic identities
backing identities
semantic plan digest
numerical witness digest
SHA/runtime-identity counters
```

The object is evidence, not commit capability.

---

## 10. R3G-R2 binding

R3 reads only cloneable receipts from the already-Prepared R3G mutation set.

Weight and Momentum are matched by:

```text
canonical parameter index
semantic role
exact target generation
exact PhysicalAllocationId
logical byte length
submission_completed = true
completion_coverage_exact = true
```

The move-only R3G mutation capability is not exposed.

---

## 11. Update non-overclaim

R3G-R2 persistent generation mutation set currently covers persistent W/M targets, not the transient orthogonal Update scratch as committed generation state.

Therefore R3 does NOT claim an R3G persistent Update receipt.

Update remains bound by the existing BP-DK Update evidence lease / backing identity and numerical observation authority.

---

## 12. Generation seal

Per-parameter bindings aggregate into:

```text
BpDkRuntimeIdentityGenerationSealR3
```

Required properties:

```text
one source generation
one target generation
one identity policy
no missing observed parameter binding
no duplicate parameter binding
one R3G prepared generation digest
```

RuntimeIdentity policy additionally requires:

```text
full_payload_sha_count = 0
runtime_identity_count = 3 * parameter_count
```

ExactContentAudit policy requires:

```text
full_payload_sha_count = 3 * parameter_count
```

---

## 13. Disabled BP-DK authority

When BP-DK does not observe:

```text
BpDkGenerationAuthorityR3::NotObserved
```

is bound explicitly to source and target generation.

No fake empty observed generation seal is fabricated.

---

## 14. R3C-R2 integration

`FullTrainableGenerationPreparedR3C` now privately owns:

```text
BpDkGenerationAuthorityR3
```

Its authority digest is included in the R3C prepared digest.

Before commit, R3C validates:

```text
BP-DK target generation == R3C target generation
BP-DK R3G prepared digest == R3C R3G prepared digest
```

Successful commit returns:

```text
bpdk_generation_authority_digest
bpdk_identity_policy
bpdk_full_payload_sha_count
bpdk_runtime_identity_count
```

for post-commit witness parity.

---

## 15. Production witness

Canonical production emits:

```text
[ASH-BP-DK-R3][production-authority]
```

with:

```text
source_generation
target_generation
identity_policy
full_payload_sha_count
runtime_identity_count
r3g_generation_prepared_digest
generation_authority_digest
r3c_generation_binding=true
admitted=true
```

For normal production the expected values are:

```text
identity_policy=RUNTIME_IDENTITY
full_payload_sha_count=0
r3c_generation_binding=true
```

`runtime_identity_count` equals three times the observed parameter count for the generation.

---

## 16. Exact audit preservation

R3 does not delete:

```text
base_train_bp_dk_device_post_update_sha256_r1.wgsl
TensorCubeBpDkDevicePostUpdateProducerR1 exact SHA path
hash_target_only_cf3 exact audit implementation
```

ExactContentAudit still produces actual W/M/U SHA-256.

The SHA WGSL is byte-preserved from the parent bake.

---

## 17. Canary / checkpoint preservation

R3 does not modify the current canary bit-exact state digest authority.

Confirmed bake boundary:

```text
crates/base_train/src/eve_mcu_close_r2_physical_canary_r1.rs
    byte-preserved
```

R3 does not reinterpret RuntimeIdentity equality as bit-exact equality.

Checkpoint/artifact content-integrity hashing is outside this change and remains unchanged.

---

## 18. Wait / residency preservation

R3 adds no new:

```text
wait_for_submission_exact
device.poll(PollType::Wait)
```

in the R3 authority / R3C / scheduler integration delta.

R3 changes no:

```text
source/target residency
arena budget
allocator retention
optimizer math
Muon math
Adam math
```

No VRAM or numerical-performance claim is made by this revision.

---

## 19. Static seals

Current bake static results:

```text
changed Rust files                                      10
ADD / MOD / DEL                                         1 / 9 / 0

ActiveDeviceCandidate exact-SHA forcing refs             0
FreshGenesis direct hash_target_only calls in base_train 0
FreshGenesis seal_with_target_digests refs                0
new exact-wait additions                                  0

RuntimeIdentity -> canonical *_sha256 semantic assignment 0
canary bit-exact source changed                            NO
SHA WGSL changed                                          NO

changed Rust delimiter balance                            10 / 10 PASS
```

This is STATIC evidence only.

---

## 20. Source delta

```text
ADD
crates/base_train/src/bp_dk_runtime_identity_production_authority_r3.rs

MOD
crates/burn_webgpu_backend/src/bp_dk_device_post_update_r1.rs
crates/base_train/src/adams_rib_eve_submission_bound_mutation_lease_r3g_r2.rs
crates/base_train/src/bp_delta_k_persistent_device_runtime_r1.rs
crates/base_train/src/eve_himuon_full_trainable_generation_commit_r3c.rs
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/unified_atlas_mcu_bp_dk_device_post_update_reduction_exact_digest_compact_evidence_r1.rs
crates/base_train/src/unified_atlas_mcu_bp_dk_device_resident_post_update_segmented_successor_r1.rs

DEL
none
```

Final source SHA-256:

```text
e61ddc849ea26a01f1f95f491d01aab9f94e99b418ac66b6ed7134d08f8c159f  crates/burn_webgpu_backend/src/bp_dk_device_post_update_r1.rs
7839a0e5fb207b1d2060c99fd2d461a14024185df250bd3e7adc03af753c78c9  crates/base_train/src/adams_rib_eve_submission_bound_mutation_lease_r3g_r2.rs
0e505fe8d39b19af2bfe9acda6e93454a1d5ac7efd27b7b4954756166b19ff9f  crates/base_train/src/bp_delta_k_persistent_device_runtime_r1.rs
cdd5c61381773398f9fc1167852fe631fb2c814168b775de9dc256a680720dec  crates/base_train/src/bp_dk_runtime_identity_production_authority_r3.rs
fb49c3f1b54b155662ab3a04d1ff2507f7b28fa2dfefc3506bbb14651d829ead  crates/base_train/src/eve_himuon_full_trainable_generation_commit_r3c.rs
092771c58e261e5c31de5bf384a6b1b17bc1502ca0707b65457d35b34fac9751  crates/base_train/src/lib.rs
2e66b12f87b5438742f7c794ba6f0f0f1c401d8b7b1178d7c0b73dd9679183e2  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
d50e48a515dee72e84ea4939c595610702bc2b322aeabf9412b92f1c2b6f54af  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
d0b1c6bc0684cbbd16a3489b7557571b0e2bdae24ee9af0120c268e227c371c6  crates/base_train/src/unified_atlas_mcu_bp_dk_device_post_update_reduction_exact_digest_compact_evidence_r1.rs
352a8710408485f58334982362ce0d52afff90d0019f9966f2f4258829f9a2f7  crates/base_train/src/unified_atlas_mcu_bp_dk_device_resident_post_update_segmented_successor_r1.rs
```

---

## 21. Bake artifacts

Full code-only ZIP:

```text
ASH_PASS3_BP_DK_R3_RUNTIME_IDENTITY_PRODUCTION_AUTHORITY_EXACT_SHA_AUDIT_DECOUPLING_CODE_ONLY.zip
SHA-256: 755b70a13ee3c02095b0b32b8161113f6d3ce0888a78f9fab1a396cd2f1e65f0
Files: 8426
CRC: PASS
```

Overlay code-only ZIP:

```text
ASH_BP_DK_R3_RUNTIME_IDENTITY_PRODUCTION_AUTHORITY_EXACT_SHA_AUDIT_DECOUPLING_OVERLAY_CODE_ONLY.zip
SHA-256: 2114e9cc8a955139997b25d408e830d4401b72af7f78ee7ceea5062ad24566e5
Files: 10
CRC: PASS
```

Both ZIPs contain:

```text
specs/                         0
artifacts/                     0
JSON/YAML manifest artifacts   0
spec markdown                  0
```

Cargo manifests / lockfile remain because they are build authority, not runtime artifact manifests.

---

## 22. Forbidden repairs

```text
NO RuntimeIdentity stored as canonical *_sha256 evidence
NO ActiveDeviceCandidate implicit ExactSha256 promotion
NO non-ActiveAsync implicit ExactSha256 promotion
NO dual SHA + RuntimeIdentity on every normal production parameter
NO fake metadata GPU submission
NO synthetic SubmissionEpoch
NO R3G completion bypass
NO Update persistent-R3G overclaim
NO numerical witness removal
NO BP-DK disablement used to avoid SHA
NO new per-parameter exact wait
NO canary bit-exact digest removal
NO checkpoint integrity digest removal
NO allocator / residency change
NO optimizer math change
```

---

## 23. Evidence boundary

At bake time:

```text
SOURCE / STATIC   PASS
ARCHIVE CRC       PASS
COMPILE           UNVERIFIED
RUNTIME-TEST      UNVERIFIED
PHYSICAL          UNVERIFIED
PERFORMANCE       UNMEASURED
```

Do not promote this spec commit beyond STATIC until operator-side Rust tests pass.

---

## 24. Operator qualification commands

Debug R3 regression:

```powershell
cargo test -p base_train --lib --locked bp_dk_r3_
```

Release R3 regression:

```powershell
cargo test -p base_train --lib --release --locked bp_dk_r3_
```

Parent authority regression:

```powershell
cargo test -p base_train --lib --release --locked r3g_r2_
cargo test -p base_train --lib --release --locked r3c_r2_
```

Backend regression:

```powershell
cargo test -p burn_webgpu_backend --lib --release --locked
```

Backend release compile:

```powershell
cargo build -p burn_webgpu_backend --lib --release --locked
```

Canonical production binary:

```powershell
cargo build -p base_train --bin base_train --release --locked -j 1
```

No full `cargo clean` is required.

---

## 25. Physical production acceptance

A real normal production campaign must show:

```text
[ASH-BP-DK-R3][production-authority]
identity_policy=RUNTIME_IDENTITY
full_payload_sha_count=0
r3c_generation_binding=true
admitted=true
```

and R3G/R3C target-generation parity.

Explicit ExactContentAudit may instead show nonzero full-payload SHA count. That is an audit lane and must not be classified as normal production hotpath evidence.

---

## 26. Promotion tokens

After compile/runtime regression:

```text
PASS_BP_DK_R3_RUNTIME_IDENTITY_PRODUCTION_AUTHORITY_EXACT_SHA_AUDIT_DECOUPLING
```

After physical normal-production observation:

```text
PASS_BP_DK_R3_PHYSICAL_RUNTIME_IDENTITY_PRODUCTION_AUTHORITY
```

Otherwise:

```text
HOLD_BP_DK_R3_PRODUCTION_IDENTITY_AUTHORITY_UNPROVEN
```

---

## 27. Final law

> Production generation ownership, write completion and numerical observation are no longer made dependent on a full W/M/U cryptographic scan.

> RuntimeIdentity identifies the runtime target. R3G-R2 proves the target write completed. BP-DK compact evidence proves the numerical observation. R3C-R2 consumes the resulting generation authority.

> Exact SHA remains exact content evidence. It is preserved for explicit audit and persistent content-integrity use, and is not silently redefined as RuntimeIdentity.

> BP-DK-R3 changes no canary bit-exact claim, checkpoint integrity claim, optimizer mathematics or residency policy.
