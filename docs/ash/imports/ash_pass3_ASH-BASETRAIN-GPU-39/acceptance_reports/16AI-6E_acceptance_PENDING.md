# 16AI-6E Acceptance PENDING

- status: PENDING_RUNTIME
- model_identity: Ash 1.1B
- spec_path_status: legacy_filename_not_model_size_ssot
- generation: false
- checkpoint_required: false
- vocab_augmented: false
- dp_path_selected: true
- assembled_token_ids_generated: true
- token_ids_mutated: false
- committed_prompt_ids: baseline

## Acceptance Criteria

- [x] AC-16AI-6E-1 DP Best Token Path Assembler probe file exists.
- [x] AC-16AI-6E-2 16AI-6D TokenCandidateLattice is used as the upstream layer.
- [x] AC-16AI-6E-3 BestTokenPath structure exists.
- [x] AC-16AI-6E-4 AssemblyResult structure exists.
- [x] AC-16AI-6E-5 assembled_token_ids field exists.
- [x] AC-16AI-6E-6 baseline_token_ids / baseline_decoded fields exist.
- [x] AC-16AI-6E-7 baseline and assembled fragmentation score fields exist.
- [x] AC-16AI-6E-8 fragmentation_delta exists.
- [x] AC-16AI-6E-9 path total_cost and path_score exist.
- [x] AC-16AI-6E-10 selected_candidate_ids / selected_surfaces / selected_pieces exist.
- [x] AC-16AI-6E-11 committed_prompt_ids=baseline is the default diagnostic contract.
- [x] AC-16AI-6E-12 token_ids_mutated=false is preserved.
- [x] AC-16AI-6E-13 generation=false and checkpoint_required=false are preserved.
- [x] AC-16AI-6E-14 vocab_augmented=false is preserved.
- [x] AC-16AI-6E-15 model_identity=Ash 1.1B is recorded.
- [x] AC-16AI-6E-16 legacy_filename_not_model_size_ssot is recorded.

## Runtime note

Static bake cannot prove Rust compilation in this environment. Run the 16AI-6E probe in a Rust-enabled local environment to close acceptance.
