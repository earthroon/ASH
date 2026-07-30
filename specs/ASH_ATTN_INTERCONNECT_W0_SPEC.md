# ASH-ATTN-INTERCONNECT-W0 명세

## Verified Headwise Route Pointer /
## Verified TensorCube Stage10 Pointer /
## Dual-Authority Runtime Binding Receipt /
## Model Instance Identity /
## Headwise Output Authority Preservation /
## TensorCube Shadow-Only Role /
## No Route Mutation /
## No Stage Mutation /
## Artifact Digest Revalidation Seal

> 상태: SPEC RELEASE rev.2  
> Patch ID: `ASH-ATTN-INTERCONNECT-W0`  
> Build revision: `W0-dual-authority-runtime-binding-v1`  
> 선행 조건: TensorCube `R2-R15 / Stage10Active` 실제 PASS  
> 후속 조건: `W1 Runtime Shape Authority`, `W2 Lease Provenance`  
> production attention authority: `Headwise` 유지  
> TensorCube 권한: `ShadowObserverOnly`, dispatch 권한 없음  
> 실행 방식: 직접 `cargo run`만 canonical, 신규 실행 스크립트 없음

---

# 0. 패치 경계

W0는 Headwise와 TensorCube의 계산 경로를 아직 연결하지 않는다.

W0가 수행하는 범위는 다음뿐이다.

```text
1. Headwise 출력 권위를 실제 artifact·manifest·route LUT·model binding에서 재구성한다.
2. TensorCube Stage10 권위를 실제 pointer·runtime artifact·manifest에서 재검증한다.
3. 두 권위를 동일한 VerifiedModelInstanceBinding에 결속한다.
4. Headwise가 유일한 attention output authority임을 보존한다.
5. TensorCube를 ShadowObserverOnly로 등록한다.
6. route·stage·입력 artifact가 변경되지 않았음을 증명한다.
7. runtime artifact와 local manifest를 Rust gate가 실행 시점에 산출한다.
```

W0 PASS가 뜻하지 않는 것:

```text
TensorCube Stage10 live dispatch
실제 Headwise Q/K lease tap
TensorCube output candidate
Headwise ↔ TensorCube 수치 parity
KV cache read/write
Stage11 진입
production route 승격
```

금지 호출:

```text
run_tensorcube_stage10_row_block_max_exp_sum_on_existing_device()
dispatch_native_qkv_*()
compare_and_swap_stage_pointer()
headwise_candidate_nonce.fetch_add()
device.poll()
map_async()
Tensor::from_data()
```

---

# 1. 선행 권위

## 1.1 TensorCube Stage10

```text
pointer schema           ash.attn.tensorcube.stage-pointer.v10
active stage             tensorcube-stage-10-row-block-max-exp-sum-v1
feature                  tensorcube-per-row-block-max-exp-sum-reduction-v1
feature mask             0x00000000000001ff -> 0x00000000000003ff
generations              42 -> 43 -> 44
pointer write_count      1
runtime pass             true
bit_exact_parity         true
same device              true
same queue lineage       true
host materializations    0
host uploads             0
payload readbacks        0
payload buffer maps      0
KV writes                0
```

W0는 Stage10 shader, dispatch, pointer schema, feature mask, generation을 수정하지 않는다.

## 1.2 Headwise

현재 Headwise에는 TensorCube pointer와 동등한 단일 파일형 active pointer가 없다. 따라서 `Verified Headwise Route Pointer`는 다음 근거를 읽기 전용으로 정규화한 논리 권위다.

```text
VerifiedModelInstanceBinding
Headwise parent runtime artifact
Headwise parent local manifest
compiled route LUT policy + digest
HeadwiseAttentionPromotionPolicySnapshot, 존재 시
NativeWgpu backend identity
HeadwiseAtlasDispatcher requirement
NativeWgpuRuntimeHandles requirement
```

`HeadwiseActive` 문자열 하나만으로 권위를 인정하지 않는다.

---

# 2. SSOT 구조

신규 모듈:

