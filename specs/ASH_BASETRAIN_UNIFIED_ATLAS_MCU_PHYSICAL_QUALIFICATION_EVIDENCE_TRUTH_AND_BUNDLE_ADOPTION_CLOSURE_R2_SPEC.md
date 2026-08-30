# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-PHYSICAL-QUALIFICATION-EVIDENCE-TRUTH-AND-BUNDLE-ADOPTION-CLOSURE-R2

## 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-PHYSICAL-QUALIFICATION-EVIDENCE-TRUTH-AND-BUNDLE-ADOPTION-CLOSURE-R2`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-R6-R7-R8-R8A-RUST-NATIVE-PHYSICAL-QUALIFICATION-MATERIALIZATION-CLOSURE-R1`

PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_PHYSICAL_QUALIFICATION_EVIDENCE_TRUTH_AND_BUNDLE_ADOPTION_CLOSURE_R2`

## 1. Purpose

R1 materialized a bounded Rust-native physical qualification chain across R6, R7, R8 and R8A. R2 closes evidence truth: every production-adoptable physical PASS field must be derived from the exact typed runtime evidence that proves that claim.

Core invariant:

`PASS field = typed evidence + exact provenance + validated predicate`.

A physical PASS field may not be emitted because a later phase succeeded, because the result is expected by construction, or because a caller supplied an ungrounded boolean.

## 2. Authority preservation

R2 creates no new GPU executor, adapter, Device, Queue, optimizer authority, routing policy, Atlas geometry, Physical N2 authority or training commit authority.

Physical execution remains owned by the existing `TensorCubeLocalMuonBatchExecutor` and existing `wgpu::Device/Queue`. R8A Queue submission identity remains the existing typed `SubmissionEpoch` returned by the submission-lease runtime. Existing exact submission waits remain active.

## 3. Scope

R2 owns:

- R6 shadow-membership evidence truth;
- R6 direct-R5 versus queued-R6 physical output parity;
- R6 stale-generation negative fixture truth;
- R6 mutable-range alias negative fixture truth;
- R7 E1/E2 physical expert-versus-E0 numerical evidence;
- R8 deterministic routing replay evidence;
- R8 homogeneous Active physical execution evidence;
- R8A heterogeneous indexed physical execution evidence;
- receipt derivation from typed evidence;
- child receipt/evidence digest binding;
- final bundle validation before publication.

R2 does not claim production training-Wave qualification, full-matrix Muon, fused-pair qualification, ActiveAsync, performance improvement, hardware Tensor Core execution or global MCU ownership.

## 4. Claim ownership

| Claim | Exact evidence owner |
|---|---|
| R6 shadow membership parity | R6 seal/legacy membership comparison |
| R6 active output bit parity | physical direct E0/R5 reference vs R6-derived queued descriptors |
| R6 stale-generation rejection | stale seal after queue generation advance |
| R6 mutable alias rejection | overlapping writable-range negative fixture |
| R7 E1 numerical compatibility | physical E1 vs E0 |
| R7 E2 numerical compatibility | physical E2 vs E0 |
| R8 routing determinism | identical descriptor/policy route replay |
| R8 homogeneous Active execution | dedicated homogeneous assignment physically executed through expert override |
| R8 heterogeneous physical materialization | forbidden R8 claim |
| R8A heterogeneous materialization | indexed multi-expert physical execution |
| R8A Queue submit | exact existing `SubmissionEpoch` |
| R8A exact wait | exact submission wait observed by backend |
| R8A indirection parity | indexed output vs direct selected-expert baseline |

## 5. R6 evidence contract

R2 introduces `McuR6PhysicalQualificationEvidenceR2`.

It records at minimum:

- expected and observed shadow membership counts;
- shadow membership divergence count;
- physical direct reference execution observed;
- physical queued execution observed;
- candidate-weight bit divergence count;
- candidate-momentum bit divergence count;
- orthogonal-update bit divergence count;
- status divergence count;
- stale-generation fixture executed/rejected/exact error class;
- mutable-alias fixture executed/rejected/exact error class;
- evidence digest.

The R6 qualification receipt is derived from this evidence. The receipt constructor does not accept caller-owned PASS booleans.

Required stale-generation error:

`E_UNIFIED_ATLAS_MCU_STALE_TENSORCUBE_JOB_QUEUE_GENERATION_R6`

Required alias error:

`E_UNIFIED_ATLAS_MCU_TENSORCUBE_JOB_MUTABLE_RANGE_ALIAS_R6`

A generic failure does not qualify either negative fixture.

## 6. R6 physical parity

R6 scheduling representation must not change qualified R5/E0 arithmetic. The physical qualification fixture therefore executes the same deterministic data twice:

1. direct canonical Local Muon tile descriptors;
2. descriptors regenerated from an actual sealed R6 queue epoch.

Candidate weight, candidate momentum, orthogonal update and status require exact bit/status parity.

## 7. R7 evidence contract

R2 introduces `McuR7ExpertPhysicalQualificationEvidenceR2` for E1 and independently for E2.

Evidence binds:

- exact expert identity;
- subgroup size 32;
- active Device SHADER_F16 capability;
- fixture-plan digest;
- E0 reference execution observed;
- target expert execution observed;
- maximum candidate-weight error;
- maximum candidate-momentum error;
- maximum orthogonal-update error;
- nonfinite/overflow divergence counts;
- subnormal classification;
- evidence digest.

Allowed numerical bounds remain the versioned R7 contract. R2 does not widen a bound from observed data.

`E1 PASS != E2 PASS`.

If E2 is optional and fails qualification, no production E2 receipt or PASS-shaped evidence is emitted.

## 8. R8 replay evidence

R2 introduces `McuR8RoutingReplayEvidenceR2`.

The same explicit policy source, qualified-expert mask and descriptor fixture are evaluated twice. The assignment-manifest digests must be identical and all routing/unqualified/duplicate/missing divergence counters must be zero.

The replay fixture may be heterogeneous. Heterogeneous routing proves routing determinism only.

## 9. R8 homogeneous Active evidence

R2 separates routing replay from physical homogeneous execution.

A dedicated nonzero homogeneous fixture is routed first. The selected already-qualified R7 expert is then physically executed through the existing Local Muon expert-override path. Evidence records:

- policy digest;
- expert-manifest digest;
- homogeneous assignment digest;
- selected expert;
- physical execution observed;
- Queue submit observed;
- exact wait observed;
- direct selected-expert parity;
- evidence digest.

R8 qualification may set:

`homogeneous_active_execution_materialized=true`

only as a consequence of this evidence.

R8 must emit:

`heterogeneous_active_execution_materialized=false`.

R8A child success may not retroactively fabricate R8 homogeneous evidence or make R8 claim heterogeneous materialization.

## 10. R8A heterogeneous evidence

R2 introduces `McuR8aHeterogeneousPhysicalQualificationEvidenceR2`.

A qualifying R8A fixture requires at least two nonempty expert buckets and records:

- qualified and physically executed expert masks;
- E0/E1/E2 job counts;
- nonempty bucket count;
- expert dispatch count;
- logical descriptor-index H2D bytes;
- numerical payload repack bytes;
- additional bucket D2H bytes;
- command encoder count;
- Queue submit count;
- exact `SubmissionEpoch.device_id`;
- exact `SubmissionEpoch.queue_id`;
- exact `SubmissionEpoch.ordinal`;
- Queue submission observed;
- backend outcome observed;
- exact wait observed;
- direct-baseline tile/status divergence;
- evidence digest.

Required current one-Wave invariants:

- `expert_dispatch_count == nonempty_bucket_count`;
- `logical_index_h2d_bytes == total_job_count * 4`;
- `logical_index_h2d_bytes <= 65,536`;
- source repack bytes = 0;
- momentum repack bytes = 0;
- candidate repack bytes = 0;
- additional bucket D2H bytes = 0;
- command encoder count = 1;
- Queue submit count = 1;
- exact submission wait observed = true;
- direct indexed-vs-selected-expert divergence = 0.

## 11. Receipt derivation rule

Production physical receipt construction follows:

`physical execution -> typed evidence -> evidence validation -> receipt derivation -> receipt seal`.

Forbidden for physical observation claims:

- literal PASS booleans;
- caller-provided PASS booleans;
- inference from pipeline construction;
- inference from execution-plan construction;
- inference from a different child stage.

Structural configuration declarations remain distinct from physical observations.

## 12. Bundle R2

Top-level schema:

`ash.basetrain.unified_atlas_mcu.physical_qualification_evidence_truth_bundle.r2`

The R2 bundle binds at minimum:

- Native CF1 binary identity;
- Cross-Release Physical Parent identity;
- Device capability digest;
- fixture-plan digest;
- R6 receipt digest + R6 evidence digest;
- R7 E1 receipt digest + evidence digest;
- optional R7 E2 receipt digest + evidence digest;
- R8 receipt digest + replay evidence digest + homogeneous physical evidence digest;
- R8A receipt digest + heterogeneous physical evidence digest;
- qualified and physically executed expert masks;
- zero training/optimizer/checkpoint/Physical-N2 mutation counts;
- bundle digest.

A receipt without its matching evidence is not adoptable. Evidence without its matching sealed receipt is diagnostic only.

## 13. Validation-before-publication

The materializer writes to staging first. Before staging becomes the final output root, the Rust-native bundle validator reopens and validates:

- every mandatory child receipt;
- every mandatory evidence object;
- every evidence digest;
- receipt/evidence binding to bundle digests;
- optional E2 receipt/evidence cardinality;
- R8 `heterogeneous_active_execution_materialized=false`;
- R8/R8A policy and expert-manifest parent binding;
- top-level bundle digest and zero-mutation declarations.

A failed validation must not publish a production-adoptable final root.

This revision does not yet introduce the later content-addressed immutable publication/current-pointer architecture.

## 14. Runtime entry

New child-only CLI:

`--materialize-unified-atlas-mcu-physical-qualification-evidence-truth-r2`

It reuses:

- `--mcu-physical-qualification-output-root`;
- `--mcu-r8-policy-source`;
- optional `--mcu-physical-qualification-require-e2`;
- mandatory Native CF1 release authority;
- mandatory Cross-Release Physical Parent authority.

The former R1 materializer entry is superseded and must not emit the old over-broad PASS-shaped receipts.

## 15. Static validation

R2 static validation proves at least:

- typed R6/R7/R8/R8A evidence structures exist;
- R6 negative fixtures bind exact failure classes;
- R8 replay and homogeneous physical evidence are separate;
- R8 heterogeneous materialization remains false;
- R8A exact submission epoch is threaded into evidence;
- bundle revalidation exists;
- forbidden literal physical PASS assignments are absent.

Static validation does not substitute for physical GPU qualification.

## 16. State mutation exclusion

Qualification mode performs no:

- training generation advance;
- optimizer commit;
- checkpoint commit;
- Physical N2 write;
- parent-state mutation.

Fixture candidate tensors are comparison-only and never become training candidate authority.

## 17. PASS semantics

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_PHYSICAL_QUALIFICATION_EVIDENCE_TRUTH_AND_BUNDLE_ADOPTION_CLOSURE_R2`

