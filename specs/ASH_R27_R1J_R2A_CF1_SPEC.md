# R27-R1J-R2A-CF1

## V5 GENESIS SKELETON STRUCTURAL FILL

Patch class: fresh-genesis structural initialization authority.

Parent blocker: BTR27R1JR2ACurrentV5ZeroPatternCanaryMismatch.

Physical source observation:
- layer 20 projection frontier: 6 zero / 1 nonzero
- layer 20 RMS: 1 nonzero / 1 zero
- layer 21 projection frontier: 7 zero / 0 nonzero
- layer 21 RMS: 0 nonzero / 2 zero

The projection frontier already matches the current V5 contract. The input ash_v5_native_genesis_full.safetensors is a skeleton, not a fully structurally initialized training genesis.

## Authority

- Source skeleton is read-only.
- A distinct ash_v5_native_genesis_structural_filled.safetensors target is published.
- Only all-zero decoder RMS gamma tensors and all-zero model.norm.weight are mutation candidates.
- Existing nonzero RMS payloads are byte preserved.
- Projection, embedding, and LM-head payloads are outside mutation authority.
- No forward, backward, optimizer step, cursor movement, or RNG initialization occurs.

## Model admission

- modelSpecId must equal model_tinyllama_1p1b_v5_48259.
- decoder layer count must equal 22.
- All 44 decoder RMS keys are required.
- model.norm.weight is required.
- model.embed_tokens.weight is required.
- lm_head.weight is required for untied embeddings.

## RMS fill

All-zero RMS payloads are written with canonical dtype-specific one values:
- F32: 0x3f800000
- F16: 0x3c00
- BF16: 0x3f80

Dtype and shape are preserved. A nonzero RMS tensor with nonfinite values fails closed instead of being overwritten.

## Projection preservation

All 154 decoder projection tensors are write-forbidden.

Layer 20 exact role vector:
- Q ZERO
- K ZERO
- V ZERO
- O ZERO
- GATE ZERO
- UP ZERO
- DOWN NONZERO

Layer 21 exact role vector:
- Q ZERO
- K ZERO
- V ZERO
- O ZERO
- GATE ZERO
- UP ZERO
- DOWN ZERO

The exact role vectors must match before and after fill.

## Physical parity

The implementation first performs a byte-exact source-to-staging copy, then writes only admitted RMS ranges. After mutation it physically compares every non-mutated tensor payload between source and target.

Admission requires nonAllowlistParityMismatchCount == 0.

The source SHA is recalculated after fill and must remain unchanged. The safetensors header digest and tensor descriptors must remain exact.

## R2A canary preservation

The existing production_atlas_plan_materialization.rs gate remains unchanged and strict:
- L20 projection zero == 6
- L20 projection nonzero == 1
- L21 projection zero == 7
- L21 projection nonzero == 0
- L20 RMS nonzero == 2
- L21 RMS nonzero == 2

BTR27R1JR2ACurrentV5ZeroPatternCanaryMismatch is not disabled or weakened.

## Lineage rebuild handoff

tools/run_r27r1j_training_lineage_rebuild.ps1 now executes:
source skeleton -> V5_STRUCTURAL_FILL -> filled genesis -> R2A atlas plan materialization -> R2E/R3 training lineage.

R2A plan materialization and the initial R2E training invocation use the filled genesis, not the skeleton.

The recovery anchor preserves both GENESIS_SKELETON_SOURCE_POINTER.json and GENESIS_POINTER.json.

## Changed files

- ADD crates/base_train/src/v5_genesis_skeleton_structural_fill_r1.rs
- MOD crates/base_train/src/bin/base_train.rs
- MOD crates/base_train/src/lib.rs
- MOD tools/run_r27r1j_training_lineage_rebuild.ps1
- ADD tools/validate_ash_r27_r1j_r2a_cf1_v5_genesis_structural_fill_static.py

## Source SHA-256

- afd9384d4eb0bc0f83176a8234d409dbc37c6423170e586a1b652c34898414b4  crates/base_train/src/v5_genesis_skeleton_structural_fill_r1.rs
- fe54c5a4766a396ea0e91ef9ce9ae1c13cd9de1695acc812e5a219c1399afffa  crates/base_train/src/bin/base_train.rs
- b355ec39d0099bf119dbc7ad92327dc46803a98b7e21a11aaa07b19e8577bc29  crates/base_train/src/lib.rs
- b91baa1e68c7371dd964c29d4de1b721a9ea75017932bab48b6933238e78885f  tools/run_r27r1j_training_lineage_rebuild.ps1
- 9db2430256cf544b4c7d7f6bea437b547d51821a600c4bd035fce17850d2ce7b  tools/validate_ash_r27_r1j_r2a_cf1_v5_genesis_structural_fill_static.py

## Static qualification

- Structural-fill static: 44/44 PASS.
- Existing lineage rebuild static: 86/86 PASS.
- TensorCube R3-CF1 production callsite static: 51 PASS.
- Python validator compile: PASS.
- Changed Rust delimiter inventory: balanced.

Evidence boundary for this bake:
- SOURCE PASS
- STATIC PASS
- COMPILE NOT RUN
- RUNTIME NOT RUN
- PHYSICAL NOT RUN
- R2A CANARY PHYSICAL NOT RUN
- LINEAGE HANDOFF PHYSICAL NOT RUN
- PROMOTED NO

## Artifacts

Overlay:
- ASH_R27_R1J_R2A_CF1_V5_GENESIS_STRUCTURAL_FILL_OVERLAY_CODE_ONLY.zip
- SHA-256 ac2801d580388e515072f4c075680a083546ed83b0dc2c2a5cfacd90fd2536d3
- FILES 5
- CRC PASS

Full:
- ASH_PASS3_R27_R1J_R2A_CF1_V5_GENESIS_STRUCTURAL_FILL_CODE_ONLY.zip
- SHA-256 5b913a7c8257a766006f485ab3fa12c01b17a921718d421a63c134f032d45e95
- FILES 8481
- CRC PASS

## Physical acceptance

The first real fill must show:
- sourceUnchanged=true
- nonAllowlistParityMismatchCount=0
- projectionMutationCount=0
- embeddingMutationCount=0
- lmHeadMutationCount=0
- decoderRmsZeroAfter=0
- decoderRmsNonzeroAfter=44
- finalNormNonzeroAfter=true
- r2aCurrentV5CanaryPass=true
- admitted=true

Then the unchanged R2A materializer must accept the filled checkpoint and the canonical lineage rebuild must continue from it.

## Final law

The V5 skeleton remains immutable. CF1 initializes only structurally empty RMSNorm gamma state into a separately hashed target, preserves the intentional projection frontier byte-exactly, and rebinds canonical lineage rebuild to the filled genesis before any training step.