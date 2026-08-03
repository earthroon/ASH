# ASH-ATTN-DECODE-W9F

## Distributed Multi-Node Decode Authority /
## Cross-Host KV Shard Lineage /
## Hardware Root Attestation /
## Federated Transparency Witness /
## Reproducible Release Mesh /
## No Cross-Host Authority Split-Brain Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-DECODE-W9F`  
> Build revision: `W9F-w9e-distributed-authority-kv-lineage-attestation-r1`  
> Parent: `ASH-ATTN-DECODE-W9E`  
> Parent state: `PHYSICAL PASS`  
> Token commit authority: exactly one fenced commit leader  
> KV authority: exact shard lineage with generation fencing  
> Attestation authority: nonce-bound hardware-root evidence  
> Transparency authority: federated witness quorum  
> Release authority: reproducible multi-builder release mesh  
> Cross-host split-brain tolerance: zero

---

# 1. Parent authority

W9F adopts the exact W9E physical PASS lineage:

```text
multi-model fleet authority
heterogeneous device profile routing
signed release channels
append-only transparency log
inclusion and consistency proofs
remote compact telemetry
proof-bound automatic recovery
exact model partition binding
exact device profile binding
no cross-model authority bleed
no cross-profile authority bleed
no nearest-profile fallback
no dual production writer
no silent fallback
no post-commit rollback
no unrecoverable token commit
```

W9F may not widen authority outside this parent domain without a new signed qualification artifact.

---

# 2. Goal

W9F extends one W9E model authority into a distributed decode cluster while preserving one production token-commit authority.

Canonical topology:

```text
W9E Signed Release Channel
  -> W9F Cluster Authority Artifact
  -> Attested Host Enrollment
  -> Distributed Session Authority
  -> Commit Leader Lease + Fencing Token
  -> KV Shard Assignment Graph
  -> Per-Host Worker Receipts
  -> Single Token Commit Certificate
```

Required invariants:

```text
active commit leader count = 1
fencing token strictly monotonic
token commit certificate per session step = 1
authoritative holder per KV shard generation = 1
minority partition production commit = 0
stale leader commit = 0
stale host authority reuse = 0
foreign model/session KV shard admission = 0
cross-host split-brain = 0
```

---

# 3. Cluster and host identity

Cluster identity binds:

```text
product lineage
release channel
release artifact
model partition
route matrix
cluster id
cluster epoch
authority epoch
revocation epoch
```

Host identity binds:

```text
cluster identity
host id and host epoch
machine identity
hardware root
boot measurement
runtime build
device profile
driver identity
network identity
```

Any mismatch creates a different authority domain.

Roles are capability-scoped:

```text
CommitLeader
CoordinatorCandidate
AttentionWorker
KvShardHolder
VerificationObserver
TransparencyWitness
ReleaseBuilder
```

A worker-only host cannot commit the token ledger. A shard-holder-only host cannot elect itself leader.

---

# 4. Hardware-root attestation

Each production host must present verifier-issued, single-use, short-lived evidence bound to:

```text
challenge nonce
verifier nonce
host epoch
cluster epoch
hardware root key
boot, firmware, OS, runtime measurements
device and driver identity
model partition
release artifact
```

Accepted roots may include TPM, TEE, secure-element, platform-attestation services, or a deterministic fixture root used only by the local physical simulation.

The following are denied:

```text
nonce replay
expired nonce
unknown root key
measurement mismatch
wrong release binding
wrong model binding
old host epoch
revoked host
```

---

# 5. Membership journal and leader fencing

Cluster membership SSOT is one generation-monotonic journal published by CAS.

The journal owns:

```text
active hosts
revoked hosts
host capabilities
membership generation
current commit leader
current fencing token
```

Leader election requires a majority quorum of attested voters. Election publishes:

```text
leader host id
lease generation
strictly higher fencing token
quorum certificate
monotonic lease window
```

A higher fencing token permanently invalidates lower-token commits, including commits from a previously isolated leader after network healing.

Wall clock alone is not authority. Commit validation binds the membership generation, quorum certificate, lease generation, monotonic tick window, and fencing token.

---

# 6. Distributed session and step authority

A distributed session pins:

```text
cluster identity
membership generation
model partition
release artifact
route matrix
session epoch
commit leader lease
fencing token
KV shard graph
```

A decode step pins one exact session authority and one KV graph generation. Worker receipts bind:

