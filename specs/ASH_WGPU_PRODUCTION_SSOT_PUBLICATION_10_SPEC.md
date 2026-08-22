# ASH-WGPU-PRODUCTION-SSOT-PUBLICATION-10

## Physical Permit Bound Production Authority / Immutable Publication Journal / Startup Admission

### 0. Status

| Field | Authority |
|---|---|
| Patch ID | `ASH-WGPU-PRODUCTION-SSOT-PUBLICATION-10` |
| Parent | `ASH-WGPU-BENCHMARK-PROMOTION-09` |
| Physical promotion input | D09 `BenchmarkPromotionPermit` |
| Production canonical authority | D10 publication journal head |
| Publication storage | immutable monotonic `P{generation}.json` journal |
| Active without publication | forbidden except explicit D09 physical candidate lane |
| Silent fallback | forbidden |
| Rollback | new monotonic publication generation |
| Optimizer math change | none |
| Backend/WGSL change | none |
| Current bake publication state | `UNPUBLISHED` |
| Validation class | `STATIC_SOURCE_ONLY` |

D10 is not another optimizer or GPU-performance patch. It answers one final question:

> Which exact, physically benchmarked runtime profile is allowed to call itself production canonical?

The answer is not “the newest code”, “the branch that merged”, or “the path whose static validator passed”. The answer is the latest valid D10 publication whose embedded D09 physical permit, candidate identity, ABI identity, exact scope, and runtime profile all validate.

---

## 1. Final authority chain

```text
A00 buffer authority
A01 lifetime
A02 arena
A03 transfer
B04 resident Muon state
B05 device candidate
B06 full-generation commit
C07 compact evidence
C08 async retirement
D09 physical benchmark permit
D10 production publication
```

D09 may prove that a candidate deserves promotion. D10 alone publishes that promotion as production SSOT.

---

## 2. D09 parent hardening before first physical permit

No physical D09 promotion permit existed when D10 was introduced.

D10 therefore hardens `BenchmarkRunIdentity` before any permit can become durable production evidence. D09 schema moves from V1 to:

```text
ASH_WGPU_BENCHMARK_PROMOTION_V2
```

The candidate identity now additionally binds:

```text
numerical_policy_digest
runtime_abi_digest
wgsl_tree_digest
```

The runtime-mode digest is also checked against the actual production semantic snapshot containing:

```text
B04 mode
B05 mode
B06 mode
C07 mode
C08 mode
C07 qualification state
C08 active physical admission state
segmented successor capability
```

A D09 V1 sample or permit cannot be used by D10.

This is a parent identity correction, not a retroactive physical performance claim.

---

## 3. D10 publication request

A new publication request contains exactly:

```text
BenchmarkPromotionPermit
BenchmarkRunIdentity
ProductionRuntimeAbiIdentity
ProductionRuntimeProfile
```

Publication scope is **derived from the D09 candidate identity**. The caller does not supply a broader scope.

This eliminates a class of accidental scope inflation during publication.

---

## 4. D09 permit gate

D10 revalidates the permit hash using the exact D09 permit serialization contract.

Required:

```text
patch ID exact
baseline != HistoricalRecorded
valid sample count > 0
physicalBenchmarkPassed = true
numerical parity = true
generation parity = true
lifetime parity = true
evidence parity = true
candidate bulk D2H = 0
candidate hot-path blocking waits = 0
permit self-hash exact
```

Failure:

```text
FAIL_D10_D09_PROMOTION_PERMIT_REQUIRED
FAIL_D10_D09_PERMIT_HASH_MISMATCH
FAIL_D10_D09_PHYSICAL_PROMOTION_REQUIRED
```

Static-ready D09 state cannot mint production publication.

---

## 5. Candidate revision binding

```text
permit.candidateIdentityHash
==
candidateIdentity.identityDigest
```

and the candidate identity itself includes the exact code revision.

Any candidate revision drift requires a new D09 physical permit.

Branch names are not authority.

---

## 6. Runtime ABI identity

D10 defines:

```text
ProductionRuntimeAbiIdentity
```

