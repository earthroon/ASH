# ASH-TOK-TENSOR 다음 세션 인계사항

## 0. 현재 세션 결론

현재 라인은 `ASH-TOK-TENSOR`로 새로 분리한다.
기존 `QW-TOK-FORGE` / `ASH-FT` / `BURN` 라인과 연결은 하되, 이번 목적은 **tokenizer_v5 보캡을 유지한 상태에서 QWave/천지인 텐서 피처를 side-channel로 붙이고, 미완성 safetensors 및 base_train full-load 경로를 막는 것**이다.

핵심 SSOT:

```txt
보캡은 동결한다.
token_id는 동결한다.
embedding row 의미도 동결한다.

천지인/QWave는 새 token이 아니라 token position에 붙는 side-channel tensor row로 매핑한다.
미완성 safetensors는 completed checkpoint로 취급하지 않는다.
base_train의 full load / full upload / full snapshot / full optimizer path는 위험 callsite로 봉인한다.
최종 경로는 atlas parallel grouped sequential route로 재바인드한다.
```

---

## 1. 완료된 패치

### ASH-TOK-TENSOR-00

```txt
ASH-TOK-TENSOR-00
Tokenizer V5 External Reference Freeze + Cheonjiin/QWave Side-Channel Map /
No Token Id Remap No Vocab Expansion No Asset Vendoring Seal
```

완료 산출물:

```txt
ash_pass3_ASH-TOK-TENSOR-00_external_reference_vocab_freeze_baked.zip
```

반영 파일:

```txt
crates/model_core/src/ash_tok_tensor_00_vocab_freeze_external_refs.rs
crates/model_core/src/bin/ash_tok_tensor_00_vocab_freeze_external_refs.rs
crates/model_core/src/lib.rs
acceptance_reports/ASH-TOK-TENSOR-00.md
patch_reports/ASH-TOK-TENSOR-00_bake_report.md
ASH_TOK_TENSOR_00_STATIC_CHECKS.txt
ASH_TOK_TENSOR_00_BAKE_MANIFEST.json
```

확정 봉인:

```txt
vocab_size = 48259
min_token_id = 0
max_token_id = 48258

token_id_remapped = false
vocab_expanded = false
embedding_row_reordered = false

tokenizer_v5.vocab = external reference only
tokenizer_v5.model = external reference only
safetensors = external reference only

include_manifest_in_zip = false
include_vocab_in_zip = false
include_model_in_zip = false
include_safetensors_in_zip = false
```

천지인/QWave signal token:

```txt
<qwave:on>     id = 58
<delta_k:on>   id = 60
<morph:on>     id = 62
<cheon:on>     id = 64
<ji:on>        id = 65
<in:on>        id = 66
```

천지인 축 매핑:

```txt
X = Ji / ji_support
Y = In / in_bridge
Z = Cheon / cheon_core
```

중요 주의:

```txt
reserved signal token은 numeric feature carrier가 아니다.
<cheon:on>, <ji:on>, <in:on>은 값 토큰이 아니라 side-channel control flag다.
천지인/QWave 값을 vocab에 추가하지 않는다.
```

---

## 2. 참조 전용 외부 자산

다음 파일들은 **ZIP에 포함 금지**다. 이미 선배 로컬에 있고, 산출물에는 경로/해시/계약만 기록한다.

```txt
tokenizer_manifest_v5_final.json
tokenizer_manifest_v5_final.before_manifest_hash_cleanup.json
tokenizer_v5.vocab
tokenizer_v5.model
D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\ash_v5_native_genesis.forge01_smoke.safetensors
```

중요:

```txt
safetensors는 아직 완성본이 아니다.
풀로 올리면 터진다.
completed checkpoint로 취급하면 안 된다.
full row parity probe를 지금 하면 안 된다.
```

---

## 3. 직전 SSOT 변경점

기존에 계획했던 `ASH-TOK-TENSOR-01 Safetensors Embedding Row Parity Probe`는 폐기한다.

폐기된 전제:

```txt
safetensors_file_exists = true
safetensors_header_read = true
embedding_row_count_checked = true
lm_head_row_count_checked = true
row_parity_probe_pass = true
```

