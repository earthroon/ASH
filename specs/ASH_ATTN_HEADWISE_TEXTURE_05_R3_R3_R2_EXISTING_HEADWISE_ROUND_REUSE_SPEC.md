# ASH-ATTN-HEADWISE-TEXTURE-05-R3-R3-R2

## Existing Headwise Round Reuse / Sequential Wave Packetization / Encode-Only Wave Span Adoption / Multi-Dispatch Single Encoder / Single In-Flight Packet Authority / Packet-Scoped Completion Fence / Bounded Workgroup Sum / Queue-Ahead Packet Zero / Per-Wave Numeric Order Preservation Seal

## Identity

```text
Patch ID: ASH-ATTN-HEADWISE-TEXTURE-05-R3-R3-R2
Build revision: HEADWISE-TEXTURE-05-R3-R3-R2-existing-headwise-round-reuse-v1
Parents:
  ASH-ATTN-HEADWISE-TEXTURE-05-R3-R3-R1
  ASH-ATTN-HEADWISE-TEXTURE-05-R4-R1
Pass token:
  PASS_ASH_ATTN_HEADWISE_TEXTURE_05_R3_R3_R2_EXISTING_HEADWISE_ROUND_REUSE_SEQUENTIAL_WAVE_PACKETIZATION_SEALED
```

## Purpose

R3-R3-R1 sealed a bounded sequential topology with 72,864 canonical waves, 72,864 submits, 72,864 completion polls, one in-flight wave, and no queue-ahead submission. R4-R1 established executor-sourced topology counts and retired the static `58 submits / 13 polls` census as runtime authority.

R3-R3-R2 preserves every parent wave and its numerical order while grouping adjacent waves into bounded packets. Each packet uses one command encoder, one command buffer, one queue submit, and one completion poll.

## Reuse decision

This patch does not introduce an independent packet executor. It reuses:

- the existing Headwise encode-only measurement-span ownership model;
- the existing Headwise pair-local single-encoder round pattern;
- the existing submitted-span promotion pattern;
- the TensorCube ordered multi-pass command-buffer pattern;
- Base Train deterministic bounded grouping;
- LoRA bounded microbatch tail handling; and
- R4-R1 executor-sourced topology census.

The new module owns packet planning and receipts only. The existing Headwise dispatcher retains device, queue, encoder, submission, completion, resource, and authority ownership.

## Non-goals

```text
No WGSL numerical algorithm change
No streaming-softmax order change
No token-tile-size change
No per-dispatch workgroup-ceiling change
No persistent descriptor arena
No multiple in-flight packets
No queue-ahead submit
No runtime adaptive packet size
No reference/candidate packet mixing
No production executor switch
```

## Physical profile

```text
waves per packet cap                 4
dispatches per packet cap           16
workgroup sum per packet cap      4096
descriptor bytes per packet cap 1048576
maximum in-flight packets            1
prepared packet capacity             1
minimum aggregate submit reduction 0.50
minimum aggregate poll reduction   0.50
```

The profile is fixed for this revision. Runtime self-tuning and silent fallback are forbidden.

## SSOT flow

```text
R3-R3-R1 canonical schedule
-> deterministic R3-R3-R2 packet plan
-> existing Headwise dispatcher
-> ordered wave encoding into packet-owned encoder
-> one submit
-> one packet completion poll
-> R3-R3-R2 packet receipts
-> R4-R1 actual topology reconciliation
```

## Packet plan

```rust
pub struct HeadwiseTexture05R3R3R2PacketPlan {
    pub packet_index: u32,
    pub first_wave_index: u32,
    pub last_wave_index: u32,
    pub wave_count: u32,
    pub dispatch_count: u32,
    pub workgroup_sum: u64,
    pub descriptor_bytes: u64,
    pub boundary_reason: String,
    pub wave_order_digest: String,
    pub packet_digest: String,
}
```

The planner greedily appends canonical waves until the next wave would exceed the wave, dispatch, workgroup-sum, or descriptor-byte ceiling. A tail packet is sealed explicitly. A single parent wave that exceeds a packet ceiling fails closed and is not split.

Required closure:

```text
sum(packet wave counts) == parent wave count
packet wave ranges are contiguous
packet ranges do not overlap
packet ranges cover the complete schedule
all packet ceilings pass
```

## Existing Headwise round adoption

Reference and candidate paths each execute their own packet sequence:

```text
create one packet encoder
for each packet wave in canonical order:
  encode partial pass
  encode merge pass
  encode optional finalize pass
  encode final candidate compare only after the final wave
finish one command buffer
submit once
poll once
```

`single encoder` does not mean `single compute pass`. Explicit pass boundaries and storage dependencies remain intact.

Forbidden reorderings:

```text
all partial passes before all merge passes
parallel or unordered running-state merge
balanced merge tree
reverse wave order
cross-packet merge migration
reference/candidate dispatch interleaving
finalize before the last canonical wave
```

## Resource lifetime

The implementation follows the existing Headwise per-wave immutable parameter pattern. Per-wave parameter buffers and bind groups may be temporary, but their encoded command references remain valid through the packet submission and completion boundary.

Required counters:

```text
descriptor alias count         0
parameter overwrite count      0
resource epoch mismatch count  0
```

Persistent descriptor reuse is deferred to R3-R3-R3.

## Packet admission receipt

