# ASH-WGPU-D10-MIRROR-QUALIFICATION-ADMISSION-CLOSURE-10A

## 0. Status and parent

- Patch ID: `ASH-WGPU-D10-MIRROR-QUALIFICATION-ADMISSION-CLOSURE-10A`
- Parent authority: `ASH-WGPU-PRODUCTION-SSOT-PUBLICATION-10`
- Purpose: close the unpublished Mirror qualification admission deadlock without changing D09 promotion semantics or D10 publication-journal semantics.
- Production canonical authority remains the D10 publication journal head.
- This patch cannot mint a D09 permit and cannot publish D10.

## 1. Problem statement

The physical Mirror qualification stack requires the exact mode profile:

```text
B04 = ACTIVE_VERIFIED
B05 = MIRROR_VERIFIED
B06 = MIRROR_VERIFIED
C07 = MIRROR_VERIFIED
C08 = MIRROR_VERIFIED
```

B04 must be Active because B05/B06 Mirror execution needs the real persistent resident committed/candidate backing. The previous D10 unpublished admission used `any_active()` as the authority classifier. Therefore B04 Active alone caused the whole stack to be misclassified as a D09 full-Active physical candidate, which then required B05-B08 Active and `C08_CANDIDATE`. That was an authority-classification deadlock, not a backend-mode invariant.

10A replaces boolean Active detection as the unpublished admission SSOT with an exact whole-profile classifier.

## 2. Authority classes

`RuntimePublicationAuthorityClass` adds:

```text
UNPUBLISHED_MIRROR_QUALIFICATION
```

The complete conceptual set remains:

```text
UNPUBLISHED_DIAGNOSTIC
UNPUBLISHED_MIRROR_QUALIFICATION
D09_PHYSICAL_CANDIDATE
PUBLISHED_CANONICAL
PUBLISHED_DIAGNOSTIC_DOWNGRADE
```

`UNPUBLISHED_MIRROR_QUALIFICATION` is explicitly:

```text
publicationDigest = null
productionCanonical = false
mirrorQualification = true
d09PhysicalCandidate = false
```

It is a qualification authority only. It is not a production authority and not a promotion permit.

## 3. Exact unpublished profile classifier

Unpublished startup admits only exact classified profiles.

### 3.1 Diagnostic

```text
B04 OFF
B05 OFF
B06 OFF
C07 OFF
C08 OFF
```

Result:

```text
authorityClass = UNPUBLISHED_DIAGNOSTIC
productionCanonical = false
```

A `C08_CANDIDATE` lane with this profile is rejected because the D09 candidate lane requires the full Active profile.

### 3.2 Mirror qualification

```text
B04 ACTIVE_VERIFIED
B05 MIRROR_VERIFIED
B06 MIRROR_VERIFIED
C07 MIRROR_VERIFIED
C08 MIRROR_VERIFIED
```

Result:

```text
authorityClass = UNPUBLISHED_MIRROR_QUALIFICATION
productionCanonical = false
publicationDigest = null
```

No D09 lane may be attached to this profile. This prevents Mirror evidence from acquiring D09 authority.

### 3.3 D09 physical candidate

```text
B04 ACTIVE_VERIFIED
B05 ACTIVE_DEVICE_CANDIDATE
B06 ACTIVE_VERIFIED
C07 ACTIVE_COMPACT
C08 ACTIVE_ASYNC
```

This profile is admitted only with:

```text
ASH_D09_BENCHMARK_LANE=C08_CANDIDATE
```

Result:

```text
authorityClass = D09_PHYSICAL_CANDIDATE
productionCanonical = false
```

### 3.4 Mixed profiles

Any unpublished profile not matching the three exact classes is rejected with:

```text
FAIL_D10_UNPUBLISHED_MIXED_MODE_PROFILE
```

No silent downgrade to OFF or Mirror is allowed.

## 4. State ownership / SSOT

D10 owns:

```text
whole-stack runtime authority class
publication/canonical status
Mirror qualification privilege
D09 physical candidate privilege
```

B04 owns:

```text
resident graph allocation
committed/candidate resident generations
resident partition lifecycle
```

B05 owns:

```text
device Muon candidate production and address parity
```

B06 owns:

```text
full trainable generation identity
Muon/AdamW disjoint ownership closure
Mirror/Active commit coordination
```

C07 owns:

```text
GPU evidence kernel qualification
candidate evidence sealing and parity
```

C08 owns:

```text
submission completion
async map lifecycle
deferred retirement
```

The exact profile classifier is the single unpublished admission SSOT. Component modules do not infer whole-stack authority independently.

## 5. B04 Active is a qualification substrate

In `UNPUBLISHED_MIRROR_QUALIFICATION`, B04 Active does not imply production promotion.

