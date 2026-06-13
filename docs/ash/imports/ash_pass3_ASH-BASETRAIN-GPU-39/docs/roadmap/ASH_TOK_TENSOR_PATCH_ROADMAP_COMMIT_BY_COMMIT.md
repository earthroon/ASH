# ASH-TOK-TENSOR Commit-by-Commit Patch Roadmap

## SSOT

`ASH-TOK-TENSOR`는 `tokenizer_v5`의 vocab/token_id/embedding row 의미를 고정한 채, QWave/천지인 피처를 vocab 확장이 아닌 side-channel tensor row로 붙이고, 미완성 safetensors 및 `base_train`의 monolithic full-load 경로를 차단한 뒤, atlas parallel grouped sequential route로 재바인드하는 라인이다.

## Merge Contract

- 두 ZIP은 하나의 ASH 본체 트리로 병합했다.
- 같은 경로가 겹친 파일은 `용량이 작은 ZIP = 최신`이라는 사용자 지시를 SSOT로 삼아 작은 ZIP 쪽 파일을 최종본으로 채택했다.
- 이번 병합에서 겹친 실제 파일은 `crates/model_core/src/lib.rs` 1개였다.
- `crates/model_core/src/lib.rs`는 BURN-23 본체의 기존 export에 `ASH-TOK-TENSOR-00` module/use export가 추가된 형태였으므로, 작은 ZIP의 최신본을 최종 활성 파일로 두었다.
- 원본 tokenizer/model/safetensors 외부 자산은 ZIP에 새로 vendoring하지 않는다.

---

## 00. Already Baked Baseline

### ASH-BURN-23

```txt
ASH-BURN-23
WCTX Approval Commit Receipt /
No Auto Accept No Unapproved State Commit Seal
```

역할:

```txt
BURN/WCTX 승인 커밋 영수증 라인의 현재 본체 기준점.
이 ZIP이 병합 베이스 트리다.
```

닫히는 것:

```txt
auto_accept = false
unapproved_state_commit = false
review_queue_bypass = false
```

### ASH-TOK-TENSOR-00

```txt
ASH-TOK-TENSOR-00
Tokenizer V5 External Reference Freeze + Cheonjiin/QWave Side-Channel Map /
No Token Id Remap No Vocab Expansion No Asset Vendoring Seal
```

역할:

```txt
보캡/token_id/embedding row 의미를 동결하고,
천지인/QWave를 새 token이 아닌 side-channel tensor row 계약으로 붙인다.
```

닫히는 것:

```txt
token_id_remapped = false
vocab_expanded = false
embedding_row_reordered = false
asset_vendored = false
```

PASS:

```txt
PASS_ASH_TOK_TENSOR_00_EXTERNAL_REFERENCE_VOCAB_FREEZE_NO_TOKEN_ID_REMAP_NO_VOCAB_EXPANSION_NO_ASSET_VENDORING
```

---

## 01. ASH-TOK-TENSOR-01

```txt
ASH-TOK-TENSOR-01
Incomplete Safetensors Artifact Sentinel /
No Full Tensor Load No Row Parity Claim Seal
```

목적:

```txt
미완성 safetensors를 completed checkpoint로 취급하지 못하게 막고,
base_train의 full checkpoint load / full embedding-lmhead upload /
unconditional full checkpoint snapshot / full base optimizer path를 위험 callsite로 봉인한다.
```

구현 범위:

```txt
crates/model_core/src/ash_tok_tensor_01_incomplete_safetensors_sentinel.rs
crates/model_core/src/bin/ash_tok_tensor_01_incomplete_safetensors_sentinel.rs
acceptance_reports/ASH-TOK-TENSOR-01.md
patch_reports/ASH-TOK-TENSOR-01_bake_report.md
ASH_TOK_TENSOR_01_STATIC_CHECKS.txt
ASH_TOK_TENSOR_01_BAKE_MANIFEST.json
```

열리는 것:

