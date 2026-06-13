# 16AI-QW-10 — QWave Graph Serialization / JSONL Trace + Markdown Diagnostic Seal

## Scope

This seal consumes QW-09 Korean minimal pair regression evidence and QWave graph snapshots to serialize syllable cells, pulse vectors, syllable transitions, eojeol chains, morph overlays, sentence edges, sentence graph, shadow tokenizer diff, and regression report into stable JSONL/JSON traces. It also creates a Markdown diagnostic report while forbidding graph recomputation, fixture assertion mutation, token id mutation, vocab augmentation, embedding resize, new token creation, production tokenizer commit, SFT feature export, LoRA routing hint creation, or backend QWave switching.

## Required Evidence

- QW-09 regression receipt id/fingerprint
- QW-09 regression report id/fingerprint
- QWave graph snapshot bundle id/fingerprint
- cell trace file receipt
- pulse vector trace file receipt
- transition trace file receipt
- eojeol chain trace file receipt
- morph overlay trace file receipt
- sentence graph trace file receipt
- shadow diff trace file receipt
- regression report trace file receipt
- Markdown diagnostic report receipt
- serialization policy id/fingerprint

## Guards

- QW-09 regression receipt required
- snapshot bundle required
- cell trace required
- pulse vector trace required
- transition trace required
- eojeol trace required
- morph overlay trace required
- sentence graph trace required
- shadow diff trace required
- regression report trace required
- Markdown diagnostic required
- all required files must be created
- all required files must be nonempty
- stable ordering required
- graph recompute forbidden
- fixture assertion mutation forbidden
- token id mutation forbidden
- vocab augmentation forbidden
- embedding resize forbidden
- new token creation forbidden
- production tokenizer commit forbidden
- SFT feature export forbidden
- LoRA routing hint creation forbidden
- backend QWave switch forbidden

## Acceptance Tests

- builds serialization manifest with all required traces
- creates cell/vector/transition JSONL traces
- creates eojeol/morph/sentence graph traces
- creates Markdown diagnostic report
- stable ordering is verified
- missing QW-09 receipt rejected
- missing required trace rejected
- empty required trace file rejected
- graph recompute or tokenizer mutation rejected
- deterministic serialization receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_QW11 until QWave SFT feature export consumes serialized graph traces and emits pulse vector batch matrices.