with explicit B04/B05/B06/C07/C08 ABI/schema digests.

Its self-hash must equal:

```text
candidateIdentity.runtimeAbiDigest
```

D10 does not infer ABI compatibility from file names or patch order.

---

## 7. Canonical profile

The D10 v1 publication target is the physically benchmarked full Active chain:

```text
B04 ACTIVE_VERIFIED
B05 ACTIVE_DEVICE_CANDIDATE
B06 ACTIVE_VERIFIED
C07 ACTIVE_COMPACT
C08 ACTIVE_ASYNC
```

The profile carries the exact D09 `runtimeModeDigest` and a D10 profile self-hash.

A Mirror or partial-Active profile cannot be relabeled as the benchmarked Active publication.

---

## 8. Exact-only publication scope in v1

D10 v1 intentionally does not implement universal GPU or workload-class publication.

Scope is exact:

```text
device identity digest
backend
vendor id
device id
build identity digest
workload digest
numerical policy digest
optimizer routing digest
registry digest
runtime mode digest
runtime ABI digest
WGSL tree digest
```

This exact scope is mechanically derived from the D09 candidate identity.

Therefore:

```text
one RTX 3080 / DX12 permit
!=
all NVIDIA GPUs
```

and:

```text
one workload digest
!=
all model sizes
```

Device-class or workload-class expansion requires a future independently qualified publication model.

---

## 9. Publication journal is the SSOT

D10 does not use a mutable `current.json` file as production authority.

Canonical storage is:

```text
<publication-root>/publications/P0000000000000001.json
<publication-root>/publications/P0000000000000002.json
...
```

The head is the highest **contiguous, fully valid** publication generation.

Every journal entry validates:

```text
self hash
D09 permit
candidate identity
runtime ABI
scope
profile
previous publication digest
monotonic generation
```

An invalid publication file is an error. Runtime does not silently skip it and fall back to an older head.

---

## 10. Atomic publish model

D10 publication is PREPARE then COMMIT.

### PREPARE

Fallible work:

```text
D09 permit validation
candidate identity validation
ABI validation
exact scope derivation
profile validation
current journal-head capture
next generation selection
prepared self-hash
```

### COMMIT

The publication is serialized to a temporary file in the publication directory, flushed with `sync_all`, and renamed to the not-yet-existing next-generation journal path.

The final filename is immutable.

If another publisher wins the same next generation first, the second publisher fails with a stale-head error instead of overwriting it.

No existing publication file is modified.

---

## 11. Head compare-and-swap semantics

Prepared publication stores:

```text
expectedPreviousPublicationDigest
publicationGeneration
```

Immediately before COMMIT, D10 re-reads the journal head.

If the head changed:

```text
FAIL_D10_PUBLICATION_HEAD_CHANGED
```

This provides publication-generation CAS semantics without a mutable authority pointer.

---

## 12. Publication object

`ProductionOptimizationPublication` embeds:

```text
publication generation
previous publication digest
full D09 permit
full D09 candidate identity
runtime ABI identity
exact publication scope
canonical runtime profile
optional rollback target digest
publication self-hash
```

The publication remains self-contained for startup verification.

---

## 13. Rollback is a new publication

Rollback never rewinds the journal head.

If current is P4 and the operator wants the runtime profile previously published as P2:

```text
P5 = new publication
     payload authority copied from P2
     previous = P4
     rollbackOf = P2
```

The history remains monotonic and auditable.

Rollback target must already be a valid, non-revoked D10 publication.

---

## 14. Revocation

Revocations are immutable records under:

```text
<publication-root>/revocations/<publication-digest>.json
```

A revoked current head fails production admission until an explicit rollback/new publication is performed.

D10 does not silently roll back on revocation.

---

## 15. Runtime admission

Before BaseTrain constructs B04-B08 runtime modes it calls:

```text
enforce_runtime_publication_authority_from_environment()
```

This is important. D10 is not a post-hoc log check. It executes before Active runtime admission.

---

## 16. Production publication configuration

Runtime publication root:

```text
ASH_D10_PUBLICATION_ROOT
```

Observed deployment identity:

