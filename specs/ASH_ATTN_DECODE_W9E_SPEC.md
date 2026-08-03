# ASH-ATTN-DECODE-W9E

## Multi-Model Fleet Authority /
## Heterogeneous Device Profile Routing /
## Signed Release Channel /
## Transparency Log /
## Remote Telemetry Compaction /
## Automatic Recovery Rollout /
## No Cross-Model Authority Bleed Seal

> Status: SPEC RELEASE rev.1
> Patch ID: `ASH-ATTN-DECODE-W9E`
> Build revision: `W9E-w9d-multimodel-profile-release-transparency-r1`
> Parent: `ASH-ATTN-DECODE-W9D-R1B`
> Parent state: `PHYSICAL PASS`
> Parent writer: `TensorCube FleetGlobalDefaultWriter`
> Parent fallback: `HeadwiseFullActive`
> Cross-model authority bleed tolerance: zero
> Cross-profile authority bleed tolerance: zero
> Raw prompt, token, context, logits telemetry: forbidden

---

# 1. Parent authority

W9E adopts the exact W9D physical PASS lineage:

```text
signed fleet authority artifact
rollout wave authority
authority revocation
driver update requalification
device-loss recovery re-adoption
fleet-wide instant demotion
epoch-monotonic revocation journal
cross-installation consistency
Headwise fleet-safe demoted default
no stale global authority
no dual production writer
no full context readback
no full logits readback
no silent fallback
no post-commit rollback
no unrecoverable token commit
```

W9E may not widen authority outside this parent domain without new qualification evidence.

---

# 2. Goal

W9E extends a single-model fleet authority into independent model partitions and exact heterogeneous device profiles.

Canonical authority topology:

```text
Product Root Authority
  -> Signed Release Channel Head
  -> Model Authority Partition
  -> Checkpoint / Tokenizer / KV / Geometry Contract
  -> Device Profile Route Authority
  -> Installation Adoption Receipt
  -> Session Authority Snapshot
  -> Decode-Step Writer Lease
```

Recovery topology:

```text
Fault Receipt
  -> Demotion Receipt
  -> Requalification Receipt
  -> Recovery Candidate Artifact
  -> Recovery Rollout Wave
  -> Re-Adoption Receipt
```

Transparency topology:

```text
Release Artifact Digest
  -> Append-Only Transparency Leaf
  -> Inclusion Proof
  -> Signed Tree Head
  -> Consistency Proof
```

---

# 3. Model authority partition

The partition SSOT is the digest of:

```text
product lineage
model family
model architecture
checkpoint
tokenizer
vocabulary
KV schema
RoPE contract
attention geometry
output projection
sampler contract
```

Any mismatch creates a different partition. Human-readable model names are diagnostic only and cannot select authority.

Each partition independently owns:

```text
fleet authority epoch
rollout epoch
revocation epoch
release channel head
device profile allowlist
qualification receipts
recovery lineage
telemetry namespace
```

A session pins one exact partition for its full lifetime. Model switching requires a new session after old writer leases and KV owners reach zero.

---

# 4. No cross-model authority bleed

The following are fatal authority violations:

```text
Model A artifact authorizes Model B session
Checkpoint A qualification authorizes Checkpoint B writer
Tokenizer A receipt authorizes Tokenizer B token commit
KV schema A generation references KV schema B cache
Projection A consumes Model B hidden state
Sampler contract A consumes Model B logits
```

Detection action:

```text
block current token commit
quarantine session
quarantine affected installation
demote partition authority
hold fleet rollout
emit cross-model incident receipt
```

Cross-model bleed is manual-recovery-only. Automatic recovery rollout is forbidden.

---

# 5. Heterogeneous device profile authority

The exact device profile digest binds:

```text
backend
vendor
architecture
adapter identity
driver identity
shader compiler identity
features
limits
subgroup size
TensorCube layout
```

Route policy:

```rust
pub enum AttentionDecodeW9EProfileRoute {
    TensorCubeGlobalDefault,
    TensorCubeRestricted,
    HeadwiseSafeDefault,
    Denied,
}
```

Model and device selection must resolve one exact route matrix entry:

```text
model partition
+ installation device profile
+ active release artifact
= exact route matrix entry
```

Nearest-profile fallback is forbidden. Missing entries resolve to `HeadwiseSafeDefault` or `Denied` according to the signed policy.

Each profile independently binds full-layer qualification, latency budget, VRAM budget, long-session soak, rollback matrix, driver requalification, device-loss recovery, and writer exclusivity proof.

---

# 6. Signed release channels

Required channels:

```text
development
canary
stable
recovery
emergency
```

Each channel has independent sequence, signing key, release head, revocation head, and transparency head.

Normal promotion:

```text
development -> canary -> stable
```

Stable promotion requires:

