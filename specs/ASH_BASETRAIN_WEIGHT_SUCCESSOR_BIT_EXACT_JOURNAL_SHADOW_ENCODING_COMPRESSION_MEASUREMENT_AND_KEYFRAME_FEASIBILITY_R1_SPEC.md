# ASH-BASETRAIN-WEIGHT-SUCCESSOR-BIT-EXACT-JOURNAL-SHADOW-ENCODING-COMPRESSION-MEASUREMENT-AND-KEYFRAME-FEASIBILITY-R1

## Canonical Weight G→G+1 Byte Successor / Shadow-Only Journal / RAW-Zstd / XOR-Zstd / XOR+Byte-Shuffle+Zstd / XOR+Bit-Plane+Zstd / Immediate Bit-Exact Reconstruction / Bounded 16 MiB Blocks / 96 MiB Scratch Authority / Zero Additional Optimizer Execution / Zero Additional Device Readback / Keyframe Feasibility Simulation / No Durable Promotion

## 0. Revision identity

Revision:

`ASH-BASETRAIN-WEIGHT-SUCCESSOR-BIT-EXACT-JOURNAL-SHADOW-ENCODING-COMPRESSION-MEASUREMENT-AND-KEYFRAME-FEASIBILITY-R1`

Parent:

`ASH-BASETRAIN-RAM-ADAM-COMMITTED-A-INACTIVE-B-CANDIDATE-GENERATION-TRANSACTIONAL-SWAP-AND-FAILURE-ATOMICITY-CLOSURE-R1`

Semantic parents:

- `ASH-BASETRAIN-TRAINABLE-GENERATION-DURABILITY-DESCRIPTOR-AND-ACTIVE-TRAINING-STATE-HEAD-BINDING-R1`
- `ASH-BASETRAIN-UNIFIED-ATLAS-MCU-FULL-TRAINABLE-DEVICE-GENERATION-BOUNDED-DURABLE-PACK-PROJECTION-AND-OUTER-HOST-SCATTER-RETIREMENT-CLOSURE-R1`

Static/source PASS token:

`PASS_ASH_BASETRAIN_WEIGHT_SUCCESSOR_BIT_EXACT_JOURNAL_SHADOW_ENCODING_COMPRESSION_MEASUREMENT_KEYFRAME_FEASIBILITY_R1_STATIC`

Physical HOLD token:

`HOLD_ASH_BASETRAIN_WEIGHT_SUCCESSOR_JOURNAL_SHADOW_PHYSICAL_MEASUREMENT_PENDING_R1`

Full release/physical PASS is not claimed by this source bake.

---

## 1. Purpose

The current ASH training path already owns one exact logical source-weight stream G and one exact canonical target-weight stream G+1.

That target stream already feeds existing authorities such as:

- `weight_pack_hasher`;
- `SequentialPackWriter` when a physical `weights.r6pack` is required;
- `ResidentWeightPackBuilder` when the successor remains resident;
- the existing 02 bounded device projection path under ActiveVerified.

R1 adds a non-authoritative observer that consumes those same already-existing source/target bytes and asks one question:

> Which reversible representation best compresses the actual ASH G→G+1 successor bits while reconstructing every target bit exactly?

It does not change the optimizer, generation authority, durable format, restart path, or current head.

---

## 2. Center invariant

Canonical path remains:

```text
source weight generation G
↓
existing optimizer / FullTrainable device generation
↓
canonical target weight bytes G+1
↓
existing R6 / ResidentWeightPack sinks
```

Shadow R1 only tees:

```text
same source bytes G
+
same canonical target bytes G+1
↓
reversible transform
↓
Zstd
↓
Zstd decode
↓
inverse transform
↓
byte/bit comparison against canonical G+1
↓
measurement evidence
```

The shadow path never supplies canonical target bytes back into the training authority.

---

## 3. Actual source truth after bake

