# ASH-FT-33
## Training Corpus Pack Registry / No Shadow Route Seal

SSOT: ASH-FT-33 returns to the atlas group sequential fine-tune mainline after ASH-FT-24 and creates the training corpus registry SSOT for ASH-FT-34. ASH-FT-27 through ASH-FT-32 remain frozen as a side-chain and must not be resumed by this patch.

## State authority
- ASH-FT-24 receipt: training schedule authority, read-only.
- Corpus files: read-only data sources.
- Tokenizer manifest: read-only future encode target.
- ASH-FT-33 corpus registry artifacts: output authority.

## Allowed
- Discover existing `.jsonl`, `.txt`, `.tsv`, `.csv` corpus files.
- Compute SHA256 hashes and line/sample counts.
- Probe schema and split samples deterministically.
- Record domain/source/license metadata and duplicate hints.

## Forbidden
- Shadow route, shadow candidate, delta packet creation, delta stack append.
- Model forward, backward, training, optimizer step, weight update.
- Tokenizer mutation and encode cache creation.
- Runtime default apply, checkpoint alias rebind, promotion.

## Expected PASS
`PASS_ASH_FT33_TRAINING_CORPUS_PACK_REGISTRY_NO_SHADOW_ROUTE`

## Next
ASH-FT-34 Tokenizer Encode Cache Builder / Frozen Tokenizer Seal
