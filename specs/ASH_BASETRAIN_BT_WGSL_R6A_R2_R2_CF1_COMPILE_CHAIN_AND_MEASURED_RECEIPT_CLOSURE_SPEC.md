# ASH-BASETRAIN-BT-WGSL-R6A-R2-R2-CF1-COMPILE-CHAIN-AND-MEASURED-RECEIPT-CLOSURE

## Revision / authority

- Patch: `ASH-BASETRAIN-BT-WGSL-R6A-R2-R2-CF1-COMPILE-CHAIN-AND-MEASURED-RECEIPT-CLOSURE`
- Build: `bt-wgsl-r6a-r2-r2-cf1-compile-chain-and-measured-receipt-closure`
- Code parent: Pass109 / `ASH-BASETRAIN-BT-WGSL-SUBGROUP32-TILED-SEGMENT-GRADIENT-ACCUMULATOR-AND-ADAMW-06C-R27-R1J-R6A-R2-R2`
- Physical parent authority remains: R5 committed generation3 / optimizer step3 / cursor-next3.
- Role: close Rust compile authority, physical WGSL/subgroup evidence, measured segment-gradient/AdamW receipts, parent validator succession, and archive identity before N=2 physical promotion.
- Training math change: forbidden.
- AdamW formula change: forbidden.
- Accumulation8 semantic change: forbidden.
- 16 MiB gradient page policy change: forbidden.
- Long-horizon production promotion: CLOSED.

## 1. Compile-chain closure

R2-R2 may no longer be promoted from static source checks alone.

Required chain:

```text
source static validators
    -> cargo fmt --check
    -> cargo check base_train
    -> cargo check structural gate
    -> targeted CF1 Rust tests
    -> cargo build base_train
    -> authoritative binary SHA256
    -> runtime binary SHA256 exact match
```

The compile-chain receipt schema is `ash.basetrain.r6a_r2_r2_cf1.compile_receipt.v1`.

A physical runtime invocation without `--r6a-r2-r2-cf1-compile-receipt` is rejected.

## 2. Gradient observation cursor repair

`observe_accumulated_gradients()` owns one monotonic observation cursor named `offset`.

The stale undefined assignment is retired. Each chunk advances only through checked arithmetic:

```text
offset <- offset + count
```

Required invariants:

- zero-progress chunk count = 0;
- expected observed elements = actual observed elements;
- final cursor covers the exact finalized gradient segment length;
- no full gradient payload host materialization is introduced.

## 3. Physical subgroup observation

Subgroup size is no longer a host literal pretending to be runtime evidence.

CF1 creates a physical WGPU subgroup probe on the same production device/queue lineage and reads one compact u32 observation produced from WGSL `@builtin(subgroup_size)`.

Required:

```text
required subgroup size = 32
observed subgroup size = 32
subgroup mismatch count = 0
payload readback count = 0
```

Gradient and AdamW production kernels retain their own subgroup-size fail-closed status paths. A device subgroup mismatch cannot silently return a successful terminal receipt.

## 4. Measured segment accumulator authority

`R6DeviceGradientAccumulator` owns the segment allocation telemetry.

Measured fields include gradient segment count, segment buffer creation count, maximum segment bytes/elements, malformed overlap/duplicate counters, full-parameter gradient route counters, full LM-head / embedding route counters, oversized page allocation attempts, cross-page merge, lane merge, and shader-module/pipeline creation counts.

The successful R2-R2 path requires:

```text
max gradient segment bytes <= 16 MiB
full parameter gradient buffer create count = 0
full LM-head gradient buffer create count = 0
full embedding gradient buffer create count = 0
oversized gradient buffer create attempts = 0
cross-page merge count = 0
microbatch lane merge count = 0
```

Eight lanes remain eight independent `batch_size=1` authorities.

## 5. Measured AdamW/readback authority

Every segment AdamW dispatch reports the actual output movement it performed.

The candidate receipt records AdamW segment dispatch count, implicit zero-gradient gap dispatch count, maximum AdamW segment bytes, candidate weight/M/V readback count and bytes, optimizer compact status readback, and shader module/pipeline creation counts.

Gradient payload readback remains prohibited:

```text
gradient payload readback count = 0
gradient payload readback bytes = 0
```

Candidate readback is not falsely reported as zero. Current crash-safe packed persistence is allowed to read candidate weight/M/V to host staging, and CF1 records the actual count and bytes.

## 6. No hardcoded runtime evidence

Policy constants and runtime observations are separate authorities.

Allowed policy constants include required subgroup size 32, gradient page budget 16 MiB, logical tile 256 elements, and eight elements per subgroup lane.

Forbidden terminal construction includes patterns equivalent to:

```text
observed subgroup size = 32 literal
full parameter gradient buffer count = 0 literal
oversized allocation attempt count = 0 literal
candidate readback count = guessed/theoretical value
```

Terminal R2-R2 receipt values are aggregated from the subgroup probe, accumulator receipt, AdamW I/O receipt, and observation receipt.

## 7. R2-R2 structural contract adoption

CF1 adds an explicit 104-gate structural contract:

```text
--require-bt-wgsl-r27r1j-r6a-r2-r2-contract-001=true
...
--require-bt-wgsl-r27r1j-r6a-r2-r2-contract-104=true
```

The structural bridge is appended after R6A-R2-R1 and remains honest about physical state:

```text
physical compile receipt observed = false
physical measured receipt observed = false
long-horizon training admitted = false
```

Structural readiness does not fabricate physical execution.

## 8. Parent validator semantic rebase