```text
crates/model_core/src/attention_interconnect_binding.rs
```

## 2.1 HeadwiseRouteAuthoritySnapshot

필수 필드:

```text
schema                              ash.attn.interconnect.headwise-route-authority.v1
authority_state                     HeadwiseActive
authority_kind                      verified-runtime-artifact+route-lut+model-binding
model_instance_id
model_instance_binding_digest
parent_patch_id
parent_runtime_schema
parent_manifest_schema
parent_runtime_artifact_path
parent_local_manifest_path
parent_runtime_artifact_sha256
parent_local_manifest_sha256
route_policy_revision
route_policy_id                     evidence_bucket_route_lut_v4
route_lut_digest
promotion_policy_present
promotion_policy_*                  optional
native_wgpu_backend_verified        true
atlas_dispatcher_required           true
runtime_handles_required            true
output_authority                    headwise
route_mutation_permitted            false
snapshot_digest
```

## 2.2 TensorCubeStage10AuthoritySnapshot

필수 필드:

```text
schema                              ash.attn.interconnect.tensorcube-stage10-authority.v1
model_instance_id
stage_pointer_path/hash/schema
lineage_patch_id
parent_patch_id
parent_stage_id
active_stage_id                     tensorcube-stage-10-row-block-max-exp-sum-v1
feature_id                          tensorcube-per-row-block-max-exp-sum-reduction-v1
feature_mask_before                 0x00000000000001ff
feature_mask_after                  0x00000000000003ff
generation_before                   42
prepared_generation                 43
generation_after                    44
write_count                         1
pointer_receipt_digest
runtime artifact path/hash/schema
local manifest path/hash/schema
runtime_pass                        true
runtime_verdict                     exact R2-R15 PASS token
bit_exact_parity                    true
same_device                         true
same_queue_lineage                  true
host_materializations               0
host_uploads                        0
payload_readbacks                   0
payload_buffer_maps                 0
tensorcube_kv_writes                0
output_authority                    none
role                                shadow_observer_only
stage_mutation_permitted            false
snapshot_digest
```

## 2.3 AttentionInterconnectBindingReceipt

```text
schema                              ash.attn.interconnect.w0.binding-receipt.v1
patch_id                            ASH-ATTN-INTERCONNECT-W0
build_revision                      W0-dual-authority-runtime-binding-v1
model_instance_id
model_instance_binding_digest
effective_runtime_binding_digest
headwise_authority_digest
tensorcube_authority_digest
output_authority                    headwise
tensorcube_role                     shadow_observer_only
headwise_output_commit_allowed      true
tensorcube_dispatch_allowed         false
tensorcube_output_commit_allowed    false
tensorcube_downstream_handoff       false
tensorcube_kv_read_allowed          false
tensorcube_kv_write_allowed         false
route_mutation_allowed              false
stage_mutation_allowed              false
binding_epoch
binding_write_count                 1
idempotent_rebind
decision_counters
binding_digest
pass
verdict
```

모델 내부에는 `AttentionInterconnectBindingSlot`을 두며 첫 결속만 허용한다. 동일 digest 재결속은 같은 receipt를 반환하고, 다른 authority digest 덮어쓰기는 fail-closed한다.

---

# 3. Model Instance Identity

`VerifiedModelInstanceBinding.instance_binding_digest`는 다음 semantic payload로 재계산한다.

```text
domain
backend_kind
base_runtime_binding_digest
effective_runtime_binding_digest
checkpoint_set_digest
overlay_digest
model_instance_epoch
construction_ordinal
```

PASS 조건:

```text
schema exact
backend_kind == NativeWgpu
verified_before_first_forward == true
computed digest == stored digest
model_instance_id == "model-instance:" + normalized digest
```

Headwise snapshot과 W0 receipt는 같은 `model_instance_id`, `model_instance_binding_digest`, `effective_runtime_binding_digest`를 사용한다. TensorCube 기존 artifact는 수정하지 않고 W0 receipt 안에서만 해당 model instance에 admission한다.

---

# 4. Artifact closure