```text
source channel PASS
three consecutive stability windows
valid signed channel head
valid transparency inclusion proof
valid transparency consistency proof
cross-model bleed count = 0
cross-profile bleed count = 0
revocation journal current
telemetry budget PASS
```

Channel heads are monotonic. Rollback is represented by a new signed sequence and never by moving the head to an older sequence.

Recovery and emergency channels remain independent lineages. Emergency may demote to Headwise but may not promote TensorCube.

---

# 7. Release artifact

The release artifact binds:

```text
channel id, epoch, sequence
model partition key
route matrix digest
parent W9D artifact, manifest, no-stale seal
model binary digest
tokenizer binary digest
shader bundle digest
runtime build digest
minimum authority epoch
minimum revocation epoch
validity interval
issuer key
payload digest
signature
artifact digest
```

Unsigned, expired, not-yet-valid, revoked, old-epoch, wrong-partition, or wrong-route artifacts are denied before session publication.

---

# 8. Transparency log

Required leaf kinds:

```text
release
revocation
channel promotion
channel rollback
key rotation
recovery rollout
```

Every adopted release requires:

```text
append-only leaf lineage
valid inclusion proof
valid signed tree head
valid consistency proof
non-decreasing tree size
matching artifact digest
matching model partition
```

Two installations observing different roots for the same tree size constitute a split-view incident:

```text
hold fleet rollout
quarantine channel
deny TensorCube promotion
preserve Headwise safe default
```

Each installation persists its last accepted tree head. Fleet witness PASS requires one root digest and zero split views.

---

# 9. Remote telemetry compaction

Remote telemetry may contain only deterministic aggregate receipts.

Forbidden fields and payloads:

```text
raw prompt
raw token ids
raw decoded text
raw context vectors
raw logits
raw KV tensors
raw attention matrices
user identifiers
filesystem paths
```

Allowed compact evidence:

```text
fleet, cohort, partition, profile, channel digests
window epoch and index
session and committed-token aggregate counts
rollback, demotion, recovery counts
latency buckets
VRAM buckets
cross-model bleed count
cross-profile bleed count
stale authority count
dual writer count
unrecoverable commit count
```

Pipeline:

```text
local detailed receipts
  -> schema validation
  -> forbidden-field scan
  -> deterministic bucketization
  -> minimum-cohort aggregation
  -> compact receipt digest
  -> signed upload envelope
```

Upload failure does not interrupt token generation. Exceeding telemetry freshness budget holds the next channel promotion.

---

# 10. Automatic recovery rollout

Automatic recovery is allowed only for proof-bound known faults:

```text
fixed numerical regression
requalified driver regression
replayed device-loss regression
corrected telemetry or profile budget regression
```

Manual-only incidents:

```text
cross-model bleed
cross-profile bleed
signature compromise
transparency split view
dual production writer
unrecoverable token commit
```

Recovery waves:

```text
R0 shadow
R1 1%
R2 5%
R3 25%
R4 50%
R5 100%
```

Every wave requires an independent PASS window. Any bleed, stale authority, dual writer, unrecoverable commit, or budget breach aborts recovery and preserves Headwise safe default.

---

# 11. Anti-rollback and partition journal

Each model partition stores independent maxima:

```text
max channel epoch
max channel sequence
max authority epoch
max rollout epoch
max revocation epoch
max transparency tree size
active release artifact digest
journal generation
```

Journals from different model partitions may not be merged or reused.

---

# 12. Production adoption sequence

```text
session requests model
-> resolve exact model partition
-> read active channel head
-> verify release signature
-> verify transparency inclusion
-> verify transparency consistency
-> verify partition journal anti-rollback
-> resolve installation device profile
-> resolve exact route matrix entry
-> verify W9D fleet authority
-> adopt W9C local authority
-> publish immutable session snapshot
```

Any failure denies TensorCube adoption. There is no silent or nearest-profile fallback.

---

# 13. Implementation plan

## model_core

```text
attention_decode_w9e.rs
attention_decode_w9e_model_partition.rs
attention_decode_w9e_session_binding.rs
attention_decode_w9e_device_profile.rs
attention_decode_w9e_route_matrix.rs
attention_decode_w9e_release_channel.rs
attention_decode_w9e_release_artifact.rs
attention_decode_w9e_transparency_log.rs
attention_decode_w9e_telemetry_compaction.rs
attention_decode_w9e_recovery_rollout.rs
attention_decode_w9e_partition_journal.rs
attention_decode_w9e_bleed_guard.rs
attention_decode_w9e_authority_runtime.rs
```

## burn_webgpu_backend

```text
attention_decode_w9e_device_profile_probe.rs
attention_decode_w9e_partition_binding_probe.rs
attention_decode_w9e_cross_profile_probe.rs
attention_decode_w9e_telemetry_compaction_probe.rs
```

## orchestrator_local

