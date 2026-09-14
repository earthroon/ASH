# EVE-MCU-R3H-CF4

## BP-DK OBSERVER CHECKPOINT STREAMING AUTHORITY

**Revision:** EVE-MCU-R3H-CF4  
**Parent:** EVE-MCU-R3H-CF3  
**Class:** BP-DK observer checkpoint host-residency closure / parameter-scoped streaming serialization authority

```text
+ PARAMETER-SCOPED OBSERVER STATE READBACK
+ DIRECT PAYLOAD FILE STREAMING
+ INCREMENTAL PAYLOAD SHA256
+ MANIFEST-METADATA-ONLY ACCUMULATION
+ RETIRE snapshot_all_states FULL STATE RETENTION
+ RETIRE snapshots.to_vec DEEP CLONE
+ RETIRE GIANT payload Vec
+ EXACT PARAMETER STATE SHA PRESERVATION
+ EXACT PAYLOAD OFFSET / LENGTH PRESERVATION
+ CF1 / CF2 / CF3 PRESERVATION
+ NO CHECKPOINT SEMANTIC CHANGE
```

## 1. Parent physical blocker

The CF3 physical campaign passed the earlier packed-copy, mapped-clone, and submission-lease blockers and reached:

```text
[ASH-EVE-MCU-R3H-CF2][mapped-consume] ... admitted=true
[ASH-MCU-EVE-R1K][candidate-return] ... resident_phase=Some(CandidateComplete)
[ASH-RAM36-HIMUON-SPARSE-ADAM-OVERLAY-COVERAGE-R1B] ... verdict=EXACT
memory allocation of 536870912 bytes failed
```

The new failure is exactly 512 MiB and occurs after candidate/overlay closure, in the checkpoint-persistence phase.

## 2. Parent checkpoint topology

The parent observer checkpoint path performed:

```text
GPU observer states
    -> snapshot_all_states()
    -> Vec<TensorCubeBpDkLocalObserverStateSnapshot>
       where every snapshot owns Vec<u8>
    -> build_bp_dk_observer_state_snapshot()
    -> snapshots.to_vec() deep clone
    -> giant aggregate payload Vec<u8>
    -> payload file
```

This makes host residency scale with total observer-state payload and allows several representations of the same payload to overlap.

## 3. CF4 authority law

CF4 changes only host serialization topology.

```text
one parameter observer state
    -> mapped readback
    -> borrowed &[u8]
    -> payload_file.write_all(bytes)
    -> parameter SHA-256
    -> incremental aggregate SHA-256
    -> metadata-only manifest entry
    -> drop mapped range / unmap
    -> next parameter
```

The complete observer payload is never materialized as one host `Vec<u8>` on the production persistence path.

## 4. Backend scoped mapped observer iterator

`burn_webgpu_backend::TensorCubeBpDkLocalObserver` now exposes:

```text
for_each_state_snapshot_mapped_r3h_cf4
```

It enumerates the canonical `BTreeMap` state order and provides:

```text
TensorCubeBpDkLocalObserverStateMetadataR3HCF4
&[u8] mapped_state_bytes
```

to a scoped consumer.

The metadata type owns no state payload.

The mapped sequence remains:

```text
COPY GPU state -> MAP_READ buffer
queue submit
map request
device poll Wait
map completion
get_mapped_range
consumer(metadata, borrowed bytes)
drop mapped view
buffer.unmap
```

A normal consumer `Result::Err` is propagated only after the mapped view has been dropped and the buffer has been unmapped.

## 5. Legacy whole-state API compatibility

The existing:

```text
snapshot_all_states(...)
```

is retained for qualification / restore compatibility and is implemented on top of the new scoped mapped iterator.

Production checkpoint persistence has zero `snapshot_all_states()` calls after CF4.

This preserves public/backend compatibility without retaining the old production topology.

## 6. Production persistence topology

`ProductionMuonRuntime::persist_bp_dk_observer_state` no longer calls the whole-state snapshot builder.

It now:

