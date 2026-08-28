# ASH-BASETRAIN-TENSORCUBE-MUON-ATLAS-WAVE-STREAMING-HOST-FULL-CANDIDATE-MATERIALIZATION-RETIREMENT-R1

## Status

Implementation-bound production retirement of dedicated full-parameter Muon host candidate payloads.

The preceding physical N8 closed successor ResidentWeightPack reservation-to-physical-allocation ownership for GEN5->6 and GEN6->7, then terminated after the first GEN6->7 BP-DK witness with a raw allocator failure:

```text
memory allocation of 1044033536 bytes failed
```

The exact owner of that raw allocation was not emitted by the allocator. Source review shows multiple full-cardinality host surfaces in the Muon path, including a scheduler source packed scratch and dedicated candidate weight/momentum/orthogonal-update aggregates. Therefore R1 does not claim that the raw failure belonged to one specific Vec. It retires the dedicated full candidate aggregates and preserves exact attribution for any next first failure.

## Production admission

R1 is explicitly requested by:

```text
ASH_MUON_ATLAS_WAVE_STREAMING_HOST_RETIREMENT_R1=1
```

When requested, production requires:

```text
ASH_MUON_RESIDENT_STATE_MODE=ACTIVE_VERIFIED
ASH_HIMUON_DEVICE_CANDIDATE_MODE=MIRROR_VERIFIED
ASH_HYBRID_DEVICE_COMMIT_MODE=MIRROR_VERIFIED
ASH_BP_DK_ACTIVE_FUSION_REPLAY_MODE=DISABLED
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_MODE=DISABLED
```

The R1 route fails closed if these authorities do not match. It does not silently fall back to the legacy full-host candidate route.

B05/B06 Active device commit is not promoted by this revision because the current production consumer capability does not authorize B06 Active. R1 therefore uses verified wave-bounded mirror readback while retiring cross-wave host payload aggregation.

## Authority split

```text
Atlas Scheduler / Resident State Graph
    owns wave geometry and page bound

Muon Wave Executor
    owns only current bounded wave source/candidate payload

BP-DK Streaming Post Builder
    owns compact incremental evidence and digest state

Production Muon Momentum Runtime
    owns committed momentum destination ranges

Scheduler packed_muon_weight scratch
    owns source packed payload and is reused in-place as candidate-weight destination
```

No new full candidate-weight destination Vec is created in the R1 production route.

## R1 candidate residency contract

Legacy production shape:

```text
full source packed scratch
+ full source momentum clone
+ full candidate weight
+ full candidate momentum
+ full orthogonal update
```

R1 production shape:

```text
existing source packed scratch, reused in-place as candidate weight destination
+ persistent Muon momentum, updated per canonical tile
+ one Atlas-bounded wave source payload
+ one Atlas-bounded wave candidate payload
+ bounded pending canonical/pair evidence
```

Dedicated full candidate weight, candidate momentum, and orthogonal update payloads are forbidden in the admitted R1 path.

## Atlas wave bound

Wave capacity derives from the existing resident-state Atlas page authority:

```text
atlas_page_bytes = resident_state_graph.atlas_page_bytes()
max_surface_elements = atlas_page_bytes / sizeof(f32)
```

Fusion execution domains are ordered by canonical minimum tile identity and grouped into bounded waves whose source element cardinality does not exceed the Atlas surface bound.

A wave may contain local and fused domains. Local and fused subpartitions are executed as bounded requests and immediately consumed into canonical tile evidence/destinations.

## No cross-wave full candidate accumulation

The admitted R1 path does not allocate:

```text
vec![0.0f32; full_parameter_elements] candidate_weight
vec![0.0f32; full_parameter_elements] candidate_momentum
vec![0.0f32; full_parameter_elements] orthogonal_update
```

It also does not return an aggregate full candidate payload from the streaming executor.

Instead each wave performs:

```text
Prepare bounded wave source
-> GPU execute
-> bounded mirror readback
-> map results to canonical tile identity
-> feed incremental BP-DK post evidence
-> commit candidate weight tile into existing packed source scratch
-> commit candidate momentum tile into persistent momentum destination
-> retire orthogonal update after evidence consumption
-> retire wave payload
```

## Canonical commit and bounded pending tiles

Fused-down domains may produce a later canonical tile together with an earlier tile. R1 therefore permits a bounded pending-tile map rather than assuming physical completion order equals canonical commit order.

The pending map is bounded by:

```text
full_tile_cols + atlas_wave_tile_capacity
```

and fails closed with:

```text
FAIL_ASH_BASETRAIN_MUON_CROSS_WAVE_HOST_ACCUMULATION
```

if the bound is exceeded.

Every canonical tile must have exactly one owner and is committed exactly once.

## BP-DK post-update streaming evidence

The previous post-update builder required full source/candidate/update slices. R1 adds `AshBpDkPostUpdateStreamingBuilder`.

It consumes one canonical 256-element tile at a time and preserves candidate weight, candidate momentum, and orthogonal-update digests; per-tile RMS evidence; per-pair delta/update cosine evidence; transition kind; source graph/plan generation ownership; and target optimizer/BP generation ownership.

Candidate digests are computed incrementally with framing exactly matching the canonical `replay_f32_slice_digest` function. A unit fixture requires streaming digest parity with the canonical full-slice digest.

Replay and same-source counterfactual modes are explicitly disabled in R1 because their current contracts require full candidate/source payload reconstruction. No silent weakening of those contracts is permitted.

