# 16AI-QW-38G-R6A-DECODE-02 Report

Token Transition Context Guard / Local Coherence Decode Seal baked.

## Implemented
- Added `model_core::decode_transition_guard` SSOT.
- Added `TransitionGuardConfig`, `TransitionRuntimeContext`, `TransitionDecision`, `TransitionAction`, and `TransitionReason`.
- Added transition fields to `CpuOracleCandidateTrace`.
- CPU oracle now evaluates transition risk and can soft-penalize or hard-block candidates when guard is enabled.
- `probe_only` mode records risk without changing logits.
- Runtime env gate: `ASH_DECODE_TRANSITION_GUARD=off|probe|on`.
- Generation sampled decode now attaches id-based recent context through `TransitionRuntimeContext`.

## Limits
- GPU shader transition parity is intentionally deferred to DECODE-02A.
- Full piece/text candidate hints are not yet available for every runtime candidate; missing piece context is recorded as unavailable.
- Cargo/rustfmt/WebGPU runtime validation was not run in this container.
