# TENSORCUBE-TABLE-R4B-CF1

## DEVICE-HOT OPTIMIZER PAGE BINDING
## + GPU ACCUMULATOR DIRECT ADAMW CONSUMPTION
## + DIRTY M/V GPU→RAM CIRCULATION AUTHORITY

## 0. Revision

Patch ID: TENSORCUBE-TABLE-R4B-CF1

Canonical name:
ASH-BASETRAIN-TENSORCUBE-TABLE-R4B-CF1-
DEVICE-HOT-OPTIMIZER-PAGE-
GPU-ACCUMULATOR-DIRECT-ADAMW-
DIRTY-MV-RAM-CIRCULATION

Direct parent:
TENSORCUBE-TABLE-R4B
GENERATION-RESIDENT TRAINING STATE TABLE

Preserved parents:
- R6A-R1 GPU accumulation8
- RAM-resident Adam M/V
- AdamW ActiveDevice candidate backend
- AdamW pending generation scheduler
- MCU Eve R3A / R3G exact Adam source lease
- MCU Eve R3B bounded RAM writeback circulation
- MCU SESSION R7 / R7A
- A01 SubmissionEpoch
- R3C / R3C1 generation commit

No Adam math, accumulation math, optimizer routing, B06, BP-DK or generation commit semantics are changed.

## 1. Source-truth correction

The earlier planning draft described a three-slot device-hot optimizer page window. Current production source has two distinct parent topologies:

- legacy RAM-MV PCIe overlap path = 3 transfer slots
- canonical ActiveDevice Adam path = bounded pending scheduler + R3B two-slot bounded M/V writeback staging

R4B-CF1 adopts the existing canonical ActiveDevice topology. It does not reintroduce the legacy three-slot ring simply to match a draft diagram.

Canonical path:

R6 GPU accumulator
→ exact GPU gradient segment lease
→ Eve/R3A/R3G Adam source authority
→ ActiveDevice source W/M/V on GPU
→ bounded pending AdamW GPU execution
→ GPU candidate W/M/V
→ R3B bounded candidate M/V GPU→RAM circulation
→ Eve CandidateComplete
→ R3C/R3C1 commit authority

## 2. Core authority law

After admitted CF1:

full Adam M/V semantic run-local authority = RAM

active Adam execution state = bounded GPU DeviceHot segments

candidate Adam M/V = GPU first, then bounded exact RAM candidate circulation

full Adam M/V permanent VRAM residency = false

Runtime must distinguish:

opt_state_execution_on_gpu = true
full_opt_state_on_gpu = false

## 3. Materialized source authority

New module:

crates/base_train/src/tensorcube_table_r4b_cf1_device_hot_optimizer_page.rs

Materialized constants:

TENSORCUBE_TABLE_R4B_CF1_DEVICE_HOT_ADAM_MV_MATERIALIZED = true
TENSORCUBE_TABLE_R4B_CF1_GPU_ACCUMULATOR_DIRECT_ADAMW_BINDING_MATERIALIZED = true
TENSORCUBE_TABLE_R4B_CF1_ADAMW_ROUTE_TABLE_MATERIALIZED = true
TENSORCUBE_TABLE_R4B_CF1_FULL_ADAM_MV_GPU_RESIDENCY = false

Historical R4B parent constants are not rewritten.

## 4. R4B parent binding

CF1 extends the existing generation-lifetime R4B runtime. It does not create another generation owner.

CF1 may be enabled only when R4B is enabled.

The child runtime opens at source generation G / optimizer step S and rebinds after each canonical commit G→G+1, S→S+1.

## 5. Real GPU accumulator binding

CF1 binds the existing real R6DeviceAccumulatorReceipt.

Required:
- microbatch_count = 8
- accumulator_dtype = F32
- production_gradient_payload_readback_count = 0
- full_gradient_host_materialization_count = 0

No second accumulator is created.

## 6. Direct gradient-to-Adam binding

The canonical ActiveDevice Adam scheduler consumes the existing GPU gradient lease supplied by production accumulation.

