# 16AI-QW-38G-R6A-DECODE-16 Bake Report

## Status
PASS_STATIC_TM_CONTEXT_BRIDGE_CONTRACT

## Scope
- Added Translation Memory context policy, previous cue context, TM snapshot, register continuity, violation, bridge, receipt, and stub modules.
- Extended DECODE-04 quality score snapshot with TM/register continuity slots.
- Added static fixtures and receipts for pass, polite-to-casual drift, term memory drift, honorific mismatch, abrupt tone shift, and missing previous context.

## Non-execution guarantees
- candidate_reject_executed_count: 0
- rewrite_executed_count: 0
- fallback_apply_executed_count: 0
- rollback_executed_count: 0
- runtime_decode_executed_count: 0
- model_forward_executed_count: 0
- sampling_executed_count: 0
- external_tm_lookup_executed_count: 0

## Canonical receipt keys
```json
{
  "register_pass": "q4sha256:8ac1656b1d9d4b387475a8ce9b50364c8b83001d63538b8c7eea84cd7603cbc3",
  "polite_to_casual_drift": "q4sha256:ffcb176d566f441e4ecb675580e02ce8ccaabcccdaf0d622ba01099d76dbabb6",
  "term_memory_drift": "q4sha256:5e0be6c1b08dcd864f89fa1f6ef8e8883fe4b84eaecd20a7690fc76b147795e4",
  "honorific_mismatch": "q4sha256:247d6d7994b51f15305f78491ea1e71f33aedf24e80abc2db9237f8db95489e9",
  "abrupt_tone_shift": "q4sha256:3ef6ab7aa8690543f2c4319210331dc8469502c3379e1c39fc1e2a3f3db2eeb1",
  "missing_previous_context": "q4sha256:1d30f05eca896f877387052aaedd825141a5e0b7ff67e3c9d987532fd1495698"
}
```

## Boundary
This patch seals previous cue/register/TM continuity recommendations only. It does not rewrite, reject, fallback, rollback, run model forward, sample, or call external TM services.
