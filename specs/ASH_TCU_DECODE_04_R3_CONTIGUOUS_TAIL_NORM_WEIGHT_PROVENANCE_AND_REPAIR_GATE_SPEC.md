# ASH-TCU-DECODE-04-R3 SPEC

## CONTIGUOUS_TAIL_NORM_WEIGHT_PROVENANCE_AND_REPAIR_GATE

```text
patch_id=ASH-TCU-DECODE-04-R3_CONTIGUOUS_TAIL_NORM_WEIGHT_PROVENANCE_AND_REPAIR_GATE
parent_patch=ASH-TCU-DECODE-04-R2_FINAL_PROJECTION_INPUT_ORIGIN_DIAGNOSTIC
parent_execution_id=decode04r2-9937058fbd1e064ae888
parent_status=PASS_ASH_TCU_DECODE_04_R2_FINAL_PROJECTION_INPUT_ORIGIN_DIAGNOSTIC
parent_verdict=decode04_r2_final_norm_output_degenerate
parent_root_cause_class=final_norm_output_degenerate
parent_route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
checkpoint_tensor_count=201
repair_target_count=4
non_target_tensor_count=197
norm_tensor_count=45
healthy_norm_peer_count=41
original_checkpoint_mutation_allowed=false
production_checkpoint_pointer_change_allowed=false
```

## Status

```text
PASS=PASS_ASH_TCU_DECODE_04_R3_CONTIGUOUS_TAIL_NORM_WEIGHT_PROVENANCE_AND_REPAIR_GATE
HOLD=HOLD_ASH_TCU_DECODE_04_R3_CONTIGUOUS_TAIL_NORM_WEIGHT_PROVENANCE_AND_REPAIR_GATE
FAIL=FAIL_ASH_TCU_DECODE_04_R3_CONTIGUOUS_TAIL_NORM_WEIGHT_PROVENANCE_AND_REPAIR_GATE
```

PASS proves only that a separate quarantined checkpoint was created, exactly four authorized RMSNorm tensors changed, all 197 non-target tensor payloads stayed bit-identical, and four repaired-weight consumers were observed without vocab projection or output promotion.

## Exact repair set

```text
model.layers.20.post_attention_layernorm.weight
model.layers.21.input_layernorm.weight
model.layers.21.post_attention_layernorm.weight
model.norm.weight
```

Original targets must be F32 `[2048]`, 8192 bytes, all zero, with payload SHA-256 `9f1dcbc35c350d6027f98be0f5c8b43b42ca52b7604459c0c42be3aa88913d47`.

Repaired targets must be F32 `[2048]`, exact ones, with payload SHA-256 `fc3bd1e348ef843a5052596a42863c169d54cc3c352449596039497873862155`.

## Provenance

Supported modes:

```text
canonical-source
genesis-unit-scale-consensus
```

Canonical-source requires the same 201 tensor names, dtypes and shapes, exact parity for all 197 non-target payloads, and exact-one values for all four targets.

Genesis-unit-scale-consensus requires exactly 41 healthy norm peers at exact f32 one, exactly four authorized zero norm targets, no additional zero norm tensors, and operator token:

```text
approve-exact-four-tail-norm-unit-scale-reconstruction
```

Missing provenance or approval is HOLD. Heuristic replacement values are forbidden.

## Checkpoint transaction

```text
open original read-only
reject output aliasing original
reject existing final output
clone original safetensors bytes
replace only four target payload ranges
write create_new temporary file
flush and sync_all
reload and validate temporary file
verify 197 non-target payload digests
verify four repaired payload digests
atomically rename temporary to quarantine output
re-hash output
re-hash original and require byte identity
```

The original checkpoint, default pointer and production registry remain unchanged.

## Post-repair consumer probe

Load the repaired checkpoint and observe exactly four consumers in one bounded smoke pass that stops before vocab projection:

```text
layer_20_post_attention_layernorm
layer_21_input_layernorm
layer_21_post_attention_layernorm
final_norm
```

For each consumer, input, runtime weight and output must contain exactly 2048 finite values. Runtime weight must be exact ones. Input and output must be non-degenerate. Required counters:

```text
generation_pass_count=1
consumer_probe_count=4
vocab_projection_count=0
tensorcube_dispatch_count=0
sampler_use_count=0
token_commit_count=0
kv_cache_persist_count=0
runtime_output_changed=false
```

## CLI

Genesis consensus mode:

```text
--repo-root <PATH>
--model-spec <PATH>
--checkpoint <ORIGINAL_PATH>
--output-checkpoint <QUARANTINE_PATH>
--parent-manifest <R2_MANIFEST>
--provenance-mode genesis-unit-scale-consensus
--operator-repair-decision approve-exact-four-tail-norm-unit-scale-reconstruction
--smoke-token-id 1
--probe-timeout-ms 120000
--require-parent-r2-final-norm-output-degenerate-pass
--require-checkpoint-tensor-count 201
--require-target-count 4
--require-non-target-count 197
--require-norm-tensor-count 45
--require-healthy-norm-peer-count 41
--require-target-elements 2048
--require-target-bytes 8192
--require-target-dtype f32
--require-original-zero-payload-digest 9f1dcbc35c350d6027f98be0f5c8b43b42ca52b7604459c0c42be3aa88913d47
--require-replacement-one-payload-digest fc3bd1e348ef843a5052596a42863c169d54cc3c352449596039497873862155
--require-all-non-target-digests-identical
--require-original-checkpoint-unchanged
--require-atomic-output-write
--run-post-repair-consumer-smoke
--require-consumer-probe-count 4
--require-no-vocab-projection
--require-no-tensorcube-dispatch
--require-no-sampler-use
--require-no-token-commit
--require-no-default-pointer-change
--require-no-production-replacement
--write-runtime-artifacts
--write-local-manifest
```

Canonical-source mode replaces the provenance mode and decision token with `--provenance-checkpoint <PATH>`.

Exit codes:

```text
0=PASS repair and proof sealed
2=HOLD provenance or consumer proof incomplete
1=FAIL mutation, parity or authority contract broken
```

## Next state

R3 PASS authorizes only explicit diagnostic use of the repaired checkpoint:

```text
R3 repaired checkpoint
-> rerun DECODE-04-R2 with repaired checkpoint
-> require all hidden stages non-degenerate
-> rerun DECODE-04 with unchanged tolerances
-> require non-degenerate Burn reference and mismatch_count=0
-> only then consider DECODE-05
```

R3 never promotes the repaired checkpoint or changes the default checkpoint pointer.