```text
weight successor shadow module                         true
shadow default OFF                                     true
MeasureOnly mode                                       true
MaterializeShadow mode                                 true
16 MiB maximum uncompressed journal block              true
96 MiB RAM36 shadow scratch bound                      true
RAW_ZSTD                                                true
XOR_ZSTD                                                true
XOR_BYTE_SHUFFLE_ZSTD                                   true
XOR_BITPLANE_ZSTD                                       true
immediate compress→decode→inverse→exact compare        true
source whole-stream SHA binding                        true
target whole-stream SHA binding                        true
keyframe feasibility simulator                         true
candidate-local shadow materialization                 true
RAM36 shadow scratch owner                             true
exact RAM inventory shadow scratch category            true
additional optimizer execution                         false by structure
additional device weight D2H                           false by structure
required R6 weight pack retired                        false
ResidentWeightPack replaced                            false
durability descriptor journal binding                  false
P3 journal participant                                 false
active training-state schema change                    false
physical compression ratio measured                    false
physical keyframe replay campaign                      false
release compile                                        not claimed
Cargo.lock zstd resolution                             not claimed
```

---

## 4. New source module

New module:

`crates/base_train/src/weight_successor_bit_exact_journal_shadow_r1.rs`

Exported by:

`crates/base_train/src/lib.rs`

Primary runtime owner:

`WeightSuccessorJournalShadowRuntimeR1`

The owner contains only bounded observation and codec state. It does not own canonical model weights.

---

## 5. Shadow activation is explicit

Environment authority:

`ASH_WEIGHT_SUCCESSOR_JOURNAL_SHADOW_R1_MODE`

Accepted forms:

```text
unset / OFF / 0 / FALSE
→ shadow disabled

MEASURE / MEASURE_ONLY
→ MeasureOnly

MATERIALIZE / MATERIALIZE_SHADOW
→ MaterializeShadow
```

The default is OFF.

A normal training run does not silently begin compression work merely because the source module exists.

---

## 6. Shadow mode semantics

`WeightSuccessorJournalShadowModeR1` has two materialized modes:

```text
MeasureOnly
MaterializeShadow
```

### MeasureOnly

For every bounded block:

```text
transform
→ compress
→ decode
→ inverse
→ exact compare
→ discard compressed payload
→ retain metrics
```

### MaterializeShadow

Performs the same validation but additionally writes non-authoritative shadow containers and a shadow receipt under the candidate directory.

Neither mode changes canonical generation authority.

---

## 7. Canonical byte domain

The journal observes exact weight bytes in current canonical logical F32 order.

The transformation layer treats those values as opaque bytes/U32 bit patterns.

Forbidden journal math includes:

- floating-point subtraction;
- quantization;
- F16/BF16 conversion;
- epsilon thresholding;
- sparse approximation;
- lossy coding.

XOR means exact bitwise XOR, not numerical weight delta.

---

## 8. Bounded block geometry

Materialized constant:

`WEIGHT_SUCCESSOR_JOURNAL_SHADOW_MAX_BLOCK_BYTES_R1 = 16 * 1024 * 1024`

This matches the existing R6 stream-chunk scale.

The shadow runtime does not allocate a whole-model transform buffer.

Canonical observation proceeds through bounded blocks in logical byte order.

---

## 9. Actual scratch bound

Materialized bound:

```text
WEIGHT_SUCCESSOR_JOURNAL_SHADOW_SCRATCH_BOUND_BYTES_R1
= 6 × 16 MiB
= 96 MiB
```

The initial design estimate was smaller, but implementation audit showed that live bounded source, target, transformed, compressed, decoded, and reconstruction buffers must be visible to the process-memory authority.

Therefore the source truth is 96 MiB.

This is a configured maximum scratch classification, not a physical high-water claim.

---

## 10. RAM36 integration

New RAM owner:

`HostRamOwner::WeightSuccessorJournalShadowScratch`

The RAM-resident production paths reserve the bounded shadow scratch through the existing RAM36 process-budget authority before in-process shadow measurement.

If the scratch cannot be admitted, shadow observation is held/dropped rather than silently using untracked memory.

Canonical generation remains unaffected because the journal is non-authoritative.

---

## 11. Exact RAM inventory integration

New exact inventory category:

`BaseTrainRamCategory::WeightSuccessorJournalShadowScratch`

Registration entrypoint:

`register_weight_successor_journal_shadow_scratch_r1()`

The inventory registers the 96 MiB configured transient bound so RAM36 and exact-inventory accounting refer to the same shadow scratch concept.

---

## 12. Packed legacy RAM36 boundary

The packed legacy function does not currently receive the RAM36 authority object.

It may therefore run the explicitly enabled bounded shadow observer without a local RAM36 reservation call.

RAM-resident paths, where the RAM36 authority is available, perform the reservation.

R1 does not pretend the packed legacy callsite has a RAM36 object that its current API does not expose.

