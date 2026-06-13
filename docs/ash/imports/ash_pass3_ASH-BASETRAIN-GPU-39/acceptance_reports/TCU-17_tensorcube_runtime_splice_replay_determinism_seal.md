# TCU-17 TensorCube Runtime Splice Replay / Determinism Seal

## Status
PASS_TCU_17_RUNTIME_SPLICE_REPLAY_IDENTICAL

## Sealed
- AshTensorCubeRuntimeSpliceReplayMode
- AshTensorCubeRuntimeSpliceReplayFingerprint
- AshTensorCubeRuntimeSpliceReplayInputSeal
- AshTensorCubeRuntimeSpliceReplayComparisonStatus
- AshTensorCubeRuntimeSpliceReplayComparison
- AshTensorCubeRuntimeSpliceDeterminismFailureKind
- AshTensorCubeRuntimeSpliceDeterminismFailure
- AshTensorCubeRuntimeSpliceReplayReport
- AshTensorCubeRuntimeSpliceDeterminismReport
- AshTensorCubeRuntimeSpliceReplayConfig
- runtime splice input fingerprint
- runtime splice output fingerprint
- native path decision replay
- same-device borrow decision replay
- fallback pressure decision replay
- buffer lease decision replay
- environment mismatch separation
- TCU-12 bridge integration

## Policy
- Same input and same environment must produce same output decision
- Native/fallback decision drift blocks apply candidate
- Lease decision drift blocks apply candidate
- Environment mismatch requires manual review and is not treated as determinism failure
- Missing telemetry snapshot blocks deterministic replay
- Missing buffer lease plan blocks deterministic replay when required
- reason/warnings are not fingerprint sources
- replay is read-only
- runtime pointer is not mutated
- LoRA attach/detach is not executed
- TensorCube/GPU buffer is not mutated
- runtime splice is not executed
- no SFT/DPO training execution
- no Python validator

## Boundary
TCU-17 only seals runtime splice replay determinism.
TCU-18 promotes TensorCube metrics into PerfGuard.
TCU-19 handles TensorCube emergency demotion / safe tensor mode.
TCU-20 handles long-horizon TensorCube health ledger.
