# ASH-ATTN-INTERCONNECT-W0-R1 교정 명세

## Headwise HOLD Authority Interpretation Correction /
## Existing Production Reference Route Preservation /
## Candidate Promotion Non-Admission /
## Exact HOLD Artifact Closure /
## W0 Dual-Authority Binding Repair Seal

> 상태: SPEC RELEASE
> Patch ID: `ASH-ATTN-INTERCONNECT-W0-R1`
> Parent patch: `ASH-ATTN-INTERCONNECT-W0`
> Build revision: `W0-R1-headwise-hold-authority-correction-v1`
> 교정 대상: `W0HeadwiseRuntimePassMismatch`

---

# 0. 교정 사유

초기 W0 구현은 다음 Headwise 부모 artifact를 일반적인 승격 PASS artifact로 해석했다.

```text
workspace/runtime/attention/
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r6_r5_runtime_artifact.json
```

그러나 이 artifact의 canonical 계약은 `pass=true`가 아니다.

```text
parent gate pass          false
parent verdict            HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_OBSERVER_BASELINE_DRIFT_AUTHORITY_OR_TAIL_ATTRIBUTION_NOT_PROVEN
final admission state     CombinedDriftHold
active route unchanged    true
active route              existing-production-headwise-reference-v1
held candidate route      gqa4-cluster-production-canary-v1
candidate promoted        false
negative controls         1120 / 1140
```

후속 `R6-R5-R1` 게이트도 부모 `pass == false`, exact HOLD token, `CombinedDriftHold`, `active_route_unchanged == true`를 직접 요구한다.

따라서 `pass=false`는 Headwise 전체 output authority의 실패가 아니다. 실험 candidate 승격이 보류되고 기존 production Headwise reference route가 계속 활성인 fail-closed 상태다.

---

# 1. 교정 원칙

W0-R1은 `pass=false`를 무시하거나 성공으로 뒤집지 않는다.

다음을 전부 검증할 때만 Headwise output authority를 인정한다.

```text
runtime pass == false
manifest pass == false
runtime verdict == exact R6-R5 HOLD token
manifest verdict == runtime verdict
final_admission_state == CombinedDriftHold
active_route_unchanged == true
active route == existing-production-headwise-reference-v1
candidate route == gqa4-cluster-production-canary-v1
candidate_promoted == false
negative_control_expected == 1140
negative_control_passed == 1120
runtime/manifest path and SHA-256 closure exact
compiled route LUT digest exact
VerifiedModelInstanceBinding exact
```

다음 주장은 금지한다.

```text
R6-R5 candidate가 promotion PASS했다.
CombinedDriftHold가 해제됐다.
production route가 candidate route로 변경됐다.
Headwise 부모 artifact의 pass=false를 무시했다.
```

---

# 2. HeadwiseRouteAuthoritySnapshot v2

Schema:

```text
ash.attn.interconnect.headwise-route-authority.v2
```

추가 필드:

```text
parent_gate_pass                    false
parent_verdict                      exact R6-R5 HOLD token
parent_admission_state              CombinedDriftHold
parent_active_route_unchanged       true
active_route_id                     existing-production-headwise-reference-v1
candidate_route_id                  gqa4-cluster-production-canary-v1
candidate_promoted                  false
```

`authority_state = HeadwiseActive`는 Headwise route family와 기존 production reference route의 활성 상태를 뜻한다. held candidate의 승격 상태를 뜻하지 않는다.

`output_authority = headwise`는 기존 production reference route에만 귀속된다.

---

# 3. Decision counter 교정

기존의 거짓 의미:

```text
headwise_runtime_pass_mismatch
```

교정:

```text
headwise_parent_hold_mismatch
```

값은 다음 중 하나라도 발생하면 1이다.

```text
runtime pass가 true로 바뀜
exact HOLD token 불일치
CombinedDriftHold 불일치
active route changed
fallback/reference route identity 불일치
held candidate identity 불일치
candidate promoted
```

PASS 조건은 0이다.

---

# 4. Negative control 교정

Negative control 09:

```text
Headwise HOLD artifact misclassified as promoted
```

주입:

```text
parent_gate_pass = true
```

기대 결과:

```text
rejected == true
binding_state_unchanged == true
route_state_unchanged == true
stage_state_unchanged == true
partial_artifact_count == 0
```

전체 negative control 수는 34개로 유지한다.

---

# 5. 불변 경계

W0-R1은 다음을 변경하지 않는다.

```text
Headwise runtime artifact
Headwise local manifest
Headwise candidate HOLD state
Headwise active production reference route
Headwise route LUT policy bands
TensorCube Stage10 pointer
TensorCube Stage10 runtime artifact/manifest
TensorCube generation 44
TensorCube feature mask 0x03ff
TensorCube dispatch permission false
TensorCube output commit permission false
TensorCube KV read/write permission false
```

W0-R1은 계산 커널 패치가 아니다.

```text
Headwise Q/K/V dispatch 0
TensorCube Stage10 dispatch 0
WGSL 변경 0
route mutation 0
stage mutation 0
```

---

# 6. Rust 산출 경계

코드 ZIP에는 명세 Markdown, W0 runtime artifact, W0 local manifest를 포함하지 않는다.

Rust gate가 실행 시 다음을 산출한다.

```text
workspace/runtime/attention/interconnect/
ash_attn_interconnect_w0_*.json
ash_attn_interconnect_w0_runtime_artifact.json
ash_attn_interconnect_w0_local_manifest.json
```

Child artifact 계약은 유지한다.

```text
child_artifact_expected       26
child_artifact_list_sha256     fad95a027a54957cc295de0bc4a2538395aa3ca885e255000b6bc6cd4e7f32e2
```

---

# 7. 실행

저장소 루트에서 직접 실행한다.

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_interconnect_w0_gate `
  -- `
  "@specs/cli/ash_attn_interconnect_w0.args"
```

정상 시작 revision:

```text
W0-R1-headwise-hold-authority-correction-v1
```

오래된 다음 revision이 보이면 stale binary다.

```text
W0-dual-authority-runtime-binding-v1
```

---

# 8. PASS 의미

W0-R1 PASS는 다음만 확정한다.

```text
R6-R5 candidate는 CombinedDriftHold 상태를 유지한다.
기존 production Headwise reference route는 변경 없이 output authority를 유지한다.
TensorCube Stage10은 ShadowObserverOnly로 결속된다.
Headwise와 TensorCube의 입력 artifact는 변경되지 않는다.
W0 binding receipt와 runtime artifact/manifest는 Rust가 실행 시 산출했다.
```

TensorCube live dispatch, Q/K lease tap, Headwise와 TensorCube의 수치 parity는 아직 확정하지 않는다.
