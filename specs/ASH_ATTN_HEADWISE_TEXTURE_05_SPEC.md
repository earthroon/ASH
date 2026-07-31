# ASH-ATTN-HEADWISE-TEXTURE-05

## Sustained Live Shadow Soak /
## Route·Sequence-Length Coverage Matrix /
## Latency·Residency Budget /
## Divergence Quarantine /
## Automatic Shadow Disable /
## BufferAtlas Uninterrupted Authority Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-05`  
> Build revision: `HEADWISE-TEXTURE-05-sustained-live-shadow-soak-v1`  
> Parent: `ASH-ATTN-HEADWISE-TEXTURE-04-R1` PASS  
> Canonical local source SHA-256: `e3b3993b3e6cd66dfe07a8adf219a2b507334d3a1616a1cec2c0d7c95d77ddd8`  
> Canonical local source lines: `1837`  
> Canonical local source bytes: `43339`  
> Active executor: `BufferAtlasV1`  
> Candidate executor: `KvTextureGqa4V1`  
> Parent readiness: `LiveShadowParityBound`  
> Target readiness: `SustainedShadowSoakBound`  
> Output authority: `HeadwiseFullActive` unchanged

---

# 0. Purpose

TEXTURE-04-R1 proves one live-shadow incremental commit and one live-shadow chunk commit across every model layer. TEXTURE-05 turns that point proof into sustained, bucketed, budgeted and self-quarantining runtime evidence.

Canonical flow:

```text
BufferAtlas authoritative production
  -> bounded production Q/reference GPU capture
  -> KvTexture GQA4 live shadow
  -> device-side compact parity token
  -> route/length coverage supervisor
  -> timestamp and residency accounting
  -> divergence quarantine and automatic shadow disable
```

Candidate failure, budget violation or quarantine must never block, replace, suppress or roll back BufferAtlas production output.

---

# 1. Authority state

```text
BufferAtlasV1
  ProductionActive
  UninterruptedAuthority

KvTextureGqa4V1
  LiveShadowParityBound
  -> SustainedShadowSoakBound
  ProductionOutputCommitForbidden

Headwise output authority
  HeadwiseFullActive
```

Required zero counters:

```text
candidate output commit
candidate downstream consumer
route authority mutation
output authority mutation
physical executor switch
TensorCube texture consumer
host upload
host repack
CPU materialization
payload readback
production blocked by shadow
production output suppressed
production output replaced
```

---

# 2. Coverage matrix

Sequence-length evidence is cell-local. Evidence from one bucket cannot satisfy another.

`seq_kv` buckets:

```text
1..128
129..256
257..512
513..1024
1025..1536
1537..2048
```

Route and `seq_q` buckets:

```text
IncrementalDecode
  Q1 x 6 seq_kv buckets = 6 cells

ChunkedDecode
  Q2..4 x 6 seq_kv buckets   = 6 cells
  Q5..8 x 6 seq_kv buckets   = 6 cells
  Q9..16 x 6 seq_kv buckets  = 6 cells
  Q17..32 x 6 seq_kv buckets = 6 cells
```

Required matrix:

```text
30 / 30 cells
2 healthy commits per cell
60 bounded healthy commits
22 layers per commit
1320 candidate layer dispatches
1320 device compare dispatches
60 compact token drains
```

Long-duration promotion evidence is distinct from the bounded gate:

```text
8 healthy commits per cell
240 total healthy commits
128 consecutive healthy commits
```

The bounded gate does not claim the long-duration threshold.

---

# 3. Deterministic gate geometry

Canonical representative values:

```text
Incremental seq_q
  1

Chunk seq_q
  2, 6, 12, 24

seq_kv
  64, 192, 384, 768, 1280, 1792
```

The 60-commit order is deterministic and provides two post-warmup windows for residency plateau evidence.

---

# 4. Timestamp query ring

TEXTURE-05 adds a compact timestamp-query envelope around actual live-shadow work. It does not read back Q, K, V, reference output or candidate output payloads.

Measured intervals:

```text
production Q/reference capture
candidate GQA4 dispatch
output comparison
compact token finalize
total shadow GPU envelope
queue wait
```

Canonical runtime profile:

```text
capture overhead p95 ratio     <= 8 percent
capture overhead p95 absolute  <= 500 us
total shadow GPU p95           <= 20 ms
total shadow GPU p99           <= 35 ms
queue wait p99                 <= 50 ms
consecutive soft misses        <= 3
```

The physical gate may use a separately digested device-specific budget profile. A changed budget changes evidence identity and cannot overwrite another device profile silently.

Timestamp integrity failure is a divergence event.

---

# 5. Residency budget

The supervisor accounts for:

```text
current and previous K/V texture generations
copy-on-write staged pages
Q snapshots
reference output snapshots
candidate score/probability/output scratch
compact parity token buffers
timestamp query and resolve buffers
```

Canonical initial limits:

```text
retained texture generations   2
snapshot commits in flight     4
snapshot budget               64 MiB
candidate scratch budget     256 MiB
timestamp ring budget           4 MiB
total shadow budget           768 MiB
plateau growth ratio          <= 2 percent
```