means that the current Native-CF1-sealed binary on the current admitted physical Device executed the bounded mandatory qualification fixtures and every production-adoptable physical PASS field was derived from its exact typed runtime evidence.

It specifically means:

- R6 shadow parity, active bit parity, stale rejection and alias rejection were separately observed;
- R7 low-precision qualification came from physical expert-vs-E0 evidence;
- R8 routing replay and homogeneous Active execution were separately observed;
- R8 did not claim heterogeneous physical materialization;
- R8A physically executed heterogeneous indexed dispatch, observed the real Queue submission and exact wait, retained zero numerical payload repack, and matched direct selected-expert baselines;
- the final bundle revalidated the receipt/evidence chain before publication.

It does not mean production training-Wave qualification, ActiveAsync, full parameter-domain qualification, fused-pair qualification, hardware Tensor Core execution, performance improvement or global MCU ownership closure.

## 18. Packaging

GitHub publication for this revision is spec-only unless a separate implementation publication is explicitly requested.

Implementation ZIP/full-source bake must exclude:

- this specification;
- all `specs/` content;
- patch-note/spec Markdown artifacts;
- bake manifests and manifest digests;
- generated qualification receipts/evidence/bundle manifests;
- static-check output artifacts and review reports.

The ZIP contains implementation source, build files and executable validation tooling only.

## 19. Center sentence

**R1 made the GPU walk the R6 -> R7 -> R8 -> R8A path. R2 seals exactly which physical footprint produced each sentence in the receipt: `true` is no longer evidence, it is only a compact consequence of validated evidence.**