```text
attention_decode_w9e_cli_registry.rs
attention_decode_w9e_model_matrix.rs
attention_decode_w9e_profile_matrix.rs
attention_decode_w9e_release_channel_plan.rs
attention_decode_w9e_transparency_plan.rs
attention_decode_w9e_telemetry_plan.rs
attention_decode_w9e_recovery_plan.rs
attention_decode_w9e_scenario_plan.rs
ash_attn_decode_w9e_verification_gate.rs
ash_attn_decode_w9e_physical_gate.rs
```

---

# 14. Verification gate

Verification must prove:

```text
W9D parent artifact, manifest, no-stale seal exact
at least two independent model partitions
checkpoint, tokenizer, KV, projection mismatch denial
at least two exact device profiles
nearest-profile fallback denial
cross-profile qualification denial
signed channel heads
channel epoch and sequence monotonicity
channel isolation
stable promotion eligibility
append-only transparency leaves
inclusion and consistency proofs
split-view negative control
forbidden telemetry field denial
deterministic compaction
minimum cohort enforcement
eligible automatic recovery
manual-only recovery denial
recovery wave abort control
```

Verification PASS token:

```text
PASS_ASH_ATTN_DECODE_W9E_MULTI_MODEL_PARTITION_DEVICE_PROFILE_ROUTE_MATRIX_SIGNED_RELEASE_CHANNEL_TRANSPARENCY_LOG_TELEMETRY_COMPACTION_RECOVERY_ROLLOUT_CROSS_MODEL_BLEED_STATIC_VERIFICATION_SEALED
```

---

# 15. Physical gate

Physical gate phases:

```text
A. Bootstrap at least two model partitions
B. Bootstrap actual and deterministic fixture device profiles
C. Sign development, canary, stable release artifacts
D. Append artifacts to transparency log
E. Verify inclusion and consistency proofs
F. Inject Model A artifact into Model B session and reject before commit
G. Inject Profile A authority into Profile B and reject before admission
H. Compact detailed local receipts and prove forbidden payload absence
I. Run eligible demotion, requalification, R0-R5 recovery rollout
J. Inject manual-only cross-model incident and deny automatic recovery
```

Physical PASS criteria:

```text
model partition count >= 2
device profile count >= 2
exact route resolution for all admitted sessions
channel rollback accepted = 0
transparency proof failures = 0
unresolved split views = 0
forbidden telemetry fields = 0
raw prompt, token, context, logits payloads = 0
cross-model authority bleed = 0
cross-profile authority bleed = 0
nearest-profile fallback = 0
session partition mutation = 0
foreign KV authority = 0
dual production writer = 0
sampler double invocation = 0
token double commit = 0
silent fallback = 0
post-commit rollback = 0
unrecoverable token commit = 0
```

Physical PASS token:

```text
PASS_ASH_ATTN_DECODE_W9E_MULTI_MODEL_FLEET_AUTHORITY_HETEROGENEOUS_DEVICE_PROFILE_ROUTING_SIGNED_RELEASE_CHANNEL_APPEND_ONLY_TRANSPARENCY_LOG_INCLUSION_CONSISTENCY_PROOF_REMOTE_TELEMETRY_COMPACTION_AUTOMATIC_RECOVERY_ROLLOUT_EXACT_MODEL_PARTITION_BINDING_EXACT_DEVICE_PROFILE_BINDING_CHANNEL_SEQUENCE_MONOTONICITY_NO_CROSS_MODEL_AUTHORITY_BLEED_NO_CROSS_PROFILE_AUTHORITY_BLEED_NO_NEAREST_PROFILE_FALLBACK_NO_RAW_PROMPT_TELEMETRY_NO_RAW_TOKEN_TELEMETRY_NO_RAW_CONTEXT_TELEMETRY_NO_RAW_LOGITS_TELEMETRY_NO_DUAL_PRODUCTION_WRITER_NO_SILENT_FALLBACK_NO_POST_COMMIT_ROLLBACK_NO_UNRECOVERABLE_TOKEN_COMMIT_SEALED
```

---

# 16. Completion state

```text
Model Authority
  MultiPartition
  CheckpointBound
  TokenizerBound
  KVSchemaBound
  ProjectionBound

Device Authority
  HeterogeneousProfileBound
  ExactRouteMatrixBound
  NoNearestFallback

Release Authority
  SignedChannelHead
  SequenceMonotonic
  TransparencyProofBound

Telemetry
  CompactOnly
  Deterministic
  RawPayloadDenied

Recovery
  FaultBound
  QualificationBound
  AutomaticWaveBound
  ManualOnlyIncidentDenied

Safety
  NoCrossModelBleed
  NoCrossProfileBleed
  NoDualWriter
```

Next patch: `ASH-ATTN-DECODE-W9F`, distributed multi-node decode authority and no cross-host split-brain seal.