Plateau evidence compares two completed post-warmup windows while the runtime remains alive. Process exit is not residency plateau evidence.

---

# 6. Backpressure and nonblocking production

Canonical backlog policy:

```text
captured max       4
ready max          4
submitted max      2
total pending max  6
```

When candidate capacity is exhausted:

```text
new candidate capture skipped
CoverageDeferred receipt emitted
BufferAtlas production proceeds
```

Already submitted GPU work is drained to completion. The implementation does not claim cancellation of submitted work.

---

# 7. Divergence quarantine

Immediate quarantine events include:

```text
numeric mismatch
nonfinite reference or candidate value
compact token integrity failure
generation mismatch
session epoch mismatch
invocation lineage mismatch
texture generation-view mismatch
candidate dispatch failure
compare dispatch failure
token drain failure
timestamp integrity failure
candidate output commit attempt
downstream consumer attempt
authority mutation attempt
```

Latency, residency and backlog soft limits use consecutive-window policy. Hard ceilings quarantine immediately.

Quarantine ledger is append-only and binds:

```text
model instance
session and epoch
supervisor generation
route and coverage cell
KV and texture generation
invocation lineage
fault kind
compact telemetry
prior ledger digest
record digest
```

---

# 8. Automatic shadow disable

```text
Healthy
  -> Quarantined
  -> CaptureAdmissionClosed
  -> UnsubmittedTicketsRetired
  -> SubmittedWorkDrainOnly
  -> SnapshotAndScratchFenceAwareRelease
  -> DisabledBySupervisor
```

The same session does not reactivate automatically.

Reactivation requires at minimum:

```text
explicit operator action or new session epoch
TEXTURE-01 authority revalidation
TEXTURE-02 full persistent snapshot
TEXTURE-03 generation parity
new supervisor generation
```

---

# 9. BufferAtlas uninterrupted authority drill

The fault drill uses an isolated supervisor state so healthy soak evidence remains immutable.

```text
healthy live shadow
  -> intentional numeric divergence
  -> candidate quarantine
  -> automatic shadow disable
  -> 8 additional BufferAtlas-only production commits
```

The drill proves:

```text
fault-generation BufferAtlas output committed
post-disable BufferAtlas output committed 8 times
candidate dispatch admitted 0 after disable
production wait on candidate 0
production output suppression 0
production output replacement 0
HeadwiseFullActive pointer unchanged
```

---

# 10. Runtime ownership

New backend modules:

```text
headwise_gqa4_live_shadow_soak.rs
headwise_texture_shadow_timing.rs
headwise_texture_shadow_residency_budget.rs
```

New model modules:

```text
headwise_texture_shadow_coverage.rs
headwise_texture_shadow_quarantine.rs
headwise_texture_shadow_supervisor.rs
```

`NativeWgpuModel` owns the model-scoped supervisor registry, timestamp policy and residency budget. `DecodeState` stores only evidence digests and does not own the production executor pointer.

---

# 11. Gate contract

```text
positive cases              192 / minimum 184
negative controls           200 / minimum 192
decision counters           164
child artifacts             136
CLI key/value pairs         116
response-file lines         232
coverage cells               30
healthy commits              60
model layers                 22
post-disable commits          8
```

Child artifact ordered-list digest:

```text
357170b1028984f093ec1741f0bdeb000cf63b646f27c8ec25bf52e838917004
```

This digest is computed as SHA-256 of the exact 136 ordered semantic artifact IDs joined by `\n` without a trailing newline.

---

# 12. Runtime artifacts

```text
workspace/runtime/attention/headwise/texture/05/
workspace/runtime/attention/headwise/texture/ash_attn_headwise_texture_05_runtime_artifact.json
workspace/runtime/attention/headwise/texture/ash_attn_headwise_texture_05_local_manifest.json
```

First-class children include the coverage matrix, latency summary, residency summary, quarantine ledger, disable receipt, BufferAtlas continuity receipt, sustained-soak receipt, decision counters and child hashes.

---

# 13. Direct execution

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_texture_05_gate `
  -- `
  "@specs/cli/ash_attn_headwise_texture_05.args"
```

Expected revision:

```text
HEADWISE-TEXTURE-05-sustained-live-shadow-soak-v1
```

PASS token:

```text
PROMOTE_ASH_ATTN_HEADWISE_TEXTURE_05_SUSTAINED_LIVE_SHADOW_SOAK_ROUTE_SEQUENCE_LENGTH_COVERAGE_MATRIX_LATENCY_RESIDENCY_BUDGET_DIVERGENCE_QUARANTINE_AUTOMATIC_SHADOW_DISABLE_BUFFERATLAS_UNINTERRUPTED_AUTHORITY_SEALED
```

---

# 14. Completion state

After PASS:

```text
KvTextureGqa4V1
  CapabilityBoundCandidate
  PersistentKvResidencyBound
  IncrementalAppendParityBound
  LiveShadowParityBound
  SustainedShadowSoakBound
  ProductionOutputCommitForbidden
```

The next stage is `ASH-ATTN-HEADWISE-TEXTURE-06`, covering prefill baseline publication, bounded full-prefill Q/output snapshots, prefill GQA4 shadow replay, long-sequence tile coverage and cross-route parity closure.