Its purpose is to provide the physical F32 resident backing required to test:

```text
committed weight
candidate weight
committed momentum
candidate momentum
orthogonal update scratch
```

The Mirror chain retains reference/host commit authority.

## 6. Mirror execution semantics

### B05

Mirror must execute a real device candidate and verify:

```text
canonical packed address parity
model projection parity
physical B04 partition parity
written Muon coverage exact
range gap = 0
duplicate write = 0
physical overlap = 0
AdamW intrusion = 0
```

Bulk candidate readback may exist in Mirror because it is verification traffic. D09 Active later requires candidate bulk D2H to be zero.

### B06

Mirror must observe:

```text
prepare count > 0
mirror commit count > 0
Muon + AdamW = total trainable
overlap = 0
unclassified = 0
missing = 0
duplicate write = 0
partial commit violation = 0
```

The device candidate is not the final commit authority in Mirror.

### C07

Mirror qualification must prove two separate layers:

1. current kernel qualification receipt is valid;
2. real candidate evidence path executed and host/reference witness parity passed.

A fixture-only kernel qualification is insufficient for final 10A physical PASS.

Required candidate evidence conditions:

```text
evidenceBundleCount > 0
mirrorHostWitnessCount > 0
mirrorWitnessMismatchCount = 0
nonfiniteRejectCount = 0
coverageMismatchCount = 0
postEvidenceMutationCount = 0
```

### C08

Mirror qualification requires:

```text
qualification receipt valid
completion callback armed > 0
completion callback observed > 0
deferred retirement > 0
retired > 0
```

C08 Mirror may retain exact waits as parity authority. D09 Active later requires hot-path waits to be zero.

## 7. Admission before B04

D10 classification remains pre-B04.

Required order:

```text
read B04-B08 requested modes
classify exact unpublished profile
seal D10 runtime admission receipt
write admission receipt to run output
then create ProductionMuonRuntime/B04 resident graph
```

10A must not allocate B04 first and classify authority afterward.

## 8. Early admission receipt

`d10_runtime_admission_receipt.json` is written immediately after successful authority admission and before Muon runtime construction.

This is required because later existing N8 gates may intentionally terminate with HOLD after compute/durable closure. A later HOLD must not erase the evidence describing which D10 authority admitted the run.

The same sealed receipt is passed into `ProductionMuonRuntime::load_or_initialize_with_admission`; the runtime must not independently reclassify the same startup and create split authority.

## 9. Mirror physical execution receipt

Mirror runs additionally emit:

```text
d10_mirror_qualification_execution_receipt.json
```

The receipt binds:

```text
source/final model generation
source/final optimizer step
exact B04-B08 modes
B04 resident observation
B05 Mirror execution/coverage
B06 Mirror prepare/commit
C07 kernel qualification
C07 real candidate evidence execution/parity
C08 qualification/callback/retirement
committed-state mutation violations
publication journal mutation count
productionCanonical
publicationDigest
qualificationPass
self hash
```

It is written before asserting PASS so failure/HOLD still leaves a diagnosis artifact.

## 10. Physical PASS gate

`PASS_ASH_D10_UNPUBLISHED_MIRROR_QUALIFICATION` is emitted only when all mandatory observations are true.

`READY_ASH_D09_FULL_ACTIVE_PHYSICAL_CANDIDATE` is emitted only after the same receipt passes.

Minimum PASS conditions:

```text
B04 resident graph observed
B05 Mirror executed with exact Muon coverage
B06 Mirror prepare + commit observed
C07 kernel qualified
C07 real candidate evidence executed
C07 host/reference witness parity passed
C08 async qualification valid
C08 callback completion observed
C08 deferred retirement observed
committed-state mutation violation count = 0
publication journal mutation count = 0
productionCanonical = false
publicationDigest = null
```

If the mode profile was admitted but required physical execution is absent, the gate is:

```text
HOLD_D10_MIRROR_QUALIFICATION_NOT_EXECUTED
```

Admission and execution are not conflated.

## 11. Generation preservation

Mirror failure cannot mutate the previously committed generation outside the normal reference/host commit authority.

Candidate failure must never cause an autonomous B05/B06 device promotion.

The receipt records B04 committed-state mutation violations and requires zero for PASS.

## 12. No authority leakage

Mirror qualification cannot:

```text
create a D09 BenchmarkPromotionPermit
write a D10 publication journal entry
write a revocation entry
set productionCanonical=true
set publicationDigest
claim D09_PHYSICAL_CANDIDATE
```

`publicationJournalMutationCount` is fixed to zero for this authority class and validated.

## 13. Published runtime behavior unchanged

If `ASH_D10_PUBLICATION_ROOT` is present, D10 published admission remains authoritative. 10A's unpublished classifier is not used to bypass a publication.

