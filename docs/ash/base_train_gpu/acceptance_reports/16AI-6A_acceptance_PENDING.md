# 16AI-6A Acceptance PENDING

- status: PENDING_RUNTIME
- gate: Protected Span Scanner
- generation: false
- checkpoint_required: false
- assembly_mode: off
- default_mode: diagnostic
- chatml_lite_excluded: true

## Acceptance Criteria

- [x] AC-16AI-6A-1 Protected span scanner probe bin is added.
- [x] AC-16AI-6A-2 `사용자:` / `어시스턴트:` / `질문:` / `답변:` are scanned before Korean run classification.
- [x] AC-16AI-6A-3 manifest special tokens `<pad>` / `<bos>` / `<eos>` / `<unk>` are loaded as ProtectedSpecial candidates.
- [x] AC-16AI-6A-4 ProtectedWrapper bypasses Korean analyzer classification.
- [x] AC-16AI-6A-5 ProtectedSpecial bypasses Korean analyzer classification.
- [x] AC-16AI-6A-6 newline is separated as SpanKind::Newline.
- [x] AC-16AI-6A-7 vocab_exact_hit and fallback_required are recorded per protected span.
- [x] AC-16AI-6A-8 wrapper_label_fragmented is recorded.
- [x] AC-16AI-6A-9 protected_span_risk_score is emitted.
- [x] AC-16AI-6A-10 diagnostic mode preserves baseline token id sequence.
- [x] AC-16AI-6A-11 generation=false and checkpoint_required=false are preserved.
- [x] AC-16AI-6A-12 chatml-lite is excluded by default.
- [x] AC-16AI-6A-13 JSON / MD / acceptance paths are supported.

## Runtime note

This bake was produced in an environment without `cargo`; compile/runtime acceptance must be closed in the local Rust environment.

## R1 Identity Seal Note

- model_identity: Ash 1.1B
- spec_path_status: legacy_filename_not_model_size_ssot
- note: spec filename contains `300m`, but model identity is Ash 1.1B.
