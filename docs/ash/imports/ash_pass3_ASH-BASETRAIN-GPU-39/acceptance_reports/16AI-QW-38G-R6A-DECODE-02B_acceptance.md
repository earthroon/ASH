# Acceptance — 16AI-QW-38G-R6A-DECODE-02B

Status: STATIC_PASS / EXECUTION_NOT_RUN

## Accepted static scope
- TransitionValidationMode exists.
- Runtime transition probe receipt schema exists.
- Probe-to-On summary exists.
- Candidate trace version 3 is required for transition parity.
- CPU/GPU selected transition action and reason mask comparison path exists.
- Probe integrity missing counters are not promoted to PASS; they are recorded as PARTIAL and promotion-blocking.

## Not run
- cargo check
- cargo test
- rustfmt
- WebGPU runtime probe

## Promotion state
`TRANSITION_ON_CANDIDATE_READY` is not granted by this bake. Runtime receipt must first provide probe integrity counters or an equivalent direct no-mutation proof.
