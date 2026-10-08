# AOF-R1-VH6: Real Quality / GPU / Commit Qualification

## Revision
- Parents: AOF-R1-CF1 and AOF-R1-CF2.
- Scope: native held-out quality, rank/depth parity and canonical commit matrix.
- Successor: AOF-R1-CF3 evaluator compute compaction.
- **No fused production cutover, no quality-based automatic rank choice, no performance promotion.**

## Physical producer route
Existing implementation owners are mandatory. Do not substitute static fixtures for:
1. `base_train::aof_r1_head_quality_native::evaluate_aof_r1_frozen_heads`: *real* model/tokenizer/head checkpoint; same held-out split, head pair and rank identities; per offset +2/+3/+4/+5 valid targets, CE, accuracy and root-conditional measurements. Training rows never become evaluation evidence.
2. `profile_campaign`: D1/D2/D4 real prefix acceptance, matched-prefix histograms and verified proposal counts, same split, rank and workloads, sealed sidecars.
3. `vh5` with `cf2_lifetime_canary=true`: actual WGPU legacy vs packed/fused logits, winner/runner-up near-tie and numerical thresholds unchanged, two ranks × D1/D2/D4, FuturePool currentness, queue completion, retirement and same-owner canary; numerical-error physical coverage separately labeled from forced early-exit copy fixture.
4. `commit_stability`: EOS/StopSequence/MaxNewTokens, cancel before/after publication, emit failure and ACK distinction, stale identity, duplicate consume, partial prefix/tail discard, repeated fresh sessions, OFF/ON token/text/stop/KV logical-position comparison.

## Same-source input law
Use one explicit run configuration tying together:
```text
matrix_id
cf1_compile_receipt
quality_input
profile_input
vh5_input
commit_input
```
Exact canonicalized model, tokenizer, checkpoint pair, rank, held-out split identity are required. Recheck tracked inputs before each physical producer. Fresh native outputs must be created in the current run, not resurrected from disk.

## Numerical and canonical invariants
```text
for all horizons: finite CE, accuracy; valid_target_count > 0
rank relation = dominance | tradeoff | measured equality | evidence insufficient
loss decrease alone never qualifies a rank
D1, D2, D4 actual GPU comparisons all covered
existing atol/rtol, winner match and near-tie gap unchanged
canonical KV publication after GPU completion and currentness/admission/cancel checks
duplicate KV/token append = 0; duplicate commit = 0
stale publication = 0; precompletion reuse = 0
failed emit is not ACK; already-published canonical history remains
EOS / stop / max token result and final canonical state exact when comparability conditions hold
```

## Implementation targets
- `crates/orchestrator_local/src/aof_r1_vh6_cli.rs` (new composition; `--vh6 INPUT --out NEW_DIRECTORY`).
- `crates/orchestrator_local/src/aof_r1_vh5_cli.rs` (CF2 real-Queue lifetime witness).
- `crates/orchestrator_local/src/bin/ash_aof_r1_cf7_cf8_cf9_gate.rs` (CLI registration).

## Receipt
`vh6_qualification.json`, schema `ash.aof_r1.vh6.real_quality_gpu_commit_qualification.v1`: parent CF1 source/compile seal; two rank checkpoints; held-out split seal; +2/3/4/5 metrics; D1/D2/D4 profile acceptance; VH5 GPU parity and CF2 canaries; commit coverage; no early admission; per-producer receipt seals; zero false promotion. Cross-run device/queue identity not proven merely by leg-local owner IDs must be **UNKNOWN**, not invented same physical ID.

## Evidence / stop rules
- Any absent/failed source, rank/split binding, actual native execution, GPU depth or commit case => HOLD/FAIL; no `PASS` aggregate.
- One rank may trade off CE/accuracy/acceptance against the other; do not invent a threshold to force a winner.
- A successful runtime campaign may emit `PASS_AOF_R1_VH6_REAL_QUALITY_GPU_COMMIT_QUALIFICATION` only for the exact covered matrix, and only if its bound model/queue/frozen quality and commit legs ran and accepted.
- Full numerical-rejection lifetime coverage that is not exercised must remain separately unqualified, even if the WGPU-copy early-exit fixture passes.
- All performance conclusions remain NOT_PROMOTED; `production_admission=false`, `promoted=false`.

## Parent negative gates
CF1 source/compile PASS required; CF2 real queue lifetime receipt required; source and Cargo.lock identities fixed. No queue callback simulation, host FuturePool full-tree readback, implicit CPU fallback, relaxed tolerances, or merged failed/valid quality observations.