```text
ASH_D10_RUNTIME_OBSERVED_IDENTITY
```

The observed identity binds:

```text
code revision
runtime mode digest
workload digest
device identity digest
backend
build identity digest
numerical policy digest
optimizer routing digest
registry digest
runtime ABI digest
WGSL tree digest
```

The observed record is self-hashed.

---

## 17. Published canonical admission

For a publication-backed canonical run, all observed fields must exactly match the publication scope/candidate identity.

The environment-projected B04-B08 modes must also exactly equal the publication profile.

Then the runtime receipt is:

```text
authorityClass = PUBLISHED_CANONICAL
productionCanonical = true
admitted = true
```

The environment is only a projection of the published profile. It cannot expand publication authority.

---

## 18. No upward environment override

If publication permits a lower mode and the environment requests a stronger mode, or if no publication exists and the environment requests Active production:

```text
FAIL_D10_UNPUBLISHED_ACTIVE_OVERRIDE
```

Environment/configuration cannot mint production Active authority.

---

## 19. Explicit diagnostic downgrade only

A published Active profile may be intentionally run at a lower diagnostic mode only when:

```text
ASH_D10_ALLOW_DIAGNOSTIC_DOWNGRADE=1
```

and every selected mode is no stronger than the published profile.

Such a run is admitted as:

```text
authorityClass = PUBLISHED_DIAGNOSTIC_DOWNGRADE
productionCanonical = false
```

There is no silent fallback.

---

## 20. Pre-publication D09 Active exception

A circular gate must be avoided: D09 must benchmark the Active candidate before D10 can publish it.

Therefore publication-free Active is allowed only when:

```text
ASH_D09_BENCHMARK_LANE=C08_CANDIDATE
```

and the environment profile is the complete Active B04-B08 profile.

The runtime receipt is explicitly:

```text
authorityClass = D09_PHYSICAL_CANDIDATE
productionCanonical = false
publicationDigest = null
```

This exception cannot be interpreted as production publication.

Any other publication-free Active startup is rejected.

---

## 21. Publication-free non-Active runtime

OFF/Shadow/Mirror development or qualification runs may still run without a publication.

They receive:

```text
authorityClass = UNPUBLISHED_DIAGNOSTIC
productionCanonical = false
```

This keeps D10 bake usable before the first physical D09 permit while preserving the rule that unpublished Active is not production canonical.

---

## 22. Runtime admission receipt

Every ProductionMuonRuntime carries:

```text
ProductionRuntimeAdmissionReceipt
```

and the scheduler writes:

```text
d10_runtime_admission_receipt.json
```

for each production invocation.

The receipt exposes:

```text
authority class
publication generation/digest
canonical profile digest
observed identity digest
revision match
ABI match
device/backend/workload match
numerical-policy match
ownership-policy match
WGSL-tree match
profile match
diagnostic override
productionCanonical
admitted
self-hash
```

This becomes the answer to “what authority did this run actually use?”.

---

## 23. D09 semantic receipt records D10 status

The D09 semantic identity snapshot additionally records:

```text
D10 authority class
D10 productionCanonical flag
D10 publication digest
```

A pre-publication physical candidate therefore cannot be confused with a published production measurement later.

These D10 fields are deliberately excluded from the D09 B04-B08 runtime-mode digest because publication status changes after promotion while the benchmarked runtime modes do not.

---

## 24. D10 CLI

The bake adds:

```text
ash_wgpu_production_ssot_publication_10
```

Commands:

```text
seal-abi
seal-profile
seal-observed
prepare
publish
rollback
revoke
admit
inspect
```

The CLI does not run D09 benchmark and does not edit a D09 permit.

---

## 25. No baked publication artifact

The source bake contains:

```text
D10 code
D10 CLI
D10 spec
D10 static validator
```

but contains no:

```text
BenchmarkPromotionPermit output
PreparedProductionPublication output
ProductionOptimizationPublication journal entry
ProductionPublicationReceipt output
RevocationRecord output
```

The current source tree is therefore structurally D10-ready but **UNPUBLISHED**.

---

## 26. No optimizer semantic changes

