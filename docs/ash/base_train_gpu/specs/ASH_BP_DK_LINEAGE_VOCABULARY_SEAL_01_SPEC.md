# ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01

## Data-Plane Revision / Policy Generation / Qualification Generation Axis Separation / Legacy R1-R2 Token Quarantine / Non-Semantic Patch Identity / Cross-Generation Adoption Contract

## 0. Status

```text
Patch ID: ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01
Direct parent: ASH-LINEAGE-RECONCILIATION-00
Role: ASH BP-DeltaK semantic vocabulary authority
Change class: registry schema / vocabulary helper / static validator / CF1 wiring
Runtime algorithm change: forbidden
Optimizer mathematics change: forbidden
Delta-K formula change: forbidden
Fusion/Fission predicate change: forbidden
Policy threshold change: forbidden
Production pointer change: forbidden
Existing patch ID/source-file rename: forbidden
Legacy R1/R2 token deletion: forbidden
Patch-number / Git-date semantic inference: forbidden
Parallel lineage registry: forbidden
```

Current bake implementation:

```text
tools/ash_lineage_reconciliation_00_registry.py
tools/ash_lineage_vocabulary_01.py
tools/validate_ash_bp_dk_lineage_vocabulary_seal_01.py
tools/run_ash_bp_dk_lineage_vocabulary_seal_01.ps1
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

The 00 registry remains the single lineage SSOT. 01 enriches its descriptors; it does not introduce a competing registry.

## 1. Central SSOT

```text
PATCH ID
!= DATA-PLANE REVISION
!= POLICY GENERATION
!= QUALIFICATION GENERATION

Latest Patch != Latest Data Plane
Latest Policy Generation != Effective Production Policy
Qualification Generation != Production Activation
Higher Patch Number != Higher Authority
```

Existing `R1`, `R2`, `R2A`... strings remain immutable historical identity only.

## 2. Canonical axes

### Data plane

```text
bp-dk-data-plane/observation/v1
bp-dk-data-plane/bridge/v1
bp-dk-data-plane/candidate-graph/v1
bp-dk-data-plane/active-fusion/v1
```

### Policy generations

```text
bp-dk-policy/legacy/g1
bp-dk-policy/production-aware/g2
```

### Qualification generations

```text
bp-dk-qualification/legacy/g1
bp-dk-qualification/production-aware/g2
```

Canonical axis identifiers do not use bare legacy `R1/R2` semantic segments.

## 3. Registry vocabulary fields

`LineageDescriptor` is extended with:

```text
legacy_revision_tokens
owned_data_plane_revision
target_data_plane_revision
owned_policy_generation
target_policy_generation
owned_qualification_generation
accepted_qualification_generations
generation_relations
vocabulary_binding_status
```

Binding states:

```text
Exact
HistoricalAliasOnly
EvidenceInsufficient
Contradictory
```

No missing generation is defaulted to G1, G2, latest, parent, or current pointer state.

## 4. Data-plane mapping

```text
00 -> observation/v1
01 -> observation/v1
02 -> observation/v1

03A -> bridge/v1
03B -> bridge/v1

