# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-CONTROL-PLANE-R1

## 0. Revision Identity

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-CONTROL-PLANE-R1`

Admission environment:

`ASH_UNIFIED_ATLAS_MCU_CONTROL_PLANE_R1=1`

Runtime PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_CONTROL_PLANE_R1`

Static PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_CONTROL_PLANE_R1_STATIC`

## 1. Purpose

Establish one process-wide Unified Atlas MCU control-plane authority above the existing Atlas/chunk/segment execution paths without moving numerical or persistent data-plane ownership.

R1 centralizes only:

- Atlas geometry namespace;
- Wave identity and ordinal namespace;
- Slot identity and slot-generation namespace;
- Credit namespace vocabulary;
- Submission/completion observation namespace;
- Canonical commit ordinal namespace;
- Logical retirement namespace;
- subsystem registration.

R1 does not yet transfer GPU execution ownership from legacy subsystems to the MCU.

## 2. Data-Plane SSOT Preservation

The following remain authoritative where they are today:

- current weight: `ResidentWeightPack`;
- successor weight: `ResidentWeightPackBuilder`;
- Adam M/V: `RamResidentAdamMv`;
- gradient: existing gradient accumulator authority;
- Muon state: existing TensorCube Muon state authority;
- vocab/embedding/LM-head weight: existing weight authority.

The MCU must not own full weight, gradient, Adam M/V, candidate payloads, Muon momentum, embedding, or LM-head tensors.

`data_plane_owner_changed=false` is mandatory for R1.

## 3. MCU Ownership

The process-wide `UnifiedAtlasMcuR1` owns only control-plane metadata:

- `Unified Wave ID`;
- `Unified Wave Ordinal`;
- `Unified Slot ID`;
- `Unified Slot Generation`;
- `Unified Commit Ordinal`;
- active-wave ledger;
- live slot-lease ledger;
- aggregated observation counters.

There must be one production MCU singleton per process. Per-subsystem MCU authorities are forbidden.

## 4. Shared Geometry Authority

Canonical R1 geometry:

- Atlas page bytes: `16,777,216`;
- slot count: `3`.

At MCU boot, exact parity is required across the currently existing geometries:

- Vocab micro-atlas page bytes;
- Vocab ring slot count;
- Gradient page bytes;
- AdamW scheduler chunk bytes;
- Adam M/V PCIe transfer window bytes;
- Adam M/V transfer slot count;
- Muon atlas page authority.

Geometry mismatch fails closed with an `E_UNIFIED_ATLAS_MCU_GEOMETRY_PARITY_MISMATCH:*` token.

R1 does not delete legacy geometry constants. It binds and checks them against the shared MCU geometry namespace.

## 5. Subsystem Registry

Required registered families:

- `Gradient`;
- `AdamW`;
- `TensorCubeMuon`;
- `VocabEmbedding`;
- `LMHead`.

Execution ownership modes:

- `LegacyExternal`;
- `MCUOwned`.

R1 production execution remains `LegacyExternal`. The `MCUOwned` namespace exists only for later adoption revisions.

No dual execution authority is permitted.

## 6. Unified Wave Identity

Canonical schema contains at least:

- Wave ID;
- Wave ordinal;
- subsystem ID;
- parameter index;
- parameter ID;
- source generation;
- source optimizer step;
- target generation;
- target optimizer step;
- logical element start/count;
- byte start/count;
- optional slot ID;
- optional slot generation.

Wave ID is identity. Wave ordinal is ordering authority. They are not interchangeable.

## 7. Slot Lease Identity

A reusable slot is identified by:

`Slot ID + Slot Generation`

The same live slot lease identity may not own two live waves.

R1 rejects:

- slot ID outside the shared slot count;
- partial slot identity where only ID or only generation exists;
- duplicate live slot leases;
- step termination with a still-live slot lease.

## 8. Slot Lifecycle Vocabulary

The canonical state vocabulary is:

`Free -> Reserved -> Preparing -> Submitted -> Executing -> CompletionObserved -> CommitReady -> Committing -> LogicallyRetired -> Free`

R1 does not force all legacy paths to be physically driven by this state machine yet. It establishes the vocabulary and exact observation namespace for later adoption.

## 9. Logical Retirement

`logical_retired=true` does not mean backing allocation destruction.

R1 explicitly separates:

- semantic payload retirement;
- physical host/GPU backing memory destruction.

Backing slots and slabs may be reused by later slot generations. This is the contract required by the later bounded-slot adoption revisions.

## 10. Bounded MCU Ledger

MCU bookkeeping must not become an unbounded RAM consumer.

R1 requires an explicit bounded active-wave ledger. Retired wave payloads are removed from the active ledger and only aggregate counters / terminal receipts remain.

The MCU may not retain full parameter payloads.

## 11. Legacy Observation Adapter

R1 provides an observation API for legacy execution:

- boot/register;
- observe legacy wave;
- observe completion;
- observe commit;
- observe logical retirement;
- emit step-level receipt.

The initial physical wiring is intentionally narrow: existing AdamW segmented work is mirrored into the MCU namespace without altering its numerical execution, transfer ring, commit, or data ownership.

Muon, Vocab/Embedding/LMHead, and Gradient are registered in R1 but execution ownership migration is deferred to their explicit adoption revisions.

This avoids a false claim that MCU R1 already executes all subsystem waves.

## 12. AdamW Mirror Binding

For each existing AdamW segment, R1 binds:

- source-record parameter index;
- parameter ID;
- source/target generation;
- source/target optimizer step;
- exact logical element start/count;
- exact byte start/count;
- legacy transfer slot ID/generation when a PCIe lease exists.

The MCU observes completion only after the legacy candidate batch returns.

The MCU observes commit only after the legacy M/V RAM update and existing transfer-ring commit boundary.

The wave is then logically retired from the MCU active ledger.

No AdamW numerical behavior is changed.

## 13. Commit Ordering

The MCU owns a monotonic commit ordinal namespace.

Observed legacy commits must not regress relative to MCU wave ordinals.

R1 does not repair a legacy ordering mismatch by sorting receipts. A regression fails closed.

## 14. Required Runtime Witnesses

Boot:

`[ASH-UNIFIED-ATLAS-MCU-BOOT-R1]`

Subsystem registration:

`[ASH-UNIFIED-ATLAS-MCU-SUBSYSTEM-R1]`

Wave:

`[ASH-UNIFIED-ATLAS-MCU-WAVE-R1]`

Completion:

`[ASH-UNIFIED-ATLAS-MCU-COMPLETION-R1]`

Commit:

`[ASH-UNIFIED-ATLAS-MCU-COMMIT-R1]`

Retirement:

`[ASH-UNIFIED-ATLAS-MCU-RETIREMENT-R1]`

Step:

`[ASH-UNIFIED-ATLAS-MCU-STEP-R1]`

Final R1 receipt:

`[ASH-BASETRAIN-UNIFIED-ATLAS-MCU-CONTROL-PLANE-R1]`

## 15. Final R1 Receipt Requirements

The final control-plane witness must state at least:

- `mode=MirrorObservedLegacy`;
- geometry page bytes = 16 MiB;
- geometry slot count = 3;
- geometry parity = true;
- wave authority owner = UnifiedAtlasMcu;
- slot identity authority owner = UnifiedAtlasMcu;
- slot generation authority owner = UnifiedAtlasMcu;
- commit namespace owner = UnifiedAtlasMcu;
- execution authority owner = LegacySubsystems;
- data-plane authority changed = false;
- numerical behavior changed = false;
- bounded MCU ledger = true;
- historical `1,044,033,536` allocation owner remains unclaimed;
- verdict = PASS.

## 16. Historical Allocation Boundary

R1 must preserve:

`historical_1044033536_owner_claimed=false`

The raw `1,044,033,536`-byte allocation is not attributed by this revision.

Exact allocation owner attribution is reserved for:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LARGE-TRANSIENT-ALLOCATION-OWNER-ATTRIBUTION-R1`

