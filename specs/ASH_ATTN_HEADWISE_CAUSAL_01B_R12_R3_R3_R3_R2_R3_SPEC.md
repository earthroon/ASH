# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R3

## Reference Measurement Pipeline Validation Scope /
## First-Fault Encoder Poison Capture /
## Shader-Pipeline-BindGroup-Pass Stage Receipt /
## Secondary EncoderInvalid Suppression Seal

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R3
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R2
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r3.runtime_artifact.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R3
reference_validation_scope_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R3
forced_route_parity_ownership_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R2
promotion_scope=incremental_decode_only
```

This revision changes validation visibility and encoder-failure handling. It does not change attention math, WGSL algorithm semantics, route policy, timing boundaries, ring capacities or performance thresholds.

## 1. Bound failure

R2-R2 completed ascending and descending probe epochs with forced-route parity on the Production dispatcher at capacity 4. It then entered the first production bucket at `seq_kv=8` and terminated with:

```text
wgpu Validation Error
In a CommandEncoder
In a pass parameter
Encoder is invalid
```

The error escaped as a process panic with exit code 101. The message identifies only a poisoned encoder, not the first invalid operation.

## 2. Objective

R2-R3 must capture the first WGPU validation error, name the exact failed stage, use fresh diagnostic encoders, stop immediately after first fault, never finish or submit a poisoned encoder, prevent a secondary EncoderInvalid message from replacing the first fault, run validation preflight outside timestamp spans and preserve zero output-value readback.

## 3. Validation stages

```text
0 pipeline_layout
1 shader_module
2 pipeline_layout_compatibility
3 compute_pipeline
4 bind_group
5 reference_pass
6 encoder_finish
7 queue_submit
```

Each stage owns a validation error scope. The scope is pushed before the target operation and resolved before the next stage is admitted.

## 4. Reference pipeline bundle

The cached Reference measurement bundle is constructed through stage-scoped validation for bind-group layout, shader module, pipeline-layout compatibility and compute pipeline. A failed resource is not inserted into the cache. A successful bundle is reused by the bucket preflight and timed path.

## 5. Per-bucket preflight

Before warmup for each production bucket, the gate calls:

```rust
validate_native_reference_measurement_pipeline(prepared, reference_output)
```

The preflight uses the exact bucket Q/K/V leases, position snapshot, output tensor shape, bind-group ranges and dispatch geometry. It validates the cached pipeline bundle, exact output raw borrow, params buffer, exact bind group, fresh diagnostic encoder, Reference compute pass, encoder finish, queue submit and completion poll.

No preflight sample enters Reference or Atlas timing populations.

## 6. Encoder poison policy

Allowed success lifecycle:

```text
Created → Recording → PassClosed → Finished → Submitted
```

Allowed failure lifecycle:

```text
Created → Invalid → Discarded
```

Required:

```text
poisoned_encoder_reuse_count=0
secondary_encoder_invalid_count=0
post_first_fault_submission_count=0
```

## 7. First-fault error

A scoped failure reports:

```text
ReferenceMeasurementValidationFailure:
stage=<stage>
stage_index=<index>
seq_kv=<bucket>
encoder_state_before=<state>
encoder_state_after=Invalid
device_error_kind=validation
device_error_message=<original wgpu error>
secondary_encoder_invalid_suppressed=true
build_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R3
```

The original WGPU message is preserved. The gate does not continue to later stages after the first fault.

## 8. Receipts

Required backend receipts:

```text
HeadwiseReferenceValidationStageReceipt
HeadwiseReferenceMeasurementPreflightReceipt
```

The preflight receipt contains the revision, bucket identity, tier pass states, per-stage pass states, first-fault fields, poison counters, preflight wait count and zero-readback counters.

## 9. Runtime artifact

```text
workspace/runtime/attention/
  ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r3_reference_validation_preflight_receipts.json
```

Runtime artifacts, local manifests, target directories and repository metadata are excluded from the source bake.

## 10. Performance boundary

```text
preflight_samples_in_performance_population=0
preflight_wait_inside_timed_span_count=0
output_value_readback_count=0
output_host_materialization_count=0
```

The production timing contract remains Reference start to Reference end and Atlas start to Atlas end.

## 11. Negative controls

R2-R3 inherits 960 controls and adds 40 validation-scope, encoder-poison, stage-receipt and boundary controls.

```text
negative_control_count=1000
negative_control_executed_count=1000
negative_control_skipped_count=0
negative_control_fail_count=0
```

## 12. CLI additions

```text
--require-reference-validation-preflight true
--require-reference-pipeline-stage-receipts true
--require-production-pair-scaffold-preflight true
--require-first-fault-capture true
--require-fresh-encoder-per-validation-stage true
--require-poisoned-encoder-discard true
--require-secondary-encoder-invalid-zero true
--require-uncaptured-validation-error-zero true
--require-validation-panic-zero true
--require-preflight-outside-timed-spans true
--require-preflight-performance-population-zero true
--expected-negative-controls 1000
```

## 13. PASS boundary

PASS requires exact R2-R2 source binding, preserved dispatcher ownership, successful Reference resource and pass scopes for every production bucket, zero poisoned-encoder reuse, zero secondary EncoderInvalid, zero post-fault submission, zero preflight timing contamination, zero output-value readback, complete probe/production/tail/rollback gates, 1000 controls and static/digest truth.

PASS proves validation closure, not universal performance, numerical parity, transactional KV rollback, canonical full-model decode or model-quality improvement.

## 14. Expected tokens

PASS:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R3_REFERENCE_MEASUREMENT_PIPELINE_VALIDATION_SCOPE_FIRST_FAULT_ENCODER_POISON_CAPTURE_SHADER_PIPELINE_BIND_GROUP_PASS_STAGE_RECEIPT_SECONDARY_ENCODER_INVALID_SUPPRESSION_INCREMENTAL_ONLY_NO_OUTPUT_VALUE_READBACK_NO_MODEL_QUALITY_OVERCLAIM
```

HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R3_REFERENCE_MEASUREMENT_FIRST_FAULT_VALIDATION_OR_ENCODER_POISON_SUPPRESSION_INCOMPLETE
```
