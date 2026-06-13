# ASH-35 Event-to-SFT Sample Ledger

## Status
PASS_EVENT_TO_SFT_SAMPLE_LEDGER

## Sealed
- AshEventSftSampleClassification
- AshEventSftSampleSourceKind
- AshEventSftLabelKind
- AshEventSftPrivacyPolicy
- AshEventSftTrainingEligibility
- AshEventSftAdapterIntentHint
- AshEventSftSampleCandidate
- AshEventSftSampleLedger
- AshEventSftSamplingReport
- runtime event to sample classification
- privacy/export eligibility gate
- fingerprint dedupe
- sample occurrence counting
- adapter training intent hints

## Policy
- Runtime events are not directly trained.
- Sample ledger is not final dataset.
- MetadataOnly is the default privacy policy.
- Raw prompt/output is not fabricated.
- Sensitive samples are excluded.
- Training eligibility is explicit.
- JSONL export is not performed in ASH-35.
- LoRA SFT is not executed.
- No Python validator is added.

## Boundary
ash_core computes sample candidates and ledger candidates.
orchestrator_local reports sample ledger evidence.
artifact_store may preserve optional sample snapshots.
ASH-36 builds curriculum from the sample ledger.
