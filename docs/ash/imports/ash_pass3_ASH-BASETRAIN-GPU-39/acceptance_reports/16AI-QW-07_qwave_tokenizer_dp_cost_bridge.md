# 16AI-QW-07 — QWave Transition Graph → Tokenizer DP Cost Bridge / No Token ID Mutation Seal

## Scope

This seal consumes the QW-06 `QWaveSentenceTransitionGraph` and existing tokenizer DP candidate paths to create deterministic QWave cost adjustments. It may reward graph continuity and penalize boundary mismatch, byte fallback, and unknown-token fallback, but it must not create new tokens, mutate token IDs, augment vocabulary, resize embeddings, switch backend QWave, mutate the sentence graph, or mutate committed prompt IDs.

## Required Evidence

- QW-06 sentence graph receipt id/fingerprint
- QWaveSentenceTransitionGraph id/fingerprint
- existing DP lattice id/fingerprint
- existing candidate paths and token IDs
- DP bridge policy id/fingerprint
- source text fingerprint

## Guards

- QW-06 sentence graph receipt required
- sentence graph required and finite
- candidate paths required
- cost adjustment required
- QWave continuity reward required
- QWave boundary mismatch penalty required
- QWave byte fallback penalty required
- token IDs must remain unchanged
- new token creation forbidden
- token ID mutation forbidden
- vocab augmentation forbidden
- embedding resize forbidden
- backend QWave switch forbidden
- sentence graph mutation forbidden
- committed prompt ID mutation forbidden

## Acceptance Tests

- builds DP cost bridge from sentence graph
- applies byte fallback penalty
- keeps token IDs unchanged
- missing QW-06 receipt rejected
- missing candidate paths rejected
- sentence graph fingerprint mismatch rejected
- token ID mutation rejected
- new token creation rejected
- non-finite candidate cost rejected
- deterministic DP bridge receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_QW08 until Tokenizer Shadow Run consumes this bridge without committing mutated token IDs.
