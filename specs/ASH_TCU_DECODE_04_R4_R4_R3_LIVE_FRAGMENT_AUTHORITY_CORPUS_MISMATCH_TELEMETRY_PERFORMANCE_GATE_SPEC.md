# ASH-TCU-DECODE-04-R4-R4-R3
# Live Fragment Authority Corpus / Mismatch Telemetry / Performance Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R4-R3_LIVE_FRAGMENT_AUTHORITY_CORPUS_MISMATCH_TELEMETRY_PERFORMANCE_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R4-R2_FOUR_ROUTE_TENSORCUBE_FRAGMENT_AUTHORITY_STREAM_COMMIT_PARITY_GATE`
- Runtime mode: `live_four_route_fragment_authority_corpus_mismatch_telemetry_performance`
- Cached authority: generation-buffered terminal commit
- Streaming authority: current-fragment compare-before-emit
- Legacy oracle: mandatory full dual-run
- Token/KV/sampler/RNG authority: existing production path only
- General production apply: false
- Legacy retirement: false
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R4-R4_TENSORCUBE_DEFAULT