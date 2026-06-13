# 16AI-6E-R4a-R1 Acceptance

Status: PENDING_RUNTIME

## Scope

- Patch type: Delta Reporter Schema Alignment Patch
- Target bin: `af16ai6e_r4_assembly_delta_report`
- generation: false
- token_ids_mutated: false
- committed_prompt_ids: baseline
- DP recompute: false
- tokenizer logic change: false

## Acceptance Criteria

- [x] AC-16AI-6E-R4a-R1-1 R4 reporter reads result-level delta fields.
- [x] AC-16AI-6E-R4a-R1-2 R4 reporter reads nested assembly fields as fallback.
- [x] AC-16AI-6E-R4a-R1-3 required/recommended delta fields are separated.
- [x] AC-16AI-6E-R4a-R1-4 recommended-field-only misses do not force PARTIAL.
- [x] AC-16AI-6E-R4a-R1-5 protected-only cases are not treated as incomplete because `path_score=0` or `delta=0`.
- [x] AC-16AI-6E-R4a-R1-6 missing required fields are recorded case-by-case.
- [x] AC-16AI-6E-R4a-R1-7 missing recommended fields are recorded case-by-case.
- [x] AC-16AI-6E-R4a-R1-8 field-status log is emitted.
- [x] AC-16AI-6E-R4a-R1-9 partial-reason log is emitted when needed.
- [ ] AC-16AI-6E-R4a-R1-10 R4 rerun preserves `total=21 improved=14 unchanged=7 worsened=0`.
- [ ] AC-16AI-6E-R4a-R1-11 R4 rerun reaches `status=PASS_DELTA_REPORT`.
- [x] AC-16AI-6E-R4a-R1-12 generation=false remains preserved.
- [x] AC-16AI-6E-R4a-R1-13 token_ids_mutated=false remains preserved.
- [x] AC-16AI-6E-R4a-R1-14 committed_prompt_ids=baseline remains preserved.
- [x] AC-16AI-6E-R4a-R1-15 generation quality remains unknown.

## Runtime Command

```powershell
.\scripts\run_16AI_6E_R4_assembly_delta_report.ps1
```

## Expected Seal

```txt
[16AI-6E-R4][seal] ASSEMBLY_DELTA_RECORDED status=PASS_DELTA_REPORT generation=false token_ids_mutated=false committed_prompt_ids=baseline
```
