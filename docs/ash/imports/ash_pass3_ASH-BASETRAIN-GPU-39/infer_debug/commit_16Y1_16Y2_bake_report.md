# Commit 16Y-1/16Y-2 static validation

## 16Y-1 allocation probe hooks
903:            embedding: vec!["model.embed_tokens.weight".into(), "tok_embeddings.weight".into(), "embed_tokens.weight".into()],
904:            lm_head: vec!["lm_head.weight".into(), "output.weight".into()],
1009:        "[native-alloc-probe] tensor={} shape=[{}] dtype=F32 bytes={}",
1017:fn checkpoint_tensor_2d_named<B: Backend>(
1026:        "[native-alloc-probe] tensor={} shape=[{}, {}] dtype=F32 bytes={}",
1040:    checkpoint_tensor_2d_named::<B>("unnamed.2d", values, rows, cols, device)
1049:    let weight = checkpoint_tensor_2d_named::<B>(&target_key, &src.weight, src.out_dim, src.in_dim, device);
1111:        token_embedding: Param::from_tensor(checkpoint_tensor_2d_named::<B>(
1112:            "model.embed_tokens.weight",
1118:        lm_head: Param::from_tensor(checkpoint_tensor_2d_named::<B>(
1119:            "lm_head.weight",

## 16Y-2 projection mode hooks
crates/runtime/src/infer.rs:414:pub enum NativeVocabProjectionMode {
crates/runtime/src/infer.rs:421:impl Default for NativeVocabProjectionMode {
crates/runtime/src/infer.rs:425:impl NativeVocabProjectionMode {
crates/runtime/src/infer.rs:447:pub enum NativeEmbeddingMode {
crates/runtime/src/infer.rs:453:impl Default for NativeEmbeddingMode {
crates/runtime/src/infer.rs:457:impl NativeEmbeddingMode {
crates/runtime/src/infer.rs:516:        let effective_vocab_projection = match req.native_vocab_projection {
crates/runtime/src/infer.rs:517:            NativeVocabProjectionMode::Auto => {
crates/runtime/src/infer.rs:521:                    NativeVocabProjectionMode::GpuAtlas
crates/runtime/src/infer.rs:523:                    NativeVocabProjectionMode::GpuFull
crates/runtime/src/infer.rs:529:            NativeEmbeddingMode::Auto => {
crates/runtime/src/infer.rs:533:                    NativeEmbeddingMode::RowGather
crates/runtime/src/infer.rs:535:                    NativeEmbeddingMode::GpuFull
crates/runtime/src/infer.rs:541:            requested_vocab_projection: req.native_vocab_projection.as_str().to_string(),
crates/runtime/src/infer.rs:551:            gpu_full_vocab_upload_skipped: effective_vocab_projection == NativeVocabProjectionMode::GpuAtlas,
crates/runtime/src/infer.rs:581:    pub native_vocab_projection: NativeVocabProjectionMode,
crates/runtime/src/infer.rs:585:    pub native_embedding_mode: NativeEmbeddingMode,
crates/runtime/src/infer.rs:1063:    pub native_vocab_allocation_probe: NativeVocabAllocationProbe,
crates/runtime/src/infer.rs:2609:    let native_vocab_allocation_probe = NativeVocabAllocationProbe::new(
crates/runtime/src/infer.rs:2627:        native_vocab_allocation_probe.requested_vocab_projection,
crates/runtime/src/infer.rs:2628:        native_vocab_allocation_probe.effective_vocab_projection,
crates/runtime/src/infer.rs:2629:        native_vocab_allocation_probe.requested_embedding_mode,
crates/runtime/src/infer.rs:2630:        native_vocab_allocation_probe.effective_embedding_mode,
crates/runtime/src/infer.rs:2631:        native_vocab_allocation_probe.vocab_size,
crates/runtime/src/infer.rs:2632:        native_vocab_allocation_probe.hidden_size,
crates/runtime/src/infer.rs:2633:        native_vocab_allocation_probe.full_vocab_bytes,
crates/runtime/src/infer.rs:2634:        native_vocab_allocation_probe.vocab_tile_size,
crates/runtime/src/infer.rs:2635:        native_vocab_allocation_probe.avoid_full_vocab_gpu_upload,
crates/runtime/src/infer.rs:2636:        native_vocab_allocation_probe.max_single_gpu_buffer_bytes,
crates/runtime/src/infer.rs:2808:        native_vocab_allocation_probe,
crates/runtime/src/infer/request_resolution.rs:7:use super::{NativeEmbeddingMode, NativeVocabProjectionMode, QWaveInferenceHints, StandardInferRequest, SubtitleCueContext};
crates/runtime/src/infer/request_resolution.rs:54:    pub native_vocab_projection: NativeVocabProjectionMode,
crates/runtime/src/infer/request_resolution.rs:58:    pub native_embedding_mode: NativeEmbeddingMode,
crates/runtime/src/infer/request_resolution.rs:119:            native_vocab_projection: req.native_vocab_projection,
crates/runtime/src/lib.rs:80:    NativeEmbeddingMode,
crates/runtime/src/lib.rs:82:    NativeVocabProjectionMode,
crates/orchestrator_local/src/infer_entry.rs:13:use runtime::{build_candidate_plan_for_task, run_standard_infer, run_standard_infer_candidate_pool, run_standard_infer_with_decode, NativeEmbeddingMode, NativeVocabProjectionMode, StandardInferDecodeOverride, StandardInferRequest};
crates/orchestrator_local/src/infer_entry.rs:273:    let native_vocab_projection = NativeVocabProjectionMode::parse(payload_str(
crates/orchestrator_local/src/infer_entry.rs:275:        "nativeVocabProjection",
crates/orchestrator_local/src/infer_entry.rs:276:        "native_vocab_projection",
crates/orchestrator_local/src/infer_entry.rs:296:    let native_embedding_mode = NativeEmbeddingMode::parse(payload_str(
crates/orchestrator_local/src/infer_entry.rs:303:        native_vocab_projection.as_str(),
crates/orchestrator_local/src/infer_entry.rs:339:        native_vocab_projection,
crates/orchestrator_local/src/infer_entry.rs:383:    output_json.insert("native_vocab_allocation_probe".to_string(), json!(&result.native_vocab_allocation_probe));
crates/orchestrator_local/src/infer_entry.rs:384:    output_json.insert("native_vocab_projection".to_string(), json!(&result.native_vocab_allocation_probe.effective_vocab_projection));
crates/orchestrator_local/src/infer_entry.rs:385:    output_json.insert("native_vocab_tile_size".to_string(), json!(result.native_vocab_allocation_probe.vocab_tile_size));
crates/orchestrator_local/src/infer_entry.rs:386:    output_json.insert("native_full_vocab_bytes".to_string(), json!(result.native_vocab_allocation_probe.full_vocab_bytes));
crates/orchestrator_local/src/infer_entry.rs:387:    output_json.insert("native_gpu_full_vocab_upload_skipped".to_string(), json!(result.native_vocab_allocation_probe.gpu_full_vocab_upload_skipped));
crates/orchestrator_local/src/infer_entry.rs:388:    output_json.insert("native_embedding_mode".to_string(), json!(&result.native_vocab_allocation_probe.effective_embedding_mode));
crates/orchestrator_local/src/infer_entry.rs:741:    response_json.insert("nativeVocabAllocationProbe".to_string(), json!(&result.native_vocab_allocation_probe));
crates/orchestrator_local/src/infer_entry.rs:742:    response_json.insert("nativeVocabProjection".to_string(), json!(&result.native_vocab_allocation_probe.effective_vocab_projection));
crates/orchestrator_local/src/infer_entry.rs:743:    response_json.insert("nativeVocabTileSize".to_string(), json!(result.native_vocab_allocation_probe.vocab_tile_size));
crates/orchestrator_local/src/infer_entry.rs:744:    response_json.insert("nativeFullVocabBytes".to_string(), json!(result.native_vocab_allocation_probe.full_vocab_bytes));
crates/orchestrator_local/src/infer_entry.rs:745:    response_json.insert("nativeGpuFullVocabUploadSkipped".to_string(), json!(result.native_vocab_allocation_probe.gpu_full_vocab_upload_skipped));
crates/orchestrator_local/src/infer_entry.rs:746:    response_json.insert("nativeEmbeddingMode".to_string(), json!(&result.native_vocab_allocation_probe.effective_embedding_mode));

## StandardInferRequest initializer coverage
crates/audio_kernel/src/qwave_pipeline.rs:223:        native_vocab_projection: Default::default(),
crates/runtime/src/lora_smoke.rs:131:        native_vocab_projection: Default::default(),
crates/orchestrator_local/src/lib.rs:589:            native_vocab_projection: Default::default(),
crates/runtime/examples/infer_only.rs:197:        native_vocab_projection: Default::default(),
crates/runtime/src/causal_lm.rs:296:        native_vocab_projection: Default::default(),
crates/runtime/examples/infer_only_v4_lora.rs:335:        native_vocab_projection: Default::default(),
crates/runtime/examples/infer_final_layers6.rs:85:        native_vocab_projection: Default::default(),
crates/orchestrator_local/src/infer_entry.rs:339:        native_vocab_projection,
crates/runtime/examples/infer_run01.rs:28:        native_vocab_projection: Default::default(),

## Cargo availability
cargo not available in bake container; local build required
