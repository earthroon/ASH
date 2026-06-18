# ASH-BASETRAIN-GPU-70K-G49 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G49
Selected Atlas Group Materialization /
Explicit Atlas Route Bootstrap To One Selected Group Resident Candidate Seal
No Full Tensor Load No Loss No Backward No Optimizer
```

## Purpose

G49 consumes the `ASH-BASETRAIN-GPU-70K-G48` Atlas route bootstrap and required local manifest binding receipts, then creates a selected atlas group resident candidate surface.

G49 exists to bind one selected atlas group from local `specs/` and `artifacts/` metadata without full tensor load. It may generate G49 receipt JSON locally, but it must not fabricate required input manifests, missing slice metadata, tensor shapes, dtypes, or silently select a group from multiple candidates.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent atlas route bootstrap: `ASH-BASETRAIN-GPU-70K-G48`
- Current patch: `ASH-BASETRAIN-GPU-70K-G49`
- Next patch: `ASH-BASETRAIN-GPU-70K-G50`

## Implementation style

G49 is baked in a lookup-table-first and match-based boundary style.

- `EXPECTED_STATE_LUT` holds the expected truth table.
- `G49ProbeKey` enumerates route bootstrap, local manifest, selected group, resident candidate, and closed-boundary fields.
- `expected_value(...)` uses `match` for expected state lookup.
- `observed_value(...)` uses `match` for receipt field projection.
- `classify_boundary(...)` uses `match` to map observed mismatches to `G49FailureReason`.
- `run_from_env()` generates G49 receipt JSON locally under `--out-dir`, defaulting to `specs`.
- Forbidden claim patterns are kept in static receipt JSON, not in source, to prevent source self-hit contamination.

## Local JSON generation contract

Allowed:

- Generate G49 receipt JSON locally.
- Scan local `specs/` and `artifacts/` for existing manifest/plan paths when explicit CLI paths are not supplied.
- Accept explicit local paths through CLI arguments.
- Accept `--selected-group-id` explicitly.
- Infer selected group id only when the atlas group plan exposes a single unambiguous candidate.
- Record missing required paths or selected group metadata as incomplete binding evidence.

Forbidden:

- Generate missing tensor group manifest as input SSOT.
- Generate missing atlas group plan as input SSOT.
- Generate missing sequential load plan as input SSOT.
- Fabricate missing slice metadata, dtype, or shape.
- Silently select the first group when multiple candidates exist.
- Fall back to FreshInit, SpecOnly, or CPU training route.
- Read a full safetensors payload.
- Load a full checkpoint or full tensor.
- Upload GPU weights, write GPU buffers, or dispatch GPU kernels.

## Runtime CLI

```bash
cargo run -p base_train --bin ash_basetrain_gpu_70k_g49_selected_atlas_group_materialization -- \
  --local-root . \
  --selected-group-id <group_id> \
  --out-dir specs
```

Explicit local path mode:

```bash
cargo run -p base_train --bin ash_basetrain_gpu_70k_g49_selected_atlas_group_materialization -- \
  --g48-atlas-route-bootstrap specs/ASH_BASETRAIN_GPU_70K_G48_ATLAS_ROUTE_BOOTSTRAP_RECEIPT.json \
  --g48-required-manifest-binding specs/ASH_BASETRAIN_GPU_70K_G48_REQUIRED_MANIFEST_BINDING_RECEIPT.json \
  --g48-atlas-route-validation specs/ASH_BASETRAIN_GPU_70K_G48_ATLAS_ROUTE_VALIDATION_RECEIPT.json \
  --g48-local-artifact-path-discovery specs/ASH_BASETRAIN_GPU_70K_G48_LOCAL_ARTIFACT_PATH_DISCOVERY.json \
  --tensor-group-manifest specs/<local_tensor_group_manifest>.json \
  --atlas-group-plan artifacts/<local_atlas_group_plan>.json \
  --sequential-load-plan artifacts/<local_sequential_load_plan>.json \
  --selected-group-id <group_id> \
  --out-dir specs