This remains a source-truth boundary rather than a hidden fallback claim.

---

## 13. Source/target pair API

The journal exposes bounded observation surfaces including:

- `observe_weight_successor_f32_r1(...)`;
- `observe_source_f32_target_bytes_r1(...)`;
- `observe_weight_successor_bytes_r1(...)`.

Each observation requires equal source/target byte cardinality and canonical logical ordering.

---

## 14. Canonical cursor

The runtime owns a logical byte cursor.

Incoming observation must correspond to the next canonical logical region.

R1 does not allow arbitrary block reordering and then repair the stream later.

---

## 15. Whole-stream source identity

While observing source bytes, the shadow runtime computes the observed source weight SHA256.

At finish, it must equal the expected source weight digest supplied by the current generation authority.

Drift fails the shadow observation.

It does not invalidate an otherwise canonical generation.

---

## 16. Whole-stream target identity

The shadow runtime also hashes every canonical target byte it receives.

At `finish_r1(...)`, observed target SHA256 must equal the canonical candidate target-weight SHA256.

The journal therefore cannot quietly measure a byte stream different from the one the rest of the generation committed.

---

## 17. No second whole source-pack pass

The journal module contains no source `File::open(...)` path for reading `weights.r6pack` again.

Required structural counters remain:

```text
extraSourcePackReadBytes = 0
extraTargetPackReadBytes = 0
```

The source/target pair must come from the candidate pipeline where both already exist.

---

## 18. No second optimizer

The journal module imports no WGPU execution backend, no `SubmissionEpoch`, no R6 Adam candidate executor, and no FullTrainable device-generation executor.

Required structural truth:

```text
additionalOptimizerExecutionCount = 0
```

---

## 19. No additional device readback

Under ActiveVerified, the observer consumes the already-mapped logical target weight bytes produced by the 02 bounded device projection.

It does not request another device→host candidate copy.

Required structural truth:

```text
additionalWeightD2HBytes = 0
```

Physical counters still require a real campaign before PASS.

---

## 20. Codec set

R1 evaluates exactly four compressed codec families:

```text
RAW_ZSTD
XOR_ZSTD
XOR_BYTE_SHUFFLE_ZSTD
XOR_BITPLANE_ZSTD
```

The uncompressed target byte count is recorded separately as the baseline.

No codec is source-selected as the winner.

---

## 21. Zstd dependency source truth

`crates/base_train/Cargo.toml` now pins:

`zstd = "=0.13.3"`

R1 uses in-process Rust calls:

- `zstd::stream::encode_all(...)`;
- `zstd::stream::decode_all(...)`.

No external `zstd.exe`, shell process, PowerShell compression stage, or Python compression authority is introduced.

---

## 22. Cargo.lock boundary

The bake environment contains no `cargo`, `rustc`, or `rustfmt`.

Therefore:

```text
Cargo.toml exact Zstd pin        materialized
Cargo.lock Zstd resolution       not materialized
cargo check                      not run
release build                    not run
```

The existing `Cargo.lock` was not manually fabricated or edited to guess transitive dependencies.

The first downstream compile gate must run Cargo resolution and then verify the resulting lockfile before release qualification.

---

## 23. Zstd profile is explicit

When shadow is enabled, these environment values are required:

- `ASH_WEIGHT_SUCCESSOR_JOURNAL_ZSTD_LEVEL`;
- `ASH_WEIGHT_SUCCESSOR_JOURNAL_ZSTD_PROFILE_ID`.

`WeightJournalZstdProfileR1::from_env_r1()` validates both.

There is no hidden default compression level that could make campaign-to-campaign comparisons ambiguous.

---

## 24. Same compressor profile for all transforms

One `WeightJournalZstdProfileR1` is shared across all four codecs in a shadow session.

Current profile records:

```text
profile ID
compression level
single-threaded = true
checksum enabled = false
```

Transform comparison is therefore not allowed to hide different Zstd levels behind each codec.

---

## 25. RAW_ZSTD

Input:

`canonical target weight bytes`

Transform is identity.

This measures how well the target weight stream compresses without a source-dependent delta transform.

It is also the conceptual full-keyframe representation used by the feasibility simulator.

---

## 26. XOR_ZSTD

For equal-length source and target U32 words:

```text
xorWord[i] = sourceWord[i] XOR targetWord[i]
```

The exact XOR byte stream is then compressed with the same Zstd profile.

