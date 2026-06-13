# 16AI-6V-5-R1 Branch-Local Byte Leak Triage

## Purpose

Compare `v5-baseline` and `v6-branch-local` on the same approved dialogue-ko cases to determine whether the `<0x63>` byte-like output leak observed in 16AI-6V-5 is caused by the v6 branch-local path or is shared by the baseline decoder/model path.

## Scope

- generation=true
- checkpoint_required=true
- gpu_execution=false
- compare_modes=v5-baseline,v6-branch-local
- max_new_tokens=1
- global_default_commit=false
- gpu_default=false
- token_ids_mutated=false
- vocab_augmented=false
- new_token_ids_created=false
- embedding_resize_required=false

## Causality Decisions

- BranchLocalNotCausal: baseline and v6 both leak.
- V6BranchLocalLeakRegression: baseline is clean and v6 leaks.
- LeakResolved: neither branch leaks.
- V6ImprovedOutputSanity: baseline leaks and v6 is clean.
- Inconclusive: reserved for incomplete comparisons.