```

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g49_selected_atlas_group_materialization.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g49_selected_atlas_group_materialization.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G49_SELECTED_ATLAS_GROUP_CHOICE_RECEIPT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G49_SELECTED_ATLAS_GROUP_SLICE_BINDING_RECEIPT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G49_SELECTED_ATLAS_GROUP_RESIDENT_CANDIDATE_RECEIPT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G49_ATLAS_ROUTE_BOOTSTRAP_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G49_SELECTED_GROUP_MATERIALIZATION_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G49_NO_FULL_TENSOR_LOAD_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G49_NO_FORWARD_LOSS_BACKWARD_OPTIMIZER_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G49_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G49_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G49_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G49_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.md` markdown files
- `*.sha256` sidecars
- `*.py` helper scripts
- full safetensors payloads
- training dataset payloads
- model checkpoints
- final output artifacts
- display surface artifacts
- route/default adoption artifacts
- approval artifacts
- loss/backward/optimizer artifacts
- model delta/checkpoint/weight artifacts

## Allowed in G49 runtime probe

- Read G48 Atlas route bootstrap evidence.
- Read G48 required manifest binding evidence.
- Resolve local manifest/plan paths from explicit CLI args or local `specs/`/`artifacts/` scan.
- Resolve selected group id from explicit CLI args or single-candidate inference only.
- Generate G49 receipt JSON locally.
- Create selected atlas group choice receipt.
- Create selected atlas group slice binding receipt.
- Create selected atlas group resident candidate receipt.
- Create Atlas route bootstrap lineage audit.
- Create selected group materialization boundary audit.
- Create no-full-tensor-load and no-forward/loss/backward/optimizer audits.
- Validate state through lookup-table and match-based boundary classification.

## Closed in G49

G49 must keep closed: selected group silent auto-selection when multiple candidates exist, missing manifest fabrication, missing slice metadata fabrication, missing tensor shape fabrication, missing dtype fabrication, implicit default group selection, FreshInit fallback, SpecOnly fallback, CPU training fallback, full safetensors payload read, full checkpoint load, full tensor load, full embedding load, full lm_head load, unrelated group materialization, multi group materialization, GPU weight upload, GPU buffer write, GPU dispatch, model forward, logits materialization, decode, sampling, generation, loss target creation, loss computation, backward, gradient materialization, optimizer state creation, optimizer execution, model delta materialization, model delta commit, checkpoint mutation, weight mutation, route promotion execution, controlled promotion execution, runtime default adoption, default route mutation, silent adoption, production route switch, training claim, and model quality claim.

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G49_SELECTED_ATLAS_GROUP_MATERIALIZATION_READY_LOCAL_JSON_GENERATION_NO_GPU_UPLOAD_NO_FORWARD_RUNTIME_PASS_CLAIM
```

The baked ZIP contains the G49 source/runtime probe surface and metadata receipts. In the current bake environment, the user's local `specs/` and `artifacts/` manifest paths were unavailable, and `cargo`/`rustc` were unavailable, so no local compile claim or runtime PASS claim is made. The patch supports local JSON generation when run in the user's local workspace where the required manifest paths and selected group id are available.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G49_SELECTED_ATLAS_GROUP_MATERIALIZATION
```

G49 reaches runtime PASS only when G48 bootstrap evidence is accepted, required local manifest/plan paths are readable, selected group id is explicit or uniquely inferable, selected group metadata exists, G49 receipt JSON is generated locally, and every closed boundary remains closed.

## Next

```text
ASH-BASETRAIN-GPU-70K-G50
Group Local Forward Logits Smoke /
One Selected Group Resident Candidate To Forward Logits Candidate Seal
No Decode No Sampling No Loss No Backward No Optimizer
```
