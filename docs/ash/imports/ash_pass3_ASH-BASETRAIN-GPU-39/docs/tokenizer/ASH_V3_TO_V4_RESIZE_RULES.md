# ASH V3 -> V4 embedding / lm_head resize rules

## SSOT

This migration assumes the following files are the authoritative contract inputs:

- `tokenizer_manifest_clean_v3.json`
- `tokenizer_manifest_clean_v4.json` or a fully built V4 manifest
- `model_spec.toml` for the source checkpoint
- `model_spec_1p1b_v2.toml` for the target checkpoint
- the source checkpoint `.safetensors`

The checkpoint keys follow the project's checkpoint writer / loader contract:

- embedding: `model.embed_tokens.weight`
- lm_head: `lm_head.weight`
- fallback aliases accepted by the loader: `tok_embeddings.weight`, `embed_tokens.weight`, `output.weight`

These names come from the Rust checkpoint writer and loader in `base_train` and `model_core`. The migration script below uses the same aliases so the draft matches the project contract.

---

## Critical rule: V4 is a remap, not a pure append

The current V4 reserved-token draft inserts new reserved tokens at IDs `32..71`.
That means old V3 non-reserved token IDs are no longer stable.

So the migration must **not** do this:

- copy rows `0..old_vocab_rows`
- append extra rows at the tail

That would be wrong.

Instead the migration must do this:

1. build `token -> old_id` from the V3 manifest
2. build `token -> new_id` from the V4 manifest
3. for every V4 token, copy the V3 row only when the **token string matches** and the old id is within the source checkpoint row range
4. initialize missing rows with warm-start heuristics

In other words:

> row transfer is keyed by **token string**, not by raw row index.

---

## Row-count authority

There is already a source mismatch risk in the current project:

- source model spec uses `vocab_size = 56000`
- source V3 manifest may enumerate more entries than that

So the migration must treat the checkpoint tensor shape as the source of truth for loadable rows.

Rules:

- `source_rows = embedding.shape[0]`
- `target_rows = target model spec dimensions.vocab_size`
- any V3 manifest token whose `id >= source_rows` is **metadata only** for migration purposes and must not be copied from the checkpoint
- any V4 manifest token whose `id >= target_rows` is invalid and must fail validation

---

## Exact-copy rules

Copy rows exactly for:

- every token present in both V3 and V4
- where the V3 id is `< source_rows`
- and the V4 id is `< target_rows`

This includes preserved reserved tokens `0..31` and any overlapping non-reserved tokens.

Special validation:

- V3 and V4 tokens at ids `0..31` must be identical
- `<pad> <bos> <eos> <unk>` ids must remain `0 1 2 3`

---

## Initialization rules for new rows

Rows that exist in V4 but not in V3 must be initialized, not left zeroed.

### Embedding warm-start order

1. **Exact-copy** if token exists in V3
2. **Group centroid** if target token is a new reserved token
3. **Global centroid** for ordinary new vocabulary rows
4. add **small gaussian noise** scaled from the source tensor statistics

### lm_head warm-start order

Use the same rule as embeddings, independently.

### Default donor groups

Since V3 does not have `identity / bridge / guard / style / signal`, use donor centroids from existing V3 reserved groups:

- `identity` -> mean of `task + language + control`
- `bridge` -> mean of `control`
- `guard` -> mean of `control`
- `style` -> mean of `task + control`
- `signal` -> mean of `control + cue`
- `task` extension tokens -> mean of existing `task`
- ordinary new vocab -> global mean of all copied rows

This is a draft heuristic, not a proved optimum.

---

## Noise rule

For initialized rows:

- `row = centroid + N(0, sigma * init_scale)`
- suggested `init_scale = 0.01`

Where `sigma` is computed per tensor from the source tensor values.

Why:

- pure zeros are too artificial
- exact duplicated centroids make the new rows too collapsed
- tiny noise gives separation without blowing up logits

---

## Required outputs

A successful migration should emit:

- resized checkpoint safetensors
- migration report JSON
- optional copied V4 runtime/spec files into an output directory

The report should include at least:

- source rows / target rows
- copied row count
- initialized row count
- dropped source token count
- preserved special-token validation result
- key names actually used for embedding / lm_head

---

## Failure conditions

Abort if:

- V4 special tokens do not match expected ids
- V4 target rows do not equal target model spec vocab_size
- embedding / lm_head hidden dims do not match
- no embedding key can be found
- no lm_head key can be found
- V4 manifest has no `vocab` array and the caller did not choose reserved-only dry-run mode

---

## Practical command shape

```bash
python ash_v3_to_v4_migrate.py \
  --source-checkpoint ./workspace/base_train_runs/ash_1p1b_prod/full_model.safetensors \
  --source-manifest ./tokenizer_manifest_clean_v3.json \
  --target-manifest ./tokenizer_manifest_clean_v4.json \
  --source-model-spec ./specs/model_spec.toml \
  --target-model-spec ./specs/model_spec_1p1b_v2.toml \
  --target-runtime-profile ./specs/runtime_profile_v2.toml \
  --out-checkpoint ./workspace/base_train_runs/ash_1p1b_prod_v4/full_model.safetensors \
  --out-report ./workspace/base_train_runs/ash_1p1b_prod_v4/migration_report.json \
  --copy-switch-files
```

---

## Recommendation

Before a real migration run, do this in order:

1. finalize the real V4 tokenizer build
2. generate the full V4 manifest with a complete `vocab` array
3. run the migration in `--dry-run`
4. inspect the report
5. only then write the resized checkpoint

If the final V4 manifest is still just a scaffold with reserved tokens and no full vocab, only a reserved-only dry-run is honest. A full checkpoint migration is not yet grounded until the V4 vocabulary is actually built.
