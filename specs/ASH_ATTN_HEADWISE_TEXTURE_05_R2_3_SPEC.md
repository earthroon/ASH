# ASH-ATTN-HEADWISE-TEXTURE-05-R2.3

## Device-Scoped Pipeline Factory /
## Manager-Orchestrated Pipeline Authority /
## Single Initialization Creation /
## Ready-State Per-Commit Creation Zero /
## Authoritative Device-Lost Transition /
## Generation-Bound Wake-Up Rehydration /
## Pipeline Cardinality·Wake Receipt /
## Manual GC Preservation Seal

> Status: SPEC RELEASE rev.2  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-05-R2.3`  
> Build revision: `HEADWISE-TEXTURE-05-R2.3-pipeline-factory-manager-device-loss-wakeup-v2`  
> Parent: `ASH-ATTN-HEADWISE-TEXTURE-05-R2.2`  
> Parent readiness: `PerCommitManualGcBound`  
> Active executor: `BufferAtlasV1` unchanged  
> Candidate executor: `KvTextureGqa4V1` unchanged  
> Output authority: `HeadwiseFullActive` unchanged  
> Patch-local readiness: `PipelineManagerWakeBound`

---

# 0. Physical evidence

R2.2 manual GC preserved all 69 post-owner-drop cleanup boundaries, but the physical rerun remained HOLD:

```text
p50Ns            3,530,291,200
p95Ns           16,000,145,408
p99Ns           16,270,633,984
maxNs           16,270,633,984
worstGeneration 19
worstRoute      incremental_decode
worstSeqQ       1
worstSeqKv      1792
```

The result proves that transient-resource reclamation alone did not close the latency defect.

The active Texture-05 path visibly creates at least:

```text
BufferAtlasReference          22 per healthy commit
TexturePopulation             22 per healthy commit
TexturePersistentPopulation   22 per healthy commit
TextureValidation             22 per healthy commit
Candidate                      1 per healthy commit
Compare                        1 per healthy commit
Finalize                       1 per healthy commit

healthy commit total          91
healthy 60-commit total       5,460
fault/post-disable reference    198
visible minimum total         5,658
```

R2.3 removes pipeline construction from commit and layer scopes.

---

# 1. Goal

Canonical lifecycle:

```text
Device generation G established
  -> PipelineFactory creates seven canonical bundles once
  -> PipelineManager validates identity and cardinality
  -> Manager enters Ready(G)
  -> every layer and commit acquires existing bundles
  -> per-commit creation zero
  -> per-layer creation zero

Authoritative device loss for G
  -> new commit admission closes
  -> active commit is not resumed across generations
  -> Manager enters DeviceLost(G)
  -> old entries are invalidated
  -> device generation G+1 established
  -> Factory creates seven bundles once for G+1
  -> Manager validates wake receipt
  -> Manager enters Ready(G+1)
  -> new commit admission reopens
