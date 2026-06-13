# 16AI-QW-38G-R6A-PERF-REVIEW-00
## Ash 1.1B Runtime / Vocab Cap / EN-KO Subtitle Quality Baseline Review

## 1. Model SSOT

- Domain SSOT: `en_to_ko_translation_subtitle_machine`
- Primary model spec: `specs/model_spec.toml`
- Primary model name: `Ash 1.1B Subtitle-First Task LM`
- Primary model spec id: `model_1p1b_v1`
- Profile: `subtitle_first_bilingual`
- Architecture: `decoder_only_transformer`
- Dimensions: `{'vocab_size': 56000, 'hidden_size': 1536, 'num_layers': 32, 'num_attention_heads': 12, 'num_key_value_heads': 4, 'head_dim': 128, 'intermediate_size': 4096, 'max_position_embeddings': 8192}`

## 2. 1.1B Confirmation

Static archive contains two relevant 1.1B lines:

1. `specs/model_spec.toml`: Ash 1.1B Subtitle-First Task LM, vocab 56000, hidden 1536, layers 32.
2. `specs/model_spec_v5_48259.toml` + checkpoint fingerprint: TinyLlama/Ash 1.1B V4 lineage, vocab 48259, hidden 2048, layers 22.

300M specs are present as stale/experiment files and were not promoted to body SSOT.

## 3. Vocab / Vocab Cap 48256 Analysis

- Primary `model_spec.toml` vocab: `56000`
- V5 model spec vocab: `48259`
- tokenizer manifest v5 vocab list length: `48259`
- checkpoint fingerprint embedding vocab: `48259`
- operator expected vocab cap: `48256`
- static source confirming `48256` as runtime cap: `false`
- static source confirming `48259` vocab lineage: `true`

Conclusion: this bake confirms 1.1B lineage and 48259 static vocab/fingerprint lineage, but does **not** confirm 48256 as a runtime cap source. `48256` appears in the archive as token id / banlist-style evidence, not as the final cap SSOT. This needs a dedicated vocab trace patch.

## 4. Runtime Path Analysis

- WebGPU/Burn backend config exists: `True`
- KV cache static path evidence exists: `True`
- GPU argmax / vocab atlas static path evidence exists: `True`
- CPU fallback disabled in primary specs/profile: `True`
- actual runtime execution confirmed: `false`

## 5. Checkpoint Shape Status

Checkpoint fingerprint exists, but the actual `.safetensors` weight file was not present in the extracted archive path. Therefore checkpoint shape is metadata-backed, not weight-file-verified.

## 6. Sampler / Decode Config Status

Static scan found sampling-related code/config terms, but actual applied runtime decode config was not executed. No claim is made about top-k/top-p/temperature effectiveness.

## 7. EN-KO Subtitle Quality Baseline

Generated fixture:

- `eval/perf_review_00/en_ko_subtitle_quality_baseline_100.jsonl`
- case count: 100
- categories: short dialogue, interjection, negative sentence, proper noun, numbers/dates, rough speech, honorific/casual, context-dependent, compression, linebreak, idiom/slang.

Actual model outputs were not generated in this environment. Translation quality scoring is therefore not performed.

## 8. Runtime Performance Baseline

Runtime benchmark was not executed. No tokens/sec or latency claim is made.

## 9. Bottleneck Classification

- BOTTLENECK_RUNTIME_UNAVAILABLE
- BOTTLENECK_VOCAB_CAP_UNRESOLVED
- BOTTLENECK_NO_ENKO_EVAL_OUTPUT
- BOTTLENECK_WEBGPU_NOT_MEASURED
- BOTTLENECK_CHECKPOINT_WEIGHT_FILE_NOT_PRESENT
- BOTTLENECK_SAMPLER_APPLICATION_UNCONFIRMED

## 10. Recommended Next Patches

1. `16AI-QW-38G-R6A-VOCAB-00` — Runtime Vocab Cap 48256 Trace / Logit Head Range Seal
2. `16AI-QW-38G-R6A-EVAL-TRANS-00` — EN-KO Subtitle Actual Output Eval / Translation Quality Baseline Seal
3. `16AI-QW-38G-R6A-RUNTIME-PROBE-00` — WebGPU 1.1B Runtime Tokens/sec / KV Cache Probe Seal
4. `16AI-QW-38G-R6A-DECODE-SAMPLER-00` — Applied Sampling Runtime / Greedy Escape Quality Probe Seal

## 11. No False Claims

- No translation quality claim without outputs.
- No tokens/sec claim without benchmark.
- No checkpoint shape verification claim without weight file.
- No 48256 cap confirmation without source.