## 4.1 Headwise

입력:

```text
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r6_r5_runtime_artifact.json
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r6_r5_local_manifest.json
```

검증:

```text
actual file SHA-256 recomputation
runtime/manifest schema exact
patch id exact
runtime pass true
manifest pass true
runtime/manifest verdict identity
manifest runtime_artifact_path closure
manifest artifact path/digest closure
compiled route LUT validation
compiled route LUT digest identity
```

CLI digest가 `revalidate-from-file`이면 실제 파일 digest와 manifest closure가 expected authority다. 임의 digest 폴백이나 파일 수정은 없다.

## 4.2 TensorCube

입력:

```text
workspace/runtime/tensorcube/ash_tensorcube_stage_active_pointer.json
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r6_r5_r1_r2_r15_runtime_artifact.json
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r6_r5_r1_r2_r15_local_manifest.json
```

검증:

```text
pointer schema/lineage/stage/feature/mask/generations/write_count exact
pointer receipt digest recomputation
runtime/manifest actual SHA-256
runtime/manifest schema and patch exact
build revision exact
R2-R15 PASS token exact
Stage10Active exact
[42,43,44] exact
child artifact count 48
ordered child list digest exact
manifest runtime link exact
manifest pointer path/hash exact
29_same_device_queue.json closure and mismatch == 0
host movement/readback/map/cross-device/KV-write all 0
```

---

# 5. 트랜잭션과 불변성

## 5.1 Prepare

메모리에만 준비한다.

```text
VerifiedModelInstanceBinding validated copy
HeadwiseRouteAuthoritySnapshot
TensorCubeStage10AuthoritySnapshot
AttentionInterconnectBindingReceipt candidate
input artifact pre-hash snapshot
```

## 5.2 Validate

실패 시:

```text
binding write 0
route write 0
stage write 0
artifact repair 0
TensorCube enable 0
partial W0 artifact 0
```

## 5.3 Commit

모든 검증 후 `AttentionInterconnectBindingSlot`에 receipt를 1회 결속한다. W0는 다음을 변경하지 않는다.

```text
Headwise parent artifact/manifest
Headwise route LUT
Headwise production policy
Headwise candidate nonce
Headwise rollback count
Headwise quarantine state
TensorCube stage pointer
TensorCube runtime artifact/manifest
TensorCube feature mask/generation
```

입력 파일은 W0 시작 전과 child artifact 산출 전, runtime artifact 산출 후에 실제 SHA-256을 다시 비교한다.

---

# 6. Decision counters

```text
model_binding_schema_mismatch
model_binding_digest_mismatch
model_instance_id_mismatch
model_backend_mismatch
headwise_runtime_digest_mismatch
headwise_manifest_digest_mismatch
headwise_runtime_manifest_link_mismatch
headwise_runtime_pass_mismatch
headwise_route_lut_digest_mismatch
headwise_promotion_policy_digest_mismatch
headwise_promotion_model_instance_mismatch
tensorcube_pointer_digest_mismatch
tensorcube_pointer_identity_mismatch
tensorcube_stage_identity_mismatch
tensorcube_feature_mask_mismatch
tensorcube_generation_mismatch
tensorcube_runtime_digest_mismatch
tensorcube_manifest_digest_mismatch
tensorcube_runtime_manifest_link_mismatch
tensorcube_runtime_pass_mismatch
output_authority_mismatch
tensorcube_role_mismatch
mixed_authority_attempt
route_mutation_detected
stage_mutation_detected
input_artifact_mutation_detected
duplicate_binding_write
partial_binding_write
```

PASS 조건은 전부 0이다. 첫 nonzero 이름과 실제 값을 오류로 출력한다.

---

# 7. Negative controls

Canonical 34건을 실제 실행한다.

