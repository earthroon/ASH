# 16AI-6D Acceptance PENDING

- status: PENDING_RUNTIME
- model_identity: Ash 1.1B
- spec_path_status: legacy_filename_not_model_size_ssot
- generation: false
- checkpoint_required: false
- assembly_mode: off
- token_ids_mutated: false
- vocab_augmented: false
- dp_path_selected: false
- chatml_lite_excluded: true

## Acceptance Criteria

- [x] AC-16AI-6D-1 Existing Vocab Lookup Lattice probe is added.
- [x] AC-16AI-6D-2 SurfaceCandidate to TokenCandidateLattice flow is present.
- [x] AC-16AI-6D-3 lookup variants include surface and boundary-marker variants.
- [x] AC-16AI-6D-4 LookupStatus variants are defined.
- [x] AC-16AI-6D-5 TokenCandidate records token_ids / decoded / lookup_status / lookup_source / variant_used.
- [x] AC-16AI-6D-6 unknown / byte-like / boundary-marker counts are recorded.
- [x] AC-16AI-6D-7 lattice_cost / lattice_score are produced.
- [x] AC-16AI-6D-8 max_lattice_candidates_per_span is enforced.
- [x] AC-16AI-6D-9 dp_path_selected=false is preserved.
- [x] AC-16AI-6D-10 generation/checkpoint/vocab mutation remain disabled.

## Runtime note

Static bake cannot prove Rust compilation until the binary is run in a Rust-enabled environment.
