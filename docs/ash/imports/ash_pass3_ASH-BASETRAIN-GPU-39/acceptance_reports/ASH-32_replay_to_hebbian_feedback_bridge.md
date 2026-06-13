# ASH-32 Replay-to-Hebbian Feedback Bridge

## Status
PASS_REPLAY_TO_HEBBIAN_FEEDBACK_BRIDGE

## Sealed
- AshReplayHebbianFeedbackMode
- AshReplayHebbianFeedbackKind
- AshReplayHebbianFeedbackSeverity
- AshReplayHebbianFeedbackConfig
- AshReplayHebbianFeedbackEvent
- AshReplayFeedbackLedgerPatchCandidate
- AshReplayHebbianFeedbackReport
- AshReplayDerivedHebbianProposalSet
- replay result to feedback event conversion
- feedback event to Hebbian proposal bridge
- replay-derived ledger patch candidate
- explicit apply preservation
- source fingerprint trace preservation

## Policy
- Replay feedback is evidence, not direct mutation.
- ASH-32 does not mutate registry.
- ASH-32 does not mutate current pointer.
- ASH-32 does not mutate the coactivation ledger in-place.
- Replay-derived proposals require explicit apply.
- Replay-derived proposal set remains applied=false.
- Silent fallback regression is critical.
- Weight telemetry missing is fail-hard evidence.
- Pass-only replay creates NOOP by default.
- No Python validator.

## Boundary
ash_core computes replay feedback and proposals.
orchestrator_local reports feedback bridge evidence.
artifact_store preserves feedback snapshots.
ASH-19 apply gate performs any later registry application.
