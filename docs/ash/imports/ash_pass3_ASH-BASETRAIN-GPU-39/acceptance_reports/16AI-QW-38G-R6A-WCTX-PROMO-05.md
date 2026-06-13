# 16AI-QW-38G-R6A-WCTX-PROMO-05

## Real Runtime TopK Trace Capture / No Full Logits No Token Selection Seal

### SSOT

Ash remains an EN-to-KO translation subtitle-machine domain component. PROMO-05 captures compact real-runtime top-k token trace evidence from PROMO-04 forward dry-probe output only. It does not select a token, decode a surface, create candidate text, insert into any queue, create RT-00 receipts, apply runtime mutation, train, backpropagate, optimize, commit weights, or append delta stack entries.

### PASS status

`PASS_WCTX_PROMO_05_REAL_RUNTIME_TOPK_TRACE_CAPTURE_NO_FULL_LOGITS_NO_TOKEN_SELECTION`

### Required chain

- PROMO-00 boundary respected
- PROMO-01 adapter interface respected
- PROMO-02 identity bundle respected
- PROMO-03 tokenized input respected
- PROMO-04 real forward dry probe respected
- real runtime forward output digest bound
- logits shape digest bound
- logits finite check passed
- compact top-k trace emitted

### Opened in this patch

- `topk_trace_allowed = true`
- `topk_trace_emitted = true`

### Still sealed

- full logits attachment/persistence
- selected token creation
- token selection
- sampling/generation
- decode / decoded surface
- candidate text / draft shadow
- preview queue / production review queue
- operator approval
- candidate commit
- runtime apply
- RT-00 receipt creation
- training/backward/optimizer/weight commit/delta stack append

### Matrix

- Positive cases: 4
- Negative cases: 54
- Total cases: 58

### Static status

`BAKED_STATIC_NO_CARGO`
