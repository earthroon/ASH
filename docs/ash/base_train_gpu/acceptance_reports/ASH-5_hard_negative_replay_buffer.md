# ASH-5 Hard Negative Replay Buffer

## Status
PASS_STATIC / PASS_ASH_HARD_NEGATIVE_REPLAY_BUFFER

## Sealed
- ReplayStatus
- ReplaySeverity
- ReplayPriority
- AshFailureReplayRecord
- AshHardNegativeReplayBuffer
- failure replay fingerprint
- replay -> curriculum sample conversion
- replay -> curriculum route helper

## Routing
- SilentFallback / ZeroDeltaPass -> runtime_attach_integrity
- LogicContradiction / UnsupportedClaim -> logic_repair
- TokenFragmentation / RepetitionLoop -> korean_response_stability
- ContextDrop -> context_binding

## Guards
- duplicate fingerprint requires Duplicate status
- P0 failures are critical/high priority
- unknown capability rejected
- corrected response required for reasoning repair cases
- Python validator forbidden

## Boundary
ash_core interprets replay records only.
ash_core does not write datasets.
ash_core does not execute LoRA training.
ash_core does not run runtime forward.
