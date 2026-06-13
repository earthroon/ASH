# Commit 16O-16V — Native Output Tail / Cache / Tokenizer Alignment Probes

## SSOT

16N conclusion is preserved:

- Adapter is not the current root-cause target.
- Base-only native inference can still repeat `걱정이네...`.
- Adapter quality must not be judged again until base-only output is normalized.

This patch moves the debug target to the base native generation pipeline:

1. tail id decode
2. output artifact freshness
3. tokenizer/checkpoint vocab alignment
4. sampling / argmax / cache matrix
5. native routing / density / penalty disable path
6. adapter re-entry only after base is clean

---

## Commit 16O — Native Output Tail Decode / Cache Stale Probe

Runtime now seals these fields into both the response JSON and the output artifact:

- `promptLen` / `prompt_len`
- `generatedTailLen` / `generated_tail_len`
- `generatedTailHead` / `generated_tail_head`
- `generatedTailDirectDecode` / `generated_tail_direct_decode`
- `generatedTailManifestDecode` / `generated_tail_manifest_decode`
- `outputTextPreview` / `output_text_preview`
- `usedHotTokenCache` / `used_hot_token_cache`
- `tailDecodeProbe` / `tail_decode_probe`

Decision rule:

- If direct tail decode is also `걱정이네...`, the selected generated ids already contain that phrase.
- If direct tail decode differs from output preview/text, inspect output extraction, postprocess, stale artifact, or cache reuse.

---

## Commit 16P — Output Artifact Freshness Seal

`outputPath` now includes:

- timestamp with milliseconds
- request id
- seed

The artifact itself now stores:

- `request_id`
- `seed`
- `input`
- `prompt_ids`
- `generated_ids`
- `output`
- tail decode probe
- tokenizer/checkpoint probe
- native auxiliary probe
- `artifact_freshness_seal`

The response now returns `artifactFreshnessSeal`:

- `outputPath`
- `outputStamp`
- `artifactModifiedAtUnixMs`
- `artifactTextMatchesResponseText`
- `pathIncludesRequestId`
- `pathIncludesSeed`

Standalone verifier:

```bash
python scripts/commit_16p_verify_artifact.py \
  --artifact artifacts/<output>.json \
  --request-id <request-id> \
  --seed <seed>
```

---

## Commit 16Q — Tokenizer Direct Decode Probe

Runtime probe compares:

1. `NativeTokenizer.decode(generated_tail_ids)`
2. manifest-piece detokenization from token ids
3. postprocessed artifact output text

Standalone probe:

```bash
python scripts/commit_16q_decode_ids.py \
  --manifest artifacts/tokenizer_manifest_v5_final.json \
  --ids 29035,13032
```

Known observation from this snapshot:

```json
{
  "tokenizer_vocab_size": 48259,
  "pieces": ["▁걱정이네", "▁나오거든요"],
  "manifest_piece_decode": "걱정이네 나오거든요"
}
```

So ids `29035,13032` really do map to `걱정이네 나오거든요` in the bundled tokenizer manifest.

---

## Commit 16R / 16T / 16U — Matrix Probe Generator

Matrix request generator:

```bash
python scripts/commit_16r_16t_matrix_requests.py \
  --runtime-profile specs/runtime_profile.toml \
  --model-spec specs/model_spec.toml \
  --tokenizer-manifest artifacts/tokenizer_manifest_v5_final.json \
  --checkpoint-paths <checkpoint.safetensors> \
  --prompt "안녕" \
  --seed 42 \
  --max-new-tokens 32
```

It writes:

```text
infer_debug/commit_16r_16t_16u_matrix.jsonl
```

Rows include:

- 16R-A: kv-cache on / gpu-argmax on
- 16R-B: kv-cache off / gpu-argmax on
- 16R-C: kv-cache on / gpu-argmax off
- 16R-D: kv-cache off / gpu-argmax off
- 16R-E: temperature 0.0
- 16R-F: temperature 0.7
- 16R-G: max_new_tokens 4
- 16R-H: max_new_tokens 32
- 16T: `1`, `안녕`, `테스트`, `A`, `.`
- 16U: routing off, density off, penalty off, aux all off

Payload flags accepted by `orchestrator_local/src/infer_entry.rs`:

- `disableNativeStructureRouting`
- `disableNativeTextDensity`
- `disableNativeGpuPenalty`

Aliases are also accepted:

- `disableNativeRouting` / `disable_native_routing`
- `disableNativeDensity` / `disable_native_density`
- `disableNativePenalty` / `disable_native_penalty`

---

## Commit 16S — Checkpoint / Tokenizer / Vocab Alignment Probe

Runtime now emits:

- `tokenizer_vocab_size`
- `model_spec_vocab_size`
- `checkpoint_embedding_shape`
- `checkpoint_lm_head_shape`
- `checkpoint_embedding_vocab_size`
- `checkpoint_lm_head_vocab_size`
- `max_generated_token_id`
- `max_banned_token_id`
- range checks
- `vocab_alignment_ok`
- warnings

Standalone probe:

```bash
python scripts/commit_16s_vocab_alignment_probe.py \
  --manifest artifacts/tokenizer_manifest_v5_final.json \
  --model-spec specs/model_spec.toml \
  --checkpoint <checkpoint.safetensors> \
  --generated-ids 29035,13032
```

Known observation from this snapshot when pairing `artifacts/tokenizer_manifest_v5_final.json` with `specs/model_spec.toml`:

- tokenizer vocab size: `48259`
- model spec vocab size: `56000`

That pairing is not aligned. The active runtime may use a different spec, so the probe is sealed into runtime output rather than treated as a universal verdict.

---

## Commit 16V — Adapter Re-entry Gate

Adapter inference quality is still sealed behind this order:

1. base-only normal output confirmed
2. 04096 attach
3. 221628 attach
4. compare output diff / top-k / gate / rerank delta

Until step 1 is green, adapter verdicts remain invalid.