```

An ordinary cache miss, latency HOLD, GC delay, numeric mismatch or unknown state must never trigger recreation.

---

# 2. Pipeline kinds

```rust
pub enum HeadwiseTexturePipelineKind {
    BufferAtlasReference,
    TexturePopulation,
    TexturePersistentPopulation,
    TextureValidation,
    Candidate,
    Compare,
    Finalize,
}
```

Canonical cardinality:

```text
pipeline kinds                     7
initial creation count per kind    1
Ready-state creation count         0
Ready-state factory call count     0
```

---

# 3. Factory responsibility

```rust
pub struct HeadwiseTexturePipelineFactory {
    device: Arc<backend_wgpu::Device>,
    device_identity_digest: String,
    device_generation: u64,
}
```

The factory may:

```text
create shader modules
create bind-group layouts
create pipeline layouts
create compute pipelines
seal source and identity digests
return one complete seven-kind pipeline set
```

The factory may not:

```text
select routes
admit commits
mutate production authority
own coverage state
own manual GC state
perform lazy creation after manager seal
```

Allowed factory call sites:

```text
initial manager construction
verified device-loss wake-up for a newer device generation
```

Forbidden factory call sites:

```text
healthy commit loop
layer loop
fault drill commit
post-disable commit
ordinary cache miss
latency HOLD handling
manual GC boundary
```

---

# 4. Manager responsibility

```rust
pub struct HeadwiseTexturePipelineManager {
    state: HeadwiseTexturePipelineManagerState,
    device_identity_digest: String,
    device_generation: u64,
    pipeline_set_digest: String,
    entries: BTreeMap<HeadwiseTexturePipelineKind, Arc<HeadwiseTexturePipelineBundle>>,
}
```

The manager is the pipeline lifecycle SSOT.

```rust
pub enum HeadwiseTexturePipelineManagerState {
    Cold,
    Initializing { device_generation: u64 },
    Ready { device_generation: u64, pipeline_set_digest: String },
    DeviceLost { lost_generation: u64, loss_receipt_digest: String },
    Waking { source_generation: u64, target_generation: u64 },
    Quarantined { reason: String },
}
```

Ready-state acquisition:

```text
requested kind exists
bundle generation equals manager generation
bundle device identity equals manager identity
bundle source digest validates
pipeline-set digest remains unchanged
```

Ready-state miss:

```text
HeadwiseTexturePipelineMissingReadyEntry
```

A Ready-state miss is an invariant failure. The manager must not call the factory.

---

# 5. Bundle identity

Each bundle binds:

```text
pipeline kind
device identity digest
device generation
shader source digest
bind-group layout digest
pipeline layout digest
entry-point identity
workgroup/specialization identity
compute pipeline identity digest
bundle digest
```

A bundle from device generation G cannot be used on generation G+1.

Global unkeyed process singletons are forbidden. Pipeline authority is scoped to one device identity and generation.

---

# 6. Normal execution

Manager construction occurs before the 60-commit soak loop.

```text
manager initialize
  -> seven bundles created once
  -> cardinality verified
  -> pipeline-set digest sealed
  -> Ready
```

Every physical path receives the manager or an acquired bundle:

```text
BufferAtlas reference dispatch
K/V texture population
K/V persistent population
K/V texture validation
candidate dispatch
compare dispatch
finalize dispatch
```

Expected no-loss acquisitions:

```text
BufferAtlasReference          1,518
TexturePopulation             1,320
TexturePersistentPopulation   1,320
TextureValidation             1,320
Candidate                        60
Compare                          60
Finalize                         60
```

Expected creation deltas:

```text
60 healthy commits            0
1 fault commit                0
8 post-disable commits        0
69 manual-GC boundaries       0
```

---

# 7. Manual GC preservation

R2.2 remains authoritative for transient reclamation:

```text
commit evidence complete
  -> tickets dropped
  -> residency registry dropped
  -> device.poll(PollType::Wait)
  -> GC receipt sealed
  -> next commit admitted
```

Manual GC may destroy:

```text
buffers
textures
texture views
snapshots
scratch
transient bind groups
timestamp resources
```

Manual GC must preserve:

```text
PipelineManager
seven pipeline bundles
pipeline-set digest
device identity
device generation
Ready state
```

After every ordinary GC boundary:

```text
creation delta                 0
pipeline identity changes      0
manager generation changes     0
manager state                  Ready
```

---

# 8. Authoritative device loss

Wake-up is allowed only after an authoritative device-loss receipt.

The receipt binds:

```text
lost device identity
lost device generation
loss reason
loss observation source
active commit identity if any
admission closure state
receipt digest
```

Loss transition:

```text
Ready(G)
  -> admission closed
  -> in-flight commit aborted or failed
  -> old entries invalidated
  -> DeviceLost(G)
```

Forbidden:

```text
continuing an in-flight G commit with G+1 pipelines
retaining old entries as active
reusing old pipeline handles on the new device
silently treating cache miss as device loss
```

---

# 9. Wake-up rehydration

Wake-up requires:

```text
valid device-loss receipt
new device identity established
new queue lineage established
target generation > source generation
old active entry count == 0
new commit admission remains closed
```

Wake flow:

```text
DeviceLost(G)
  -> Waking(G -> G+1)
  -> Factory creates seven new bundles
  -> cardinality == 7
  -> each creation count == 1
  -> identities bind G+1
  -> new pipeline-set digest sealed
  -> wake receipt verified
  -> Ready(G+1)
  -> admission reopened
