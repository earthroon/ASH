# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF7

## D10 R3B PHYSICAL ATTRIBUTION ACTIVE-CANDIDATE / C08-MIRROR CANARY PROFILE

### Revision

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF7

Class:
D10 NON-PROMOTING CANARY AUTHORITY
R3B ACTIVE-CANDIDATE PHYSICAL ATTRIBUTION
C08 MIRROR BOUNDARY PRESERVATION

Direct parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF6
```

CF7 starts after CF6 physically established exact FreshGenesis source lifetime and the first failure moved to:

```text
ASH_C08_ASYNC_RETIREMENT_QUALIFICATION_FAILED:
FAIL_C08_ACTIVE_PHYSICAL_ADMISSION_MISSING
```

## 1. Parent physical conclusion

CF6 witnesses established:

```text
pre-cache             generation=0 optimizer_step=0 cursor=0 exact
post-cache            generation=0 optimizer_step=0 cursor=0 exact
parent binding        generation/step/cursor exact
pre-Adam hydration    source_identity_exact=true
                      budget_exact=true
CANARY budget         requested=2 expected=2
```

Therefore the N8 FreshGenesis / budget blocker is crossed. CF7 does not modify that source lineage.

## 2. Existing C08 boundary

Current C08 ActiveAsync production promotion remains fail-closed. Existing source and prior specs do not authorize synthesizing:

```text
active_physical_admission=true
```

for the unfinished ActiveAsync path.

CF7 therefore does not change C08 qualification or P5 promotion logic.

## 3. Exact CF7 profile

CF7 admits exactly one CANARY-only unpublished profile:

```text
B04 = ActiveVerified
B05 = ActiveDeviceCandidate
B06 = ActiveVerified
C07 = ActiveCompact
C08 = MirrorVerified
```

and only when:

```text
cfg.training.admit_eve_mcu_close_r2_phys_canary_r1 = true
```

The same 5-mode tuple with CANARY=false is rejected by the CF7 classifier.

## 4. New D10 authority class

Materialized:

```text
RuntimePublicationAuthorityClass::R3bPhysicalAttributionCanary
UnpublishedRuntimeProfileClass::R3bPhysicalAttributionCanary
```

The exact profile predicate is:

```text
ProductionRuntimeProfile::exact_r3b_physical_attribution_canary_cf7()
```

It requires all five modes exactly. No fuzzy or downward match is accepted.

## 5. D10 admission contract

The environment admission path now receives the CANARY execution authority explicitly:

```text
enforce_runtime_publication_authority_from_environment_for_canary(canary_mode)
```

Existing no-argument admission remains as a wrapper with:

```text
canary_mode=false
```

so existing non-CANARY callsites cannot acquire the new authority class.

## 6. Receipt semantics

`ProductionRuntimeAdmissionReceipt` now records:

```text
r3b_physical_attribution_canary
```

Validation requires exact parity with the new authority class.

For CF7:

```text
r3b_physical_attribution_canary = true
mirror_qualification            = false
d09_physical_candidate          = false
production_canonical            = false
publication_digest              = None
```

The CANARY execution receipt remains independently fixed to:

```text
promotion_claim=false
```

CF7 creates no production promotion claim.

## 7. D10 CF7 witness

Successful unpublished CF7 admission emits:

```text
[ASH-D10-CF7][r3b-attribution-canary]
```

with:

```text
canary_mode=true
B04 ActiveVerified
B05 ActiveDeviceCandidate
B06 ActiveVerified
C07 ActiveCompact
C08 MirrorVerified
profile_exact=true
authority_class=R3bPhysicalAttributionCanary
promotion_claim=false
d09_physical_candidate_claim=false
c08_active_async_claim=false
admitted=true
```

No D09 lane is needed for this authority class.

## 8. Existing D09 profile preservation

The existing D09 physical-candidate profile remains:

```text
B04 ActiveVerified
B05 ActiveDeviceCandidate
B06 ActiveVerified
C07 ActiveCompact
C08 ActiveAsync
```

and still requires:

```text
BenchmarkLane::C08Candidate
```

CF7 does not alter its predicate or claim.

## 9. Existing mirror profile preservation

The existing unpublished mirror qualification remains exact and separate:

```text
B04 ActiveVerified
B05 MirrorVerified
B06 MirrorVerified
C07 MirrorVerified
C08 MirrorVerified
```

CF7 does not reuse `UnpublishedMirrorQualification` for the active B05/B06/C07 canary profile.

## 10. Runtime recheck

D10 pre-admission alone is insufficient. `ProductionMuonRuntime` now rechecks the actual runtime objects when the authority class is CF7.

Required actual runtime state:

```text
B04 resident state graph = ActiveVerified
B05 runtime              = ActiveDeviceCandidate
B06 coordinator          = ActiveVerified
C07 evidence runtime     = ActiveCompact
C08 retirement runtime   = MirrorVerified
```

Fail-closed errors:

```text
E_D10_CF7_RUNTIME_PROFILE_DRIFT:B04
E_D10_CF7_RUNTIME_PROFILE_DRIFT:B05
E_D10_CF7_RUNTIME_PROFILE_DRIFT:B06
E_D10_CF7_RUNTIME_PROFILE_DRIFT:C07
E_D10_CF7_RUNTIME_PROFILE_DRIFT:C08
```

Successful runtime parity emits:

```text
[ASH-D10-CF7][runtime-profile]
```

with all promotion/D09/C08-active claims false.

## 11. Trainable-session authority propagation

`build_trainable_session_admission_seal_r4a()` now passes:

```text
cfg.training.admit_eve_mcu_close_r2_phys_canary_r1
```

to D10 admission.

This keeps the CANARY authority in the sealed trainable-session environment instead of inferring it from environment strings or step count.

## 12. Scheduler fallback authority propagation

The non-R4A-hotpath fallback D10 admission in `production_multistep_loop_accumulation8_scheduler.rs` also passes the same CANARY config bit.

There is no hidden environment-only CF7 admission path.

## 13. C08 semantics

CF7 does not change:

```text
AsyncRetirementRuntimeMode
qualify_async_completion()
active_physical_admission
assert_active_ready()
P5 ActiveAsync qualification
pending-wave ActiveDeviceCandidate capability
```

When CF7 environment selects:

```text
C08 = MirrorVerified
```

`assert_active_ready()` is not the selected C08 authority path.

No `active_physical_admission` value is rewritten.

## 14. No D09 claim

The CF7 receipt and witnesses keep:

```text
d09_physical_candidate=false
```

Even if a stale D09 environment lane is present, the CF7 exact profile does not become the D09 ActiveAsync profile because C08 is MirrorVerified.

Recommended physical-run hygiene still removes the D09 lane environment variable.

## 15. No production publication

CF7 admission has:

```text
production_canonical=false
publication_generation=None
publication_digest=None
canonical_profile_digest=None
```

It does not mutate the D10 publication ledger.

## 16. R1K preservation

CF7 keeps the R1K-required active candidate chain:

```text
B04 ActiveVerified
→ B05 ActiveDeviceCandidate
→ B06 ActiveVerified
→ C07 ActiveCompact
```

R3B still requires real ActiveVerified candidate execution, R3A handoff, R3B materialization, CandidateComplete and the real R3B receipt.

CF7 does not synthesize any R3B state.

## 17. R1J/R1I preservation

No change to:

```text
SessionInjected reader subgroup authority
ResidentGraph reader authority
R7A1 producer/reader identity witness
queue-domain device parity guard
cross-device adoption guard
```

## 18. CF5/CF6 preservation

No change to:

```text
CANARY budget = 2
Full R1B budget = 8
FreshGenesis source identity checks
CF6 pre-cache witness
CF6 post-cache witness
CF6 parent-binding witness
CF6 pre-Adam witness
```

## 19. Actual source delta

Relative to the CF6 full code-only parent:

```text
ADD 0
MOD 4
DEL 0
```

Changed files:

```text
crates/base_train/src/d10_production_ssot_publication.rs
  parent: 4eefe4fe74de64cadf99c6d7bde74afdba65a764cae7172196784a5da793faf5
  CF7:    7c3d9686bd82118d5789cd96c1e801213988c55d009cdf7bae9149afa3b60122