## In-place candidate weight ownership

`source_weight_packed` becomes mutable only in the explicitly admitted streaming path.

For canonical tile k:

```text
source tile snapshot
-> candidate evidence
-> BP-DK compact evidence update
-> overwrite same packed tile with candidate weight
```

No second full candidate-weight Vec is created.

The scheduler receives:

```text
candidate_weight_in_place=true
candidate_weight_packed=[]
```

and scatters candidate values from the reused packed scratch.

## In-place momentum candidate ownership

The legacy full source-momentum clone is not created in admitted R1.

For each canonical tile the source momentum range is copied only into bounded tile/wave evidence, then the persistent runtime momentum destination range is overwritten with candidate momentum after evidence consumption.

Failure after partial in-memory candidate mutation remains fail-stop. This revision does not promote a partially mutated RAM candidate to durable training authority. The immutable durable source remains the restart authority.

## Orthogonal update retirement

Orthogonal update is an intermediate candidate/evidence payload, not durable training state. R1 keeps it only long enough to produce the required BP-DK per-tile/per-pair evidence and then retires it with the wave/pending tile payload. It is not reconstructed as a full parameter Vec.

## B05 Active host-capacity correction

The lower local and fused executors previously used `Vec::with_capacity(full_or_partition_elements)` even when B05 bulk readback was disabled, while the Active guard checked only `is_empty()`.

R1 changes Active execution to create zero-capacity host candidate Vecs and requires both:

```text
len == 0
capacity == 0
```

for candidate weight, candidate momentum, and orthogonal update.

This closes the len-only host-retirement claim without promoting B05 Active in the current N8 production route.

## Runtime witnesses

Per wave:

```text
[ASH-MUON-ATLAS-WAVE-HOST-CANDIDATE-RETIREMENT-R1]
```

The witness binds parameter index, generation, optimizer step, wave ID, Atlas page bytes, canonical coverage before/after, pending tile count/bound, local tile count, fused pair count, maximum bounded host wave candidate bytes, zero full-candidate allocation counts, and payload retirement.

Terminal witness:

```text
[ASH-MUON-ATLAS-WAVE-STREAMING-RETIREMENT-R1]
```

with:

```text
source_scratch_reused_in_place=true
source_scratch_retired=false
momentum_candidate_committed_in_place=true
orthogonal_update_retired_per_wave=true
coverage_exact=true
```

Runtime PASS token:

```text
PASS_ASH_BASETRAIN_TENSORCUBE_MUON_ATLAS_WAVE_STREAMING_HOST_FULL_CANDIDATE_MATERIALIZATION_RETIREMENT_R1
```

## Preserved closed axes

R1 preserves Physical N2 authority, RAM36 parent authority, cross-release authority, BP-DK SOURCE/TARGET optimizer-generation binding, RAM36 remaining-underflow attribution, successor ResidentWeightPack physical-allocation ownership transition, and Muon numerical kernel/profile math.

The exact RAM36 hard limit remains 38,654,705,664 bytes.

## Forbidden repairs

```text
No Hard-Limit Increase
No Private-Usage Discount
No Full Candidate Reservation Admission As Repair
No Mode Mutation On OOM
No Emergency Wave Resize
No Disk Spill Replacement
No Silent Legacy Full-Host Production Fallback
No Replay Contract Weakening
No Counterfactual Contract Weakening
No Muon Math Change
No BP-DK Generation Rebinding
No N2 Mutation
No RAM36 Parent Replacement
No Successor Reservation Reopen
```

## Focused acceptance

Static acceptance requires explicit R1 production admission, B04 ActiveVerified, B05 MirrorVerified, B06 MirrorVerified, replay disabled, counterfactual disabled, Atlas page-derived wave bounds, no full expected-elements candidate Vec in the streaming executor, empty aggregate candidate output, in-place candidate-weight and momentum commit, incremental canonical candidate digests, exact canonical coverage, B05 Active len+capacity zero guards, and all prior RAM36/BP-DK static closures remaining PASS.

## Physical acceptance

The next exact N8 must show wave retirement witnesses and the R1 PASS token while preserving the previously closed RAM36 successor transition and BP-DK target-generation witnesses.

If the raw 1,044,033,536-byte allocator failure disappears, this R1 has retired a relevant candidate high-water contributor. If a new allocator failure occurs before the R1 wave witness, its exact owner becomes the next first-failure axis rather than being masked by a larger RAM36 limit.

## Important non-claim: full source packed scratch

R1 retires **dedicated full candidate materialization**. It does not claim retirement of the scheduler's existing full `packed_muon_weight` source scratch.

That source scratch is reused in-place as the candidate-weight destination so R1 removes one additional full-size candidate copy, but the source scratch itself remains full-cardinality in this revision.

If the next physical witness proves that source scratch allocation is itself the first failing owner, the correct successor revision is a source-packing Atlas-wave projection retirement, not a reopening of this candidate-retirement closure.

## Non-claims

R1 does not claim all Muon host memory is O(max-wave-elements), full source scratch retirement, N8 completion, GEN13, global RAM36 optimality, B05 Active production admission, or B06 Active production admission.

It claims that the explicitly admitted R1 path no longer constructs a second full candidate-weight Vec, a full candidate-momentum Vec, or a full orthogonal-update Vec across the parameter, and that their host residency is bounded to Atlas waves plus compact canonical evidence.