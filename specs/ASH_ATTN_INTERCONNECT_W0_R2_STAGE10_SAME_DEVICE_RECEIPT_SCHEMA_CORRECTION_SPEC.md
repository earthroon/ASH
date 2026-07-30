# ASH-ATTN-INTERCONNECT-W0-R2 교정 명세

## Stage10 Same-Device Receipt Schema Correction /
## R15 Child Artifact Writer Parity /
## Flat Receipt Field Admission /
## No Authority Relaxation /
## Rust Artifact Closure Preservation Seal

> 상태: SPEC RELEASE  
> Patch ID: `ASH-ATTN-INTERCONNECT-W0-R2`  
> Parent patch: `ASH-ATTN-INTERCONNECT-W0-R1`  
> Build revision: `W0-R2-stage10-same-device-receipt-schema-correction-v1`  
> 교정 대상: `W0JsonFieldMissing:group_id`

---

# 0. 원인

R15 Stage10 gate는 `same_device_queue.json`을 다음 평면 JSON으로 산출한다.

```json
{
  "physical_device_digest": "<sha256>",
  "mismatch": 0
}
```

그러나 W0-R1 reader는 이를 runtime artifact의 `atlas_groups.same_device_queue` wrapper와 혼동하여 다음 경로를 요구했다.

```text
group_id
fields.mismatch
```

따라서 실제 R15 child artifact를 읽을 때 `W0JsonFieldMissing:group_id`로 fail-closed했다.

---

# 1. SSOT

Child artifact schema의 권위는 R15 writer다.

```text
crates/orchestrator_local/src/bin/
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r6_r5_r1_r2_r15_gate.rs
```

Canonical writer:

```rust
artifact_values.insert(
    "same_device_queue.json".into(),
    serde_json::json!({
        "physical_device_digest": current_device_digest,
        "mismatch": runtime.device_queue_lineage_mismatch_count
    }),
);
```

`atlas_groups.same_device_queue`와 독립 child artifact `same_device_queue.json`은 의미는 같지만 envelope가 다르다. W0는 manifest가 가리키는 독립 child artifact를 읽으므로 평면 schema를 따라야 한다.

---

# 2. 교정

제거:

```text
same_device_receipt.group_id == "same_device_queue"
same_device_receipt.fields.mismatch == 0
```

도입:

```text
same_device_receipt is JSON object
same_device_receipt.physical_device_digest is non-empty string
same_device_receipt.mismatch == 0
```

다음 검증은 유지한다.

```text
manifest artifact path closure
manifest-declared SHA-256 == actual file SHA-256
same_device_queue.json 존재
cross-device copy count == 0
runtime same-device and same-queue claims 유지
TensorCube output/KV authority 없음
```

---

# 3. 금지되는 완화

W0-R2는 다음을 하지 않는다.

```text
missing field를 0으로 간주
wrapper/plain schema를 추측 폴백
SHA-256 검증 생략
mismatch 필드 생략 허용
physical_device_digest 공백 허용
TensorCube dispatch 허용
Headwise output authority 변경
route/stage mutation
```

R15 writer가 바뀌면 W0 reader도 명시적 schema revision으로 다시 상승해야 한다.

---

# 4. 불변 경계

```text
Headwise R6-R5 CombinedDriftHold 해석 유지
existing-production-headwise-reference-v1 output authority 유지
TensorCube Stage10 ShadowObserverOnly 유지
Stage10 pointer generation 44 유지
feature mask 0x03ff 유지
child artifact expected 26 유지
child artifact ordered-list digest 유지
negative controls 34 유지
decision counters 28 유지
```

---

# 5. 코드 변경

수정 파일:

```text
crates/model_core/src/attention_interconnect_binding.rs
crates/orchestrator_local/src/bin/ash_attn_interconnect_w0_gate.rs
```

Build revision은 두 파일에서 동일해야 한다.

```text
W0-R2-stage10-same-device-receipt-schema-correction-v1
```

명세 Markdown과 W0 runtime artifact/local manifest는 코드 ZIP에 포함하지 않는다. Runtime artifact와 manifest는 Rust gate 실행 시 산출한다.

---

# 6. 실행

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
W0-R2-stage10-same-device-receipt-schema-correction-v1
```

---

# 7. PASS 의미

W0-R2 PASS는 R15의 실제 독립 `same_device_queue.json` schema를 정확히 해석하면서도, 파일 digest와 device/queue lineage mismatch 0을 계속 fail-closed로 검증했음을 뜻한다.
