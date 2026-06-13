# 16AI-6C Acceptance PENDING

- status: PENDING_RUNTIME
- model_identity: Ash 1.1B
- spec_path_status: legacy_filename_not_model_size_ssot
- generation: false
- checkpoint_required: false
- assembly_mode: off
- token_ids_mutated: false
- vocab_augmented: false
- chatml_lite_excluded: true

## Acceptance Criteria

- [x] AC-16AI-6C-1 Korean Surface Candidate Generator is added.
- [x] AC-16AI-6C-2 Every Korean span can emit WholeSpan SurfaceCandidate.
- [x] AC-16AI-6C-3 Particle suffixes can emit ParticleSplit candidates.
- [x] AC-16AI-6C-4 Ending suffixes can emit EndingSplit candidates.
- [x] AC-16AI-6C-5 Compound/foreign/fallback candidates are represented.
- [x] AC-16AI-6C-6 FallbackSyllable / FallbackChar are counted and diagnosed.
- [x] AC-16AI-6C-7 max_candidates_per_span and max_splits_per_span are exposed.
- [x] AC-16AI-6C-8 deduplicated_candidate_count is recorded.
- [x] AC-16AI-6C-9 ProtectedWrapper / ProtectedSpecial are not candidate-generator targets.
- [x] AC-16AI-6C-10 protected_wrapper_leak_count is recorded.
- [x] AC-16AI-6C-11 generation=false is preserved.
- [x] AC-16AI-6C-12 checkpoint_required=false is preserved.
- [x] AC-16AI-6C-13 assembly_mode=off is preserved.
- [x] AC-16AI-6C-14 token_ids_mutated=false is preserved.
- [x] AC-16AI-6C-15 vocab_augmented=false is preserved.
- [x] AC-16AI-6C-16 model_identity=Ash 1.1B is recorded.
- [x] AC-16AI-6C-17 spec_path_status=legacy_filename_not_model_size_ssot is recorded.
- [x] AC-16AI-6C-18 JSON / MD / acceptance paths are wired.

## Runtime note

Static bake cannot prove Rust compilation because this execution environment has no Rust toolchain. Run `scripts/run_16AI_6C_surface_candidate_probe.ps1` or `.sh` in a Rust-enabled Ash checkout to close runtime acceptance.