Decoder reconstructs:

```text
targetWord[i] = sourceWord[i] XOR xorWord[i]
```

---

## 27. XOR_BYTE_SHUFFLE_ZSTD

After exact XOR, the four little-endian byte lanes of every U32 word are transposed block-locally.

For N words:

```text
out[lane * N + i]
= xorBytes[4*i + lane]
```

The inverse transform must restore the exact XOR stream before source XOR reconstruction.

---

## 28. XOR_BITPLANE_ZSTD

After exact XOR, the 32 bit positions are transposed into 32 block-local bit planes.

For bit `b` and word `i`:

```text
plane[b][i]
= (xorWord[i] >> b) & 1
```

Bits within each plane byte are packed in deterministic increasing word order. Unused terminal high bits remain zero.

The inverse transform reconstructs every XOR U32 bit before applying the source XOR.

---

## 29. Immediate exact reconstruction

Every codec follows the actual execution sequence:

```text
encode transform
→ Zstd encode
→ Zstd decode
→ inverse transform
→ reconstruct target
→ mismatch_counts_r1(...)
```

There is no encode-only PASS.

---

## 30. Exact mismatch rule

For every codec frame:

```text
byteMismatchCount = 0
bitMismatchCount = 0
```

is mandatory for `exact_reconstruction = true`.

One wrong bit disqualifies the observed codec result regardless of compression ratio.

---

## 31. Receipt fields

`WeightSuccessorShadowCodecReceiptR1` records at least:

- codec ID;
- Zstd profile ID;
- frame count;
- raw target bytes;
- transformed bytes;
- compressed bytes;
- compression ratio;
- encode wall time;
- decode wall time;
- peak scratch bytes;
- compressed stream SHA256;
- reconstructed-target SHA256;
- byte mismatch count;
- bit mismatch count;
- exact reconstruction verdict.

---

## 32. Main shadow receipt

`WeightSuccessorJournalShadowReceiptR1` binds:

- source/target model generation;
- source/target optimizer generation;
- source weight SHA256;
- target weight SHA256;
- canonical layout digest;
- logical weight bytes;
- configured block bound;
- frame count;
- extra source/target read counters;
- additional device D2H counter;
- additional optimizer execution counter;
- raw baseline bytes;
- all codec receipts;
- authority flags;
- physical HOLD token;
- receipt digest.

---

## 33. Authority flags are permanently false in R1

The source receipt explicitly emits:

```text
shadowAuthoritative = false
r6WeightPackRetired = false
descriptorBindingMaterialized = false
p3ParticipantMaterialized = false
physicalMeasurementClaimed = false
```

The existence of an encoder does not make it durable state.

---

## 34. ActiveVerified integration

The 02 device projection path already owns:

```text
logical source-weight window
logical mapped target-weight window
```

R1 tees those same windows into the shadow observer.

It does not invoke `FullTrainableDeviceGenerationR1` a second time and does not issue a second device projection.

---

## 35. Legacy packed integration

The existing packed candidate path already owns source `weight` and canonical candidate `weight_bytes`.

R1 passes that exact pair to the same common shadow observer.

No separate legacy journal implementation exists.

---

## 36. RAM-resident legacy integration

The RAM-resident mixed Muon/Adam and batched Adam paths likewise feed the already-materialized source/candidate pair into the same observer.

This remains independent of the RAM Adam A/B state authority. The journal observes weights only.

---

## 37. Best-effort shadow failure boundary

Production scheduler integration treats shadow initialization/observation/finalization as non-authoritative best-effort evidence.

If shadow cannot start, runs out of admitted scratch, or a codec observation fails:

```text
canonical candidate authority continues
shadow result is logged/held as failed observation
```

R1 does not permit a shadow codec bug to overwrite canonical generation state.

---

## 38. Qualification may still fail

A dedicated shadow qualification campaign may return FAIL when exact reconstruction requirements are violated.

That qualification verdict is about the journal experiment, not the canonical model generation that supplied the bytes.

---

## 39. MaterializeShadow location

Candidate-local non-authoritative namespace:

```text
candidate_step_XXXXXX/
shadow/
weight_successor_journal_r1/
```

Possible containers:

- `weight_successor_raw_zstd.shadow.r1.bin`;
- `weight_successor_xor_zstd.shadow.r1.bin`;
- `weight_successor_xor_byte_shuffle_zstd.shadow.r1.bin`;
- `weight_successor_xor_bitplane_zstd.shadow.r1.bin`.