```text
01 model binding schema mismatch
02 backend CpuReference
03 verified_before_first_forward false
04 model binding digest flip
05 model_instance_id mismatch
06 Headwise runtime digest flip
07 Headwise manifest digest flip
08 Headwise authority schema mismatch
09 Headwise authority state mismatch
10 Headwise output authority mismatch
11 Headwise manifest/runtime link mismatch
12 Headwise manifest orphan child
13 route policy id mismatch
14 route LUT digest mismatch
15 promotion policy semantic mismatch
16 promotion policy model instance mismatch
17 TensorCube pointer schema mismatch
18 TensorCube lineage mismatch
19 TensorCube stage mismatch
20 TensorCube feature mask mismatch
21 TensorCube generation mismatch
22 TensorCube write_count mismatch
23 pointer receipt digest mismatch
24 R2-R15 runtime digest flip
25 R2-R15 runtime pass false
26 R2-R15 manifest/pointer link mismatch
27 output authority tensorcube
28 TensorCube production role
29 mixed output authority
30 route mutation attempt
31 stage mutation attempt
32 input artifact post-hash mismatch
33 different authority duplicate bind
34 partial binding write
```

각 결과:

```text
rejected == true
binding_state_unchanged == true
route_state_unchanged == true
stage_state_unchanged == true
partial_artifact_count == 0
```

---

# 8. Rust 산출물

출력 디렉터리:

```text
workspace/runtime/attention/interconnect
```

Rust gate가 실행 시점에 다음 26개 child artifact를 순서대로 산출한다.

```text
identity.json
source_inventory.json
verified_model_instance.json
headwise_parent_artifact_binding.json
headwise_parent_manifest_binding.json
headwise_route_policy.json
headwise_route_authority.json
headwise_promotion_policy.json
tensorcube_stage_pointer_binding.json
tensorcube_runtime_binding.json
tensorcube_manifest_binding.json
tensorcube_stage_authority.json
dual_authority_binding.json
output_authority_guard.json
tensorcube_shadow_role_guard.json
no_route_mutation.json
no_stage_mutation.json
input_immutability.json
digest_revalidation.json
idempotent_binding.json
negative_control_outcomes.json
static_checks.json
verdict.json
runtime_artifact.json
canonical_args.txt
canonical_run.cmd
```

```text
child_artifact_expected       26
ordered list SHA-256          fad95a027a54957cc295de0bc4a2538395aa3ca885e255000b6bc6cd4e7f32e2
```

`canonical_run.cmd`는 실행 후 provenance용 child evidence일 뿐, 코드 ZIP에 선탑재되는 helper script가 아니다.

Runtime artifact:

```text
ash_attn_interconnect_w0_runtime_artifact.json
schema = ash.attn.interconnect.w0.runtime_artifact.v1
```

Local manifest:

```text
ash_attn_interconnect_w0_local_manifest.json
schema = ash.attn.interconnect.w0.local_manifest.v1
manifest self excluded from hash graph
```

**코드 ZIP에는 W0 runtime artifact와 local manifest를 미리 포함하지 않는다.** 두 파일은 Rust gate만 산출한다.

---

# 9. 구현 파일

신설:

```text
crates/model_core/src/attention_interconnect_binding.rs
crates/orchestrator_local/src/attention_interconnect_w0_cli_registry.rs
crates/orchestrator_local/src/bin/ash_attn_interconnect_w0_gate.rs
specs/cli/ash_attn_interconnect_w0.args
```

수정:

```text
crates/model_core/src/lib.rs
crates/model_core/src/native_wgpu.rs
crates/orchestrator_local/Cargo.toml
```

신규 `.ps1` / `.cmd` 실행 스크립트는 코드 ZIP에 추가하지 않는다.

수정 금지:

```text
TensorCube WGSL
Headwise WGSL
headwise_route_lut.rs policy bands
Stage10 pointer schema
R2-R15 runtime artifact/manifest
decode_state attention callsite
KV cache implementation
```

---

# 10. CLI 계약

Binary:

```text
ash_attn_interconnect_w0_gate
```

Response file:

```text
specs/cli/ash_attn_interconnect_w0.args
```

29 canonical key/value pairs, 58 non-empty lines:

