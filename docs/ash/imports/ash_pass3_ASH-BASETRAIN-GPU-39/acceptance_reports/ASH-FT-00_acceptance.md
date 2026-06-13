# ASH-FT-00 Acceptance Report

## Status

```txt
bake_status: PASS_ASH_FT00_BAKED_STATIC
runtime_status: PENDING_LOCAL_RUN
```

This bake adds ASH-FT-00 source, binary entrypoint, templates, spec, acceptance report, and README. It does not include generated runtime artifacts.

## PASS requirements

```txt
1. QW-TOK-FORGE-01-R3 PASS receipt is observed at runtime.
2. Candidate safetensors exists.
3. Candidate SHA256 matches the expected forge01_smoke shadow candidate hash.
4. Safetensors header parse succeeds.
5. Every tensor key in the header is registered in the manifest.
6. Every tensor has dtype, shape, data_offsets, data byte size, file byte range, role, family, trainable_coverage=true.
7. Unknown tensors are included as conservative operator-review groups, not dropped.
8. Atlas group plan is non-empty.
9. Parallel compute candidates and sequential commit policy are separated.
10. Memory budget estimates are written without forcing full-load semantics.
11. full_load_required=false.
12. atlas_grouping_required=true.
13. tensor_value_materialized=false.
14. full_tensor_load_executed=false.
15. mmap_materialization_executed=false.
16. gpu_buffer_created=false.
17. gpu_upload_executed=false.
18. forward_executed=false.
19. backward_executed=false.
20. optimizer_step_executed=false.
21. candidate_weight_write_executed=false.
22. runtime_default_apply_executed=false.
23. checkpoint_alias_rebind_executed=false.
24. model/tokenizer/runtime config mutation flags remain false.
25. bake zip contains artifacts_templates/*.template.json only, not artifacts/*.json runtime receipts.
```

## FAIL conditions

```txt
1. R3 PASS dependency is missing when required.
2. Candidate SHA256 mismatch.
3. Safetensors header cannot be parsed.
4. Any tensor key is absent from the manifest.
5. Any tensor offset range exceeds file bounds.
6. Any tensor byte size disagrees with dtype x shape.
7. Unknown tensor is silently excluded.
8. Atlas group plan is empty.
9. Any forward/backward/GPU/optimizer/candidate-write/default-apply guard becomes true.
10. Runtime artifacts are packaged into the bake zip under artifacts/*.json.
```

## Static bake receipt

```txt
source_added: true
bin_added: true
lib_export_added: true
templates_added: true
spec_added: true
runtime_artifacts_packaged: false
weight_mutation_executed: false
```
