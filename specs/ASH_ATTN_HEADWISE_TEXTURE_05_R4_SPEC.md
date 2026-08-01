# ASH-ATTN-HEADWISE-TEXTURE-05-R4

## Layer·Stage Latency Decomposition /
## Reference Capture Timing /
## BufferAtlas Dispatch Timing /
## Texture Candidate Timing /
## Compare·Finalize Timing /
## Command Encoder·Submit Census /
## Device Poll·Map Wait Attribution /
## Host-Wall·GPU-Timestamp Separation /
## Per-Layer KV-Length Scaling /
## First Dominant Stage Localization Seal

> Status: **SPEC RELEASE rev.1**  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-05-R4`  
> Build revision: `HEADWISE-TEXTURE-05-R4-layer-stage-latency-decomposition-v1`  
> Parent runtime: `ASH-ATTN-HEADWISE-TEXTURE-05-R3-R3`  
> Parent accounting correction: `ASH-ATTN-HEADWISE-TEXTURE-05-R3-R2-R1`  
> Production executor: `BufferAtlasV1` unchanged  
> Candidate executor: `KvTextureGqa4V1` unchanged  
> Candidate output authority: shadow evidence only  
> Patch-local readiness: `LayerStageLatencyLocalized`

---

# 1. Trigger

The latest physical Texture-05 execution closed the residency and transient-memory axes:

```text
full population count       1
append count                5
texture generations         6
shadow commits             60
per-commit reconstruction   0
pipeline kinds              9
plateau pass              true
retirement owner zero     true
microtile peak closure    true
```

The only remaining original eligibility failures are:

```text
latency_p95_within_budget
latency_p99_within_budget
```

Latest measured envelope:

```text
p50Ns             3,472,770,048
p95Ns            15,910,064,128
p99Ns            16,294,315,008
maxNs            16,294,315,008
worstGeneration  13
worstRoute       incremental_decode
worstSeqQ        1
worstSeqKv       1792
```

R4 does not change the latency budgets. It decomposes the remaining envelope.

---

# 2. Existing timing semantic correction

The legacy helper submits an outer begin timestamp, executes the complete shadow operation, then submits an outer end timestamp with query resolution and staging copy.

The existing field:

```text
total_shadow_gpu_ns
```

is therefore not the sum of active GPU kernels. It is a GPU queue-clock interval containing active commands, submission gaps and host-induced idle intervals.

R4 canonical semantics:

```text
legacy_field_name                     total_shadow_gpu_ns
canonical_semantic_name               legacy_gpu_queue_span_ns
legacy_queue_span_is_active_gpu_sum   false
instrumented_stage_sum_authoritative  true
```

The legacy field remains for compatibility. R4 artifacts disclose the corrected meaning explicitly.

---

# 3. Exact parent topology per healthy commit

```text
outer envelope begin submit                         1
BufferAtlas reference submits                      22
Q/reference capture-copy submits                   22
two-layer microtile wave submits                   11
finalize and compact-token copy submit              1
outer envelope end/resolve/copy submit               1
-----------------------------------------------------
queue submissions                                  58
command encoders                                   58
command buffers                                    58
compute passes                                     89
device.poll(Wait)                                  13
map_async calls                                     2
```

The legacy R3-R3 dispatch receipt counts only eleven wave submits and one finalize submit. Its `submission_count=12` remains available but is marked non-exhaustive.

R4 must preserve the parent topology:

```text
new per-stage timing submissions  0
new per-stage timing polls        0
per-layer readbacks               0
payload readbacks                 0
topology mutations                0
```

The inherited outer timing pair remains visible:

```text
inherited envelope timing submissions  2
inherited envelope timing polls        1
```

---

# 4. Timestamp query authority

R4 uses a session-scoped three-slot timestamp query ring.

```text
ring slots              3
queries per slot      256
written queries       224
query pairs           112
reserved queries       32
```

Canonical ownership:

```text
0..1       outer queue-span pair
2..45      22 BufferAtlas reference pairs
46..89     22 capture-copy pairs
90..133    22 candidate-accumulate pairs
134..177   22 candidate-normalize pairs
178..221   22 compare pairs
222..223   finalize pair
224..255   reserved and unwritten
```

Every query index from zero through 223 has exactly one owner. Query resolution occurs once in the inherited envelope-end encoder. The slot is reusable only after the timing staging map and completion poll finish.

---

# 5. Topology-preserving instrumentation

R4 writes timestamps into command encoders that already exist:

```text
reference begin/end     existing reference encoder
capture begin/end       existing capture encoder
accumulate begin/end    existing layer-wave encoder
normalize begin/end     existing layer-wave encoder
compare begin/end       existing layer-wave encoder
finalize begin/end      existing finalize encoder
```

Forbidden:

```text
additional timing-only encoder or submit
per-stage device poll
per-stage map_async
per-layer timing readback
payload readback
kernel fusion or dispatch reordering
layer-wave size change
microtile size change
```

---

# 6. Host timing planes

R4 records monotonic host-wall intervals separately from GPU timestamps:

```text
commit setup
reference encode
reference submit call
capture encode
capture submit call
ticket registry work
wave encode
wave submit call
wave completion poll
wave post-completion work
finalize encode
finalize submit call
compact map request
compact poll wait
compact callback receive
compact parse
envelope begin encode and submit
envelope end encode and submit
timing map request
timing poll wait
timing callback receive
timing parse
outcome adoption
```

Host `Instant` values and GPU ticks are never directly subtracted. They remain separate clock domains.

---

# 7. Required receipts

Per commit:

```text
22 layer-stage timing receipts
11 wave synchronization receipts
1 exhaustive operation census
1 commit latency decomposition receipt
1 compact timing envelope
```

Across sixty healthy commits:

```text
layer receipts                1,320
wave receipts                   660
reference GPU observations    1,320
capture GPU observations      1,320
candidate GPU observations    1,320
normalize GPU observations    1,320
compare GPU observations      1,320
finalize GPU observations        60
```

The commit decomposition records:

```text
legacy GPU queue span
instrumented active GPU stage sum
queue unattributed interval
reference total
capture total
candidate accumulate total
candidate normalize total
compare total
finalize total
host encode total
host submit total
wave poll total
map poll total
callback total
other accounted host time
host unattributed time
first dominant GPU stage
first dominant host stage
first dominant layer when GPU-layer-specific
```

---

# 8. KV-length scaling

R4 creates scaling strata for:

```text
5 layer-specific GPU stages
× 22 layers
× 5 route/query shapes
= 550 scaling receipts
```

Each stratum contains:

```text
6 KV representatives
2 repeats per representative
12 observations
```

Every scaling receipt records:

```text
slope_ns_per_kv_token
intercept_ns
R-squared
median absolute residual
maximum absolute residual
monotonicity violation count
```

No KV point may be silently dropped.

---

# 9. Dominant-stage classification

At the worst queue-span commit, R4 compares:

```text
BufferAtlas reference GPU
capture-copy GPU
candidate accumulate GPU
candidate normalize GPU
compare GPU
finalize GPU
host wave-poll share
host map-poll share
queue unattributed share
```

A single domain is dominant when its share is at least `0.50`. Otherwise the result is explicitly classified as mixed.

Allowed classifications include:

```text
bufferatlas_reference_gpu_dominant
capture_copy_gpu_dominant
texture_candidate_accumulate_gpu_dominant
candidate_normalize_gpu_dominant
compare_gpu_dominant
finalize_gpu_dominant
wave_poll_wait_dominant
map_poll_wait_dominant
queue_unattributed_interval_dominant
no_single_dominant_stage
```

When the dominant domain is layer-specific GPU work, the dominant layer is selected from that exact stage, not from an unrelated aggregate.

---

# 10. Runtime artifacts

Physical gate artifacts:

```text
workspace/runtime/attention/headwise/texture/05/r4/
  timestamp_ring_receipt.json
  layer_stage_timing_receipts.json
  wave_synchronization_receipts.json
  operation_census_receipts.json
  commit_latency_decomposition_receipts.json
  kv_length_scaling_receipts.json
  first_dominant_stage_receipt.json
  session_summary.json