## 17. No False Performance Claim

R1 does not claim:

- async overlap active;
- triple-slot MCU execution active;
- bulk candidate D2H retired;
- global wait retired;
- 7-minute optimizer-step wall time fixed;
- historical 1GB allocation eliminated.

Those are later revisions.

## 18. Existing Closure Preservation

R1 must preserve all currently closed axes including:

- immutable N2 parent authority;
- RAM36 hard budget;
- BP-Delta-K target optimizer generation binding;
- Muon full candidate retirement;
- Muon full source scratch retirement;
- Muon host scratch slab reuse;
- per-tile heap churn retirement;
- vocab full-GPU-residency rejection;
- gradient full-host-materialization rejection.

## 19. Static Acceptance

Static validator must establish:

- one process-wide MCU singleton;
- one shared 16 MiB / 3-slot geometry namespace;
- all required subsystem IDs registered;
- legacy and future MCU execution-owner namespaces distinct;
- bounded active ledger;
- wave/slot/commit/retirement witness paths present;
- scheduler geometry bindings present;
- AdamW segment mirror binding present;
- no full tensor payload fields inside MCU;
- historical 1GB owner not claimed;
- runtime PASS token present.

## 20. Physical Acceptance

R1 physical qualification requires:

- MCU boot reached;
- all required subsystem families registered;
- geometry parity PASS;
- observed AdamW waves use unique MCU wave IDs;
- known transfer slots use unique slot ID/generation leases;
- completion precedes commit;
- commit order does not regress;
- retirement empties the active ledger by step terminal;
- no numerical/data-plane authority change;
- previous closures remain PASS.

This R1 does not require Muon/Vocab/Gradient execution ownership migration.

## 21. Closure Meaning

R1 CLOSED means:

- one unified Atlas control plane exists;
- one geometry namespace exists;
- one wave identity namespace exists;
- one slot ID/generation namespace exists;
- one commit ordinal namespace exists;
- legacy AdamW work can be mirrored through the MCU vocabulary;
- remaining subsystem families are registered for later explicit adoption;
- data-plane SSOT remains unchanged;
- numerical execution remains legacy-owned and unchanged.

R1 CLOSED does not mean all execution is MCU-owned.
