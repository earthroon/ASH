# ASH-GPU-EVIDENCE-COMPACTION-07

## Canonical-Index GPU Witness / Compact Readback / Evidence-Sealed Commit Binding

### 0. Status

| Field | Authority |
|---|---|
| Patch ID | `ASH-GPU-EVIDENCE-COMPACTION-07` |
| Parent B06 | `ASH-HYBRID-OPTIMIZER-DISJOINT-DEVICE-COMMIT-06` |
| Parent B05 | `ASH-TENSORCUBE-HIMUON-DEVICE-CANDIDATE-05` |
| Parent B04 | `ASH-TENSORCUBE-MUON-RESIDENT-STATE-GRAPH-04` |
| Completion authority | A01 exact tracked submission |
| Scratch authority | A02 usage-segregated arena |
| Compact readback authority | A03 compact readback ring |
| Evidence schema | `ASH_GPU_EVIDENCE_COMPACTION_V1` |
| Mandatory witness | deterministic integer `BitPatternWitness256` |
| Numerical payload authority | device candidate / resident state, not host Vec |
| Validation class in this bake | `STATIC_SOURCE_ONLY` |
| Physical qualification in this environment | **not executed** |
| Active C07 physical admission | **not claimed**; B06 Active is still physically closed |

C07 answers:

> After B05/B06 remove candidate bulk readback, what compact, reproducible evidence may B06 consume without reconstructing the candidate on the host?

The answer is not “a magic checksum.” C07 separates:

```text
structural truth
+ IEEE-754 classification truth
+ canonical-index bit-pattern witness
+ physical evidence-kernel qualification
```

The witness is intentionally described as a **non-cryptographic compact payload witness**. It is never advertised as collision-free mathematical proof.

---

## 1. Authority chain

```text
B04  committed Muon state
B05  sealed Muon candidate
B06  full-trainable generation commit authority
C07  compact numerical-evidence authority
```

C07 does not become a second candidate owner and does not mutate candidate payloads.

```text
Candidate payload authority = B04/B05/B06 backing
Evidence authority          = C07
Commit authority            = B06
```

---

## 2. Evidence domains

Mandatory C07 domains are:

```text
FullTrainableWeight
MuonMomentum
AdamWFirstMoment
AdamWSecondMoment
```

`MuonOrthogonalUpdate` is a candidate-time evidence domain and may be sealed before its scratch lease is reclaimed.

A domain record contains:

```text
element count
finite count
NaN count
+Inf count
-Inf count
subnormal count
negative-zero count
strict-negative count
max-abs IEEE bits
BitPatternWitness256
partial count
evidence attempt ordinal
```

---

## 3. Runtime numerical gates

For committed-state candidate domains:

```text
finiteCount == elementCount
NaN count = 0
+Inf count = 0
-Inf count = 0
```

For `AdamWSecondMoment` additionally:

```text
strictNegativeCount = 0
```

Negative zero is tracked separately and is not counted as strict negative.

Muon momentum and orthogonal update are allowed to contain ordinary negative finite values.

---

## 4. Canonical index SSOT

Witness identity is bound to **canonical logical element indices**, not physical buffer-local positions.

For every evidence element:

```text
exact IEEE-754 f32 bits
+ canonical element index
+ evidence domain tag
+ fixed schema mixing constants
```

contribute to the witness.

Therefore, with one schema and one logical payload:

```text
physical segment reorder
physical allocation reorder
Fused pair discovery order
```

must not change the final witness as long as canonical indices remain identical.

Changing canonical indices **must** change the witness.

---

## 5. Bit-pattern witness

C07 defines:

```rust
BitPatternWitness256 { lanes: [u32; 8] }
```

The exact host reference uses:

```rust
f32::to_bits()
```

and the GPU uses:

```wgsl
bitcast<u32>(value)
```

NaN payload bits and signed zero are therefore not canonicalized away during Mirror qualification.

Mandatory aggregation uses only order-independent integer operations:

```text
u32 XOR
wrapping u32 SUM
u32 MAX for absolute-bit diagnostic
```

Float atomic sums are not equality authority.

---

## 6. No cryptographic overclaim

`BitPatternWitness256` is a deterministic compact witness, not a cryptographic payload hash.

Allowed:

```text
receipt_hash = cryptographic hash of compact receipt metadata
```

Forbidden terminology:

```text
cryptographic tensor proof
collision-free tensor hash
mathematical proof of payload correctness
```

C07 gains trust through Mirror qualification against the exact host reference and through structural/generation seals, not through an unsupported collision claim.

---

## 7. Two-stage GPU reduction