새 SSOT:

```txt
safetensors file is incomplete
full safetensors load would explode
base train must not use monolithic full load
atlas parallel grouping + sequential shard route is required
row parity must be deferred to grouped shard probe
```

따라서 `ASH-TOK-TENSOR-01`은 다음 명세로 재정의한다.

```txt
ASH-TOK-TENSOR-01
Incomplete Safetensors Artifact Sentinel /
No Full Tensor Load No Row Parity Claim Seal
```

---

## 4. base_train 실제 조사 결과

확인한 주요 파일:

```txt
crates/base_train/src/bin/base_train.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/training.rs
crates/base_train/src/checkpoint.rs
crates/base_train/src/config.rs
crates/model_core/src/reference_checkpoint.rs
crates/model_core/src/ash_ft24_sequential_atlas_group_training_schedule.rs
crates/model_core/src/ash_ft25_group_local_forward_backward_executor.rs
crates/model_core/src/ash_ft40_first_group_training_step_dryrun.rs
```

### 4.1 CLI가 아직 full checkpoint path를 직접 받음

```txt
--init-checkpoint-path
```

이 값이 그대로 들어감:

```txt
cfg.training.init_checkpoint_paths
```

문제:

```txt
init_checkpoint_paths가 있으면 atlas group plan이 아니라 full checkpoint loader로 들어간다.
```

현재 부족한 CLI/config:

```txt
--atlas-group-plan
--tensor-group-manifest
--sequential-load-plan
--no-full-checkpoint-load
--base-train-route=atlas_grouped_sequential
```

### 4.2 load_full_checkpoint_weights()가 파일 전체를 메모리로 읽음

위치:

```txt
crates/model_core/src/reference_checkpoint.rs
```

위험 구조:

```rust
let bytes = fs::read(path.as_ref())?;
let tensors = safetensors::SafeTensors::deserialize(&bytes)?;

for name in tensors.names() {
    let view = tensors.tensor(name)?;
    let shape = view.shape().to_vec();
    let data = tensor_to_f32_vec(&view)?;
    out.insert(name.to_string(), (shape, data));
}
```

문제:

```txt
1. safetensors 전체 파일을 fs::read로 통째로 메모리에 올림
2. 모든 tensor를 순회함
3. 모든 tensor data를 Vec<f32>로 변환함
4. F16/BF16도 전부 F32로 확장함
5. BTreeMap<String, (shape, Vec<f32>)>에 전부 보관함
```

필요 구조:

```txt
safetensors header/index
→ tensor group manifest
→ group window
→ partial tensor slice
→ atlas group staging
→ sequential group receipt
```

### 4.3 base_train은 init checkpoint가 있으면 full model을 통째로 로드함

위치:

```txt
crates/base_train/src/training.rs
```

위험 구조:

```rust
let base_model = if init_checkpoint_paths.is_empty() {
    model_core::AshModel::<B>::new(spec.clone(), device)
} else {
    let full = load_full_checkpoint_weights(spec, &init_checkpoint_paths)?;
    load_full_checkpoint_into_model::<B>(spec, &full, device)
};
```

기본 호출은 다음과 같음:

```txt
load_full_checkpoint_into_model_with_upload_options(spec, full, device, true, true)
```

즉:

```txt
upload_full_embedding = true
upload_full_lm_head = true
```

### 4.4 save_full_checkpoint=false여도 full snapshot을 먼저 뜸

위치:

```txt
crates/base_train/src/training.rs
```

위험 구조:

```rust
let valid = model.valid();
let snapshots = collect_full_checkpoint_snapshots(&valid.base);
let checkpoint_path = output_dir.join(format!("full_step_{:05}.safetensors", step + 1));

if cfg.training.save_full_checkpoint {
    write_full_checkpoint_safetensors(&snapshots, &checkpoint_path)?;
}
```

문제:

```txt
save_full_checkpoint=false여도 collect_full_checkpoint_snapshots()가 먼저 실행된다.
즉 저장 여부와 무관하게 full CPU readback이 발생할 수 있다.
```

반드시 봉인할 문장:

```txt
save_full_checkpoint=false ≠ full snapshot allowed
```

