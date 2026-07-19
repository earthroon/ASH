# ASH-TCU-DECODE-04-R4-R4-R4
# TensorCube Default Fragment Authority / Legacy Oracle Retention Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R4-R4_TENSORCUBE_DEFAULT_FRAGMENT_AUTHORITY_LEGACY_ORACLE_RETENTION_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R4-R3_LIVE_FRAGMENT_AUTHORITY_CORPUS_MISMATCH_TELEMETRY_PERFORMANCE_GATE`
- Default fragment source: TensorCube
- Legacy role: mandatory oracle, exact fallback, post-revocation continuation
- General production apply: false
- Legacy retirement: false
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R5_LEGACY_FRAGMENT_RETIREMENT_READINESS_ORACLE_REDUCTION_GATE`

## Parent admission

Known parent:

```text
execution_id=decode04r4r4r3-9af64f782c22fb82c716
lineage_bundle_digest=9af64f782c22fb82c716ca7defc1a67990b763a77856956a7c6c66ed443a171d
unique prompts=1700
live generations=10000
selected tokens=241200
route coverage=4/4
corpus classes=19/19
unexpected mismatch=0
unexpected natural revocation=0
output divergence=0
candidate byte leak=0
performance policy pass=true
```

The exact parent manifest, model, weights, tokenizer, runtime route and default-authority policy are content-bound.

## Promotion seal

```text
--authorize-tensorcube-default-fragment-authority
```

The seal grants TensorCube default fragment authority on all four routes while retaining the legacy oracle, fallback, automatic revocation, runtime-session quarantine, identity invalidation and operator rollback. It grants no token-selection, KV, DecodeState, sampler, RNG, finish/stop, checkpoint, resume, general-production or legacy-retirement authority.

## Four-route default

| Route | Default source | Legacy role | Protocol |
|---|---|---|---|
| greedy cached | TensorCube | oracle + rollback buffer | terminal commit |
| sampled cached | TensorCube | oracle + rollback buffer | terminal commit |
| greedy streaming | TensorCube | current oracle + continuation | compare before emit |
| sampled streaming | TensorCube | current oracle + continuation | compare before emit |

Required default route coverage is 4/4. Unsupported routes select legacy before generation.

## SSOT

```text
R4R4R4DefaultAuthorityPolicy
R4R4R4DefaultAuthorityAdmission
R4R4R4DefaultAuthorityState
R4R4R4IdentityBinding
R4R4R4InvalidationReason
R4R4R4LegacyOracleRetentionPolicy
R4R4R4OperatorRollbackPolicy
R4R4R4AuthorityQuarantine
R4R4R4GenerationAuthorityReceipt
R4R4R4DefaultAuthoritySummary

build_r4r4_r4_default_authority_policy
resolve_r4r4_r4_default_fragment_authority
invalidate_r4r4_r4_default_fragment_authority
quarantine_r4r4_r4_default_authority
run_r4_r4_r4_runtime
```

There is one owner for policy, admission, invalidation, quarantine, rollback and four-route dispatch.

## Admission order

```text
operator kill switch
runtime-session quarantine
parent receipt
model and weight identity
tokenizer identity
runtime route and policy
route, batch and token limits
legacy oracle availability
TensorCube state initialization
stream sink capability
admission
```

The first rejection reason is immutable.

## Legacy retention

```text
legacy oracle bypass=0
candidate-only mode=0
legacy fragment count=TensorCube-active selected-token count
legacy exact fallback reachable=true
legacy-only boot reachable=true
```

The oracle must remain the pre-promotion legacy decoder and keep independent state.

## Failure containment

Cached mismatch:

```text
freeze candidate buffer
complete and commit legacy buffer once
output=legacy baseline
create runtime-session quarantine
```

Streaming mismatch:

```text
mismatched candidate bytes stay private
emit current oracle fragment once
revoke TensorCube once
continue legacy-only
create runtime-session quarantine
```

One natural mismatch fails promotion even when containment succeeds.

## Quarantine and rollback

One natural mismatch quarantines TensorCube default authority for the runtime session. Later generations start LegacyDefault and same-session automatic re-enable is forbidden.

Canonical kill switch:

```text
ASH_TCU_DECODE04_FORCE_LEGACY_FRAGMENT_AUTHORITY=1
```

A manual rollback during generation is latched for the next generation. Clearing quarantine requires runtime restart, explicit operator acknowledgement, fresh identity validation, policy validation and a fresh authority epoch.

## Identity invalidation

Bound identities:

```text
parent execution and lineage
model manifest and weight bundle
tokenizer manifest and intrinsic identity
reserved-token digest
byte-token mapping digest
special-token classification digest
runtime route digest
policy digest
```

Required invalidation fixtures cover parent, model, weight, tokenizer manifest, tokenizer intrinsic, reserved-token, byte mapping, classification, runtime route and policy mismatches. Every fixture must select LegacyDefault before candidate-state creation.

## Natural promotion corpus

R4-R4-R4 reuses the R4-R4-R3 corpus identity or a strict superset.

```text
TensorCube-default generations=10000
per route=2500
corpus classes=19/19
selected tokens=241200
natural mismatch=0
natural revocation=0
natural quarantine=0
natural cached rollback=0
natural stream fallback=0
natural post-revocation legacy=0
output divergence=0
candidate leak=0
UTF-8 failures=0
telemetry integrity errors=0
```

## Parity and ownership

TensorCube-default and legacy-default replay must match selected tokens, output bytes, stream chunks and boundaries, KV, DecodeState, sampler, RNG, finish reason and runtime route.

TensorCube sampler calls, RNG calls, token overrides, KV writes, DecodeState writes and route changes remain zero.

## Limits and performance

```text
batch size=1
max_new_tokens<=256
candidate+oracle+comparison p99<=5ms/token
stream publication p99<=5ms/visible fragment
cached dual-buffer<=8MiB
throughput>=70% of legacy-only per route
unbounded allocation=0
```

Identity, policy, quarantine and rollback checks are generation-start-only.

## No repair

Forbidden: lossy UTF-8, replacement fallback, trim, whitespace collapse, Unicode normalization, invalid-byte skip, silent fragment drop, silent mismatch suppression, legacy bytes reported as candidate, post-exposure repair, ignored identity mismatch, ignored quarantine or ignored rollback.

Static scans must exclude their own search literals.

## Binary and PASS

```text
ash_tcu_decode_04_r4_r4_r4_tensorcube_default_fragment_authority_legacy_oracle_retention_gate
PASS_ASH_TCU_DECODE_04_R4_R4_R4_TENSORCUBE_DEFAULT_FRAGMENT_AUTHORITY_LEGACY_ORACLE_RETENTION_GATE
```

PASS grants only:

```text
decode04_r4_r5_authorized=true
tensorcube_default_fragment_authority=true
tensorcube_general_fragment_authority=false
tensorcube_streaming_fragment_authority=true
legacy_oracle_retained=true
legacy_fallback_retained=true
production_fragment_apply_authorized=true
general_production_apply_authorized=false
legacy_decoder_retirement_authorized=false
production token/KV/sampler/RNG authority=false
```

HOLD or FAIL grants no new authority.

## Next gate

`ASH-TCU-DECODE-04-R4-R5 Legacy Fragment Retirement Readiness / Oracle Reduction Gate`

R4-R5 may evaluate oracle sampling reduction, periodic full-dual-run windows, durable quarantine, restart recovery and operator rollback drills. Legacy retirement remains forbidden until independent readiness evidence passes.
