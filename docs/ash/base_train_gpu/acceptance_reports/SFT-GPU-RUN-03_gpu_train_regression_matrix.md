# SFT-GPU-RUN-03 Acceptance

## Status

PASS_STATIC / PENDING_GPU_REGRESSION_RUNTIME

## Scope

GPU train regression matrix and multi-step loss direction seal.

## SSOT

- Source strict GPU train run seal
- Source artifact intake seal
- Regression matrix policy
- Fixture matrix
- Per-fixture GPU run evidence
- Loss direction evidence
- Adapter delta stability evidence
- Artifact parity evidence
- Matrix summary
- No runtime mutation guard
- GPU train regression matrix seal

## Confirmed Static Gates

- Source RUN-01 strict GPU train seal is required.
- Source RUN-02 artifact intake seal is required.
- Fixture matrix is required.
- Minimum fixture count is required.
- Minimum seed count is required.
- Native GPU backend is required for all fixtures.
- CPU fallback is forbidden for all fixtures.
- CPU materialization is forbidden for all fixtures.
- Silent backend demotion is forbidden for all fixtures.
- Loss values must be finite.
- Loss direction receipt is required.
- Adapter delta must be non-zero.
- Optimizer accounting is required.
- Artifact output is required.
- Save-reload parity is required.
- Runtime current pointer update is forbidden.
- Promotion apply is forbidden.
- Lifecycle mutation is forbidden.
- Slot action apply is forbidden.
- Rollback execution is forbidden.
- ASH current binding is forbidden.

## Opened

- GPU train regression matrix
- multi-fixture train receipt
- multi-seed train receipt
- multi-step loss direction receipt
- adapter delta stability matrix
- artifact parity matrix
- no CPU fallback matrix guard

## Closed

- CPU fallback
- CPU materialized train path
- silent backend demotion
- runtime current pointer update
- promotion apply
- lifecycle mutation
- slot action apply
- rollback execution
- ASH current binding

## Runtime Acceptance Pending

Requires actual strict GPU regression matrix run on target machine.
