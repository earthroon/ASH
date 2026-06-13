# 16AI-QW-03 — Pulse Vector Transition Edge / Syllable-to-Syllable Flow Seal

## Scope

This seal consumes QW-02 `QWavePulseVectorBatch` records and QW-01 `QWaveSyllableCellBatch` records to derive deterministic `QWaveSyllableTransitionEdge` records between adjacent Hangul syllable cells. It computes pulse delta, phase delta, direction alignment, amplitude transfer, closure release, coda-to-onset bridge, boundary pressure, resonance carry, flow continuity, and transition energy.

## Required Evidence

- QW-02 pulse vector receipt id/fingerprint
- QWaveSyllableCellBatch id/fingerprint
- QWavePulseVectorBatch id/fingerprint
- adjacent cell/vector pairs
- transition policy id/fingerprint
- source text fingerprint

## Guards

- QW-02 pulse receipt required
- cell batch required
- pulse vector batch required
- cell/vector source ids must match
- adjacent cell pairs only
- cross-whitespace edge forbidden
- cross-punctuation edge forbidden
- cross-protected-span edge forbidden
- pulse delta required
- phase delta required
- closure release required
- coda-to-onset bridge required
- transition energy required
- all edge values finite
- eojeol chain creation forbidden
- sentence graph creation forbidden
- morph overlay creation forbidden
- token id mutation forbidden
- vocab augmentation forbidden
- embedding resize forbidden
- backend QWave switch forbidden

## Acceptance Tests

- builds transition edges from adjacent pulse vectors
- computes pulse and phase deltas
- computes coda-to-onset bridge
- blocks cross-whitespace edge
- creates transition but no eojeol chain
- missing QW-02 receipt rejected
- cell/vector mismatch rejected
- non-finite transition policy rejected
- unexpected sentence graph creation rejected
- deterministic transition receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_QW04 until `QWaveEojeolChain` groups syllable transitions by whitespace/boundary policy.
