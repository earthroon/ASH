# AOF-R1-CF2: Packed Resource Lifetime Closure

## Revision
- Parent: AOF-R1-CF1.
- Successor: AOF-R1-VH6.
- Scope: actual same-Queue completion and packed-bank lifetime after both numerical success and early error.
- This is a **source/acceptance specification**, not a physical PASS assertion.

## Two independent authorities
```text
numerical: Pending | Qualified | UnqualifiedEarlyExit
completion: NotSubmitted | InFlight | Completed | Unknown/Failed
```
A numerical rejection is not evidence of queue completion or device failure.

## Required code boundaries
- `crates/model_core/src/aof_r1_packed_head_reuse.rs`: phase Idle/Active/PendingRetirement/QuarantinedTerminal; verify exact owner digest, generation, and bank identity; completed release is once-only; duplicate/stale completion must fail closed.
- `crates/model_core/src/aof_r1_future_heads.rs`: register the *actual bound WGPU queue* completion callback for both qualified and early-exit paths; retain `ArkPackedHeadLease`, checkpoint/runtime owner and physical queue handles until completion; no early recycle.
- `crates/model_core/src/aof_r1_packed_head_reuse_tests.rs`: deterministic CPU-only state-machine negatives (not physical proof).
- `crates/orchestrator_local/src/aof_r1_vh5_cli.rs`: distinguish terminal-owner blocker from new, independent numerical failure; optional physical early-exit lifetime canary for future VH6.

## Transition contract
```text
Active + numerical reject + in-flight -> PendingRetirement; acquire rejected
PendingRetirement + actual matching Queue completion -> Idle; same-owner reacquire allowed
Completed qualified -> Idle; counted exactly once
Stale generation / wrong owner / repeated release -> fail closed
Unprovable terminal completion -> QuarantinedTerminal; never manufacture a PASS
```
A callback discarded without completion proof must retain resources and fail closed. Avoid ordinary permanent `mem::forget` of proven-completed work.

## Physical canary evidence boundary
- On the real owner/queue, submit an actual WGPU command-buffer copy, terminate the packed candidate as `UnqualifiedEarlyExit`, observe PendingRetirement and denied acquire, then observe the callback/retirement, then reacquire with the same owner and higher generation.
- Record that this is **FORCED_UNQUALIFIED_AFTER_REAL_GPU_COPY**, a lifecycle fixture. It does **not** prove that a real learned-model logit comparison was rejected.
- For full failure-path admission, separately observe naturally rejected or deliberately rejected numerical qualification on the real packed shader path with a matching completion receipt; if absent, record that coverage as UNKNOWN and keep full failure-path physical closure unpromoted.

## Invariants
```text
precompletion reuse = 0
duplicate retire = 0
stale owner/generation retire = 0
owner drop before completion = 0
permanent quarantine of proven-completed numerical reject = 0
numerical tolerance, winner, near-tie rules unchanged
FuturePool and canonical commit unchanged
budget and no-production-promotion preserved
```

## Receipts
- Expose per-owner `ArkPackedHeadLifetimeObservation`: owner digest, generation, phase, retired-qualified count, retired-unqualified count, pending count, terminal quarantine count.
- Physical canary JSON: `ash.aof_r1.cf2.physical_early_exit.v1`, same bound device/queue, generation and completion witness.
- VH5 optional per-rank `<rank>.cf2_lifetime.json` + VH5 matrix `cf2_physical_early_exit_canaries`.
- No fabricated lease identity, no fake callback, no automatic quality/policy adoption.

## Admission
`PASS_AOF_R1_CF2_PACKED_RESOURCE_LIFETIME_CLOSURE` requires: CF1 real COMPILE PASS; real queue completion, rejected-but-completed canary with pinned owner and same-owner reacquire, currentness, duplicate and stale negatives; plus actual numerical rejection-path coverage if claiming full numerical-failure physical closure. Without real GPU execution: SOURCE/STATIC only; PHYSICAL=NOT_RUN.