CF1 records that exact lineage and forbids a GPU→CPU→GPU gradient roundtrip.

## 7. Adam route execution table

CF1 binds AdamWPendingGenerationSchedulerReceiptR1 beneath the R4B generation directory.

Required:
- submitted segment count > 0
- submitted == collected
- real SubmissionEpoch count == submitted
- final pending segment count = 0
- final active source reader count = 0
- generation complete = true
- ordinary exact wait count = 0
- legacy host source submit count = 0
- host candidate Vec materialization count = 0

## 8. DeviceHot source M/V meaning

The ActiveDevice producer binds exact GPU source allocations for Weight G, Adam M_G and Adam V_G.

These bytes originate from the existing Eve/RAM Adam authority and are projected into bounded GPU execution resources under exact generation/range identity.

DeviceHot therefore means segment-bounded optimizer execution residency, not full-pack VRAM residency.

## 9. Candidate GPU state

ActiveDevice produces Weight G+1, M_G+1 and V_G+1 on GPU with exact physical allocation identity and real SubmissionEpoch evidence.

Normal producer transfer evidence preserves:
- candidate weight full D2H = 0
- candidate M full D2H in producer = 0
- candidate V full D2H in producer = 0
- host candidate Vec materialization = 0
- ordinary exact wait = 0

## 10. Dirty M/V RAM circulation

CF1 binds McuEveAdamWritebackCandidateCompleteReceiptR3B.

R3B remains the canonical bounded candidate M/V return path.

Required:
- candidate_weight_d2h_bytes = 0
- full_candidate_m_host_vec_count = 0
- full_candidate_v_host_vec_count = 0
- Adam disk read bytes = 0
- Adam disk write bytes = 0
- final active staging submissions = 0
- final mapped staging slots = 0
- candidate_complete = true
- commit_permit_ready = true
- commit_performed = false

Candidate M/V bounded D2H is explicitly recorded and is not mislabeled as zero-PCIe execution.

## 11. RAM authority preserved

Full run-local Adam M/V SSOT remains RAM.

The GPU is the optimizer execution tier, not a replacement full-state semantic store.

## 12. No disk optimizer hot path

Under admitted R3B/RAM Adam execution:
ordinary Adam disk read bytes = 0
ordinary Adam disk write bytes = 0

No silent disk-backed optimizer fallback.

## 13. Current canonical geometry

Current source topology:
- ActiveDevice pending scheduler default max in flight = 4
- R3B bounded M/V writeback staging slots = 2

The historical RAM-MV overlap three-slot ring remains a separate compatibility/alternative path.

## 14. Activation

First physical qualification:

ASH_TENSORCUBE_TABLE_R4B_MODE=OBSERVE_ONLY
ASH_TENSORCUBE_TABLE_R4B_CF1_MODE=OBSERVE_ONLY

CF1 ActiveVerified requires all of:
- R4B enabled
- HybridDeviceCommit ActiveVerified
- R3A admitted
- R3B admitted
- RAM Adam present
- real ActiveDevice scheduler receipt
- real R3B CandidateComplete receipt

## 15. Full-route boundary

CF1 closes the AdamW route half of R4B optimizer residency.

It does not claim the final unified AdamW + HiMuon full-route training row table.

Terminal HOLD:
HOLD_TENSORCUBE_TABLE_R4B_CF1_FULL_ROUTE_TRAINING_ROW_TABLE_NOT_YET_CLOSED

## 16. Runtime receipt

Output:
tensorcube_table_r4b_cf1_device_hot_optimizer_page_receipt.json

Runtime log:
[ASH-TENSORCUBE-TABLE-R4B-CF1][optimizer-hot-state]

The receipt distinguishes opt_state_execution_on_gpu from full_opt_state_on_gpu and records actual segment, SubmissionEpoch, D2H, disk-I/O and admission evidence.

## 17. Static qualification

Validator:
tools/validate_ash_tensorcube_table_r4b_cf1_device_hot_optimizer_page_static.py

Current:
77 / 77 PASS