```txt
safetensors_declared_incomplete = true
base_train_callsite_inventory_created = true
atlas_grouped_sequential_load_required = true
base_train_route_rebind_required = true
base_train_config_schema_patch_required = true
base_train_cli_patch_required = true
ash_ft24_schedule_reuse_allowed = true
ash_ft25_group_executor_reuse_allowed = true
ash_ft40_dryrun_policy_reuse_allowed = true
```

닫히는 것:

```txt
full_safetensors_probe_executed = false
full_tensor_load_executed = false
full_checkpoint_upload_executed = false
full_embedding_materialized = false
full_lm_head_materialized = false
row_parity_probe_executed = false
embedding_row_parity_pass_claimed = false
lm_head_row_parity_pass_claimed = false
base_train_init_checkpoint_full_load_executed = false
base_train_load_full_checkpoint_weights_executed = false
base_train_load_full_checkpoint_into_model_executed = false
collect_full_checkpoint_snapshots_executed = false
full_embedding_cpu_readback_executed = false
full_lm_head_cpu_readback_executed = false
base_model_gradient_allocated = false
full_model_optimizer_state_created = false
model_forward_executed = false
tensor_projection_executed = false
weight_commit_executed = false
optimizer_step_executed = false
```

PASS:

```txt
PASS_ASH_TOK_TENSOR_01_INCOMPLETE_SAFETENSORS_SENTINEL_NO_FULL_TENSOR_LOAD_NO_ROW_PARITY_CLAIM
```

---

## 02. ASH-TOK-TENSOR-02

```txt
ASH-TOK-TENSOR-02
BaseTrain Full Load Callsite Inventory /
No Runtime Mutation Seal
```

목적:

```txt
base_train 내부의 full-load 위험 callsite를 실제 파일/함수 단위로 inventory하고,
아직 런타임 코드는 변경하지 않는다.
```

구현 범위:

```txt
crates/base_train/src/full_load_callsite_inventory.rs
crates/base_train/src/bin/ash_tok_tensor_02_full_load_callsite_inventory.rs
acceptance_reports/ASH-TOK-TENSOR-02.md
patch_reports/ASH-TOK-TENSOR-02_bake_report.md
ASH_TOK_TENSOR_02_STATIC_CHECKS.txt
ASH_TOK_TENSOR_02_BAKE_MANIFEST.json
```

확인 대상:

```txt
1. CLI init_checkpoint_paths
2. training.rs init checkpoint branch
3. streaming training branch
4. reference_checkpoint.rs fs::read full
5. reference_checkpoint.rs tensor_to_f32_vec all tensors
6. reference_checkpoint.rs upload_full_embedding=true
7. reference_checkpoint.rs upload_full_lm_head=true
8. checkpoint.rs collect_full_checkpoint_snapshots
9. training.rs snapshot before save guard
10. config.rs save_full_checkpoint default true
11. optimizer full HybridTrainModel scope
```

닫히는 것:

```txt
runtime_code_mutated = false
config_schema_mutated = false
cli_changed = false
checkpoint_loader_changed = false
training_loop_changed = false
```

PASS:

```txt
PASS_ASH_TOK_TENSOR_02_BASETRAIN_FULL_LOAD_CALLSITE_INVENTORY_NO_RUNTIME_MUTATION
```

---

## 03. ASH-TOK-TENSOR-03

```txt
ASH-TOK-TENSOR-03
Atlas Parallel Grouped Sequential Tensor Load Plan /
No Full Checkpoint Upload Seal
```

목적:

```txt
safetensors / embedding / lm_head / layer stack을 full load하지 않고,
atlas parallel group + sequential load 단위로 나누는 tensor group manifest와 load plan을 만든다.
```

구현 범위:

