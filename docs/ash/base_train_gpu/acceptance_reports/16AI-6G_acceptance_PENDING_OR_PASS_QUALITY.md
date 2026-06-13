# 16AI-6G Acceptance

Status: PENDING_RUNTIME

Scope:
- generation=true
- checkpoint_required=true
- assembly_commit_mode=compare-only
- default_commit=false
- token_ids_mutated=false
- committed_prompt_ids=branch-local compare only

Acceptance target:
- PASS_QUALITY_RECOMPARE when baseline and assembled branch-local generation both complete and quality_delta is recorded.
