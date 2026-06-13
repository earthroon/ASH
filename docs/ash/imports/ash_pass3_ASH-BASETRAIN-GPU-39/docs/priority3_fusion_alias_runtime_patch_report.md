# Priority-3 fusion alias runtime promotion patch report

## Base
- Applied on uploaded `ash_pass3 (4).zip` working tree.

## Patched files
- `vendor_fork_scaffold/burn-fusion-local/src/external_alias_barrier.rs`
- `vendor_fork_scaffold/burn-fusion-local/src/runtime_splice.rs`
- `vendor_fork_scaffold/burn-fusion-local/src/lib.rs`
- `vendor_fork_scaffold/upstream_real_insert/burn/crates/burn-fusion/src/client.rs`
- `docs/priority3_fusion_alias_runtime_patch_report.md`

## What this patch actually does
- Formalizes the scaffolded fusion alias layer with additive decision/status APIs.
- Adds `ExternalAliasBarrierDecision` so route + trace become a single SSOT object instead of loose tuples.
- Adds explicit scaffold status helpers for alias barrier and runtime splice layers.
- Adds an upstream-mirrored `resolve_tensor_float_for_write_with_runtime_splice_decision(...)` entrypoint that returns both the resolved primitive and the alias trace.

## What this patch does NOT do
- It does not fully integrate the mirrored upstream client into a real upstream fork.
- It does not remove the callback-based promotion seam.
- It does not build-verify the whole tree.

## Why this is the correct priority-3 patch
Priority-1 closed native identity/bootstrap lifetime.
Priority-2 gated consumer mode selection up front.
Priority-3 should promote the scaffolded fusion alias/runtime-splice layer into a first-class, inspectable contract so later patches can wire it into real consumers without tuple drift or silent route loss.
