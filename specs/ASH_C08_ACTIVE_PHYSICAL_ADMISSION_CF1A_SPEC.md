# ASH-C08-ACTIVE-PHYSICAL-ADMISSION-CF1A

## PRODUCTION DEVICE / QUEUE AUTHORITY REBIND

```text
+ RETIRE CF1 SYNTHETIC new_default SUBGROUP
+ RETIRE EMPTY-SPEC new_detached SUBMISSION IDENTITY
+ INHERIT MCU R7 PHYSICAL DEVICE/QUEUE AUTHORITY
+ SINGLE QUEUE-BINDING SSOT FOR CALLBACK / PARITY / MAP
+ CALLBACK SUBMISSION EXPLICIT QUEUE BINDING
+ PARITY SUBMISSION EXPLICIT QUEUE BINDING
+ READBACK SUBGROUP PHYSICAL BINDING REUSE
+ MAP SUBMISSION EXACT SAME QUEUE AUTHORITY
+ SAME DEVICE / QUEUE RECEIPT FROM ONE PRODUCTION AUTHORITY
+ NO IDENTITY RELAXATION
+ NO DEVICE-DRIFT CHECK REMOVAL
+ CF1 EVIDENCE CONTRACT PRESERVATION
```

## Patch identity

- Patch ID: `ASH-C08-ACTIVE-PHYSICAL-ADMISSION-CF1A`
- Parent: `ASH-C08-ACTIVE-PHYSICAL-ADMISSION-CF1`
- Identity schema: `ASH_C08_ACTIVE_PHYSICAL_ADMISSION_CF1A_V1`
- Identity authority source: `MCU_R7_PRODUCTION_PHYSICAL`
- PASS token: `PASS_ASH_C08_ACTIVE_PHYSICAL_ADMISSION_CF1A`

## Problem

CF1 correctly fails closed when callback, parity, and map submission identities disagree. The observed `FAIL_C08_CF1_DEVICE_IDENTITY_DRIFT` was caused by the qualification fixtures creating different software authority identities while using the same external WGPU device/queue:

```text
callback empty-spec auto submit -> detached authority A
parity   empty-spec auto submit -> detached authority B
map      synthetic new_default subgroup -> authority C
```

The identity predicate is not the defect. The identity origin is.

CF1A SHALL repair only that origin.

## Authority model

All C08 qualification fixtures SHALL inherit one production authority root:

```text
MCU R7 production physical subgroup
            |
            v
single production queue binding
      /         |         \
 callback     parity      map
      \         |         /
       same device / queue
```

C08 does not create a new device, queue, or subgroup authority for physical qualification.

## Production authority source

The base-train callsite SHALL obtain the existing MCU R7 subgroup:

```rust
self.mcu.parent_r7.device_soft_subgroup_r1a()
```

The handle may be cloned to resolve Rust borrow ownership, but the clone MUST share the same subgroup inner identity and physical runtime binding. No synthetic `new_default()` replacement is allowed.

## Qualification API

The C08 qualification API SHALL receive the production subgroup explicitly:

```rust
qualify_if_enabled(device, queue, production_subgroup)
```

and the executable qualification helper SHALL accept the same authority:

```rust
qualify_async_completion(device, queue, production_subgroup)
```

Before any fixture submission it SHALL:

1. read `physical_runtime_binding_r1()` from the production subgroup;
2. require a valid physical runtime binding;
3. read one `queue_binding()` from that subgroup;
4. require the queue binding device/queue authority IDs to equal the physical runtime binding IDs.

Failure is fail-closed.

## Callback fixture

The callback-only submission SHALL use the explicit production queue binding:

```rust
submit_with_leases(queue_binding, queue, empty_commands, &[])
```

It MUST NOT use `submit_with_leases_auto()` for authority inference.

## Parity fixture

The exact-wait parity submission SHALL use the same explicit `queue_binding` as the callback fixture.

The exact-wait parity fixture itself is preserved and remains physically exercised.

## Readback / map fixture

`acquire_compact_readback()` SHALL receive the inherited production subgroup, not a new synthetic subgroup.

The map/readback command submission SHALL use the same explicit production queue binding used by callback and parity.

## Receipt provenance

The existing CF1 physical receipt SHALL preserve all CF1 evidence fields and additionally bind:

