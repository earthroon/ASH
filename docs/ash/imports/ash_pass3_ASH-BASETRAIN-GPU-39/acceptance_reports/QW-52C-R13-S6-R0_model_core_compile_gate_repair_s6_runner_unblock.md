# QW-52C-R13-S6-R0
## Model Core Compile Gate Repair / S6 Runner Unblock Seal

## 1. SSOT
- base_patch: QW-52C-R13-S6
- parent_ssOT: QW-52C-R13
- runtime_apply_allowed: false
- promotion_eligible: false
- weight_commit_allowed: false
- safe_profile_apply_allowed: false
- policy_promotion_allowed: false

## 2. Status
- status: PATCH_APPLIED_CARGO_UNVERIFIED_IN_BAKE_ENV
- cargo_check_executed_in_bake_env: false
- reason: bake container has no cargo/rustc available

## 3. Compile Blocker Repair Matrix
| File | Error | Repair |
|---|---|---|
| crates/model_core/src/cji_plosive_force_class_fixture.rs | E0061 | aligned `qw52b_risk_level` call to `(Option<f32>, available: bool)` and preserved unavailable state |
| crates/model_core/src/dream_collapse_simulation.rs | E0308 | added explicit expected/predicted outcome mapping function |
| crates/model_core/src/controlled_awareness_soft_rerank_shadow.rs | E0505 | extracted actual/shadow top1 scalar values before moving vectors |
| crates/model_core/src/controlled_awareness_soft_rerank_shadow.rs | E0505 | extracted highest-risk scalar values before moving candidates |

## 4. No Runtime Mutation
- runtime_apply_allowed: false
- runtime_default_apply_allowed: false
- token_selection_mutation_allowed: false
- token_rank_mutation_allowed: false
- logit_mutation_allowed: false
- sampler_mutation_allowed: false

## 5. Local Verification Required
Run:

```bash
cargo check --workspace --all-targets
cargo run --bin qw52c_r13_s6_runtime_topk_shadow_observation_replay
cargo run --bin qw52c_r13_s6_runtime_topk_shadow_observation_replay_validate
```

Expected S6 runner behavior until real trace exists:

```txt
BLOCKED_MISSING_REAL_RUNTIME_TRACE_INPUT
```

## 6. Next Patch Recommendation
- QW-52C-R13-S6-R0-R1 — Local Cargo Verification Receipt / Remaining Compile Error Audit Seal