D10 changes no:

```text
Muon formula
AdamW formula
ownership routing
B04 resident buffer topology
B05 candidate topology
B06 commit math
C07 evidence WGSL
C08 completion semantics
```

The burn WebGPU backend and WGSL tree must remain byte-identical to D09 parent.

D10 operates at BaseTrain control/publication authority only.

---

## 27. Static gate

The bake carries:

```text
tools/ash_wgpu_production_ssot_publication_10_static_validate.py
```

It verifies at minimum:

```text
D10 module export
D10 CLI registration
D09 V2 identity hardening
D09 runtime-mode digest bound to semantic B04-B08 state
D09 permit self-hash revalidation
physical permit requirement
candidate identity exact binding
runtime ABI exact binding
scope derived from candidate identity
Active profile exact gate
immutable publication journal
contiguous generation validation
prepared-head CAS
atomic temp-to-final publish
rollback creates next generation
revocation records
runtime authority check before B04 runtime construction
unpublished Active rejected
D09 candidate exception explicitly non-canonical
silent fallback absent
runtime admission receipt written by scheduler
no backend source change
no WGSL change
no baked publication result
```

Static validation does not publish a production SSOT.

---

## 28. Failure classes

```text
FAIL_D10_D09_PROMOTION_PERMIT_REQUIRED
FAIL_D10_D09_PERMIT_HASH_MISMATCH
FAIL_D10_D09_PHYSICAL_PROMOTION_REQUIRED

FAIL_D10_CANDIDATE_REVISION_MISMATCH
FAIL_D10_RUNTIME_ABI_MISMATCH
FAIL_D10_WGSL_TREE_MISMATCH
FAIL_D10_BUILD_IDENTITY_MISMATCH
FAIL_D10_NUMERICAL_POLICY_MISMATCH
FAIL_D10_OWNERSHIP_POLICY_MISMATCH

FAIL_D10_PUBLICATION_SCOPE_EXPANSION
FAIL_D10_DEVICE_SCOPE_MISMATCH
FAIL_D10_BACKEND_SCOPE_MISMATCH
FAIL_D10_WORKLOAD_SCOPE_MISMATCH

FAIL_D10_RUNTIME_PROFILE_MISMATCH
FAIL_D10_UNPUBLISHED_ACTIVE_OVERRIDE
FAIL_D10_SILENT_FALLBACK_ATTEMPT

FAIL_D10_PUBLICATION_GENERATION_GAP
FAIL_D10_PUBLICATION_HEAD_CHANGED
FAIL_D10_PUBLICATION_DIGEST_MISMATCH
FAIL_D10_PREVIOUS_PUBLICATION_INVALID

FAIL_D10_ROLLBACK_TARGET_NOT_PUBLISHED
FAIL_D10_REVOKED_PUBLICATION

FAIL_D10_RUNTIME_PUBLICATION_REVISION_DRIFT
FAIL_D10_RUNTIME_PUBLICATION_ABI_DRIFT
FAIL_D10_RUNTIME_OBSERVED_IDENTITY_REQUIRED
```

---

## 29. Promotion sequence

Current sequence after this bake is:

```text
D10 source bake
→ STATIC_READY / UNPUBLISHED

B06 Active physical adoption
→ C07 Active physical qualification
→ C08 Active physical qualification
→ D09 C08_CANDIDATE physical benchmark
→ D09 BenchmarkPromotionPermit
→ D10 prepare
→ D10 publish
→ PUBLISHED_CANONICAL
```

D10 code existence does not skip any of those steps.

---

## 30. Center declaration

> **A00 through C08 define how the optimized runtime works. D09 decides whether one exact physical candidate deserves promotion. D10 decides whether that exact candidate is allowed to become production truth. Publication is an immutable monotonic journal entry derived from the D09 candidate identity, not a mutable flag or environment variable. An unpublished Active path may exist only as an explicitly labeled D09 physical candidate; it can never call itself production canonical. A published runtime must match revision, ABI, WGSL tree, numerical policy, device/backend, workload, ownership, and mode profile exactly, or startup is rejected rather than silently falling back.**
