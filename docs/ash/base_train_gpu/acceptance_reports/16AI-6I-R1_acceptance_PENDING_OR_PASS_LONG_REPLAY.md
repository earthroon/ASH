# 16AI-6I-R1 Acceptance

Status: PENDING_RUNTIME

Scope:
- generation=true
- checkpoint_required=true
- wrapper_scope=dialogue-ko
- eligible_only=true
- token_budgets=8,16
- global_default_commit=false
- branch_local_commit=true
- token_ids_mutated=false
- vocab_augmented=false
- new_token_ids_created=false

Acceptance target:
- PASS_LONG_REPLAY when the two 16AI-6I eligible dialogue-ko branch commit cases replay at token budgets 8 and 16 without regression or leak.

Judgment hold:
- Default commit safety remains unknown.
- Long-form quality beyond token budgets 8/16 remains unknown.
- DPO training effect remains unknown.
