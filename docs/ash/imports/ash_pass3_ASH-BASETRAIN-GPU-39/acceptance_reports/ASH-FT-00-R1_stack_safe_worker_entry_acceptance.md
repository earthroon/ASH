# ASH-FT-00-R1 Acceptance

## Patch

```txt
patch_id: ASH-FT-00-R1
title: Stack-Safe Worker Entrypoint / No Manifest Logic Mutation Seal
base: ASH-FT-00
```

## Purpose

ASH-FT-00 may parse a large safetensors header and serialize large manifest/plan JSON files. On Windows debug runtime, the default main-thread stack can overflow before receipt emission.

ASH-FT-00-R1 moves execution into a named worker thread with an explicit stack budget. It does not change tensor coverage logic, group planning logic, manifest schema, receipt schema, checkpoint path, candidate write policy, GPU policy, forward/backward policy, or runtime default policy.

## Fixed Symptom

```txt
thread 'main' has overflowed its stack
exit code: 0xc00000fd, STATUS_STACK_OVERFLOW
```

## Runtime Change

```txt
main thread:
- parse args
- read optional --worker-stack-mb
- spawn ash-ft00-stack-safe-worker
- return worker exit code

worker thread:
- run existing ASH-FT-00 manifest generation
- write manifest/plan/receipt
- emit PASS/FAIL status
```

## Default Worker Stack

```txt
default_worker_stack_mb: 128
optional_override: --worker-stack-mb <MB>
```

## Guards

```txt
tensor_value_materialized: false
full_tensor_load_executed: false
mmap_materialization_executed: false
gpu_buffer_created: false
gpu_upload_executed: false
forward_executed: false
backward_executed: false
optimizer_step_executed: false
candidate_weight_write_executed: false
runtime_default_apply_executed: false
checkpoint_alias_rebind_executed: false
model_config_mutation_executed: false
tokenizer_mutation_executed: false
runtime_config_mutation_executed: false
```

## PASS

```txt
1. ash_ft00_full_coverage_manifest binary no longer executes manifest generation directly on default main stack.
2. worker thread stack size is explicitly set.
3. optional --worker-stack-mb argument is accepted.
4. existing ASH-FT-00 config parsing remains delegated to ash_ft00_config_from_args.
5. existing manifest generation remains delegated to run_ash_ft00_full_coverage_manifest.
6. existing artifact writing remains delegated to write_ash_ft00_artifacts.
7. exit codes are preserved: PASS=0, FAIL receipt=1, runtime error=2.
8. no weight mutation path is added.
9. no GPU/forward/backward/optimizer path is added.
10. runtime default apply remains impossible in this binary.
```

## FAIL

```txt
1. manifest generation still runs on default main stack.
2. worker thread stack size is not explicit.
3. tensor coverage/grouping logic is changed in R1.
4. candidate safetensors write path is added.
5. GPU upload/forward/backward/optimizer step is added.
6. runtime default apply or alias rebind is added.
```

## Verdict

```txt
PASS_STATIC_STACK_SAFE_ENTRYPOINT_NO_WEIGHT_MUTATION
```