Shadow JSON receipt is also candidate-local.

---

## 40. Shadow artifact publication

Materialized containers use a `.partial` staging path followed by final rename after the shadow file is finished.

This is shadow artifact hygiene only.

Canonical commit does not wait for the shadow artifact to become durable as a P3 prerequisite.

---

## 41. Shadow deletion semantics

Deleting or corrupting the entire shadow subtree must not affect:

- `load_source()`;
- P3 restart;
- V4 descriptor validation;
- current generation identity;
- R6 pack admission;
- N8 parent authority.

If those paths ever begin depending on the shadow tree, R1 authority separation has been violated.

---

## 42. No durable descriptor binding

`TrainableGenerationDurabilityDescriptorR1` is unchanged by this child.

No journal digest, codec, keyframe interval, or shadow file path becomes a required descriptor field.

---

## 43. No P3 participant

The existing P3 descriptor-bound participant set is unchanged.

No `WEIGHT_SUCCESSOR_JOURNAL` participant is added.

---

## 44. No active-head migration

`active_training_state.json` remains the sole current-generation head and its current V4 schema is unchanged.

No V5 migration occurs in R1.

---

## 45. No R6 retirement

Required `weights.r6pack` construction remains present through `SequentialPackWriter` where existing policy calls for it.

No conditional says:

```text
shadow compression looked good
→ skip required R6 weight pack
```

---

## 46. No ResidentWeightPack replacement

`ResidentWeightPackBuilder` remains the in-process resident successor authority where currently used.

Decoded shadow output is never promoted to a new live resident weight pack in R1.

---

## 47. No source reread authority

XOR codecs must receive the exact immediate source block already in the optimizer/candidate path.

A valid G→G+1 delta replayed against another source is expected to fail target identity.

---

## 48. Frame structure

Materialized frames bind at least:

- frame index;
- logical byte offset;
- raw target byte length;
- transformed byte length;
- compressed byte length;
- source block SHA256;
- target block SHA256;
- compressed payload.

The container uses deterministic bounded framing rather than one unbounded whole-model compression buffer.

---

## 49. Independent bounded frames

Each bounded raw block is compressed independently.

This permits:

- bounded memory;
- frame-local corruption attribution;
- bounded decode;
- future random/deep audit without inflating a full model first.

---

## 50. Keyframe feasibility types

R1 materializes:

- `WeightJournalKeyframeFeasibilityReceiptR1`;
- `WeightSuccessorJournalCampaignReceiptR1`;
- `simulate_keyframe_feasibility_r1(...)`.

This is a simulation/measurement surface, not a durable keyframe implementation.

---

## 51. Keyframe semantics

The simulator treats:

```text
RAW_ZSTD
```

as the candidate full-state keyframe representation.

Exact XOR-family results are treated as immediate-predecessor delta candidates between consecutive generations.

---

## 52. Keyframe intervals are not hardcoded winners

`simulate_keyframe_feasibility_r1(...)` receives keyframe intervals from the campaign caller.

The source does not hardcode `[1, 2, 4, 8]` as an authority and does not promote any K value.

A physical campaign may choose an interval matrix appropriate to the number of observed consecutive generations.

---

## 53. No physical multi-generation replay claim

Although the feasibility simulator is materialized, this source bake has not executed a real consecutive-generation materialized journal replay campaign.

Therefore:

```text
physical keyframe feasibility PASS = not claimed
```

---

## 54. No compression ratio claim

This source bake contains no observed physical compression ratios.

It does not claim:

- XOR beats RAW;
- byte shuffle beats plain XOR;
- bit-plane wins;
- any particular bytes-per-step target.

Those are measurement outcomes, not source assumptions.

---

## 55. Negative results remain valid results

A physically measured codec may:

```text
compress worse than raw
consume too much CPU
increase storage bytes
```

and still pass exactness.

R1 must preserve that result rather than suppressing it.

---

## 56. Codec ranking boundary

Only exact-reconstructing codecs are eligible for diagnostic size ranking.

Primary measurement may sort by compressed bytes, but encode/decode time and scratch remain separately visible.

No hidden composite score selects durable architecture.

---

## 57. No project-wide winner from one step

One generation may identify a smallest observed codec for that generation.

It may not establish a durable project-wide winner.

A representative multi-generation campaign and a later selection revision are required.