C07 introduces two dedicated WGSL surfaces:

```text
shaders/gpu_evidence_partial.wgsl
shaders/gpu_evidence_reduce.wgsl
```

Existing Local Muon, fused HiMuon, AdamW, and training-math WGSL are not modified by C07.

### Stage 1

Each source segment is read directly from its existing device backing:

```text
candidate/resident source READ
→ workgroup classification
→ integer witness reduction
→ fixed partial record
```

The partial shader uses workgroup atomics only on integer words.

### Stage 2

```text
partial atlas READ
→ deterministic serial integer reduction
→ one compact final domain record
```

The final record is 32 u32 words, currently 128 bytes, below the 1 KiB compact ABI budget.

---

## 8. No giant staging copy

C07 must not first concatenate segmented candidate buffers into a giant evidence source buffer.

Each `GpuEvidenceSegmentBinding` carries:

```text
domain
canonical start
element count
physical source element offset
PhysicalAllocationId
semantic role
segment ordinal
Arc<wgpu::Buffer>
```

The shader reads the original device allocation and receives the canonical index separately.

---

## 9. Dynamic A01 evidence source leases

Evidence domain segment count is runtime-dependent. A fixed `&'static str` lease site ID cannot represent every actual source allocation without collapsing lifetime evidence.

C07 therefore extends the A01 submission-lease key from:

```text
&'static str
```

to:

```text
String
```

for `SubmissionLeaseSpec.site_id` and `TrackedSubmission.lease_ids`.

Existing literal callsites remain valid through `impl Into<String>`.

C07 creates one A01 read lease per evidence source segment:

```text
c07.evidence.source.0
c07.evidence.source.1
...
```

This is a lifetime-accounting extension only. It does not alter A01 completion semantics.

---

## 10. A02 scratch authority

C07 uses A02 for:

```text
GpuEvidenceParams      UNIFORM | COPY_DST
GpuEvidencePartial     STORAGE
GpuEvidenceFinal       STORAGE | COPY_SRC
```

Evidence scratch is ephemeral physical capacity, not a persistent semantic cache.

After A01 exact completion and evidence readback:

```text
params
partial atlas
final evidence buffer
```

are reclaimed through A02.

---

## 11. A03 compact readback authority

The final evidence record is copied to an A03 compact readback lease.

```text
GpuEvidenceFinal
→ A03 whole MAP_READ slot
→ 128-byte host record
```

C07 does not create `EvidenceReadbackPool` or any second MAP_READ allocator.

A03 whole-buffer MAP_READ lifecycle remains authoritative.

---

## 12. A01 completion remains blocking in C07

C07 calls the existing exact submission path and waits using A01 before reading compact evidence.

C07 explicitly does **not** implement:

```text
async retirement
poll removal
submission coalescing
```

Those belong to C08.

---

## 13. Evidence attempt identity

Evidence is bound to candidate and evidence attempts.

Conceptually:

```text
target generation
candidate attempt ordinal
evidence attempt ordinal
```

form the attempt identity.

Stage-1 partials carry the evidence attempt. Stage 2 rejects domain/attempt mismatches.

Stale or duplicate partial evidence may never be silently merged into the current record.

---

## 14. Coverage binding

C07 record counts are cross-checked against the existing optimizer ownership authorities.

```text
FullTrainableWeight.elementCount
= B06 total trainable elements

MuonMomentum.elementCount
= Muon-owned elements

AdamWFirstMoment.elementCount
= AdamW-owned elements

AdamWSecondMoment.elementCount
= AdamW-owned elements
```

C07 does not recalculate ownership.

---

## 15. Mirror qualification

C07 runtime modes:

```text
OFF
MIRROR_VERIFIED
ACTIVE_COMPACT
```

`MIRROR_VERIFIED` requires B06 Mirror.

The bake wires a one-time physical qualification call before optimizer execution when C07 is enabled. Qualification runs synthetic GPU fixtures through the same C07 executor and compares them with the Rust host reference.

Mandatory fixture classes include:

```text
all five evidence domains
signed zero
NaN payload
+Inf / -Inf
subnormal
physical segment reorder with stable canonical indices
```

Qualification requires exact parity of:

```text
classification counts
maxAbsBits
BitPatternWitness256
```

The current container did not execute this GPU qualification. The code path is wired; physical PASS must be produced on the target runtime.

---

## 16. Kernel qualification identity

`EvidenceKernelQualificationReceipt` binds:

```text
C07 schema revision
GPU evidence shader digest
host-reference digest
fixture count
per-domain exact parity
canonical reorder parity
classification parity
```

`ACTIVE_COMPACT` may consume evidence only when the current kernel/schema match the qualification receipt.