Parent regression retained:
- R4B 58/58 PASS
- R4A-CF2-CF1 90/90 PASS
- R4A-CF2 40/40 PASS
- R4A-CF1 90/90 PASS
- R4A 66/66 PASS
- ActiveDevice AdamW backend PASS
- ActiveDevice pending scheduler PASS
- MCU Eve R3B PASS
- MCU SESSION R7 55/55 PASS

Known code-only parent baselines remain unchanged:
- RAM Adam PCIe validator stops at missing compile-chain prerequisite
- R7A1 packed-gradient validator = 77/82

## 18. Implementation delta

Compared with supplied R4B full code-only parent:

MOD 2
ADD 2
DEL 0

Modified:
- crates/base_train/src/lib.rs
- crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs

Added:
- crates/base_train/src/tensorcube_table_r4b_cf1_device_hot_optimizer_page.rs
- tools/validate_ash_tensorcube_table_r4b_cf1_device_hot_optimizer_page_static.py

## 19. Artifact seal

Overlay ZIP
SHA-256 e5cc21bc96925c7af0c8d55ca6e30aecc2ef42f3706eac90198769499c8564be
files 4
CRC PASS

Full code-only ZIP
SHA-256 6cf0c4902b5df4ece54d793543adfded823798eb8670ccd1bff591f65b40d1fe
files 8,501
CRC PASS

## 20. Evidence boundary

SOURCE PASS
STATIC PASS
ARCHIVE PASS
COMPILE NOT RUN
RUNTIME NOT RUN
PHYSICAL NOT RUN
PERFORMANCE UNMEASURED
PROMOTED NO

The bake environment has no cargo/rustc/WGPU execution toolchain.

## 21. Compile acceptance

cargo test -p base_train --lib tensorcube_table_r4b_cf1_ --release --locked
cargo test -p base_train --lib tensorcube_table_r4b_ --release --locked
cargo test -p base_train --lib unified_atlas_mcu_adamw_active_device_ --release --locked
cargo test -p base_train --lib unified_atlas_mcu_eve_adamw_ --release --locked
cargo build -p base_train --bin base_train --release --locked

## 22. First physical qualification

Required:
- observed_optimizer_step_count > 0
- unbound_optimizer_step_count = 0
- optimizer_state_execution_on_gpu = true
- full_optimizer_state_gpu_residency = false
- AdamW submitted segment count > 0
- real SubmissionEpoch count == submitted segment count
- ordinary exact wait count = 0
- legacy host source submit count = 0
- gradient payload readback = 0
- host candidate Vec materialization = 0
- R3B candidate weight D2H = 0
- R3B candidate M/V bounded D2H > 0 for AdamW-owned ranges
- Adam ordinary disk read/write bytes = 0
- R3B candidate complete = true
- R3B commit permit ready = true

## 23. Performance boundary

CF1 does not claim guaranteed PCIe/compute overlap.

Measure optimizer wall time, pending peak, max in-flight segments, GPU idle gap, R3B M/V writeback time, host wait time and candidate M/V D2H.

## 24. Direct successor

TENSORCUBE-TABLE-R4B-CF2

FULL ROUTE TRAINING ROW TABLE
+ ADAMW / HIMUON UNIFIED GENERATION VIEW
+ WEIGHT / GRADIENT / OPTIMIZER RESIDENCY MATRIX
+ SINGLE PARAMETER COMPLETION PLANE
+ GENERATION COMMIT-READY TABLE

## 25. Final law

R4B established one generation-lifetime training-state directory and bound the real GPU accumulation8 authority.

R4B-CF1 binds the existing canonical ActiveDevice Adam path into that directory. The exact AdamW-owned source M/V segment lives on GPU while AdamW executes, the accumulated gradient is consumed without payload D2H, candidate Weight/M/V are produced on GPU, and R3B returns candidate M/V to the canonical RAM Adam authority in bounded windows.

Full Adam M/V does not become permanently VRAM-resident. DeviceHot is an execution tier, RAM remains the full run-local optimizer-state semantic authority, and disk remains outside the ordinary optimizer hot path.