```text
identity_authority_patch_id
identity_authority_schema_revision
identity_authority_source
production_device_id
production_queue_id
callback_authority_matches_production
parity_authority_matches_production
map_authority_matches_production
cf1a_identity_rebind_pass
cf1a_pass_token
```

The new fields SHALL participate in the receipt hash.

## Physical identity predicates

CF1A SHALL require both fixture equality and production authority equality:

```text
callback.device == parity.device == map.device == production.device
callback.queue  == parity.queue  == map.queue  == production.queue
```

The existing CF1 predicates:

```text
same_device_identity
same_queue_identity
```

remain intact.

CF1A MUST NOT replace them with literals and MUST NOT remove their failure paths.

## CF1 admission integration

`cf1a_identity_rebind_pass` SHALL require:

```text
identity_authority_source == MCU_R7_PRODUCTION_PHYSICAL
AND callback matches production
AND parity matches production
AND map matches production
AND same_device_identity
AND same_queue_identity
```

The existing CF1 `all_physical_witnesses_passed` predicate SHALL additionally require `cf1a_identity_rebind_pass`.

Therefore CF1A strengthens physical identity authority. It does not relax CF1.

## CF1 evidence preservation

CF1A SHALL preserve unchanged:

- local qualification default `active_physical_admission: false`;
- source qualification receipt hash binding;
- callback completion witness;
- map completion witness;
- early reclaim rejection and deferred retirement witness;
- observed-zero candidate-like exact waits;
- qualification-only exact-wait parity;
- explicit physical adoption;
- qualification hash reseal;
- `FAIL_C08_CF1_DEVICE_IDENTITY_DRIFT`;
- `FAIL_C08_CF1_QUEUE_IDENTITY_DRIFT`.

## Failure attribution

At minimum:

```text
FAIL_C08_CF1A_PRODUCTION_SUBGROUP_MISSING
FAIL_C08_CF1A_PRODUCTION_QUEUE_BINDING_MISSING
FAIL_C08_CF1A_CALLBACK_AUTHORITY_DRIFT
FAIL_C08_CF1A_PARITY_AUTHORITY_DRIFT
FAIL_C08_CF1A_MAP_AUTHORITY_DRIFT
FAIL_C08_CF1A_DETACHED_IDENTITY_OBSERVED
FAIL_C08_CF1A_SYNTHETIC_SUBGROUP_OBSERVED
```

The original CF1 device/queue drift failures remain active.

## Static gates

`tools/validate_ash_c08_active_physical_admission_cf1a_static.py` SHALL verify at minimum:

- qualification accepts a production subgroup;
- the production subgroup has a physical runtime binding;
- one queue binding is used as SSOT;
- callback uses explicit binding;
- parity uses explicit binding;
- map/readback uses inherited subgroup and explicit binding;
- no `new_default()` occurs inside the C08 qualification helper;
- no `submit_with_leases_auto()` occurs inside that helper;
- callback/parity/map each bind back to the production IDs;
- same-device / same-queue checks remain present;
- CF1 local-false and adoption contracts remain present;
- base_train injects the MCU R7 subgroup before mutably borrowing the C08 runtime;
- D09 and R4D semantic files remain unchanged;
- Cargo manifests and WGSL tree remain unchanged.

## Non-goals

CF1A SHALL NOT:

- modify D09 benchmark policy;
- modify R4D semantics;
- modify A01 submission semantics globally;
- change `submit_with_leases_auto()` behavior globally;
- remove exact-wait parity;
- create a fallback synthetic production subgroup;
- promote CF1 from a literal or mode bit.

## Physical qualification requirement

A runtime PASS requires the emitted CF1 receipt to show:

```text
identityAuthoritySource = MCU_R7_PRODUCTION_PHYSICAL
callbackAuthorityMatchesProduction = true
parityAuthorityMatchesProduction = true
mapAuthorityMatchesProduction = true
cf1aIdentityRebindPass = true
sameDeviceIdentity = true
sameQueueIdentity = true
cf1aPassToken = PASS_ASH_C08_ACTIVE_PHYSICAL_ADMISSION_CF1A
```

and all original CF1 physical evidence predicates must also pass.

## Final invariant

```text
PHYSICAL IDENTITY SHALL BE INHERITED, NOT FABRICATED.
```

C08 physical qualification may prove same-device / same-queue only when all three fixtures derive their receipt identities from the one MCU R7 production physical authority.
