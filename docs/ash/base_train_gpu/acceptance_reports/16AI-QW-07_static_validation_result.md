# 16AI-QW-07 Static Validation Result

## File existence
- [x] crates/tokenizer_core/src/hangul_qwave_dp_bridge.rs
- [x] crates/tokenizer_core/tests/hangul_qwave_dp_bridge.rs
- [x] acceptance_reports/16AI-QW-07_qwave_tokenizer_dp_cost_bridge.md
- [x] bake_artifacts/16AI-QW-07_BAKE_REPORT.md
- [x] crates/tokenizer_core/src/lib.rs

## Export checks
- [x] module export present
- [x] public type exports present

## Guard checks
- [x] NewTokenCreationForbidden
- [x] TokenIdMutationForbidden
- [x] VocabAugmentationForbidden
- [x] EmbeddingResizeForbidden
- [x] BackendQWaveSwitchForbidden
- [x] CommittedPromptIdMutationForbidden
- [x] SentenceGraphMutationForbidden
- [x] token_ids_unchanged

## Test function checks
- [x] fn qw07_builds_dp_cost_bridge_from_sentence_graph() {
- [x] fn qw07_applies_byte_fallback_penalty() {
- [x] fn qw07_keeps_token_ids_unchanged() {
- [x] fn qw07_rejects_missing_qw06_receipt() {
- [x] fn qw07_rejects_missing_candidate_paths() {
- [x] fn qw07_rejects_sentence_graph_fingerprint_mismatch() {
- [x] fn qw07_rejects_token_id_mutation_flag() {
- [x] fn qw07_rejects_new_token_creation_flag() {
- [x] fn qw07_rejects_non_finite_candidate_cost() {
- [x] fn qw07_dp_bridge_receipt_is_deterministic() {

## Brace balance
- crates/tokenizer_core/src/hangul_qwave_dp_bridge.rs: braces {=90 }=90 parens (=193 )=193
- crates/tokenizer_core/tests/hangul_qwave_dp_bridge.rs: braces {=26 }=26 parens (=167 )=167

## Native test status
- cargo: command not found
- rustc: command not found