Existing behavior remains:

```text
exact published profile -> PUBLISHED_CANONICAL
explicit allowed downward profile -> PUBLISHED_DIAGNOSTIC_DOWNGRADE
revision/ABI/device/backend/build/workload/numerical/ownership/WGSL mismatch -> reject
revoked head -> reject
```

## 14. D09 semantics unchanged

10A does not change:

```text
D09 schema V2
D09 runtime-mode identity digest
physical benchmark requirement
candidate bulk D2H = 0 requirement
candidate hot-path wait = 0 requirement
BenchmarkPromotionPermit hash/identity rules
```

Mirror qualification has its own runtime mode digest label and does not masquerade as the D09 Active candidate identity.

## 15. D10 publication semantics unchanged

10A does not change:

```text
exact publication scope
D09 permit validation
prepare/publish CAS
immutable monotonic journal
generation filename authority
previous-digest chain
rollback-by-new-generation
immutable revocation
runtime ABI identity
WGSL tree identity
```

No publication artifact is baked into the source package.

## 16. Failure codes

Mandatory classification/admission failures include:

```text
FAIL_D10_UNPUBLISHED_MIXED_MODE_PROFILE
FAIL_D10_MIRROR_PROFILE_D09_AUTHORITY_FORBIDDEN
FAIL_D10_MIRROR_PROFILE_PRODUCTION_CANONICAL_FORBIDDEN
FAIL_D10_MIRROR_PROFILE_PUBLICATION_FORBIDDEN
FAIL_D10_D09_CANDIDATE_LANE_REQUIRED
FAIL_D10_D09_CANDIDATE_PROFILE_REQUIRED
FAIL_D10_MIRROR_AUTHORITY_RECEIPT_MISMATCH
FAIL_D10_D09_AUTHORITY_RECEIPT_MISMATCH
FAIL_D10_MIRROR_JOURNAL_MUTATION
HOLD_D10_MIRROR_QUALIFICATION_NOT_EXECUTED
```

## 17. Static matrix

At minimum the validator must prove:

| B04 | B05 | B06 | C07 | C08 | D09 lane | Result |
|---|---|---|---|---|---|---|
| OFF | OFF | OFF | OFF | OFF | none/baseline | Diagnostic |
| ACTIVE | MIRROR | MIRROR | MIRROR | MIRROR | none | Mirror qualification |
| ACTIVE | ACTIVE | ACTIVE | ACTIVE | ACTIVE | C08_CANDIDATE | D09 physical candidate |
| ACTIVE | ACTIVE | ACTIVE | ACTIVE | ACTIVE | none | FAIL |
| ACTIVE | OFF | OFF | OFF | OFF | none | FAIL |
| ACTIVE | ACTIVE | MIRROR | MIRROR | MIRROR | none | FAIL |
| ACTIVE | MIRROR | ACTIVE | MIRROR | MIRROR | none | FAIL |
| ACTIVE | MIRROR | MIRROR | ACTIVE | MIRROR | none | FAIL |
| ACTIVE | MIRROR | MIRROR | MIRROR | ACTIVE | none | FAIL |
| OFF | MIRROR | MIRROR | MIRROR | MIRROR | none | FAIL |
| ACTIVE | MIRROR | MIRROR | MIRROR | MIRROR | C08_CANDIDATE | FAIL |

## 18. Completion gates

10A source closure requires:

```text
exact classifier exists
`any_active()` is not the unpublished admission authority
Mirror authority enum exists
Mirror is noncanonical and publication-free
D09 candidate remains lane-gated full Active only
mixed unpublished profiles hard-fail
early admission receipt write precedes Muon runtime construction
same admission receipt is injected into runtime
Mirror execution receipt exists
execution receipt is written before PASS assertion
fixture-only C07 qualification cannot produce final Mirror PASS
no publication journal mutation
D09/D10 publication semantics preserved
D10 static validator PASS
10A static validator PASS
cargo check -p base_train PASS on user physical tree
release build PASS on user physical tree
```

## 19. State transition

```text
D10 STATIC_READY / UNPUBLISHED
        |
        | exact Mirror profile
        v
UNPUBLISHED_MIRROR_QUALIFICATION
        |
        | physical execution receipt PASS
        v
READY_FOR_D09_ACTIVE_CANDIDATE
        |
        | exact full Active + C08_CANDIDATE
        v
D09_PHYSICAL_CANDIDATE
        |
        | D09 V2 physical benchmark PASS
        v
BenchmarkPromotionPermit
        |
        v
D10 PREPARE -> PUBLISH P1 -> PUBLISHED_CANONICAL
```

10A closes only the Mirror admission and evidence boundary. It does not skip any later physical promotion gate.