---

## 58. Embedded transform tests

The new Rust module contains deterministic unit coverage for reversible transform primitives including:

- XOR exact roundtrip;
- byte-shuffle roundtrip;
- bit-plane roundtrip with a non-multiple-of-eight word count;
- signed-zero `+0.0` / `-0.0` bit distinction.

These tests exist in source but were not executed in this assistant environment because Cargo/Rust tooling is absent.

---

## 59. Required future negative tests

Release/physical qualification should also exercise:

- wrong XOR source generation;
- truncated frame;
- reordered frame;
- corrupted compressed payload;
- header offset drift;
- target digest mismatch;
- source digest mismatch;
- NaN payload bits as opaque data;
- all-zero and high-change XOR fixtures.

No repair or zero-fill fallback is permitted.

---

## 60. Physical campaign requirements

A meaningful R1 physical campaign should include multiple consecutive real committed logical weight generations, explicit Zstd profile identity, and at least one generation with changed weight bits.

It must report per codec:

- raw bytes;
- transformed bytes;
- compressed bytes;
- ratio;
- encode wall time;
- decode wall time;
- peak scratch;
- changed-word/bit diagnostics where materialized;
- reconstructed target SHA;
- byte mismatch count;
- bit mismatch count.

---

## 61. No extra-training-work physical requirement

A real campaign must confirm:

```text
additionalOptimizerExecutionCount = 0
additionalWeightD2HBytes = 0
canonicalGenerationMutationCount = 0
```

Static source structure supports those claims but does not substitute for observed counters.

---

## 62. RAM36 physical requirement

When shadow is enabled in a RAM36-enforced process:

```text
shadow scratch peak <= admitted bound
RAM36 private hard-cap violation = 0
RAM36 reservation leak = 0
```

must be physically observed before full PASS.

---

## 63. Static validator

New validator:

`tools/validate_ash_basetrain_weight_successor_bit_exact_journal_shadow_encoding_compression_measurement_keyframe_feasibility_r1_static.py`

It verifies at least:

- module export;
- exact Zstd dependency pin;
- 16 MiB block geometry;
- 96 MiB bounded scratch identity;
- four codec families;
- Zstd encode/decode;
- reversible XOR/byte-shuffle/bit-plane transforms;
- immediate mismatch comparison;
- absence of lossy transform vocabulary;
- shadow authority flags false;
- absence of active-state/descriptor/P3 dependencies from the journal module;
- existing R6 writer retained;
- existing ResidentWeightPack retained;
- ActiveVerified and legacy tee wiring;
- absence of WGPU/SubmissionEpoch/optimizer execution in the journal module;
- absence of whole-pack `File::open` source reread;
- candidate shadow namespace and partial→final rename;
- keyframe simulator without hardcoded winner;
- RAM36 owner and exact-inventory category;
- no descriptor/P3 journal binding;
- physical PASS withheld.

---

## 64. Observed static regression chain

Final source/static campaign observed:

```text
1  Weight successor journal shadow R1              PASS
2  RAM Adam transactional A/B R1                   PASS
3  Trainable Generation Durability Descriptor V4   PASS
4  Eve R1 common Adam semantics                    PASS
5  Eve R2 canonical Adam math                      PASS
6  P1 AdamW pending scheduler                      PASS
7  B06 multi-segment ledger                        PASS
8  FullModel AdamW segmented successor             PASS
9  02 bounded durable projection                   PASS
10 SubmissionEpoch ActiveAsync                     PASS
11 P3 active transactional commit/restart          PASS
12 Unified Atlas MCU control plane                 PASS
13 RAM36 remaining-underflow attribution            PASS
14 RAM36 successor-weight ownership transition      PASS
15 Immutable N2 RAM36 exact-retry parent            PASS

PASS = 15
FAIL = 0
```

These are source/static gates only.

---

## 65. Compile boundary

A real compile remains mandatory because R1 changes:

- `base_train` dependencies;
- new Rust codec code;
- scheduler callsites;
- RAM36 owner enum;
- exact RAM inventory enum/category;
- production shadow session plumbing.

The current bake environment exposes no `cargo`, `rustc`, or `rustfmt`.

Therefore no Rust compile or unit-test PASS is claimed.

---

## 66. Cargo.lock downstream gate

Because the new exact Zstd dependency was added without an available Cargo resolver, downstream qualification must first:

```text
run Cargo dependency resolution
→ update Cargo.lock through Cargo itself
→ inspect resolved zstd/transitive versions
→ cargo check
→ release build
```

No manual fake lock entry is part of this R1 bake.

---

## 67. Physical HOLD meaning

The source exposes:

`HOLD_ASH_BASETRAIN_WEIGHT_SUCCESSOR_JOURNAL_SHADOW_PHYSICAL_MEASUREMENT_PENDING_R1`

because none of these have yet been physically established:

- actual compression ratios;
- encode/decode throughput;
- real scratch high-water;
- training slowdown;
- consecutive-generation keyframe replay;
- physical exact reconstruction campaign;
- physical zero-extra-D2H counters.

---

## 68. Packaging policy

Baked source ZIP excludes:

- this specification;
- all Markdown/specs;
- generated shadow containers;
- generated shadow JSON receipts;
- campaign/keyframe evidence;
- runtime JSON/JSONL;
- runtime packs;
- training-state outputs;
- logs;
- `target*`;
- `.git`;
- Python bytecode caches;
- backup source outputs.

Implementation Rust/Python source and source-controlled Cargo manifests remain included.

---

## 69. GitHub publication policy

Current ASH policy remains:

```text
GitHub = specification only
```

Implementation source remains in the baked ZIP.

---

## 70. Actual baked source delta

Parent-to-R1 implementation delta is exactly seven files:

```text
crates/base_train/Cargo.toml
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/ram36_process_budget.rs
crates/base_train/src/ram_budget_exact_inventory.rs
crates/base_train/src/weight_successor_bit_exact_journal_shadow_r1.rs
tools/validate_ash_basetrain_weight_successor_bit_exact_journal_shadow_encoding_compression_measurement_keyframe_feasibility_r1_static.py
```

No descriptor/P3/head implementation file is changed by this child.

---

## 71. Exact next child if physical evidence is favorable

Recommended:

`ASH-BASETRAIN-WEIGHT-SUCCESSOR-BIT-EXACT-JOURNAL-ENCODING-SELECTION-DUAL-WRITE-DURABILITY-DESCRIPTOR-BINDING-AND-CROSS-GENERATION-REPLAY-CLOSURE-R1`

That child must select an encoding and keyframe policy from physical R1 evidence, then begin dual-write while retaining the current full-weight durable path.

---

## 72. No direct retirement jump

Forbidden roadmap shortcut:

```text
shadow codec appears small
→ remove weights.r6pack
```

The next authority transition must first prove selected-journal dual-write and fresh-process reconstruction parity.

---

## 73. Final authority declaration

Before R1, ASH already had exact source G and target G+1 weight bytes but no measurement authority for deciding whether RAW, XOR, byte-shuffled XOR, or bit-plane XOR was a useful durable representation.

After R1, those exact source/target bytes can be observed by one bounded non-authoritative Rust shadow runtime. The observer performs no new optimizer execution and requests no new GPU weight readback. It evaluates `RAW_ZSTD`, `XOR_ZSTD`, `XOR_BYTE_SHUFFLE_ZSTD`, and `XOR_BITPLANE_ZSTD` using one explicit Zstd profile. Every compressed frame is decoded immediately and reconstructed against the canonical target. One mismatched bit invalidates that observed encoding regardless of compression ratio.

The journal is disabled by default. `MeasureOnly` discards compressed payload after verification. `MaterializeShadow` stores candidate-local shadow artifacts that may be deleted without affecting restart or current-generation authority. Shadow errors remain visible but do not veto the canonical generation.

The implementation operates on 16 MiB maximum raw blocks and exposes a 96 MiB RAM36/exact-inventory scratch bound. It does not reread the whole source or target pack, does not create a second optimizer, and does not replace `ResidentWeightPack` or required `weights.r6pack` output.

`TrainableGenerationDurabilityDescriptorR1`, P3 participants, `PackedRuntimeStateManifestV1`, and `active_training_state.json` remain unchanged. No codec, Zstd level, compression ratio, or keyframe interval is promoted by source.

The source pins `zstd = "=0.13.3"`, but because Cargo is unavailable in the bake environment the lockfile has not been resolved and compile/physical qualification remain open gates.

The purpose of this child is therefore measurement, not migration:

> determine what the real ASH successor bits compress into, how much CPU/RAM that costs, and whether every target bit can be recovered exactly before any durability authority is changed.