```text
host id and epoch
step authority digest
assigned shard digests
compact output digest
submission digest
completion state
```

The commit leader accepts only the exact expected worker receipt set. Missing, foreign, stale, or duplicate receipts block token commit.

Token commit certificate binds:

```text
session and step ordinal
leader lease and fencing token
session authority
KV graph
worker receipt set
sampler receipt
parent token-ledger digest
committed token digest
```

The token ledger appends by parent-digest CAS and rejects duplicate commits for the same session step.

---

# 7. Cross-host KV shard lineage

KV shard identity binds:

```text
model partition
session id and epoch
layer span
KV-head span
token span
dtype
layout
shard generation
content digest
```

Each generation has exactly one authoritative host. Replicas are read-only and hold no production commit authority.

Transfer sequence:

```text
source ownership verification
-> source freeze
-> content-digest seal
-> signed transfer manifest
-> target receive
-> target readback digest
-> target adoption receipt
-> new graph-generation CAS publish
-> source retirement receipt
```

Partial transfer, stale transfer nonce, content mismatch, foreign partition, old graph generation, old shard generation, unattested target, or non-authoritative source are denied.

Decode append publishes a new shard generation. Two authoritative children from one parent are a fatal shard fork. Shadow copies must explicitly carry `authority=false`.

---

# 8. Network partition and stale rejoin

Only the partition holding the configured majority quorum may elect a leader or commit production tokens.

Minority behavior:

```text
leader election denied
token commit denied
KV mutation denied
session frozen
Headwise diagnostic replay allowed
Headwise production ledger commit denied
```

Healing sequence:

```text
refresh membership journal
verify cluster epoch
verify current leader lease
verify fencing token
refresh KV graph
purge stale local authority
publish rejoin receipt
```

A restarted host must use a higher host epoch and fresh attestation nonce. Old membership, lease, fencing token, graph, or shard assignments cannot be reused.

---

# 9. Federated transparency witness

Release and cluster authority require a quorum of independently keyed transparency witnesses.

Each observation binds:

```text
witness identity and epoch
operator-domain digest
channel id
tree size
root digest
previous root
consistency proof
observation signature
```

The certificate requires majority witness quorum and minimum operator-domain diversity.

Different roots for the same tree size are a split-view incident:

```text
release adoption blocked
cluster authority demoted
channel quarantined
automatic recovery forbidden
```

---

# 10. Reproducible release mesh

Independent builders must reproduce one exact release output from one exact input manifest.

Input manifest binds:

```text
source commit and tree
Cargo.lock
Rust toolchain
build scripts and flags
target triple
shader sources and compiler
environment allowlist
```

Each builder is independently identified, attested, operator-domain bound, and signed.

The release mesh certificate requires:

```text
identical input-manifest digest
at least two builder receipts
minimum independent operator domains
one accepted runtime output digest
one accepted shader bundle digest
one accepted model-binding digest
one accepted release payload digest
```

Any output mismatch holds the release and blocks channel-head and transparency-leaf publication.

---

# 11. Split-brain guard

The following are fatal authority conflicts:

```text
two active commit leaders for one session epoch
two leaders using one fencing token
conflicting session-authority digests
conflicting KV-graph digests
minority production commit attempt
stale leader production commit attempt
```

On detection:

```text
block token commit
freeze session
revoke conflicting leases
demote cluster authority
preserve committed prefix only
require manual recovery certificate
```

Automatic recovery is forbidden for cross-host split-brain.

---

# 12. Verification gate

Binary:

```text
ash_attn_decode_w9f_verification_gate
```

It verifies:

```text
W9E parent lineage paths
W9F module and Cargo registration
CLI registry exactness
healthy single-leader guard
conflicting-leader negative control
required scenario-plan coverage
attestation, membership, fencing, shard, witness, release-mesh source surfaces
```

Verification PASS token:

```text
PASS_ASH_ATTN_DECODE_W9F_CLUSTER_IDENTITY_HARDWARE_ATTESTATION_MEMBERSHIP_JOURNAL_LEADER_FENCING_KV_SHARD_LINEAGE_FEDERATED_WITNESS_REPRODUCIBLE_RELEASE_MESH_SPLIT_BRAIN_STATIC_VERIFICATION_SEALED
```

---

# 13. Physical gate

Binary:

```text
ash_attn_decode_w9f_physical_gate
```