```txt
crates/model_core/src/ash_tok_tensor_03_atlas_grouped_sequential_load_plan.rs
crates/model_core/src/bin/ash_tok_tensor_03_atlas_grouped_sequential_load_plan.rs
schemas/ash_tok_tensor_group_manifest.schema.json
schemas/ash_tok_tensor_sequential_load_plan.schema.json
acceptance_reports/ASH-TOK-TENSOR-03.md
patch_reports/ASH-TOK-TENSOR-03_bake_report.md
ASH_TOK_TENSOR_03_STATIC_CHECKS.txt
ASH_TOK_TENSOR_03_BAKE_MANIFEST.json
```

열리는 것:

```txt
tensor_group_manifest_created = true
atlas_group_plan_created = true
sequential_group_order_created = true
embedding_group_plan_created = true
lm_head_group_plan_created = true
layer_group_plan_created = true
group_boundary_digest_created = true
group_order_receipt_created = true
```

닫히는 것:

```txt
full_checkpoint_upload_executed = false
full_safetensors_load_executed = false
full_embedding_materialized = false
full_lm_head_materialized = false
model_forward_executed = false
weight_commit_executed = false
```

PASS:

```txt
PASS_ASH_TOK_TENSOR_03_ATLAS_PARALLEL_GROUPED_SEQUENTIAL_TENSOR_LOAD_PLAN_NO_FULL_CHECKPOINT_UPLOAD
```

---

## 04. ASH-TOK-TENSOR-04

```txt
ASH-TOK-TENSOR-04
BaseTrain Atlas Route Config Rebind /
No Init Checkpoint Full Load Seal
```

목적:

```txt
base_train config/CLI에 atlas grouped sequential route를 추가하고,
기존 init_checkpoint_paths full-load route가 기본 경로가 되지 못하게 막는다.
```

구현 범위:

```txt
crates/base_train/src/config.rs
crates/base_train/src/bin/base_train.rs
crates/base_train/src/atlas_route_config.rs
acceptance_reports/ASH-TOK-TENSOR-04.md
patch_reports/ASH-TOK-TENSOR-04_bake_report.md
ASH_TOK_TENSOR_04_STATIC_CHECKS.txt
ASH_TOK_TENSOR_04_BAKE_MANIFEST.json
```

추가 CLI:

```txt
--base-train-route=atlas_grouped_sequential
--tensor-group-manifest <path>
--atlas-group-plan <path>
--sequential-load-plan <path>
--no-full-checkpoint-load
```

config 기본 계약:

```txt
base_train_route = AtlasGroupedSequential
allow_full_checkpoint_load = false
allow_full_embedding_upload = false
allow_full_lm_head_upload = false
save_full_checkpoint = false
save_atlas_group_delta = true
save_group_receipt = true
```

닫히는 것:

```txt
init_checkpoint_full_load_default = false
load_full_checkpoint_weights_default_route = false
load_full_checkpoint_into_model_full_upload_default = false
```

PASS:

```txt
PASS_ASH_TOK_TENSOR_04_BASETRAIN_ATLAS_ROUTE_CONFIG_REBIND_NO_INIT_CHECKPOINT_FULL_LOAD
```

---

## 05. ASH-TOK-TENSOR-05

```txt
ASH-TOK-TENSOR-05
BaseTrain Full Snapshot Guard /
No Unconditional Full Readback Seal
```

목적:

```txt
save_full_checkpoint=false여도 collect_full_checkpoint_snapshots가 먼저 실행되는 구조를 차단한다.
full checkpoint snapshot은 명시적 gate 없이는 호출되지 않아야 한다.
```

구현 범위:

```txt
crates/base_train/src/checkpoint.rs
crates/base_train/src/training.rs
crates/base_train/src/full_snapshot_gate.rs
acceptance_reports/ASH-TOK-TENSOR-05.md
patch_reports/ASH-TOK-TENSOR-05_bake_report.md
ASH_TOK_TENSOR_05_STATIC_CHECKS.txt
ASH_TOK_TENSOR_05_BAKE_MANIFEST.json
```

닫히는 것:

```txt
collect_full_checkpoint_snapshots_before_save_guard = false
full_embedding_cpu_readback = false
full_lm_head_cpu_readback = false
full_layer_stack_cpu_readback = false
```