04 -> candidate-graph/v1
05 -> active-fusion/v1
```

06 through 11 target `active-fusion/v1`; they do not create another Fusion execution generation.

03A remains explicitly parameter-local:

```text
same parameter only
Right / Down canonical adjacency
no cross-parameter Bridge
```

The historical generation-wide PRE barrier roadmap is not revived by vocabulary reconciliation.

## 5. 05 authority

05 owns:

```text
bp-dk-data-plane/active-fusion/v1
```

05 can consume a policy artifact but does not thereby own a PolicyGeneration:

```text
consumer of policy != owner of policy generation
```

## 6. Runtime qualification distinction

08A and 08B-R1 qualify the active-Fusion runtime/data plane. They are not policy `QualificationGeneration` owners.

08A therefore binds as:

```text
owned_data_plane_revision = none
target_data_plane_revision = bp-dk-data-plane/active-fusion/v1
status = QualificationOnly
```

## 7. Policy Generation G1

Canonical:

```text
bp-dk-policy/legacy/g1
```

Members:

```text
12 Calibration Recommendation
13 Operator Review
14 Candidate Canary Qualification
15 Explicit Production Activation
16 Production Soak / Rollback Health
17 Long-Horizon Stability
```

`legacy` means the first policy-control contract generation, not invalid/deprecated runtime.

## 8. Qualification Generation G1

Canonical:

```text
bp-dk-qualification/legacy/g1
```

Owned by 13 and 14.

15 owns no qualification generation and explicitly accepts only:

```text
bp-dk-qualification/legacy/g1
```

with an explicit `QualifiedBy` relation.

## 9. Policy Generation G2

Canonical:

```text
bp-dk-policy/production-aware/g2
```

Members:

```text
18 Production Evidence Recalibration Bridge
19 Production Evidence Calibration Adoption
20 Production-Aware Recommendation
21 Production-Aware Operator Review Adoption
```

18 explicitly carries:

```text
owned_policy_generation = production-aware/g2
target_policy_generation = legacy/g1
relation = CalibratedFrom(legacy/g1)
```

19, 20, and 21 retain explicit `EvidenceFrom(legacy/g1)` relations for the legacy-generation baseline evidence they consume.

## 10. Qualification Generation G2

Canonical:

```text
bp-dk-qualification/production-aware/g2
```

21 owns the current G2 operator-review / qualification-ticket contract.

21 is not:

```text
physical canary
production activation
Muon execution
parameter mutation
```

Future 22 physical R2 canary remains G2 unless its qualification contract semantics actually change. Patch number `22` never means `g22`.

## 11. Cross-generation relation vocabulary

```text
SameGeneration
EvidenceFrom
CalibratedFrom
QualifiedBy
ActivatedFrom
SupersedesGeneration
```

Older-generation evidence may be consumed by a newer contract only through an explicit typed relation. Evidence reuse does not promote the older artifact into newer-generation authority.

## 12. Explicit compatibility

Policy/data-plane compatibility:

```text
bp-dk-policy/legacy/g1
 -> bp-dk-data-plane/active-fusion/v1

bp-dk-policy/production-aware/g2
 -> bp-dk-data-plane/active-fusion/v1
```

Qualification/policy compatibility:

```text
bp-dk-qualification/legacy/g1
 -> bp-dk-policy/legacy/g1

bp-dk-qualification/production-aware/g2
 -> bp-dk-policy/production-aware/g2
```

Equal struct shape, field names, digest length, or patch proximity are not compatibility evidence.

## 13. Legacy alias quarantine

Diagnostic aliases:

```text
legacy R1 policy
 -> bp-dk-policy/legacy/g1

production-aware R2 policy
 -> bp-dk-policy/production-aware/g2

legacy R1 qualification
 -> bp-dk-qualification/legacy/g1

production-aware R2 qualification
 -> bp-dk-qualification/production-aware/g2
```

Historical physical R2 is deliberately isolated as:

```text
historical-roadmap/physical-r2
```

It is not Policy G2 or Qualification G2. R2A through R2E remain `HistoricalAliasOnly`.

## 14. Latest vs effective state

Current source-tree semantic heads:

```text
bp_dk_data_plane_head = 05
bp_dk_data_plane_revision = bp-dk-data-plane/active-fusion/v1

bp_dk_policy_control_head = 21
latest_policy_generation = bp-dk-policy/production-aware/g2

bp_dk_qualification_head = 21
latest_qualification_generation = bp-dk-qualification/production-aware/g2
```

Source-tree lineage does not establish the durable active production pointer, therefore:

```text
effective_policy_generation = unknown
effective_policy_evidence_status = EvidenceInsufficient