Physical phases:

```text
A. Bootstrap one physical WGPU device and four logical host identities
B. Create nonce-bound deterministic hardware-root attestations
C. Enroll all hosts through membership-journal CAS
D. Elect one commit leader by quorum
E. Create one distributed session and at least four KV shards
F. Execute one cross-host step and commit exactly one token certificate
G. Fail over to a new leader with a higher fencing token
H. Reject the stale leader lease
I. Partition the cluster into majority and minority sides
J. Reject minority production commit
K. Transfer one authoritative KV shard and verify readback lineage
L. Reject duplicate token commit
M. Build federated witness quorum and reject a split-view fixture
N. Build reproducible release quorum and reject a mismatched-builder fixture
O. Seal the no-cross-host-split-brain summary
```

Physical PASS token:

```text
PASS_ASH_ATTN_DECODE_W9F_DISTRIBUTED_MULTI_NODE_DECODE_AUTHORITY_CROSS_HOST_KV_SHARD_LINEAGE_HARDWARE_ROOT_ATTESTATION_NONCE_BOUND_HOST_ENROLLMENT_MEMBERSHIP_GENERATION_MONOTONIC_COMMIT_LEADER_QUORUM_FENCING_TOKEN_SINGLE_TOKEN_COMMIT_NETWORK_PARTITION_MINORITY_COMMIT_DENIAL_STALE_HOST_REJOIN_FENCING_FEDERATED_TRANSPARENCY_WITNESS_QUORUM_REPRODUCIBLE_RELEASE_MESH_EXACT_MODEL_PARTITION_EXACT_DEVICE_PROFILE_NO_FOREIGN_KV_SHARD_NO_KV_SHARD_FORK_NO_CROSS_HOST_AUTHORITY_SPLIT_BRAIN_NO_DUAL_PRODUCTION_WRITER_NO_SILENT_FALLBACK_NO_POST_COMMIT_ROLLBACK_NO_UNRECOVERABLE_TOKEN_COMMIT_SEALED
```

---

# 14. Required runtime artifacts

```text
workspace/runtime/attention/decode/w9f/
  ash_attn_decode_w9f_verification_runtime_specification.json
  ash_attn_decode_w9f_verification_runtime_artifact.json
  ash_attn_decode_w9f_verification_local_manifest.json
  ash_attn_decode_w9f_physical_runtime_specification.json
  ash_attn_decode_w9f_physical_runtime_artifact.json
  ash_attn_decode_w9f_physical_local_manifest.json
  cluster_authority_artifact.json
  cluster_identity.json
  membership_journal.json
  host_enrollment_receipts.json
  hardware_attestation_evidence.json
  leader_election_certificates.json
  leader_lease_history.json
  kv_shard_identities.json
  kv_shard_lineages.json
  kv_assignment_graph_history.json
  kv_transfer_manifests.json
  distributed_step_receipts.json
  token_commit_certificates.json
  federated_witness_observations.json
  federated_witness_certificates.json
  build_input_manifest.json
  reproducible_build_receipts.json
  release_mesh_certificate.json
  network_partition_matrix.json
  split_brain_negative_controls.json
  final_no_cross_host_authority_split_brain_seal.json
```

Runtime artifacts are generated by Rust and excluded from the code ZIP.

---

# 15. Completion state

W9F PASS establishes:

```text
Distributed Authority
  MultiNode
  QuorumBound
  FencingTokenBound
  SingleCommitLeader

Host Authority
  HardwareRootAttested
  NonceBound
  MeasurementBound
  ReleaseBound
  ModelBound

KV Authority
  CrossHostLineageBound
  SingleAuthoritativeHolder
  GenerationMonotonic
  TransferReadbackBound
  NoForeignShard
  NoFork

Transparency
  FederatedWitnessQuorum
  OperatorDiversityBound
  SplitViewDenied

Release
  MultiBuilderReproducible
  InputManifestBound
  ReleaseMeshCertificateBound

Safety
  NoCrossHostSplitBrain
  NoDualWriter
  NoDuplicateCommit
```

Next patch:

```text
ASH-ATTN-DECODE-W9G

Cross-Region Decode Authority /
WAN-Aware KV Shard Scheduling /
Regional Quorum Hierarchy /
Hardware-Backed Key Unsealing /
Live Session Migration /
No Cross-Region Authority Fork Seal
```