```text
--repo-root
--verified-model-instance-binding
--headwise-parent-artifact
--headwise-parent-manifest
--expected-headwise-parent-artifact-sha256
--expected-headwise-parent-manifest-sha256
--expected-headwise-route-state
--expected-headwise-route-policy-id
--expected-headwise-route-lut-digest
--tensorcube-stage-pointer
--tensorcube-stage10-runtime-artifact
--tensorcube-stage10-local-manifest
--expected-tensorcube-stage-id
--expected-tensorcube-feature-mask
--expected-tensorcube-generation
--output-authority
--tensorcube-role
--require-artifact-digest-revalidation
--require-model-instance-identity
--forbid-route-mutation
--forbid-stage-mutation
--forbid-tensorcube-dispatch
--forbid-tensorcube-output-commit
--forbid-tensorcube-kv-read
--forbid-tensorcube-kv-write
--negative-control-mode
--minimum-negative-controls
--out-dir
--binding-epoch
```

금지:

```text
blank line
duplicate key
unknown key
key/value displacement
unordered response-file key sequence
```

---

# 11. PASS gate

```text
VerifiedModelInstanceBinding present and digest exact
Headwise artifact/manifest closure exact
Headwise route LUT identity exact
TensorCube v10 pointer closure exact
R2-R15 artifact/manifest closure exact
Headwise output authority preserved
TensorCube role shadow_observer_only
TensorCube dispatch/output/KV permissions false
route/stage/input mutation count 0
binding_write_count 1
all 28 decision counters 0
negative controls 34/34
child artifacts 26/26
ordered list digest exact
runtime artifact pass true
local manifest pass true
```

PASS token:

```text
PROMOTE_ASH_ATTN_INTERCONNECT_W0_VERIFIED_HEADWISE_ROUTE_AUTHORITY_VERIFIED_TENSORCUBE_STAGE10_POINTER_DUAL_AUTHORITY_RUNTIME_BINDING_MODEL_INSTANCE_IDENTITY_HEADWISE_OUTPUT_AUTHORITY_TENSORCUBE_SHADOW_ONLY_NO_ROUTE_MUTATION_NO_STAGE_MUTATION_ARTIFACT_DIGEST_REVALIDATION_SEALED
```

HOLD token:

```text
HOLD_ASH_ATTN_INTERCONNECT_W0_HEADWISE_AUTHORITY_TENSORCUBE_STAGE10_POINTER_MODEL_INSTANCE_BINDING_OUTPUT_AUTHORITY_SHADOW_ROLE_NO_MUTATION_OR_DIGEST_REVALIDATION_NOT_PROVEN
```

---

# 12. 직접 실행

저장소 루트에서 다음 명령만 사용한다.

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_interconnect_w0_gate `
  -- `
  "@specs/cli/ash_attn_interconnect_w0.args"
```

W0는 WGSL을 embed하지 않으므로 `burn_webgpu_backend` package clean은 의무가 아니다. route LUT 소스가 변경됐다면 관련 crate를 정상 재컴파일하여 compiled LUT digest가 다시 계산되게 한다.

---

# 13. 최종 봉인 문장

W0 PASS 시 다음만 확정한다.

```text
현재 NativeWgpu model instance에 대해 검증된 Headwise attention authority와
검증된 TensorCube Stage10 authority가 각자의 상태와 generation을 변경하지 않은 채
하나의 immutable interconnect binding receipt로 결속되었다.

Headwise는 유일한 attention output authority를 유지하며,
TensorCube는 dispatch·output commit·KV read/write 권한이 없는
ShadowObserverOnly 역할로만 등록되었다.

입력 artifact의 실제 SHA-256은 binding 시점에 재검증되었고,
Headwise route 상태와 TensorCube stage pointer는 W0 전후 동일하다.
```

아직 금지되는 주장:

```text
TensorCube가 실제 Headwise Q/K를 소비했다.
TensorCube Stage10이 live decode에서 실행됐다.
TensorCube와 Headwise 최종 출력 parity가 통과했다.
TensorCube가 attention output을 생성하거나 commit했다.
```
