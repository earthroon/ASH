# 16AI-QW-11 — QWave SFT Feature Export / Pulse Vector Batch Matrix Seal

## Scope

This seal consumes QW-10 graph serialization evidence and QWave trace metadata to export a deterministic SFT side-channel feature matrix shaped as batch × sequence × qwave_feature_dim. It aligns QWave features to existing token byte spans while forbidding QWave graph recomputation, tokenizer rerun, token id mutation, vocab augmentation, embedding resize, new token creation, direct logit mutation, loss function mutation, LoRA routing hint creation, or backend QWave switching.

## Required Evidence

- QW-10 serialization receipt id/fingerprint
- QWave graph serialization manifest id/fingerprint
- SFT sample manifest id/fingerprint
- token ids and byte ranges
- QWave trace fingerprints
- feature schema id/fingerprint
- export policy id/fingerprint

## Guards

- QW-10 serialization receipt required
- trace manifest required
- SFT sample manifest required
- token byte ranges required
- stable sample order required
- stable token order required
- fixed feature dim required
- feature mask required
- coverage mask required
- all feature values finite
- token ids unchanged
- QWave graph recompute forbidden
- tokenizer rerun forbidden
- token id mutation forbidden
- vocab augmentation forbidden
- embedding resize forbidden
- new token creation forbidden
- direct logit mutation forbidden
- loss function mutation forbidden
- LoRA routing hint creation forbidden
- backend QWave switch forbidden

## Acceptance Tests

- builds SFT feature matrix from QWave traces
- preserves token ids
- creates feature and coverage masks
- zero-fills empty alignment with mask
- protects special/protected spans
- missing QW-10 receipt rejected
- feature dim mismatch rejected
- non-finite feature value rejected
- token id or logit mutation rejected
- deterministic feature export receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_QW12 until SFT training intake consumes the QWave side-channel feature matrix without mutating tokens or logits directly.
