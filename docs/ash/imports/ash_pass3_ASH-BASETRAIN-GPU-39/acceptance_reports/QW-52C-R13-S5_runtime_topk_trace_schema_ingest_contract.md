# QW-52C-R13-S5
## Runtime TopK Trace Schema / Ingest Contract Seal

## 1. SSOT

- base_patch: `QW-52C-R13-S4`
- parent_ssot: `QW-52C-R13`
- status: `PASS_RUNTIME_TOPK_TRACE_SCHEMA_INGEST_CONTRACT_NO_APPLY`
- runtime_apply_allowed: `false`
- runtime_default_apply_allowed: `false`
- promotion_eligible: `false`
- weight_commit_allowed: `false`
- safe_profile_apply_allowed: `false`
- policy_promotion_allowed: `false`

## 2. Schema Scope

- `RuntimeTopKToken`
- `RuntimeTopKTraceRecord`
- `RuntimeTopKTraceBatch`
- `RuntimeTraceEvidenceKind`
- `RuntimeTraceBackend`

## 3. Ingest Contract

- `actual_topk` is required.
- `selected_token_id` must exist in `actual_topk`.
- `shadow_topk` is observation-only.
- `shadow_result_applied=false`.
- token selection / token rank / logit / sampler mutation is forbidden.

## 4. Fixture Status

| field | value |
|---|---:|
| schema_only | true |
| fixture evidence_kind | StaticFixture |
| fixture_record_count | 1 |
| real_runtime_trace_ingested | false |
| real_runtime_record_count | 0 |
| model_vocab_cap_fixture | 48259 |

## 5. Forbidden Permission Check

| field | value |
|---|---|
| runtime_apply_allowed | false |
| runtime_default_apply_allowed | false |
| promotion_eligible | false |
| weight_commit_allowed | false |
| safe_profile_apply_allowed | false |
| policy_promotion_allowed | false |

## 6. No Mutation Check

| field | value |
|---|---|
| token_selection_mutation_allowed | false |
| token_rank_mutation_allowed | false |
| logit_mutation_allowed | false |
| sampler_mutation_allowed | false |

## 7. Validator Separation

- generator writes S5 outputs.
- validator reads S5 outputs only.
- validator does not ingest real runtime traces.
- validator does not regenerate historical R13/S0/S1/S2/S3/S4 artifacts.

## 8. Next Patch Recommendation

`QW-52C-R13-S6 — Runtime TopK Shadow Observation Replay / No Token Mutation Seal`
