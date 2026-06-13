# SFT-GPU-RUN-02 Acceptance

## Status

PASS_STATIC / PENDING_ARTIFACT_INTAKE_RUNTIME

## Scope

Strict GPU train artifact intake and adapter registry candidate binding.

## SSOT

- Source strict GPU train run seal
- Artifact verification evidence
- Adapter identity evidence
- Registry intake evidence
- Candidate binding evidence
- Promotion eligibility evidence
- No runtime mutation guard
- Artifact intake seal

## Confirmed Static Gates

- Source strict GPU train run seal is required.
- Source strict GPU train run must be accepted.
- CPU fallback source is rejected.
- CPU materialized source is rejected.
- Artifact manifest digest is required.
- Adapter payload digest is required.
- Safetensors digest is required.
- Artifact must be non-empty.
- Save-reload parity must pass.
- Adapter identity must match.
- Slot identity must match.
- Target module identity must match.
- Registry intake receipt is required.
- Duplicate artifact fails closed.
- Candidate binding is required.
- Promotion eligibility is required.
- Runtime current pointer update is forbidden.
- Promotion apply is forbidden.
- Lifecycle mutation is forbidden.
- Slot action apply is forbidden.
- Rollback execution is forbidden.
- ASH current binding is forbidden.

## Opened

- strict GPU train artifact intake
- adapter manifest verification
- adapter payload verification
- safetensors digest verification
- adapter registry write
- registry candidate binding
- promotion eligibility mark
- duplicate artifact guard

## Closed

- runtime current pointer update
- promotion apply
- lifecycle mutation
- slot action apply
- rollback execution
- ASH current binding
- CPU fallback source
- CPU materialized source

## Runtime Acceptance Pending

Requires actual artifact intake from RUN-01 strict GPU train output.