대체 저장:

```txt
adapter_only_checkpoint
atlas_group_delta_checkpoint
group_receipt_manifest
```

PASS:

```txt
PASS_ASH_TOK_TENSOR_05_BASETRAIN_FULL_SNAPSHOT_GUARD_NO_UNCONDITIONAL_FULL_READBACK
```

---

## 06. ASH-TOK-TENSOR-06

```txt
ASH-TOK-TENSOR-06
Embedding LMHead Atlas Shard Contract /
No Full Row Materialization Seal
```

목적:

```txt
embedding/lm_head를 full matrix로 materialize하지 않고,
vocab row / tile / group 단위의 atlas shard로 취급하는 계약을 세운다.
```

구현 범위:

```txt
crates/model_core/src/ash_tok_tensor_06_embedding_lmhead_atlas_shard_contract.rs
crates/model_core/src/bin/ash_tok_tensor_06_embedding_lmhead_atlas_shard_contract.rs
schemas/ash_embedding_lmhead_atlas_shard.schema.json
acceptance_reports/ASH-TOK-TENSOR-06.md
patch_reports/ASH-TOK-TENSOR-06_bake_report.md
ASH_TOK_TENSOR_06_STATIC_CHECKS.txt
ASH_TOK_TENSOR_06_BAKE_MANIFEST.json
```

열리는 것:

```txt
embedding_shard_contract_created = true
lm_head_shard_contract_created = true
vocab_axis_grouped = true
hidden_axis_tile_bound = true
row_parity_deferred_to_grouped_probe = true
```

닫히는 것:

```txt
full_embedding_row_materialization = false
full_lm_head_row_materialization = false
full_vocab_axis_scan = false
```

PASS:

```txt
PASS_ASH_TOK_TENSOR_06_EMBEDDING_LMHEAD_ATLAS_SHARD_CONTRACT_NO_FULL_ROW_MATERIALIZATION
```

---

## 07. ASH-TOK-TENSOR-07

```txt
ASH-TOK-TENSOR-07
BaseTrain Atlas Group Shadow Step /
No Full Model Optimizer State Seal
```

목적:

```txt
base_train이 full model optimizer state를 만들지 않고,
선택된 atlas group에 대해서만 shadow delta train step을 수행하는 계약을 만든다.
```

재사용 대상:

```txt
ASH-FT-24 schedule
ASH-FT-25 group local executor
ASH-FT-40 first group training dryrun
```

구현 범위:

```txt
crates/base_train/src/atlas_group_shadow_step.rs
crates/base_train/src/bin/ash_tok_tensor_07_atlas_group_shadow_step.rs
acceptance_reports/ASH-TOK-TENSOR-07.md
patch_reports/ASH-TOK-TENSOR-07_bake_report.md
ASH_TOK_TENSOR_07_STATIC_CHECKS.txt
ASH_TOK_TENSOR_07_BAKE_MANIFEST.json
```

열리는 것:

```txt
selected_atlas_group_train_step_created = true
group_local_forward_backward_allowed = true
shadow_delta_created = true
candidate_only_optimizer_update = true
```

닫히는 것:

```txt
full_model_optimizer_state_created = false
base_model_weight_commit = false
safetensors_mutation = false
model_forward_for_generation = false
```

PASS:

```txt
PASS_ASH_TOK_TENSOR_07_BASETRAIN_ATLAS_GROUP_SHADOW_STEP_NO_FULL_MODEL_OPTIMIZER_STATE
```

---

## 판단불가 / Probe Deferred

```txt
actual_safetensors_completion_ratio = unknown
safetensors_header_keys = unknown
embedding_tensor_key = unknown
lm_head_tensor_key = unknown
row_parity_pass = unknown
base_param_gradient_exclusion = unknown
full_model_optimizer_state_actual_creation = unknown
atlas_group_unit_final_choice = unknown
```

위 항목은 실제 probe 전까지 PASS로 주장하지 않는다.