```

Wake failure moves the manager to Quarantined and leaves admission closed.

---

# 10. Receipts

Required receipts:

```text
HeadwiseTexturePipelineInitialBuildReceipt
HeadwiseTexturePipelineIdentityRegistry
HeadwiseTexturePipelineReuseReceipt
HeadwiseTexturePipelineCardinalitySummary
HeadwiseTexturePipelineDeviceLossReceipt
HeadwiseTexturePipelineWakeReceipt
HeadwiseTexturePipelineManagerSummary
```

Initial-build receipt proves:

```text
one build
seven observed kinds
one creation per kind
manager Ready
pipeline-set digest sealed
```

Reuse receipt proves per boundary:

```text
creation count before == creation count after
creation delta == 0
manager Ready before and after
pipeline-set digest unchanged
```

Wake receipt proves:

```text
source generation
target generation
loss receipt digest
old entry count after invalidation == 0
new kind count == 7
one creation per kind
old-generation reuse count == 0
manager Ready
admission reopened after PASS
```

---

# 11. Artifact contract

Rust writes:

```text
workspace/runtime/attention/headwise/texture/05/r2_3/
  pipeline_source_registry.json
  pipeline_initial_build_receipt.json
  pipeline_identity_registry.json
  pipeline_reuse_receipts.json
  pipeline_cardinality_summary.json
  pipeline_loss_transition_fixture.json
  pipeline_wake_fixture_receipt.json
  pipeline_manager_summary.json

workspace/runtime/attention/headwise/texture/
  ash_attn_headwise_texture_05_r2_3_runtime_artifact.json
  ash_attn_headwise_texture_05_r2_3_local_manifest.json
```

Canonical artifact and manifest are authored by Rust, atomically written, read back and SHA-256 verified.

R2.3 PASS does not claim `SustainedShadowSoakBound` while the original Texture-05 latency predicates remain HOLD.

---

# 12. Completion gate

```text
canonical pipeline kinds                     7
initial build count                          1
initial creation count per kind              1
Ready-state factory calls                    0
Ready-state pipeline creations               0
per-commit creation delta                    0
per-layer creation delta                     0
healthy reuse receipts                      60
fault reuse receipts                         1
post-disable reuse receipts                  8
manual-GC boundaries                        69
manual-GC identity changes                   0
ordinary cache misses                        0
production authority mutations              0
candidate output commits                     0
```

Loss/wake fixture:

```text
accepted device-loss receipts                1
admission closures                           1
old-generation acquisitions after loss       0
target generation advance                  PASS
new kind cardinality                         7
new creation count per kind                  1
manager Ready transition                   PASS
admission reopen after wake                 PASS
```

PASS token:

```text
PASS_ASH_ATTN_HEADWISE_TEXTURE_05_R2_3_DEVICE_SCOPED_PIPELINE_FACTORY_MANAGER_SINGLE_INITIALIZATION_CREATION_READY_STATE_PER_COMMIT_CREATION_ZERO_AUTHORITATIVE_DEVICE_LOST_TRANSITION_GENERATION_BOUND_WAKE_UP_REHYDRATION_PIPELINE_CARDINALITY_WAKE_RECEIPT_MANUAL_GC_PRESERVATION_SEALED
```

---

# 13. Direct execution

R2.3 verification gate:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_r2_3_gate -- "@specs/cli/ash_attn_headwise_texture_05_r2_3.args"
```

Physical Texture-05 rerun:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_gate -- "@specs/cli/ash_attn_headwise_texture_05.args"
```

---

# 14. Packaging seal

Code-baked ZIP includes Rust implementation, verification gate, CLI registry, response file and Cargo bin registration.

Code-baked ZIP excludes:

```text
this Markdown specification
runtime artifact JSON
local manifest JSON
child runtime evidence JSON
target
.git
```

Canonical lifecycle:

```text
Factory creates only during initial construction or authoritative device-generation wake-up.
Manager owns, validates and serves the active seven-kind pipeline set.
Commits acquire and dispatch only.
Manual GC removes transient resources without touching pipeline authority.
A Ready-state miss fails closed instead of recreating silently.
```
