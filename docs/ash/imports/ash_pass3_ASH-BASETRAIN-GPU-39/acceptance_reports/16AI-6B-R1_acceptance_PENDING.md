# 16AI-6B-R1 Acceptance PENDING

- status: PENDING_RUNTIME
- patch: 16AI-6B-R1 Ash 1.1B Identity Seal Patch
- model_identity: Ash 1.1B
- spec_path_status: legacy_filename_not_model_size_ssot
- generation: false
- checkpoint_required: false
- assembly_mode: off
- token_ids_mutated: false

## Acceptance Criteria

- [x] AC-16AI-6B-R1-1 6A/6B probe JSON records model_identity = Ash 1.1B.
- [x] AC-16AI-6B-R1-2 6A/6B probe logs print model_identity = Ash 1.1B.
- [x] AC-16AI-6B-R1-3 spec_path_status = legacy_filename_not_model_size_ssot is recorded.
- [x] AC-16AI-6B-R1-4 Reports include the 300m filename warning note.
- [x] AC-16AI-6B-R1-5 300m is not used as model identity.
- [x] AC-16AI-6B-R1-6 6A Protected Span Scanner behavior is not intentionally changed.
- [x] AC-16AI-6B-R1-7 6B Cheonjiin Structural Analyzer behavior is not intentionally changed.
- [x] AC-16AI-6B-R1-8 token_ids are not changed.
- [x] AC-16AI-6B-R1-9 generation=false is preserved.
- [x] AC-16AI-6B-R1-10 checkpoint_required=false is preserved.
- [x] AC-16AI-6B-R1-11 assembly_mode=off is preserved.
- [ ] AC-16AI-6B-R1-12 Rust runtime execution verified locally.

## Runtime note

This environment does not provide cargo, so compile/runtime verification remains pending.