A static source pass is not a qualification receipt.

---

## 17. Current rollout boundary

The B06 parent currently keeps physical Active device commit closed because:

```text
real AdamW device-resident W/M/V candidate backing is not yet production-qualified
DeviceSegmentedGenerationV1 next-step consumer is not connected
```

Therefore this C07 bake provides:

```text
physical Mirror evidence-kernel qualification path
+
Active evidence ABI / B06 binding
```

but does not claim physical Active C07 admission.

No host payload is wrapped in a fake device evidence ticket to manufacture an Active pass.

---

## 18. Candidate evidence receipt

C07 defines a candidate receipt carrying:

```text
schema
candidate/target identity
canonical layout digest
ownership digest
domain records
compact readback bytes
bulk candidate readback bytes
evidence submission epochs
evidence sealed flag
receipt hash
```

The receipt hash is self-checked by clearing the hash field, serializing the canonical receipt, recomputing SHA-256, and requiring exact equality with the supplied `receipt_hash`. The same self-check applies to the evidence-kernel qualification receipt.

Canonical layout and ownership digests must match the current B06 generation metadata before B04 is evidence-sealed. C07 also rejects duplicate segment ordinals and overlapping canonical/physical source ranges inside one evidence-domain execution.

In Active mode:

```text
bulk_candidate_readback_bytes = 0
```

is mandatory.

---

## 19. B04 post-evidence mutation seal

A compact witness is worthless if the candidate may be rewritten afterward.

B04 therefore carries:

```text
c07_evidence_sealed_generation
```

and checks candidate writes in both candidate preparation and physical-completion paths.

After:

```text
seal_c07_evidence_generation(N+1)
```

any new write attempt targeting N+1 fails with:

```text
FAIL_C07_POST_EVIDENCE_MUTATION
```

The seal is cleared only when the candidate is committed or aborted and its generation lifecycle is closed.

---

## 20. B06 evidence binding

C07 stages a `CompactCandidateEvidenceBinding` into B06.

When C07 Active is required, `FullModelDeviceCommitPermit` must bind:

```text
candidate evidence receipt hash
evidence schema revision
evidence sealed = true
bulk candidate readback bytes = 0
```

B06 Active no-fail metadata commit asserts that its required compact evidence exists.

B06 Mirror does not pretend C07 replaces the existing host-authoritative candidate path.

---

## 21. Candidate evidence to committed evidence

B06 Active promotion is metadata/role promotion and performs no payload rewrite.

Therefore a future committed-generation evidence reference may adopt the exact sealed candidate evidence without recomputing the full payload, provided:

```text
post-evidence mutation = 0
commit payload rewrite = 0
exact candidate evidence hash is bound to commit permit
```

If B06 ever gains a payload-rewriting commit implementation, this invariant must be revoked and post-commit evidence regenerated.

---

## 22. Production BaseTrain integration

`ProductionMuonExecutionRuntime` owns one `GpuEvidenceRuntime`.

Initialization enforces the mode matrix against B06.

When C07 is enabled, the scheduler calls:

```text
qualify_c07_evidence_if_enabled(device, queue)
```

before the optimizer candidate execution.

The Active handoff ABI is:

```text
stage_c07_candidate_evidence(receipt)
```

which:

```text
validates domain coverage/invariants
seals B04 candidate generation
stages the C07 runtime receipt
binds the receipt into B06
```

The current production scheduler does not fabricate an Active full-candidate receipt because the B06 physical Active prerequisite is not yet satisfied.

---

## 23. Evidence telemetry

C07 records at minimum:

```text
evidence bundle count
partial record count
expected partial count
dedicated evidence submission count
compact readback bytes
bulk candidate readback bytes
Mirror host witness count
Mirror witness mismatch count
nonfinite reject count
AdamW-V negative reject count
coverage mismatch count
stale partial reject count
post-evidence mutation count
schema mismatch count
kernel mismatch count
evidence chain count
```

No evidence counter is represented as physical VRAM measurement.

---

## 24. Active target

Once B06 Active itself is physically qualified, C07 Active target is:

```text
Muon candidate weight bulk D2H = 0
Muon candidate momentum bulk D2H = 0
Muon update bulk D2H = 0

AdamW candidate weight bulk D2H = 0
AdamW M bulk D2H = 0
AdamW V bulk D2H = 0

compact evidence D2H <= compact ABI budget
post-evidence mutation = 0
```

Explicit committed-state durability materialization remains a separate B06 boundary and is not counted as candidate bulk D2H.

---

## 25. Forbidden changes

C07 must not:

