# 16AI-QW-06 — Sentence QWave Transition Graph / Eojeol-to-Eojeol Flow Seal

## Scope

This seal consumes QW-04 `QWaveEojeolChain` records, QW-05 `QWaveMorphPulseOverlay` records, and optional `StructureTensorObservation` data to create a deterministic `QWaveSentenceTransitionGraph`. It builds eojeol-to-eojeol transition edges, topic flow, predicate flow, addressivity flow, particle bridge flow, ending tension curve, sentence closure curve, and sentence pulse curve while forbidding tokenizer DP cost mutation, SFT feature export, LoRA routing hint creation, token id mutation, vocab augmentation, embedding resize, or backend QWave switching.

## Required Evidence

- QW-04 eojeol chain receipt id/fingerprint
- QW-05 morph overlay receipt id/fingerprint
- QWaveEojeolChainBatch id/fingerprint
- QWaveMorphPulseOverlayBatch id/fingerprint
- optional StructureTensorObservation id/fingerprint
- sentence graph policy id/fingerprint
- source text fingerprint

## Guards

- QW-04 eojeol receipt required
- QW-05 morph overlay receipt required
- eojeol chain batch required
- morph overlay batch required
- eojeol order must be preserved
- adjacent eojeol edges required
- topic flow required
- predicate flow required
- addressivity flow required
- particle bridge flow required
- ending tension curve required
- sentence closure curve required
- all edge values finite
- graph values finite
- missing overlay autofill forbidden
- eojeol reorder forbidden
- tokenizer DP cost mutation forbidden
- SFT feature export forbidden
- LoRA routing hint creation forbidden
- token id mutation forbidden
- vocab augmentation forbidden
- embedding resize forbidden
- backend QWave switch forbidden

## Acceptance Tests

- builds sentence graph from eojeol chains and overlays
- creates adjacent eojeol edges
- particle overlay contributes topic flow
- ending overlay contributes closure curve
- honorific/title/vocative contributes addressivity flow
- missing QW-04 receipt rejected
- missing QW-05 receipt rejected
- eojeol reorder rejected
- tokenizer DP cost mutation rejected
- deterministic sentence graph receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_QW07 until Tokenizer DP Cost Bridge consumes QWaveSentenceTransitionGraph.
