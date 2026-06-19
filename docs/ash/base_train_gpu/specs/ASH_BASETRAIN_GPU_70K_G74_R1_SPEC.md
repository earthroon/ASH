# ASH-BASETRAIN-GPU-70K-G74-R1

Patch: ASH-BASETRAIN-GPU-70K-G74-R1
Title: G73 Digest Scope Hotfix Compatibility Bake

Status: source-baked hotfix specification record.

Compile blocker observed:
- G73 source referenced gradient_buffer_layout_preflight_digest without declaring it.
- G73 lineage check used gradient_write_candidate fields while reading G72 gradient_buffer_layout_preflight inputs.

Fixed source paths:
- crates/base_train/src/ash_basetrain_gpu_70k_g73_gradient_buffer_layout_preflight_review_gate.rs
- crates/base_train/src/ash_basetrain_gpu_70k_g74_gradient_write_candidate_review_gate.rs

Runtime behavior:
- G73-R1 reads gradient_buffer_layout_preflight_digest from G72 candidate/schema receipts.
- G73-R1 validates gradient_buffer_layout_preflight_created/schema/lineage fields.
- G74-R1 accepts both original G73 PASS and G73-R1 PASS as valid predecessor statuses.

PASS targets:
- PASS_ASH_BASETRAIN_GPU_70K_G73_R1_GRADIENT_BUFFER_LAYOUT_PREFLIGHT_DIGEST_SCOPE_HOTFIX
- PASS_ASH_BASETRAIN_GPU_70K_G74_R1_GRADIENT_WRITE_CANDIDATE_REVIEW_GATE

Required predecessor SSOT:
- specs/ASH_BASETRAIN_GPU_70K_G72_GRADIENT_BUFFER_LAYOUT_PREFLIGHT.json
- specs/ASH_BASETRAIN_GPU_70K_G72_GRADIENT_BUFFER_LAYOUT_PREFLIGHT_SCHEMA_AUDIT.json
- specs/ASH_BASETRAIN_GPU_70K_G73_GRADIENT_WRITE_CANDIDATE.json
- specs/ASH_BASETRAIN_GPU_70K_G73_GRADIENT_WRITE_CANDIDATE_SCHEMA_AUDIT.json

Purpose:
- Repair G73 source compile blocker.
- Preserve G74 gradient accumulation preflight gate semantics.
- Keep execution blocked for backward, gradient buffer allocation, gradient write, accumulation, optimizer, weight, and checkpoint paths.

Packaging note: G74-R1 bake includes lib.rs registration, Cargo bin registration, path-mod bin guard, recursion limit, and excludes predecessor runtime receipts for G50 through G73.
