# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R1

## Manifest Atlas Parallel Group Map /
## Bounded Serde JSON Construction /
## Duplicate-Key Fail-Closed Merge /
## Macro Recursion Compile Closure Seal

---

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R1
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3
runtime_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3
manifest_builder_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R1
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.runtime_artifact.v1
manifest_schema=ash.attn.headwise.causal.01b.r12.r3.r3.local_manifest.v1
```

R12-R3-R3-R1 is a compile-closure revision. It does not change attention kernels, route LUT policy, crossover probes, guard math, performance thresholds, artifact filenames, or the flat manifest artifact lookup ABI.

---

## 1. Failure binding

Observed compiler failure:

```text
error: recursion limit reached while expanding `$crate::json_internal!`
source=ash_attn_headwise_causal_01b_r12_r3_r3_gate.rs
site=local manifest json! construction
```

The failure occurs before runtime execution. No R12-R3-R3 runtime artifact or manifest may be treated as authoritative from the failed build.

---

## 2. Prohibited workaround

R12-R3-R3-R1 must not solve the failure only by adding:

```rust
#![recursion_limit = "256"]
```

Increasing macro recursion depth hides an unbounded construction shape and keeps compile cost coupled to artifact count.

Required:

```text
crate recursion-limit override required=false
single deeply nested manifest json macro=false
```

---

## 3. Manifest construction SSOT

Manifest artifacts are assembled through six bounded group maps:

```text
binding
  parent binding
  scope snapshot
  promotion policy

guard
  guard policy
  micro-atlas topology
  bucket-verdict truth
  ring policy and creation
  allocation, submission, poll and overhead summaries

execution
  candidate transitions
  guard dispatch and validation
  authority commits
  fault injection
  positive, canary and rollback receipts

measurement
  measurement plan
  round receipts
  performance catalog

route_probe
  probe policy and catalogs
  crossover boundary
  route LUT
  route replay
  1024 tail closure

verification
  negative-control evidence
  static checks
  claim boundary
  verdict
```

Canonical counts:

```text
artifact_group_count=6
artifact_count=37
```

---

## 4. Flat manifest ABI preservation

The public manifest retains:

```json
{
  "artifacts": {
    "parent_binding": {"path": "...", "sha256": "..."},
    "performance_catalog": {"path": "...", "sha256": "..."}
  }
}
```

Consumers do not need to traverse group nesting.

The new `artifact_groups` field is evidence metadata only:

```json
{
  "artifact_group_count": 6,
  "artifact_groups": {
    "binding": {"artifact_count": 3, "group_digest": "..."},
    "guard": {"artifact_count": 9, "group_digest": "..."}
  }
}
```

---

## 5. Group merge contract

Each artifact entry is created by `insert_manifest_artifact`.

Each group is merged by `merge_manifest_artifact_group`.

Required fail-closed conditions:

```text
duplicate key inside one group -> error
duplicate key across groups -> error
duplicate group ID -> error
artifact group count != 6 -> error
artifact count != 37 -> error
```

No later group may silently overwrite an earlier artifact entry.

---

## 6. Digest contract

Every group records a deterministic digest over its complete JSON object before merge.

```text
group_digest = SHA-256(serde_json(group_map))
```

The final manifest continues to record every artifact path and SHA-256 digest individually.

Group digests do not replace individual artifact digests.

---

## 7. Runtime truth boundary

Unchanged:

```text
route LUT=1..1023 single / 1024.. GQA2 tiled
micro-atlas group count=8
device decision token authority=true
hot-path host wait count=0
output value readback count=0
negative-control target count=580
performance thresholds unchanged
```

R12-R3-R3-R1 proves only bounded manifest construction and compile closure. Runtime promotion still requires the complete R12-R3-R3 gate to execute and PASS.

---

## 8. Required source changes

```text
crates/orchestrator_local/src/bin/
  ash_attn_headwise_causal_01b_r12_r3_r3_gate.rs

specs/
  ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R1_SPEC.md
```

Required code symbols:

```text
MANIFEST_BUILDER_REVISION
relative_manifest_path
insert_manifest_artifact
merge_manifest_artifact_group
artifact_groups
```

---

## 9. Static checks

Required:

```text
manifest_atlas_parallel_group_map=true
manifest_builder_revision exact
manifest group count assertion exists
manifest artifact count assertion exists
duplicate-within-group assertion exists
duplicate-across-groups assertion exists
duplicate-group assertion exists
flat artifacts object exists
```

---

## 10. Canonical run

The binary and CLI remain unchanged:

```powershell
$env:CARGO_TARGET_DIR="target-ash-attn-01b-r12-r3-r3"

cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_r12_r3_r3_gate `
  -- `
  --repo-root . `
  --parent-artifact workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r2_runtime_artifact.json `
  --parent-manifest workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r2_local_manifest.json `
  --runtime-profile specs/runtime_profile_v5_48259.toml `
  --verdict-scope incremental-only `
  --promote-full-prefill false `
  --promote-incremental-decode true `
  --promote-chunked-decode false `
  --require-same-device true `
  --require-qkv-zero-copy true `
  --require-output-zero-copy true `
  --forbid-output-value-readback true `
  --forbid-output-host-upload true `
  --route-policy deterministic-bucket-lut `
  --probe-kernels single-query-head,gqa2-long-kv-tiled `
  --probe-buckets 512,768,896,1024,1152,1280,1536,2048 `
  --require-1024-gqa2-admission true `
  --require-monotonic-crossover true `
  --require-stable-crossover-neighbors true `
  --require-legacy-threshold-unreachable true `
  --route-replay-count 100 `
  --guard-mode device-native-micro-atlas-token `
  --guard-map-mode headwise-micro-atlas `
  --guard-map-group-count 8 `
  --guard-map-heads-per-group 4 `
  --guard-map-dimensions-per-head 64 `
  --guard-map-workgroup-size 64 `
  --guard-map-values-per-lane 4 `
  --guard-finalizer-workgroup-size 32 `
  --decision-token-ring-capacity 4 `
  --telemetry-ring-capacity 4096 `
  --require-device-native-decision true `
  --require-gpu-gated-o-proj true `
  --require-gpu-gated-residual true `
  --require-zero-hot-path-host-wait true `
  --require-async-telemetry-drain true `
  --require-zero-per-element-global-atomics true `
  --performance-mode paired-gpu-timestamp `
  --warmup-iterations 128 `
  --measurement-pairs 1024 `
  --measurement-rounds 32 `
  --internal-canary-prefills 0 `
  --internal-canary-decode-steps 1024 `
  --fault-injection true `
  --require-rollback true `
  --negative-control-mode executed `
  --minimum-live-negative-controls 40 `
  --expected-negative-controls 580 `
  --require-rollback-anchor true `
  --require-authority-commit-order true `
  --full-source-hash true `
  --out-dir workspace/runtime/attention
```