### 4.5 collect_full_checkpoint_snapshots() 자체가 full readback 함수

위치:

```txt
crates/base_train/src/checkpoint.rs
```

위험 구조:

```rust
fn tensor_values_2d(tensor) -> (Vec<usize>, Vec<f32>) {
    let dims = tensor.dims();
    let values = tensor.into_data().to_vec::<f32>().unwrap_or_default();
    (vec![dims[0], dims[1]], values)
}
```

문제:

```txt
GPU/Burn tensor → CPU Vec<f32> materialization
```

금지해야 함:

```txt
full_checkpoint_snapshot_collected = true
full_tensor_cpu_readback_executed = true
```

### 4.6 BaseTrainingRuntimeConfig 기본값이 full checkpoint 저장을 켬

위치:

```txt
crates/base_train/src/config.rs
```

현재 기본값:

```rust
save_full_checkpoint: true
save_adapter_checkpoint: true
```

일반 build config에서도:

```rust
save_full_checkpoint: !auto_v4_readapt
```

필요 기본값:

```txt
save_full_checkpoint = false
save_adapter_checkpoint = true
save_atlas_group_delta = true
save_group_receipt = true
```

### 4.7 optimizer scope가 full HybridTrainModel 전체를 대상으로 잡힐 수 있음

현재 루프:

```rust
let grads = loss.backward();
let grads = GradientsParams::from_grads::<B, _>(grads, &model);
model = optimizer.step(lr, model, grads);
```

`model` 구조:

```rust
pub struct HybridTrainModel<B: Backend> {
    pub base: AshModel<B>,
    pub adapters: Vec<TrainableLoraSlot<B>>,
}
```

판단불가지만 위험한 점:

```txt
base model params가 gradient/optimizer 대상에서 완전히 제외되는지 아직 확정 불가.
```

sentinel에서 막아야 할 것:

```txt
base_model_gradient_allocated = false
full_model_optimizer_state_created = false
adapter_or_group_delta_only = true
```

---

## 5. 재사용 가능한 기존 ASH-FT 재료

기존 라인에 이미 쓸 수 있는 재료가 있음.

```txt
crates/model_core/src/ash_ft24_sequential_atlas_group_training_schedule.rs
crates/model_core/src/ash_ft25_group_local_forward_backward_executor.rs
crates/model_core/src/ash_ft40_first_group_training_step_dryrun.rs
```

### ASH-FT-24

```txt
allow_full_model_upload = false
allow_active_training = false
schedule_scope = atlas_group_only
deterministic group order
```

### ASH-FT-25

```txt
allow_full_model_trainable = false
allow_full_model_upload = false
selected group / group local executor
```

### ASH-FT-40

```txt
first group training step dry-run
allow_weight_commit = false
allow_safetensors_mutation = false
optimizer_update_mode = candidate_only
```

결론:

```txt
새 철학을 만들지 말고,
base_train을 기존 ASH-FT atlas/group/no-full-upload 계약 쪽으로 재바인드한다.
```

---

## 6. 다음 패치 로드맵

### ASH-TOK-TENSOR-01

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

### ASH-TOK-TENSOR-02

```txt
ASH-TOK-TENSOR-02
BaseTrain Full Load Callsite Inventory /
No Runtime Mutation Seal
```

목적:

```txt
base_train 내부의 full-load 위험 callsite를 실제 파일/함수 단위로 inventory하고,
아직 어떤 런타임 코드도 변경하지 않는다.
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

열리는 것:

```txt
full_load_callsite_inventory_created = true
callsite_file_path_bound = true
callsite_function_name_bound = true
callsite_risk_classified = true
route_rebind_patch_plan_required_next = true
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

### ASH-TOK-TENSOR-03

```txt
ASH-TOK-TENSOR-03
Atlas Parallel Grouped Sequential Tensor Load Plan /
No Full Checkpoint Upload Seal
```

목적:

```txt
safetensors / embedding / lm_head / layer stack을 full load하지 않고,
아틀라스 병렬 그룹 + 순차 로드 단위로 나누기 위한 tensor group manifest와 load plan을 만든다.
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

### ASH-TOK-TENSOR-04

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

추가/변경 필요:

```txt
--base-train-route=atlas_grouped_sequential
--tensor-group-manifest <path>
--atlas-group-plan <path>
--sequential-load-plan <path>
--no-full-checkpoint-load