1. creates the canonical payload file,
2. creates one incremental `Sha256` payload hasher,
3. invokes the backend parameter-scoped mapped iterator,
4. validates source / observer / policy / registry / routing identity for each parameter,
5. computes exact per-parameter state SHA-256 from the borrowed mapped bytes,
6. writes those exact bytes directly to the payload file,
7. updates the aggregate payload SHA-256 incrementally,
8. records only `AshBpDkObserverStateSnapshotParameterV1` metadata,
9. releases the mapped parameter state before the next parameter,
10. syncs the payload file,
11. finalizes the aggregate SHA,
12. builds the unchanged V1 manifest,
13. writes the canonical manifest file.

## 7. No aggregate state payload

The production function contains:

```text
snapshot_all_states calls       = 0
snapshots.to_vec deep clone     = 0
giant payload Vec::new          = 0
```

The only retained O(parameter-count) object is the manifest metadata vector.

## 8. Manifest streaming finalizer

`bp_delta_k_stale_observation_seal.rs` adds:

```text
build_bp_dk_observer_state_stream_manifest_r3h_cf4
```

It preserves the existing manifest schema and validates:

```text
parameter ids non-empty
strict canonical parameter ordering
payload offsets contiguous
payload ranges within final length
final offset == payload length
state SHA field non-empty
registry digest present
routing digest present
payload SHA present
```

It emits the same:

```text
schema
patch_id
checkpoint_generation
optimizer_generation
structural_law_revision
source_revision
observer_revision
policy_revision
policy_digest
registry_digest
optimizer_routing_digest
payload_byte_length
payload_sha256
parameters
```

as the parent V1 manifest.

## 9. Parent builder parity preservation

The legacy `build_bp_dk_observer_state_snapshot` remains for qualification and now uses the same streaming manifest finalizer after constructing its parent-compatible payload.

Therefore the old whole-state builder and the new streaming production writer share one manifest-construction authority.

## 10. Exact parameter-state SHA

For parameter `P`:

```text
state_sha256 = SHA256(exact mapped serialized state bytes)
```

No RuntimeIdentity substitution is used for checkpoint persistence.

Checkpoint SHA-256 remains a durable file-integrity authority and is intentionally separate from BP-DK-R3 production RuntimeIdentity.

## 11. Exact aggregate payload SHA

The aggregate payload hash is computed by:

```text
payload_hasher.update(P0 bytes)
payload_hasher.update(P1 bytes)
...
payload_hasher.update(PN bytes)
```

in the exact same canonical order as file writes.

This is semantically equal to hashing the concatenated payload but does not require a concatenated host payload vector.

## 12. Exact offsets and lengths

Before writing parameter `P`:

```text
payload_offset = current_payload_byte_length
```

After successful write:

```text
current_payload_byte_length += state_len
```

The finalizer requires the complete offset chain to be exact and gap-free.

## 13. Empty observer behavior

If the observer contains zero states:

- the temporary created payload file is removed,
- no observer manifest is written,
- the method returns `None`,

preserving parent production semantics.

## 14. Publication semantics

CF4 does not change the existing candidate-directory transaction boundary.

The payload is synced before the manifest is published.

A parameter readback or write failure returns `Err` before manifest publication.

No partial observer manifest is admitted.

## 15. Restore compatibility

The existing checkpoint reader and decoder remain unchanged.

CF4 output continues to use:

```text
bp_dk_observer_state.bin
bp_dk_observer_state_manifest.json
ash.bp_dk.observer_state_snapshot.v1
```

No new compatibility branch is required by the reader.

## 16. CF1 preservation

The CF3 scheduler, including CF1 packed physical-span decomposition, is byte-preserved from the parent.

```text
production_multistep_loop_accumulation8_scheduler.rs
SHA-256 parent/work:
cd14a404060953818f490110490817af2e1f447f2f9f40ac1c51aa1da5cf9821
```

## 17. CF2 preservation

CF2 scoped mapped full-durable readback remains byte-preserved because the scheduler is unchanged.

No `mapped.to_vec()` regression is introduced in that production authority.

## 18. CF3 preservation

CF3 physical-allocation lease coalescing remains byte-preserved because the scheduler is unchanged.