```text
claim a cryptographic tensor proof
create a second readback pool
turn primary STORAGE buffers into MAP_READ buffers
use float reduction as exact-equality authority
recalculate optimizer ownership
mutate optimizer math WGSL
silently materialize candidate host Vecs in Active mode
remove A01 exact waits
coalesce submissions for performance
introduce mixed precision
```

---

## 26. Failure classes

```text
FAIL_C07_RUNTIME_MODE_UNKNOWN
FAIL_C07_MODE_MATRIX

FAIL_C07_SCHEMA_MISMATCH
FAIL_C07_KERNEL_QUALIFICATION_MISSING
FAIL_C07_KERNEL_DIGEST_MISMATCH

FAIL_C07_CANDIDATE_ID_MISMATCH
FAIL_C07_GENERATION_MISMATCH
FAIL_C07_EVIDENCE_ATTEMPT_MISMATCH

FAIL_C07_STALE_PARTIAL_EVIDENCE
FAIL_C07_PARTIAL_EVIDENCE_GAP
FAIL_C07_DUPLICATE_PARTIAL_EVIDENCE
FAIL_C07_EVIDENCE_COVERAGE_MISMATCH

FAIL_C07_NONFINITE_WEIGHT
FAIL_C07_NONFINITE_MUON_MOMENTUM
FAIL_C07_NONFINITE_ADAM_M
FAIL_C07_NONFINITE_ADAM_V
FAIL_C07_NONFINITE_MUON_UPDATE
FAIL_C07_NEGATIVE_ADAM_V

FAIL_C07_MIRROR_WITNESS_MISMATCH
FAIL_C07_POST_EVIDENCE_MUTATION

FAIL_C07_BULK_READBACK_ACTIVE
FAIL_C07_COMPACT_READBACK_OVERFLOW
FAIL_C07_UNQUALIFIED_ACTIVE_EVIDENCE
FAIL_C07_PAYLOAD_PROOF_OVERCLAIM
```

---

## 27. Static source validation

The bake carries:

```text
tools/ash_gpu_evidence_compaction_07_static_validate.py
```

The source gate verifies, among other things:

```text
C07 Rust module/export/spec exist
exact two new C07 evidence WGSL files exist
parent optimizer WGSL remains byte-identical
Stage1/Stage2 shaders use integer exact witness operations
no isFinite/isNan/isInf dependency
no float atomic equality authority
canonical index is part of witness mixing
host f32::to_bits reference exists
A01 dynamic evidence site IDs are supported
A02 scratch and A03 compact ring are reused
no EvidenceReadbackPool exists
B04 post-evidence mutation seal exists
B06 permit binds C07 evidence
scheduler wires Mirror qualification
current Active physical admission remains closed by parent B06 prerequisites
Cargo manifests remain parent-identical
C08 wait removal is absent
mixed precision is absent
```

`STATIC_SOURCE_ONLY` does not imply Rust typecheck or physical GPU qualification.

---

## 28. Promotion criteria

### Mirror qualification

```text
C07 mode = MIRROR_VERIFIED
B06 mode = MIRROR_VERIFIED
current schema/kernel identity exact
all synthetic and production qualification fixtures exact
Mirror witness mismatch count = 0
classification parity = true
canonical reorder parity = true
```

### Active qualification

Requires B06 Active physical admission first, then:

```text
C07 mode = ACTIVE_COMPACT
current kernel qualification receipt valid
all required candidate domains present
all required counts exact
nonfinite counts = 0
AdamW V strict-negative count = 0
candidate bulk D2H = 0
compact evidence within ABI budget
B04 evidence seal active before B06 commit
post-evidence mutation count = 0
B06 permit contains exact evidence receipt hash/schema
```

The present static bake does not claim these physical Active criteria have run.

---

## 29. C08 handoff

After B06 Active and C07 Active are physically qualified, the remaining major hotpath synchronization is the exact blocking wait inherited from A01.

C08 may then ask:

```text
How can exact A01 completion/lifetime truth be preserved
without synchronously blocking the CPU after every candidate/evidence submission?
```

C07 itself deliberately leaves that problem untouched.

### Center declaration

> **C07 does not make a large GPU tensor trustworthy by giving it a fancy checksum name. It binds exact IEEE-754 bit patterns to canonical logical indices, reduces them with deterministic integer operations, qualifies that reduction against a Rust reference in Mirror mode, and seals the candidate against subsequent writes. Active B06 may consume only the exact sealed compact evidence receipt. The payload remains on the GPU, the evidence crosses the compact A03 ring, and the distinction between witness, structural proof, and cryptographic receipt remains explicit.**
