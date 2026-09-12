# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1

## TWO-STEP PRODUCTION PHYSICAL ATTRIBUTION CANARY

### Scope

CANARY-R1 is a non-promoting short-horizon production path for EVE/MCU physical blocker attribution.

It preserves canonical model/dataset/session/optimizer/WGPU authority while reducing the execution horizon from the 24 optimizer steps of full A/B/C to exactly 2 optimizer steps.

```text
same canonical geometry
same canonical R1A fresh source
same production MCU / Adam / HiMuon authority
same gradient accumulation = 8
same route-sparse 154 Muon / 47 AdamW / 0 mixed semantics

canary optimizer steps = 2
micro-batches = 16
digest-only numerical capture
first-failure stop
promotion_claim = false
```

CANARY-R1 does not replace full A/B/C.

## Execution separation

New CLI:

```text
--eve-mcu-close-r2-phys-canary-r1
```

It is mutually exclusive with:

```text
--eve-mcu-close-r2-phys-r1b-full-production-abc
```

Conflict fails with:

```text
E_EVE_MCU_PHYS_EXECUTION_MODE_CONFLICT
```

The full A/B/C profile remains `FullAbc`, keeps 8 optimizer steps per leg, EVE close-R1, final `CloseAfterDurableWriteback`, and `CampaignModeR1::SuccessAbc`.

The canary profile is:

```text
CanaryTwoStep
production_loop_optimizer_steps = 2
EVE close-R1 leg ceremony disabled
EVE close-R2 production residency admitted under explicit canary authority
single active R4 production session
terminal invocation exit = KeepResident
```

Therefore CANARY-R1 does not request the full final durable writeback ceremony.

## Same-session authority contract

The canary retains:

```text
admit_trainable_session_active_production_owner_r4 = true
admit_trainable_session_cross_invocation_runtime_r4 = true
admit_trainable_session_sealed_admission_profile_r4a = true
admit_mcu_session_persistent_execution_fabric_r7 = true
admit_eve_mcu_close_r2 = true
```

R2-without-R1 is legal only when:

```text
admit_eve_mcu_close_r2_phys_canary_r1 = true
production_loop_optimizer_steps = 2
eve_mcu_close_r1_invocations = []
```

Any R1 + canary simultaneous admission fails closed.

The canary changes no optimizer arithmetic, route policy, model geometry, WGPU backend selection, Device/Queue ownership policy, R1H DK closure, R1I queue-domain guard, or R1J reader subgroup authority closure.

## Digest-only capture

After each committed optimizer step, CANARY-R1 records streaming SHA-256 evidence for:

```text
weights
Adam M
Adam V
HiMuon momentum
```

The digest hook runs after committed successor adoption.

It stores no full numerical tensor capture file and invokes no A/B/C numerical comparator.

Step receipts:

```text
eve_mcu_close_r2_phys_canary_r1_step_000001_digest.json
eve_mcu_close_r2_phys_canary_r1_step_000002_digest.json
```

Each step digest binds optimizer step, training generation, cursor next batch ordinal, loss, state byte lengths and SHA-256, MCU EVE authority instance ordinal, DeviceAuthorityId, QueueAuthorityId, and MCU session digest.

Successful two-step completion requires the same MCU session authority, DeviceAuthorityId, QueueAuthorityId and session digest across both step receipts.

## Completion contract

Successful CANARY-R1 requires:

```text
requested optimizer steps = 2
committed optimizer steps = 2
training generation = 2
optimizer step = 2
production micro-batches = 16
cursor next batch ordinal = 16
same session authority across both steps = true
full_tensor_capture_count = 0
abc_comparison_count = 0
durable_final_writeback_required = false
promotion_claim = false
```

Pass token:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1
```

Preflight token:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_PREFLIGHT
```

A non-parent first failure seals the canary receipt and terminates immediately with:

```text
HOLD_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_FIRST_FAILURE
```

The existing N8 / R6 parent HOLD emitted after a completed production loop is treated only as the parent terminal boundary after the two committed steps. It is not promoted as an error when the two-step canary evidence is complete.

## Source delta

Relative to the R1J full code-only parent:

```text
ADD 1
MOD 8
DEL 0
```

