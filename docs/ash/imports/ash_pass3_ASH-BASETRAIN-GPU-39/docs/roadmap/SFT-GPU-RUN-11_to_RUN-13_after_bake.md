# SFT-GPU-RUN-11 이후 로드맵

## 현재 완료

`SFT-GPU-RUN-11 — GPU-Trained Slot Arbitration / Multi-Adapter Health Merge Seal`

RUN-11은 RUN-09 post-switch health와 RUN-10 rollback drill 결과를 기반으로 GPU-trained current adapter를 전체 adapter slot registry snapshot 안에서 재평가한다.

열린 것:

- multi-adapter health merge
- slot registry snapshot merge
- GPU-trained adapter health score
- fallback readiness comparison
- rollback readiness comparison
- active recommendation
- fallback recommendation
- demotion recommendation
- quarantine recommendation

닫힌 것:

- actual current pointer switch
- rollback execution
- actual demotion apply
- actual quarantine apply
- lifecycle mutation
- ASH binding
- runtime SFT training
- runtime gradient write
- runtime optimizer step
- textureSample/sampler/normalized UV weight fetch
- silent CPU fallback success

## 다음 12번

# SFT-GPU-RUN-12 — GPU-Trained Lifecycle Ledger Merge / Training Lineage Seal

목적:

GPU-trained adapter의 strict GPU train → artifact intake → regression matrix → operator approval → attach dry-run → apply candidate → current pointer switch → post-switch health → rollback drill → slot arbitration 계보를 append-only lifecycle ledger에 병합한다.

열 것:

- training lineage event
- strict GPU train lineage entry
- artifact intake lineage entry
- regression matrix lineage entry
- promotion review lineage entry
- current pointer switch lineage entry
- post-switch health lineage entry
- rollback drill lineage entry
- slot arbitration lineage entry
- lifecycle ledger merge
- append-only lifecycle event

계속 닫을 것:

- silent lifecycle mutation
- unreviewed state transition
- actual demotion apply
- actual quarantine apply
- current pointer update
- rollback execution
- ASH binding

핵심 SSOT:

```txt
gpu_trained_lifecycle_merge_seal_id
source_slot_arbitration_merge_seal_id
source_rollback_drill_seal_id
source_post_switch_health_seal_id
source_current_pointer_switch_seal_id
strict_gpu_train_lineage_digest
artifact_intake_lineage_digest
regression_matrix_lineage_digest
operator_approval_lineage_digest
current_switch_lineage_digest
post_switch_health_lineage_digest
rollback_drill_lineage_digest
slot_arbitration_lineage_digest
lifecycle_event_append_only_confirmed = true
silent_lifecycle_mutation_detected = false
```

## 다음 13번

# SFT-GPU-RUN-13 — GPU-Trained Operator Action Apply / Lifecycle Transition Seal

목적:

RUN-11 recommendation과 RUN-12 lifecycle ledger를 기반으로 operator-reviewed action만 실제 적용한다.

열 것:

- operator-reviewed lifecycle action apply
- reviewed fallback activation
- reviewed demotion apply
- reviewed quarantine apply
- reviewed candidate switch
- lifecycle transition event
- apply receipt
- operator action seal

계속 닫을 것:

- unreviewed action apply
- recommendation mismatch apply
- silent registry correction
- runtime SFT training
- runtime gradient write
- runtime optimizer step

## 병렬 안전 보강 후보

- `SFT-GPU-SAFETY-01 — GPU Train OOM / Timeout / Device Lost Recovery Seal`
- `SFT-GPU-SAFETY-02 — Partial Artifact Quarantine / Failed Train Output Guard`
- `SFT-GPU-OBS-01 — Strict GPU Train Telemetry Dashboard / Matrix Drift Console Seal`
- `SFT-GPU-OBS-02 — Long-Horizon GPU Adapter Health Ledger / Runtime Drift Seal`

## 다음 요청 추천

```txt
SFT-GPU-RUN-12 — GPU-Trained Lifecycle Ledger Merge / Training Lineage Seal 명세
```