crates/base_train/src/trainable_session_admission_profile_r4a.rs
  parent: d75a98515b5e9e3362244a8e4b5888654a5f4c32040bd0f11ed66ea353cf32a6
  CF7:    09659071afbd1b9e5ec79fe945aeeb6611686c9888b34ae90d3420eafec75562

crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
  parent: 144106ebbfed0cab14ee2501afe15c72648e0b32c85ca604303911be97d90bfa
  CF7:    f7c96871cee2169fed5393ea406949f900e65dd1f37f578f3dacea804fe2e85e

crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
  parent: 894f2961bfb85520dc0859f9e015c4e568a82b74b52527cc7a345a71b521b9e6
  CF7:    08fb802adbb9d9c2e5189163103b834159b76838a7065f4cff8d9cedeb0c4d0f
```

Source-delta digest:

```text
6ee758ef2d0e8f7133776dece35ae12edcb80c091036c066401ac0afdc65bb45
```

## 20. Key baked locations

```text
d10_production_ssot_publication.rs
  exact CF7 profile predicate             line 217
  new authority enum                      line 910
  CF7 classifier                          line 946
  CANARY-aware admission API              line 1218
  CF7 admission witness                   line 1350

trainable_session_admission_profile_r4a.rs
  CANARY authority propagation            line 416

