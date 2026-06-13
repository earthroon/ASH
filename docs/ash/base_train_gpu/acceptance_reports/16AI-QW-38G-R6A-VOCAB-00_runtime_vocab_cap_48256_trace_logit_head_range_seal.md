# 16AI-QW-38G-R6A-VOCAB-00
## Runtime Vocab Cap 48256 Trace / Logit Head Range Seal

- domain_ssot: `en_to_ko_translation_subtitle_machine`
- status: `PASS_STATIC_VOCAB_TRACE_BASELINE_48259_RECLASSIFIED`
- model_spec_vocab_size: `56000`
- v5_model_spec_vocab_size: `48259`
- tokenizer_manifest_vocab_count: `48259`
- checkpoint/lm_head fingerprint vocab: `48259`
- prior operator vocab cap hypothesis: `48256`
- current static runtime candidate: `48259`
- 48256 runtime cap confirmed: `false`
- 48259 static lineage confirmed: `true`
- tokens above 48255 classified: `true`
- tail tokens: `<byte:FD>`, `<byte:FE>`, `<byte:FF>`
- runtime probe executed: `false`
- silent vocab mutation: `false`

## Acceptance

[PASS] model spec vocab values scanned.
[PASS] tokenizer manifest vocab count scanned.
[PASS] checkpoint fingerprint vocab scanned.
[PASS] 48256/48259/56000 static search completed.
[PASS] 48256 not falsely confirmed as runtime cap.
[PASS] 48259 reclassified as current static runtime candidate.
[PASS] last 3 token tail classified.
[PASS] no tokenizer/model/sampler mutation.