config:
base_train_route: AtlasGroupedSequential
allow_full_checkpoint_load: false
allow_full_embedding_upload: false
allow_full_lm_head_upload: false
save_full_checkpoint: false
save_atlas_group_delta: true
save_group_receipt: true
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

### ASH-TOK-TENSOR-05

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

반드시 막을 것:

```txt
collect_full_checkpoint_snapshots before save guard
full embedding CPU readback
full lm_head CPU readback
full layer stack CPU readback
```

필요 구조:

```txt
if save_full_checkpoint {
    collect_full_checkpoint_snapshots(...)
}

// 또는 더 강하게:
full_snapshot_gate.require_explicit_approval()
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

### ASH-TOK-TENSOR-06

```txt
ASH-TOK-TENSOR-06
Embedding LMHead Atlas Shard Contract /
No Full Row Materialization Seal
```

목적:

```txt
embedding/lm_head를 full matrix로 materialize하지 않고,
vocab row / tile / group 단위로 나눠 atlas shard로 취급하는 계약을 세운다.
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

### ASH-TOK-TENSOR-07

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

재사용:

```txt
ASH-FT-24 schedule
ASH-FT-25 group local executor
ASH-FT-40 first group training dryrun
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

## 7. 절대 금지 규칙 요약

```txt
1. incomplete safetensors를 completed checkpoint로 취급 금지
2. full safetensors fs::read 금지
3. 모든 tensor를 Vec<f32>로 변환 금지
4. full embedding/lm_head upload 금지
5. save_full_checkpoint=false 상태에서 full snapshot 선실행 금지
6. collect_full_checkpoint_snapshots 무조건 호출 금지
7. full model optimizer state 생성 금지
8. row parity PASS 선주장 금지
9. tokenizer/model/safetensors 원본 ZIP 포함 금지
10. base_train monolithic load route 기본값 유지 금지
```

---

## 8. 다음 세션 첫 요청 추천

다음 세션에서는 바로 이걸 요청하면 된다.

```txt
ASH-TOK-TENSOR-01
Incomplete Safetensors Artifact Sentinel /
No Full Tensor Load No Row Parity Claim Seal 베이크
```

단, 베이크 시 반드시 `base_train` 위험 callsite inventory가 포함되어야 한다.

최소 포함 필드:

```txt
base_train_callsite_inventory_created = true
load_full_checkpoint_weights_callsite_present = true
read_safetensors_map_uses_fs_read_full_file = true
read_safetensors_map_converts_all_tensors_to_f32_vec = true
load_full_checkpoint_into_model_uploads_full_embedding_by_default = true
load_full_checkpoint_into_model_uploads_full_lm_head_by_default = true
checkpoint_step_collects_full_snapshots_before_save_guard = true
unconditional_full_snapshot_before_save_guard_detected = true
save_full_checkpoint_default_true = true
atlas_group_route_fields_present_in_base_train_config = false
base_train_currently_rebound_to_atlas_group_route = false
```

---

## 9. 현재 판단불가

```txt
- 실제 safetensors가 어느 정도까지 생성됐는지
- safetensors header/key/shape 상태
- embedding/lm_head 실제 tensor key 이름
- 실제 row parity PASS 여부
- Burn derive가 base params gradient를 완전히 제외하는지
- full model optimizer state가 실제 생성되는지
- atlas group 단위를 layer/tensor/row/tile 중 무엇으로 확정할지
```

이 판단불가 항목은 임의로 메우면 안 된다.
특히 row parity나 optimizer scope는 실제 probe 전까지 PASS로 말하면 안 된다.

---

## 10. 다음 세션 SSOT 복창용 한 줄

```txt
ASH-TOK-TENSOR 라인은 tokenizer_v5 vocab/token_id/embedding row 의미를 고정한 채,
미완성 safetensors와 base_train full-load 경로를 차단하고,
atlas parallel grouped sequential route로 embedding/lm_head/base train을 재바인드하는 작업이다.
```