workspace/runtime/attention/headwise/texture/
  ash_attn_headwise_texture_05_r4_runtime_artifact.json
  ash_attn_headwise_texture_05_r4_local_manifest.json
```

Verification gate artifacts:

```text
workspace/runtime/attention/headwise/texture/05/r4_verification/
  source_topology_audit.json

workspace/runtime/attention/headwise/texture/
  ash_attn_headwise_texture_05_r4_verification_runtime_artifact.json
  ash_attn_headwise_texture_05_r4_verification_local_manifest.json
```

All files are Rust-authored with temporary write, atomic rename, readback and SHA-256 verification.

---

# 11. CLI contract

The R4 verification response file contains exactly forty key/value pairs:

```text
--repo-root
--expected-patch-id
--expected-build-revision
--parent-r3-r3-runtime-artifact
--parent-r3-r2-r1-runtime-artifact
--physical-gate-source
--backend-r4-source
--backend-dispatch-source
--ticket-registry-source
--backend-lib-source
--expected-layer-count
--expected-shadow-commit-count
--expected-wave-count-per-commit
--expected-total-wave-receipt-count
--expected-timestamp-ring-slot-count
--expected-timestamp-query-count-per-slot
--expected-written-query-count-per-commit
--expected-query-pair-count-per-commit
--expected-command-encoder-count-per-commit
--expected-command-buffer-count-per-commit
--expected-submit-count-per-commit
--expected-compute-pass-count-per-commit
--expected-poll-count-per-commit
--expected-map-count-per-commit
--expected-reference-stage-count-per-commit
--expected-capture-stage-count-per-commit
--expected-candidate-stage-count-per-commit
--expected-normalize-stage-count-per-commit
--expected-compare-stage-count-per-commit
--expected-finalize-stage-count-per-commit
--dominant-stage-share-min
--layer-outlier-ratio-min
--require-host-gpu-clock-domain-separation
--forbid-new-timing-only-submit
--forbid-per-stage-poll
--forbid-per-layer-readback
--forbid-payload-readback
--forbid-topology-mutation
--runtime-artifact
--local-manifest
```

---

# 12. Completion gate

R4 patch-local PASS requires:

```text
healthy measurements                         60
layer receipts                            1,320
wave receipts                               660
query ring slots                              3
queries per slot                            256
written queries                             224
query pairs                                 112
missing or duplicate query ownership         0
slot reuse before completion                 0
encoders/submits                             58
compute passes                               89
polls                                        13
maps                                          2
new timing-only submissions                   0
new per-stage timing polls                    0
per-layer readbacks                           0
payload readbacks                             0
topology mutations                            0
scaling receipts                            550
first dominant stage localized              true
numeric parity                              PASS
R3-R2 plateau                               PASS
R3-R3 peak closure                          PASS
production authority mutation count            0
candidate output commit count                   0
```

R4 PASS does not require the original latency p95 or p99 predicate to pass. It requires the remaining latency failure to be decomposed and localized without changing the measured topology.

Patch-local PASS token:

```text
PASS_ASH_ATTN_HEADWISE_TEXTURE_05_R4_LAYER_STAGE_LATENCY_DECOMPOSITION_REFERENCE_CAPTURE_BUFFERATLAS_TEXTURE_CANDIDATE_COMPARE_FINALIZE_ENCODER_SUBMIT_POLL_MAP_HOST_GPU_KV_SCALING_FIRST_DOMINANT_STAGE_LOCALIZATION_SEALED
```

---

# 13. Direct execution

Verification gate:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_r4_gate -- "@specs/cli/ash_attn_headwise_texture_05_r4.args"
```

Physical Texture-05 gate:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_gate -- "@specs/cli/ash_attn_headwise_texture_05.args"
```

Expected disclosure:

```text
[r4-census] encoders/submits/polls/maps/compute passes
[r4-gpu] queue span, active stage totals and unattributed interval
[r4-host] wall, encode, submit, poll, callback and unattributed time
[r4-dominant] domain, stage, layer, classification and shares
```

The original Texture-05 eligibility line remains unchanged and may still report HOLD.

---

# 14. Packaging

The code-baked ZIP includes the R4 query ring, GPU and host instrumentation, physical integration, verification gate, CLI registry, response file and Cargo registration.

It excludes:

```text
Markdown specifications
workspace/runtime
runtime artifacts and manifests
target
.git
```

R4 changes the latency number from a sealed aggregate into a stage-, layer-, synchronization- and scaling-backed optimization target. It does not forge a promotion or relax the original budget.