No per-copy lease path is reintroduced by CF4.

## 19. RAM36 preservation

`ram36_process_budget.rs` is byte-preserved.

```text
SHA-256 parent/work:
0394d326e5fddf14501db21412b98a9b4ac9d0377529daee9317baeac0fd4d3e
```

The hard limit remains unchanged.

## 20. No synchronization policy change

Global static comparison:

```text
wait_for_submission_exact
parent = 38
CF4   = 38
delta = 0
```

No new exact wait is introduced.

## 21. No persistent Weight reload

Global static comparison:

```text
ResidentWeightPack::load_once
parent = 4
CF4   = 4
delta = 0
```

CF4 introduces no new Weight reload path.

## 22. Runtime witness

Production emits:

```text
[ASH-EVE-MCU-R3H-CF4][observer-checkpoint-stream]
```

with:

```text
parameter_count
written_parameter_count
payload_bytes
peak_parameter_state_bytes
full_state_retention_count=0
deep_snapshot_clone_count=0
aggregate_payload_vec_count=0
payload_sha_exact=true
offset_chain_exact=true
admitted=true
```

This witness is emitted only after payload sync and manifest construction succeed.

## 23. Qualification tests

CF4 adds seven pure-Rust tests under the `r3h_cf4_` prefix:

```text
r3h_cf4_streaming_manifest_matches_parent_builder
r3h_cf4_offset_gap_is_rejected
r3h_cf4_manifest_accumulates_metadata_only
r3h_cf4_incremental_payload_sha_matches_concatenated_payload
r3h_cf4_unsorted_manifest_metadata_is_rejected
r3h_cf4_payload_length_drift_is_rejected
r3h_cf4_existing_decoder_roundtrip_remains_compatible
```

They cover parent-builder parity, incremental SHA parity, metadata-only manifest accumulation, order/offset/length fail-closed behavior, and existing decoder compatibility.

## 24. Source delta

```text
ADD 0
MOD 3
DEL 0
```

Modified files:

```text
crates/base_train/src/bp_delta_k_stale_observation_seal.rs
SHA-256 81d85c2209aaeda9131cf4e851e4ed742d7dd786111173cd1e6cec5a853b3e78

crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
SHA-256 7ddbb86b638a3060fc3cd6ab610ff12f2c5185b08b7980905024f192000626f9

crates/burn_webgpu_backend/src/bp_delta_k_local_observer.rs
SHA-256 acec57949dd61e3e974386b3e9f0e4201e1f70286bcdcd30d08925bfaae43559
```

## 25. Static seals from bake

```text
production snapshot_all_states calls           0
production snapshots.to_vec                    0
production giant payload Vec::new              0
production stream iterator calls               1
production direct payload write                1
production incremental payload hasher          1
CF4 production witness                         1
backend scoped mapped iterator definitions     1
stream manifest finalizer definitions          1
r3h_cf4 tests                                  7
new wait_for_submission_exact                   0
new ResidentWeightPack::load_once               0
CF1 witness count delta                         0
CF2 witness count delta                         0
CF3 witness count delta                         0
changed-Rust delimiter balance                  PASS
```

## 26. Baked artifacts

Full code-only archive:

```text
ASH_PASS3_EVE_MCU_R3H_CF4_BP_DK_OBSERVER_CHECKPOINT_STREAMING_AUTHORITY_CODE_ONLY.zip
SHA-256 63711ea3622ac61cc321cbb804542b82d55c01f0b7e65fb81583bd00af6614ea
Files 8426
CRC PASS
```

Overlay:

```text
ASH_EVE_MCU_R3H_CF4_BP_DK_OBSERVER_CHECKPOINT_STREAMING_AUTHORITY_OVERLAY_CODE_ONLY.zip
SHA-256 c547d344d2b67c396f0257371f911dc46e3ebf44c4e8588fcc0b5b041a12ebd1
Files 3
CRC PASS
```

Both code archives contain:

```text
Markdown files 0
specs/         0
artifacts/     0
```

## 27. Evidence state at bake time