```text
MOD crates/base_train/src/bin/base_train.rs
560b1e643ca42c5dbe7b91025fc967a686c876cc0e09d7761c013e237089f7b0

MOD crates/base_train/src/config.rs
b161835de83dbe6644f2864bb3bdf909761785899d3e507290327e5aef384087

MOD crates/base_train/src/eve_mcu_close_physical_campaign_r1.rs
35e298561f47c81bc743520572421423dc7a1b414f5f95d781791dd45745a5ac

MOD crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs
dfd11b4aa3a77a7067d33dec6028490540249214ae29961abca6830c4df03891

ADD crates/base_train/src/eve_mcu_close_r2_physical_canary_r1.rs
018bc0e5883a5ec249c8740b31d464f038ec6de8842eba5f9678154c9a291adb

MOD crates/base_train/src/lib.rs
20fd510c9e1c37e0e0c48d6c4d4855c25bb8e62f7bb9fd62052533a2bcfcbefa

MOD crates/base_train/src/pipeline.rs
5fd5178f0f91927d870a96719d1e0e183fe17af95d7750b3c56508ce6dd53a26

MOD crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
7d7455bcb70225778e090f7bfe2fa35e425b4733ffb7426e2dbc67cad0dda2e4

MOD crates/base_train/src/trainable_session_active_production_owner_r4.rs
ce8c9fd5700fb0aa4a6b7352907f7bbfee01251400b2aa6d166a5d0c675d35bc
```

Source-delta digest:

```text
62df4766f6a6b2746fece75b4ee27a7387cdfd8317e259afac29f6918f11d11a
```

## Archive seal

Full code-only:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_TWO_STEP_PRODUCTION_PHYSICAL_ATTRIBUTION_CANARY_CODE_ONLY.zip
SHA-256:
d63ce0398e5620993096e7d7ae180bd90ddd306ec328e89bf2ad3118e6f21872
Files: 8424
CRC: PASS
```

Overlay code-only:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_TWO_STEP_PRODUCTION_PHYSICAL_ATTRIBUTION_CANARY_OVERLAY_CODE_ONLY.zip
SHA-256:
5b791240816df4b1b34fb389cc3d98b76ac0ccde1a5feb7f6e4d23a6f61b9326
Files: 9
CRC: PASS
```

Per archive policy, neither ZIP contains `specs/`, `artifacts/`, generated manifest JSON, or this specification.

## Static acceptance

```text
PASS dedicated canary CLI exists
PASS canary / full ABC selection is mutually exclusive
PASS canary optimizer-step target = 2
PASS canonical gradient accumulation = 8 preserved
PASS full ABC FullAbc profile remains 8-step
PASS full ABC CampaignModeR1::SuccessAbc preserved
PASS canary Close-R1 leg ceremony disabled
PASS canary R2 physical residency authority explicitly admitted
PASS canary terminal exit = KeepResident
PASS full final durable writeback not requested by canary
PASS digest hook runs after committed successor adoption
PASS weight / Adam M / Adam V / HiMuon digest materialization present
PASS full tensor capture count fixed to 0
PASS ABC comparison count fixed to 0
PASS promotion_claim fixed to false
PASS first-failure result is fail-fast
PASS canary source added to native compiled-source seal
PASS code-only ZIP exclusions
```

## Evidence boundary

The bake environment has no `cargo`, `rustc` or `rustfmt` executable.

```text
SOURCE      CONFIRMED
STATIC      CONFIRMED
ARCHIVE     CONFIRMED
COMPILE     NOT VERIFIED
RUNTIME     NOT VERIFIED
PHYSICAL    NOT VERIFIED
PERFORMANCE NOT MEASURED
```

The 12x optimizer-step-count reduction is static arithmetic (`24 / 2 = 12`). No 12x wall-clock speedup is claimed before measurement.

## Final law

> CANARY-R1 shortens execution horizon and capture volume, not the production model, dataset, optimizer, session or GPU authority semantics.

> Two committed optimizer steps exercise first materialization and one reuse cycle while avoiding the 24-step A/B/C promotion campaign during blocker iteration.

> Full A/B/C remains the promotion seal. CANARY-R1 is an attribution instrument and always records `promotion_claim=false`.
