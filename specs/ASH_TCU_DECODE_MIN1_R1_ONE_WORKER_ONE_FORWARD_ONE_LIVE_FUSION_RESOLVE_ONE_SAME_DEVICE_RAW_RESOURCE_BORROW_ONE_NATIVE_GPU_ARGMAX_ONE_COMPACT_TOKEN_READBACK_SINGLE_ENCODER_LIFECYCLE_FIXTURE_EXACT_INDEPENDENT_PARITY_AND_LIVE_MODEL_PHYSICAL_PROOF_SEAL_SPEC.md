# ASH-TCU-DECODE-MIN1-R1
# One Worker / One Forward / One Live Fusion Resolve / One Same-Device Raw Resource Borrow / One Native GPU Argmax / One Compact Token Readback / Single Encoder Lifecycle / Fixture-Exact Independent Parity and Live-Model Physical Proof Seal

- Patch class: minimal physical proof
- Parent truth authority: `ASH-TRUTH-AUDIT-01-R2`
- New production decode revision: not authorized
- New promotion hierarchy: not authorized
- 16-worker execution: forbidden
- General production apply: not authorized

## 1. Purpose

The truth audit has removed direct `performed -> verified` authority, but currently reports no runtime-owned physical observation and no independent comparator. This patch proves the smallest complete decode unit:

```text
one worker
-> one prompt
-> one forward
-> one live Fusion last-logits resolve
-> one same-device raw-resource borrow
-> one native GPU argmax
-> one compact readback
-> one token ID
```

The existing 16-worker matrix, cohort loops, 2500-token target, manifest reducers, and promotion receipts are not part of MIN1.

## 2. Evidence levels

`Reported` means a component claims that work was performed.

`Observed` means runtime-owned evidence proves a submission, completion, raw-resource transition, compact readback, or returned token.

`Verified` means a physical result is compared with an independent expected result under an explicit rule.

A request, performed flag, receipt digest, or zero-failure count cannot create observation or verification authority.

## 3. Two-lane proof

MIN1 contains two independent lanes.

### Lane A: deterministic fixture parity

A fixed `f32` logits fixture is uploaded to a GPU storage buffer. The same native raw-lease argmax implementation used by live greedy decode runs against that buffer.

The CPU reference:

- ignores NaN values;
- fails when all values are NaN;
- selects the lowest token ID on equal scores;
- never reads live-model logits.

Required fixture evidence:

```text
fixture_expected_token_id present
fixture_gpu_token_id present
fixture_gpu_argmax_dispatch_observed=true
fixture_compact_readback_observed=true
fixture_readback_count=1
fixture_readback_bytes<=16
fixture_token_parity_verified=true
fixture_score_parity_verified=true
fixture_encoder_terminal_state=finalized
```

### Lane B: live-model physical execution

The existing strict live decode probe is reused with exactly:

```text
route=greedy_cached
cohort=bounded_reduced
worker_count=1
generation_count=1
selected_token_target=1
```

No new multi-worker coordinator is introduced.

## 4. Live path

The required live path is:

```text
runtime bootstrap
-> NativeWgpuModel load
-> BOS prompt
-> one forward
-> live Fusion last-logits tensor
-> owning Fusion client resolve
-> native WGPU primitive
-> same-device raw-resource borrow
-> native GPU argmax raw lease
-> compact 16-byte readback
-> one token authority receipt
```

The live path may not use:

```text
external fixture override registry
host-side full-logits materialization
host upload reconstruction
CPU greedy
legacy GPU sampler fallback
CPU oracle
```

## 5. Device and queue binding

MIN1 requires one authoritative selected token with a same-device raw lease. The selected token, GPU completion, and absence of queue mismatch together bind the live argmax to the owning runtime queue.

Required:

```text
fusion_resolve_attempt_count=1
fusion_resolve_success_count=1
raw_borrow_attempt_count=1
raw_borrow_success_count=1
same_device=true
same_queue=true
```

Unknown or mismatched device/queue identity is not PASS.

## 6. Native GPU argmax

The live and fixture lanes use `GpuPenaltyPass::dispatch_argmax_raw_lease`.

The implementation may use multiple compute passes inside one command encoder, but the lifecycle must remain singular:

```text
created
-> pass opened
-> pass closed
-> finished
-> submitted
-> completion observed
-> finalized
```

The compact output is `GpuPenaltyArgmaxOut`:

```text
token_id: u32
padding: u32
score: f32
padding: f32
```

Total readback size is 16 bytes. Full vocab logits and intermediate reduction buffers may not be mapped.

## 7. Fail-closed panic handling

Fixture and live execution are isolated with panic capture.

A WGPU validation panic, `Encoder is invalid`, map failure, or panic-contaminated run must produce:

```text
encoder_terminal_state=invalid
encoder_invalid_count>0
decode_min1_physical_proof_pass=false
```

An invalid encoder may not be reused.

## 8. Runtime-owned artifact

Canonical artifact:

```text
workspace/runtime/tensorcube/min1/ash_tcu_decode_min1_r1_runtime_artifact.json
```

Schema:

```text
ash.tcu.decode.min1.r1.runtime_artifact.v1
```

The artifact must include:

```text
worker_count
prompt_count
generation_count
fixture expected/GPU token IDs
fixture dispatch/readback/parity evidence
model load and forward counts
live Fusion resolve counts
raw borrow counts
GPU argmax dispatch/completion counts
compact readback count and bytes
live token ID
forbidden-path counters
encoder terminal states
buffer async error count
physical proof verdict
artifact digest
```

Caller input cannot set runtime observation, token ID, parity, or physical proof fields.

## 9. Non-vacuous requirements

Zero failures with zero execution is not PASS.

Required live counts:

```text
model_load_count=1
forward_count=1
fusion_resolve_attempt_count=1
fusion_resolve_success_count=1
raw_borrow_attempt_count=1
raw_borrow_success_count=1
gpu_argmax_dispatch_count=1
gpu_argmax_completion_count=1
readback_count=1
selected_token_count=1
```

The live token ID must be read from the strict token authority receipt, not supplied by the caller.

## 10. Forbidden counters

All must be zero:

```text
cpu_materialize_count
host_upload_count
legacy_fallback_count
cpu_oracle_count
external_fixture_map_attempt_count
encoder_invalid_count
buffer_async_error_count
```

## 11. PASS

PASS requires all of the following:

```text
fixture_token_parity_verified=true
fixture_score_parity_verified=true
fixture_readback_count=1
fixture_readback_bytes<=16

model_load_ok=true
forward_observed=true
fusion_resolve_ok=true
raw_resource_borrow_ok=true
same_device=true
same_queue=true

gpu_argmax_dispatch_ok=true
gpu_argmax_completion_observed=true
compact_readback_observed=true
readback_count=1
readback_bytes<=16
gpu_argmax_token_id present

encoder_terminal_state=finalized
all forbidden counters=0
live_physical_execution_observed=true
decode_min1_physical_proof_pass=true
```

## 12. HOLD

HOLD is correct when execution remains uncontaminated but physical proof is incomplete, including:

```text
fixture parity succeeds but live resolve fails
model load succeeds but raw borrow is unavailable
GPU dispatch is requested but completion is not observed
compact token readback is absent
```

HOLD may not emit verified authority.

## 13. FAIL

FAIL conditions include:

```text
fixture parity mismatch
invalid encoder
panic-contaminated live run
device or queue mismatch
full logits readback
CPU materialization
host upload fallback
legacy fallback
CPU oracle
readback larger than 16 bytes
zero token with PASS
```

## 14. Truth-audit integration

`ASH-TRUTH-AUDIT-01-R2` may consume this artifact through `--decode-min1-artifact`.

The truth audit must verify field values and non-vacuous counters. Artifact existence or digest validity alone is not physical proof.

Mapping:

```text
live physical completion -> RuntimeObservation
fixture parity -> IndependentComparator
decode_min1_physical_proof_pass -> independent physical verification
```

## 15. Governance freeze

MIN1 does not authorize:

```text
16-worker smoke rerun
2500-token route targets
new receipt hierarchy
new manifest authority layer
new decode promotion suffix
general production route switch
```

The next step after MIN1 PASS is a separate review of sampled-token MIN2 or reconnection of the existing worker gate.

## 16. Canonical seal

```text
Decode is not proven because a forward ran.
Decode is not proven because a GPU dispatch was requested.
Decode is not proven because a component reported success.

Decode MIN1 is proven only when one deterministic fixture independently
matches the native GPU argmax and one live model forward returns one token
through live Fusion resolve, same-device raw borrow, native GPU argmax,
and a compact readback with zero fallback.

One worker, one generation, one token.
No empty PASS and no receipt-made authority.
```