production_multistep_loop_accumulation8_scheduler.rs
  fallback CANARY authority propagation   line 9457

tensorcube_local_muon_production_callsite_adoption.rs
  runtime exact-profile recheck           line 3609
  runtime CF7 witness                     line 3643
```

## 21. Archive seal

Full code-only archive:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF7_D10_R3B_ACTIVE_CANDIDATE_C08_MIRROR_CANARY_PROFILE_CODE_ONLY.zip
SHA-256:
9bf834071d143ed2013d42a64c65f3c86738a71f9095f2ab1cafc29c2db98513
Files: 8424
CRC: PASS
```

Overlay code-only archive:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF7_D10_R3B_ACTIVE_CANDIDATE_C08_MIRROR_CANARY_PROFILE_OVERLAY_CODE_ONLY.zip
SHA-256:
8eccff72203e4a7d37c043067d24c72c2785f1bdad907b59f89d2ef7eb14d213
Files: 4
CRC: PASS
```

Neither archive contains:

```text
specs/
artifacts/
this specification
new generated runtime manifest/receipt files
```

## 22. Static acceptance

Confirmed in the bake tree:

```text
exact CF7 five-mode predicate present
CANARY=true required for CF7 classification
CANARY=false wrapper preserved
new D10 authority class present
D09 authority remains distinct
existing mirror qualification remains distinct
CF7 receipt marks production_canonical=false
CF7 receipt marks d09_physical_candidate=false
C08 ActiveAsync profile is not accepted by CF7 predicate
C08 active_physical_admission source is unchanged
trainable-session CANARY propagation present
scheduler fallback CANARY propagation present
runtime B04/B05/B06/C07/C08 recheck present
CF5/CF6 scheduler logic preserved except D10 callsite propagation
```

## 23. Evidence boundary

Bake environment has no Cargo/Rust compiler.

Therefore:

```text
SOURCE       CONFIRMED
STATIC       CONFIRMED
ARCHIVE      CONFIRMED
COMPILE      NOT VERIFIED
RUNTIME      NOT VERIFIED
PHYSICAL     NOT VERIFIED
PERFORMANCE  NOT MEASURED
```

No C08 ActiveAsync PASS, D09 physical-candidate PASS, P5 PASS, R1K physical PASS or full A/B/C PASS is claimed.

## 24. Re-materialization contract

```text
dataset regeneration      NOT REQUIRED
R1A regeneration          NOT REQUIRED
R1A cursor regeneration   NOT REQUIRED
base_train rebuild         REQUIRED
Native CF1 reseal          REQUIRED
fresh CANARY root          REQUIRED
full A/B/C                 NOT REQUIRED FOR CF7 ATTRIBUTION
```

## 25. Physical acceptance

A CF7 physical run must use:

```text
CANARY=true
B04 ActiveVerified
B05 ActiveDeviceCandidate
B06 ActiveVerified
C07 ActiveCompact
C08 MirrorVerified
```

and demonstrate:

```text
D10 authority_class=R3bPhysicalAttributionCanary
promotion_claim=false
d09_physical_candidate_claim=false
c08_active_async_claim=false

runtime B04/B05/B06/C07/C08 exact parity

FAIL_C08_ACTIVE_PHYSICAL_ADMISSION_MISSING is not reached

execution continues into the R1K active-device candidate path
```

## 26. Completion law

CF7 may issue a local physical closure only when the exact non-promoting CANARY profile is admitted and physically revalidated while C08 remains MirrorVerified.

A later first failure belongs to the next attribution boundary.

CF7 does not promote C08 ActiveAsync, D09, P5, full R1B or A/B/C.

## Final law

> CF7 creates one exact non-promoting D10 doorway for R3B physical attribution.

> B04/B05/B06/C07 remain genuinely active. C08 remains genuinely MirrorVerified.

> The new authority is available only when the CANARY config is true. The same mixed profile outside CANARY remains unadmitted.

> No synthetic C08 physical admission, no D09 claim, no production publication, no promotion claim.