The bake environment does not contain a Rust toolchain.

```text
SOURCE / STATIC      PASS
ARCHIVE              PASS
COMPILE              UNVERIFIED
RUNTIME-TEST         UNVERIFIED
BYTE-PARITY TEST     UNVERIFIED
PHYSICAL             UNVERIFIED
FULL CANARY          UNVERIFIED
PERFORMANCE          UNMEASURED
```

No compile/runtime/physical claim is made by the bake itself.

## 28. Compile qualification

```text
cargo test -p base_train --lib --release --locked r3h_cf4_ -- --nocapture
cargo test -p base_train --lib --release --locked r3h_cf3_
cargo test -p base_train --lib --release --locked r3h_cf2_
cargo test -p base_train --lib --release --locked r3h_cf1_
cargo test -p base_train --lib --release --locked r3h_
cargo test -p base_train --lib --release --locked r3g_r2_
cargo test -p base_train --lib --release --locked bp_dk_r3_
cargo test -p burn_webgpu_backend --lib --release --locked
cargo build -p base_train --bin base_train --release --locked -j 1
```

Static/compile/runtime-test promotion token:

```text
PASS_EVE_MCU_R3H_CF4_BP_DK_OBSERVER_CHECKPOINT_STREAMING_AUTHORITY
```

## 29. Physical qualification

Re-seal the exact rebuilt release binary and execute the existing physical canary:

```text
--eve-mcu-close-r2-phys-canary-r1
```

Required same-run witnesses:

```text
CF1 packed decomposition admitted
CF2 mapped consume admitted
CF3 lease coalescing admitted
CF4 observer checkpoint stream admitted
```

Required CF4 witness:

```text
written_parameter_count == parameter_count
full_state_retention_count=0
deep_snapshot_clone_count=0
aggregate_payload_vec_count=0
payload_sha_exact=true
offset_chain_exact=true
admitted=true
```

The parent 512 MiB aggregate allocation blocker must be passed.

Physical promotion token:

```text
PASS_EVE_MCU_R3H_CF4_PHYSICAL_OBSERVER_CHECKPOINT_STREAMING
```

Hold token:

```text
HOLD_EVE_MCU_R3H_CF4_OBSERVER_STREAMING_PHYSICAL_CLOSURE_UNPROVEN
```

## 30. Completion law

CF4 is complete only when:

1. production observer checkpoint creation no longer materializes all observer states in host RAM,
2. production no longer calls `snapshot_all_states`,
3. production no longer deep-clones all snapshots,
4. production no longer creates a giant aggregate payload `Vec<u8>`,
5. parameter states are read in canonical order,
6. each mapped state is written directly to the payload file while borrowed,
7. exact parameter SHA-256 is preserved,
8. exact aggregate payload SHA-256 is preserved incrementally,
9. exact offsets and lengths are preserved,
10. manifest schema and checkpoint filenames are unchanged,
11. the existing decoder remains compatible,
12. empty-observer semantics remain `None` with no published files,
13. payload sync occurs before manifest publication,
14. partial parameter failure cannot publish a manifest,
15. CF1 / CF2 / CF3 remain unchanged,
16. BP-DK-R3 RuntimeIdentity hotpath policy remains unchanged,
17. RAM36 hard limit remains unchanged,
18. no new exact wait is introduced,
19. no new Weight reload is introduced,
20. the physical canary passes the parent 512 MiB observer-checkpoint allocation blocker.

## 31. Final authority law

> EVE-MCU-R3H-CF4 does not change the observer checkpoint format or its integrity rules. It changes only the lifetime topology of the serialized state bytes.

> Each parameter state is borrowed from its mapped GPU readback, written directly to the canonical payload file, hashed for both parameter and aggregate integrity, represented in the manifest by metadata only, and unmapped before the next parameter payload is processed.

> Checkpoint host residency therefore scales with one parameter readback plus manifest metadata rather than the complete observer-state payload, while preserving the existing V1 manifest, exact SHA-256 integrity, payload ordering, offsets, lengths, restore compatibility, and all CF1/CF2/CF3 authorities.