R6 through R2-R1 validators are rebased to current child semantics without restoring stale source spelling.

- legacy workgroup-64 exact-string checks no longer override subgroup32 tiled execution;
- current AdamW bias-correction expression is accepted semantically;
- current decoupled weight-decay expression is accepted semantically;
- terminal-child expectations advance to CF1;
- parent training/storage semantics remain unchanged.

Static chain after CF1 bake:

```text
R6       108/108 PASS
R6A      122/122 PASS
R6A-R1   114/114 PASS
R6A-R2    92/92 PASS
R2-R1    118/118 PASS
R2-R2      36/36 PASS
CF1        80/80 PASS
```

These are static/structural results only. They are not substitutes for physical Cargo/WGPU execution.

## 9. Compile authority tool

New tool: `tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1`.

It runs all six parent validators plus CF1, validates the exact 104 structural-gate sequence, runs Cargo fmt/check/targeted tests/build, binds the generated base_train `Cargo.lock` separately by SHA256, hashes the authoritative debug `base_train` binary, and emits the compile receipt as UTF-8 without BOM.

The baked source-tree digest deliberately excludes generated `Cargo.lock`; dependency resolution is a separate `cargoLockDigest` authority after Cargo creates or updates the lockfile.

## 10. Runtime binary identity

The physical production runtime computes SHA256 of its own current executable and requires exact equality with the compile receipt.

Forbidden:

```text
compile binary A
run binary B
reuse A receipt
```

## 11. PASS and HOLD

Parent R2-R2 PASS remains required:

`PASS_ASH_BASETRAIN_BT_WGSL_SUBGROUP32_TILED_SEGMENT_GRADIENT_ACCUMULATOR_AND_ADAMW_06C_R27_R1J_R6A_R2_R2`

CF1 PASS:

`PASS_ASH_BASETRAIN_BT_WGSL_R6A_R2_R2_CF1_COMPILE_CHAIN_AND_MEASURED_RECEIPT_CLOSURE`

CF1 terminal HOLD:

`HOLD_ASH_BASETRAIN_R1J_R6A_R2_R2_CF1_COMPILE_AND_MEASURED_EVIDENCE_CLOSED_PHYSICAL_N2_PROMOTION_NOT_YET_ADMITTED`

An exit code 1 caused only by the terminal HOLD after the complete PASS chain is intended.

## 12. PASS meaning

CF1 PASS establishes that the actual executable which entered the R2-R2 production path was built through the approved compile chain, matches the compile receipt by binary SHA256, successfully created the required physical WGPU subgroup/module/pipeline path, observed subgroup32 on the production device lineage, traversed finalized gradient observations with exact cursor coverage, used bounded segmented gradient allocation without whole-parameter gradient buffers, executed segment AdamW, kept gradient payload readback at zero, and reported candidate weight/M/V readback from measured runtime counters rather than constants.

## 13. Not proven

CF1 does not prove generation3 -> generation5 N=2 physical promotion, long-horizon stability or convergence, training-quality improvement, asynchronous candidate persistence, pipeline-cache optimization, decoder segment-native matmul, R6 packed fresh resume, epoch/shuffle, periodic checkpoint retention, or distributed/cross-device determinism.

## 14. Code archive identity / bake policy

Baked source-tree identity excluding generated lockfile:

`fcbfa5c571e18041645bda95f8cc0312a395f1cbc9a77346213f34a056000ac7`

Overlay archive:

- filename: `ash_overlay_ASH-BASETRAIN-BT-WGSL-R6A-R2-R2-CF1-COMPILE-CHAIN-AND-MEASURED-RECEIPT-CLOSURE_code.zip`
- SHA256: `230191bafa9aa809cd0cd961840b1ed01726c7fd5200dbee32153f32832b5f84`
- changed/new source files: 19

Full code archive:

- filename: `ash_pass110_ASH-BASETRAIN-BT-WGSL-R6A-R2-R2-CF1-COMPILE-CHAIN-AND-MEASURED-RECEIPT-CLOSURE_code_baked.zip`
- SHA256: `068c208e4d5789dd40d5a7e4891f1c4fd021348e9c73afea0441d2fe59059f09`

Archive policy for both ZIPs:

- generated artifacts excluded;
- manifest directories/files excluded;
- Markdown reports/spec copies excluded;
- debug/handoff `.txt` files excluded;
- `*.sha256` sidecar files excluded;
- generated Cargo targets/cache excluded.

The authoritative CF1 specification lives in GitHub, not as a duplicated Markdown payload in the code archive.

## 15. Authoring-environment evidence boundary

The code bake environment used for this revision did not contain `cargo`/`rustc` or a physical WGPU device. Therefore no physical Cargo or GPU PASS is claimed by the bake itself.

The bake establishes the code path and static closure. Physical promotion begins only after the supplied compile-chain tool emits a valid compile receipt on the operator machine and the exact resulting binary consumes that receipt.

## SSOT seal

```text
EXPECTED != OBSERVED

POLICY:
required subgroup = 32
page budget = 16 MiB
logical tile = 256

PHYSICAL EVIDENCE:
compile exact source
bind exact binary
create WGSL module/pipeline
observe subgroup
measure segment allocation
measure AdamW/readback
validate receipts
then PASS

NO HARDCODED OBSERVED 32
NO HARDCODED ZERO COUNTERS
NO STRING-ONLY PROMOTION
NO GRADIENT PAYLOAD READBACK
NO WHOLE-PARAMETER GRADIENT BUFFER
NO SILENT PARENT VALIDATOR DOWNGRADE
```