effective_qualification_generation = unknown
effective_qualification_evidence_status = EvidenceInsufficient
```

Forbidden fallback:

```text
latest == effective
```

## 15. No semantic inference

Forbidden semantic assignment from:

```text
filename contains R2
patch ends in -21
numeric revision >= N
Git commit date
parent numeric suffix
```

Missing binding remains `EvidenceInsufficient`.

## 16. Canonical vocabulary digest

`tools/ash_lineage_vocabulary_01.py` owns deterministic canonical serialization and SHA-256 vocabulary digest over:

```text
patch_id
legacy_revision_tokens
owned/target data-plane revision
owned/target policy generation
owned qualification generation
accepted qualification generations
generation relations
vocabulary revision
schema revision
```

The digest is evidence identity only, never production policy-selection authority.

## 17. Static validator

`tools/validate_ash_bp_dk_lineage_vocabulary_seal_01.py` verifies at minimum:

```text
all current BP-DK 00-21 patches have Exact bindings
canonical axes contain no legacy R1/R2 semantic segment
00-02 observation/v1
03A-03B bridge/v1
04 candidate-graph/v1
05 active-fusion/v1
06-21 target active-fusion/v1 where applicable
12-17 Policy G1
13-14 Qualification G1
15 accepts only Qualification G1
18-21 Policy G2
21 Qualification G2
18 explicit CalibratedFrom G1
19-21 explicit legacy EvidenceFrom relation
historical physical R2 isolated from Policy/Qualification G2
latest and effective production generations separated
vocabulary digest determinism
no runtime vocabulary-token leakage
CF1 ordering
negative masquerade fixtures
```

Negative fixtures cover:

```text
05 owning Policy G1 because it consumes policy
18 owning data-plane v2 because docs say R2
21 masquerading as Qualification G1
15 accepting Qualification G2
historical R2A becoming production-aware Policy G2
missing generation being silently defaulted
```

## 18. CF1 integration

Required order:

```text
...
21 static validator
ASH-LINEAGE-RECONCILIATION-00 validator
ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01 validator
```

No parent validator is removed or moved ahead of its existing dependency.

## 19. Runtime preservation and packaging

01 is vocabulary/static work only.

Required parent/full comparison:

```text
crates/               byte-preserved
apps/                 byte-preserved
vendor_fork_scaffold/ byte-preserved
```

Deliverables:

```text
Overlay code ZIP
 -> changed source/tool files only

Full applied code ZIP
 -> complete 00 body plus 01 changes
```

Excluded from code ZIPs:

```text
*.md
*.sha256
__pycache__
*.pyc
generated manifests
generated receipts
generated reports
artifact directories
```

## 20. Baked static evidence

```text
ASH-LINEAGE-RECONCILIATION-00:
130 / 130 PASS

ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01:
306 / 306 PASS

registered lineage descriptors = 32
Exact vocabulary bindings = 25
HistoricalAliasOnly nodes = 5
explicit cross-generation relations = 5

Policy Generation counts:
G1 = 6
G2 = 4

Qualification Generation counts:
G1 = 2
G2 = 1
```

Existing BP-DeltaK 00 through 21 static validators were re-run against the 01 full body without failure.

```text
crates/               BYTE_PRESERVED
apps/                 BYTE_PRESERVED
vendor_fork_scaffold/ BYTE_PRESERVED
```

This is static/source evidence only. No new GPU, model-quality, training-convergence, or physical Fusion evidence is claimed.

## 21. Non-goals / next revision

01 does not implement:

```text
parameter-local PRE snapshot authority
generation completeness audit
training-generation provenance closure
control/data-plane startup provenance binding
R2 physical canary
Muon runtime decomposition
historical evidence file quarantine
```

Next:

```text
ASH-BP-DK-PARAMETER-PRE-SNAPSHOT-AUTHORITY-02
```

## 22. Final seal

```text
PATCH NUMBER IS IDENTITY, NOT SEMANTICS
R1 AND R2 ARE LEGACY TOKENS, NOT AUTHORITY

DATA-PLANE REVISION IS AN EXECUTION AXIS
POLICY GENERATION IS A POLICY-CONTRACT AXIS
QUALIFICATION GENERATION IS AN EVIDENCE-CONTRACT AXIS

LATEST DOES NOT MEAN ACTIVE
ACTIVE DOES NOT MEAN LATEST

NO GENERATION IS INFERRED
NO GENERATION IS DEFAULTED
NO GENERATION MASQUERADES AS ANOTHER

EXISTING PATCH IDENTITIES REMAIN IMMUTABLE
THE VOCABULARY CHANGES
THE WORKING ENGINE DOES NOT
```