Each reference layer and candidate layer emits a packet admission receipt that records:

```text
scheduled, encoded, submitted, and completed wave spans
planned packets
encoders and command buffers
queue submits and completion polls
maximum in-flight packets
queue-ahead and early-next-packet counts
maximum waves, dispatches, and workgroups per packet
alias, overwrite, epoch, missing, duplicate, and reorder counters
reuse markers
receipt digest
```

Per-receipt closure:

```text
scheduled waves == encoded spans == submitted spans == completed spans
planned packets == encoders == command buffers == submits == completion polls
maximum in-flight packets <= 1
queue ahead == 0
next packet before completion == 0
```

A one-wave tail may have zero local reduction. Reduction authority is the full session aggregate.

## Session reduction

```text
submit reduction ratio = 1 - total packet submits / total parent waves
poll reduction ratio   = 1 - total packet polls / total parent waves
```

Both aggregate ratios must be at least 0.50.

With four waves per packet and no tail loss, the expected topology is:

```text
waves       72864
packets     18216
encoders    18216
submits     18216
polls       18216
```

The exact packet count is not hardcoded.

## Parent reconciliation

The R3-R3-R1 runtime artifact remains immutable and supplies the before-optimization wave, submit, and poll baseline. The R4-R1 artifact remains the executor-sourced topology baseline.

Required:

```text
child wave count == parent wave count
child submit count < parent submit count
child poll count < parent poll count
```

Parent and child submit counts are intentionally not equal:

```text
parent submit count = one submit per wave baseline
child submit count  = one submit per packet runtime truth
```

## Authority preservation

```text
BufferAtlas reference remains production authority
Texture candidate remains shadow-only
candidate output commit count == 0
production authority mutation count == 0
physical executor switch count == 0
```

Wave packetization must not change wave coverage, wave order, per-wave dispatch order, streaming-softmax merge order, finalize placement, or device-compare parity.

## Files

```text
crates/burn_webgpu_backend/src/
  headwise_texture_05_r3_r3_r2_packetization.rs
  headwise_gqa4_live_shadow_dispatch.rs
  lib.rs

crates/orchestrator_local/src/bin/
  ash_attn_headwise_texture_05_gate.rs
  ash_attn_headwise_texture_05_r3_r3_r2_gate.rs
  ash_attn_headwise_texture_05_r4_r1_gate.rs

crates/orchestrator_local/src/
  headwise_texture_05_r3_r3_r2_cli_registry.rs

crates/orchestrator_local/Cargo.toml
specs/cli/ash_attn_headwise_texture_05_r3_r3_r2.args
```

## Runtime artifacts

```text
workspace/runtime/attention/headwise/texture/
  ash_attn_headwise_texture_05_r3_r3_r2_runtime_artifact.json
  ash_attn_headwise_texture_05_r3_r3_r2_local_manifest.json
  ash_attn_headwise_texture_05_r3_r3_r2_verification_runtime_artifact.json
  ash_attn_headwise_texture_05_r3_r3_r2_verification_local_manifest.json
```

Child receipts are written under the configured Texture-05 output directory in `r3_r3_r2/`.

## Execution

Physical gate first:

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_texture_05_gate `
  -- "@specs/cli/ash_attn_headwise_texture_05.args"
```

Verification gate second:

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_texture_05_r3_r3_r2_gate `
  -- "@specs/cli/ash_attn_headwise_texture_05_r3_r3_r2.args"
```

Expected token:

```text
PASS_ASH_ATTN_HEADWISE_TEXTURE_05_R3_R3_R2_EXISTING_HEADWISE_ROUND_REUSE_SEQUENTIAL_WAVE_PACKETIZATION_SEALED
```

## Completion gate

```text
Parent R3-R3-R1 artifact verified                    PASS
Parent R4-R1 artifact verified                       PASS
Headwise encode-only ownership reused                PASS
Headwise single-encoder round reused                 PASS
Submitted-span promotion pattern reused              PASS
TensorCube ordered multi-pass pattern reused         PASS
Independent packet executor introduced == false      PASS
Parent and child wave counts equal                   PASS
Missing, duplicate, and reordered waves == 0         PASS
Packet count == encoder count                        PASS
Packet count == command-buffer count                 PASS
Packet count == submit count                         PASS
Packet count == completion-poll count                PASS
Maximum in-flight packets <= 1                       PASS
Queue-ahead packets == 0                             PASS
Next packet before completion == 0                   PASS
All packet ceilings                                  PASS
Descriptor alias, overwrite, and epoch mismatch == 0 PASS
Aggregate submit reduction >= 0.50                   PASS
Aggregate poll reduction >= 0.50                     PASS
Production and output authority unchanged            PASS
Existing latency, residency, quarantine, and promotion gates remain valid PASS
```

## Follow-up

```text
ASH-ATTN-HEADWISE-TEXTURE-05-R3-R3-R3

Persistent Wave Descriptor Arena /
Dynamic Offset Parameter Binding /
Bind Group Reuse /
Depth-One Prepared Packet /
Packed Uniform and Storage Ring /
Zero Per-Wave Resource Creation /
Fence-Gated Descriptor Reuse Seal
```

R3-R3-R2 amortizes encoder, submit, and completion boundaries. R3-R3-R3 removes the remaining per-wave parameter and bind-group construction cost.