# ASH-BASETRAIN-GPU-70K-G48 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G48
Atlas Route Bootstrap Fix /
Controlled Promotion Execution Candidate To Explicit Atlas Route Bootstrap Seal
No Silent Fallback No FreshInit Fallback No Full Tensor Load
```

## Purpose

G48 consumes the `ASH-BASETRAIN-GPU-70K-G47` controlled promotion execution candidate and creates an explicit AtlasGroupedSequential route bootstrap surface.

G48 exists to bind required local `specs/` and `artifacts/` paths without silent repair. It may generate G48 receipt JSON locally, but it must not fabricate the required input manifests themselves.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent candidate-only preflight: `ASH-BASETRAIN-GPU-70K-G47`
- Current patch: `ASH-BASETRAIN-GPU-70K-G48`
- Next patch: `ASH-BASETRAIN-GPU-70K-G49`

## Implementation style

G48 is baked in a lookup-table-first and match-based boundary style.

- `EXPECTED_STATE_LUT` holds the expected truth table.
- `G48ProbeKey` enumerates local JSON generation, manifest binding, route bootstrap, and closed-boundary fields.
- `expected_value(...)` uses `match` for expected state lookup.
- `observed_value(...)` uses `match` for receipt field projection.
- `classify_boundary(...)` uses `match` to map observed mismatches to `G48FailureReason`.
- `run_from_env()` generates G48 receipt JSON locally under `--out-dir`, defaulting to `specs`.
- Forbidden claim patterns are kept in static receipt JSON, not in source, to prevent source self-hit contamination.

## Local JSON generation contract

Allowed:

- Generate G48 receipt JSON locally.
- Scan local `specs/` and `artifacts/` for existing manifest/plan paths when explicit CLI paths are not supplied.
- Accept explicit local paths through CLI arguments.
- Record missing required paths as incomplete binding evidence.

Forbidden:

- Generate missing tensor group manifest as input SSOT.
- Generate missing atlas group plan as input SSOT.
- Generate missing sequential load plan as input SSOT.
- Silently bind default paths when no matching local file exists.
- Fall back to FreshInit, SpecOnly, or CPU training route.

## Runtime CLI

```bash
cargo run -p base_train --bin ash_basetrain_gpu_70k_g48_atlas_route_bootstrap_fix -- \
  --local-root . \
  --out-dir specs
```

Explicit local path mode:

```bash
cargo run -p base_train --bin ash_basetrain_gpu_70k_g48_atlas_route_bootstrap_fix -- \
  --tensor-group-manifest specs/<local_tensor_group_manifest>.json \
  --atlas-group-plan artifacts/<local_atlas_group_plan>.json \
  --sequential-load-plan artifacts/<local_sequential_load_plan>.json \
  --out-dir specs
```

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g48_atlas_route_bootstrap_fix.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g48_atlas_route_bootstrap_fix.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G48_ATLAS_ROUTE_BOOTSTRAP_RECEIPT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G48_REQUIRED_MANIFEST_BINDING_RECEIPT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G48_ATLAS_ROUTE_VALIDATION_RECEIPT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G48_CONTROLLED_PROMOTION_CANDIDATE_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G48_LOCAL_ARTIFACT_PATH_DISCOVERY.json`
- `specs/ASH_BASETRAIN_GPU_70K_G48_NO_SILENT_FALLBACK_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G48_NO_FRESHINIT_FALLBACK_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G48_NO_FULL_TENSOR_LOAD_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G48_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G48_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G48_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G48_LOCAL_BAKE_VALIDATION.json`

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

## Allowed in G48 runtime probe

- Read G47 controlled promotion execution candidate.
- Read G47 candidate boundary evidence.
- Resolve local manifest/plan paths from explicit CLI args or local `specs/`/`artifacts/` scan.
- Generate G48 receipt JSON locally.
- Create local artifact path discovery receipt.
- Create required manifest binding receipt.
- Create AtlasGroupedSequential route bootstrap receipt.
- Create no-silent-fallback, no-FreshInit-fallback, and no-full-tensor-load audits.
- Validate state through lookup-table and match-based boundary classification.

## Closed in G48

G48 must keep closed: missing manifest fabrication, silent path repair, implicit default path binding, FreshInit fallback, SpecOnly fallback, CPU training fallback, selected atlas group materialization, safetensors payload read, full checkpoint load, full tensor load, GPU weight upload, GPU buffer write, GPU dispatch, model forward, logits materialization, loss target creation, loss computation, backward, gradient materialization, optimizer state creation, optimizer execution, model delta materialization, model delta commit, checkpoint mutation, weight mutation, route promotion execution, controlled promotion execution, runtime default adoption, default route mutation, silent adoption, production route switch, training claim, and model quality claim.

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G48_ATLAS_ROUTE_BOOTSTRAP_FIX_READY_LOCAL_JSON_GENERATION_NO_LOCAL_RUNTIME_PASS_CLAIM
```

The baked ZIP contains the G48 source/runtime probe surface and metadata receipts. In the current bake environment, the required local tensor/atlas/sequential manifest paths were not present, so no G48 runtime PASS claim is made. The patch supports local JSON generation when run in the user's local workspace where those `specs/` and `artifacts/` paths exist.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G48_ATLAS_ROUTE_BOOTSTRAP_FIX
```

G48 reaches runtime PASS only when G47 candidate-only evidence is accepted, required local manifest/plan paths are resolved and readable, G48 receipt JSON is generated locally, and every closed boundary remains closed.

## Next

```text
ASH-BASETRAIN-GPU-70K-G49
Selected Atlas Group Materialization /
Explicit Atlas Route Bootstrap To One Selected Group Resident Candidate Seal
No Full Tensor Load No Loss No Backward No Optimizer
```
